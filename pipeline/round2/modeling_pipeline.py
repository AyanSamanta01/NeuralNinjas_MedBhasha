# -*- coding: utf-8 -*-
"""
MedBhasha Round 2: End-to-End Modeling Pipeline
Stage 1: Clinical NER (CRF Model with seqeval evaluation)
Stage 2: Unsupervised Phenotype Clustering (Dense SVD + KMeans + Silhouette/DB + Graph Analytics)
Stage 3: Grounded Clinical RAG & Query Answering (Hybrid Lexical-Dense Retriever over annotated corpus)
"""

import os
import json
import numpy as np
import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer

import sklearn_crfsuite
from seqeval.metrics import classification_report, f1_score, precision_score, recall_score

# -------------------------------------------------------------
# 1. LOAD & PREPARE CORPUS
# -------------------------------------------------------------
def load_corpus(csv_path="output/annotated_corpus.csv"):
    df = pd.read_csv(csv_path)
    notes = defaultdict(list)
    note_entities = defaultdict(lambda: defaultdict(list))
    
    for _, r in df.iterrows():
        nid = str(r["note_id"])
        tok = str(r["token"])
        tag = str(r["tag"])
        notes[nid].append((tok, tag))
        if tag.startswith("B-") or tag.startswith("I-"):
            etype = tag[2:]
            note_entities[nid][etype].append(tok)
            
    doc_ids = list(notes.keys())
    doc_texts = [" ".join(tok for tok, tag in notes[nid]) for nid in doc_ids]
    return df, notes, note_entities, doc_ids, doc_texts

# -------------------------------------------------------------
# 2. STAGE 1: NER MODEL (CRF)
# -------------------------------------------------------------
def word2features(sent, i):
    word = sent[i][0]
    features = {
        'bias': 1.0,
        'word': word,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isdigit()': word.isdigit(),
        'len(word)': len(word),
    }
    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word': word1,
            '-1:word.lower()': word1.lower(),
            '-1:word.isdigit()': word1.isdigit(),
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word': word1,
            '+1:word.lower()': word1.lower(),
            '+1:word.isdigit()': word1.isdigit(),
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]

def train_ner_model(notes):
    note_list = list(notes.values())
    split_idx = int(len(note_list) * 0.8)
    train_sents = note_list[:split_idx]
    test_sents = note_list[split_idx:]

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    y_pred = crf.predict(X_test)
    
    metrics = {
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_micro": f1_score(y_test, y_pred, average='micro'),
        "f1_macro": f1_score(y_test, y_pred, average='macro'),
        "report": classification_report(y_test, y_pred)
    }
    return crf, metrics

# -------------------------------------------------------------
# 3. STAGE 2: PHENOTYPE CLUSTERING & ANALYTICS
# -------------------------------------------------------------
def perform_clustering_and_analytics(doc_ids, note_entities, n_clusters=15):
    # Extract entity vocabulary
    all_entity_words = set()
    for nid, edict in note_entities.items():
        for etype, words in edict.items():
            all_entity_words.update(words)
    sorted_words = sorted(list(all_entity_words))
    word2idx = {w: i for i, w in enumerate(sorted_words)}

    # Construct note-entity matrix
    X_ent = np.zeros((len(doc_ids), len(sorted_words)))
    for i, nid in enumerate(doc_ids):
        for etype, words in note_entities[nid].items():
            for w in words:
                if w in word2idx:
                    X_ent[i, word2idx[w]] += 1

    X_norm = normalize(X_ent)
    svd = TruncatedSVD(n_components=25, random_state=42)
    X_dense = svd.fit_transform(X_norm)
    X_dense = normalize(X_dense)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    cluster_labels = kmeans.fit_predict(X_dense)

    sil = float(silhouette_score(X_dense, cluster_labels))
    db = float(davies_bouldin_score(X_dense, cluster_labels))

    # Entity Co-occurrence Analysis
    all_entity_types = ['DIAGNOSIS', 'SYMPTOM', 'MEDICATION', 'DOSAGE', 'TEST', 'TEST_RESULT', 'BODY_SITE', 'PROCEDURE', 'TEMPORAL', 'NEGATION_UNCERTAINTY']
    co_matrix = np.zeros((len(all_entity_types), len(all_entity_types)))
    type2idx = {t: i for i, t in enumerate(all_entity_types)}
    
    for nid in doc_ids:
        present_types = list(note_entities[nid].keys())
        for t1 in present_types:
            for t2 in present_types:
                if t1 in type2idx and t2 in type2idx:
                    co_matrix[type2idx[t1], type2idx[t2]] += 1

    clustering_results = {
        "n_clusters": n_clusters,
        "silhouette_score": sil,
        "davies_bouldin_index": db,
        "cluster_distribution": Counter(cluster_labels),
        "co_matrix": co_matrix,
        "all_entity_types": all_entity_types,
        "cluster_labels": cluster_labels.tolist()
    }
    return clustering_results

# -------------------------------------------------------------
# 4. STAGE 3: HYBRID RAG & QUERY ANSWERING
# -------------------------------------------------------------
class ClinicalRAG:
    def __init__(self, doc_ids, doc_texts, note_entities, embedding_model="paraphrase-multilingual-MiniLM-L12-v2"):
        self.doc_ids = doc_ids
        self.doc_texts = doc_texts
        self.note_entities = note_entities
        
        # Lexical (TF-IDF with Unicode Word Regex)
        self.tfidf_vec = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')
        self.tfidf_mat = self.tfidf_vec.fit_transform(doc_texts)
        
        # Dense Semantic
        self.model = SentenceTransformer(embedding_model)
        self.dense_embs = self.model.encode(doc_texts, show_progress_bar=False, batch_size=64)
        
    def retrieve(self, query, alpha=0.55, top_k=2):
        q_tfidf = self.tfidf_vec.transform([query])
        lex_sims = cosine_similarity(q_tfidf, self.tfidf_mat)[0]
        
        q_dense = self.model.encode([query])
        dense_sims = cosine_similarity(q_dense, self.dense_embs)[0]
        
        hybrid_sims = alpha * lex_sims + (1 - alpha) * dense_sims
        top_indices = hybrid_sims.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "note_id": self.doc_ids[idx],
                "score": float(hybrid_sims[idx]),
                "lex_score": float(lex_sims[idx]),
                "dense_score": float(dense_sims[idx]),
                "text": self.doc_texts[idx]
            })
        return results

    def answer_query(self, query, top_k=2):
        retrieved = self.retrieve(query, top_k=top_k)
        if not retrieved:
            return "কোনো তথ্য পাওয়া যায়নি।"
        
        top = retrieved[0]
        nid = top["note_id"]
        ents = self.note_entities[nid]
        
        diag = " ".join(dict.fromkeys(ents.get("DIAGNOSIS", ["অনির্দিষ্ট"])))
        symp = " ".join(dict.fromkeys(ents.get("SYMPTOM", ["নির্দিষ্ট নয়"])))
        med = " ".join(dict.fromkeys(ents.get("MEDICATION", ["উল্লেখ নেই"])))
        dos = " ".join(dict.fromkeys(ents.get("DOSAGE", [""])))
        test = " ".join(dict.fromkeys(ents.get("TEST", ["উল্লেখ নেই"])))
        res = " ".join(dict.fromkeys(ents.get("TEST_RESULT", [""])))
        proc = " ".join(dict.fromkeys(ents.get("PROCEDURE", ["উল্লেখ নেই"])))
        
        answer = (
            f"**[প্রাসঙ্গিক নোট: {nid} | স্কোর: {top['score']:.3f}]**\n"
            f"• **সম্ভাব্য রোগ/নির্ণয় (Diagnosis):** {diag}\n"
            f"• **উপসর্গ (Symptoms):** {symp}\n"
            f"• **পরীক্ষা ও ফলাফল (Test & Result):** {test} ({res})\n"
            f"• **ওষুধ ও মাত্রা (Medication & Dosage):** {med} {dos}\n"
            f"• **চিকিৎসা পদ্ধতি (Procedure):** {proc}\n"
            f"• **নথির সরাসরি অংশ (Grounded Excerpt):** \"{top['text'][:120]}...\""
        )
        return answer, retrieved

# -------------------------------------------------------------
# 5. MAIN EXECUTION & VERIFICATION
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Loading Corpus ===")
    df, notes, note_entities, doc_ids, doc_texts = load_corpus()
    print(f"Loaded {len(doc_ids)} notes.")

    print("\n=== Training NER Model (CRF) ===")
    crf_model, ner_metrics = train_ner_model(notes)
    print(f"Precision: {ner_metrics['precision']:.4f}")
    print(f"Recall:    {ner_metrics['recall']:.4f}")
    print(f"F1 Score:  {ner_metrics['f1_micro']:.4f}")
    print(ner_metrics['report'])

    print("\n=== Executing Phenotype Clustering ===")
    clustering_res = perform_clustering_and_analytics(doc_ids, note_entities, n_clusters=15)
    print(f"Silhouette Score: {clustering_res['silhouette_score']:.4f}")
    print(f"Davies-Bouldin Index: {clustering_res['davies_bouldin_index']:.4f}")

    print("\n=== Initializing Hybrid Clinical RAG ===")
    rag = ClinicalRAG(doc_ids, doc_texts, note_entities)
    
    sample_queries = [
        "টাইপ ২ ডায়াবেটিস রোগীর উপসর্গ ও চিকিৎসার ওষুধ কি?",
        "বুকে চাপ ও হার্ট অ্যাটাকের ক্ষেত্রে কি ওষুধ ও পরীক্ষা দেওয়া হয়?",
        "শিশুর পাতলা পায়খানা ও বমির জন্য কোন স্যালাইন খাওয়াতে হবে?"
    ]
    
    for q in sample_queries:
        print(f"\n[অনুসন্ধান প্রশ্ন (Query)]: {q}")
        ans, docs = rag.answer_query(q)
        print(ans)
