# -*- coding: utf-8 -*-
"""
MedBhasha Round 2: Automated Test Evaluation Runner
Takes unlabeled test notes and Bengali queries and produces:
1. predictions_ner.csv (NER tags in BIO format)
2. clustering_results.json (Assigned cluster IDs & metrics)
3. rag_answers.json (Grounded responses for test queries)
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import argparse
import pandas as pd
import numpy as np

# Import pipeline components
from pipeline.round2.modeling_pipeline import (
    load_corpus,
    train_ner_model,
    perform_clustering_and_analytics,
    ClinicalRAG,
    sent2features
)

def run_test_eval(test_corpus_csv=None, test_queries_json=None, output_dir="output/round2_deliverables"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(">>> 1. Training Core Models on Validated Corpus...")
    df, notes, note_entities, doc_ids, doc_texts = load_corpus("output/annotated_corpus.csv")
    crf_model, ner_metrics = train_ner_model(notes)
    clustering_res = perform_clustering_and_analytics(doc_ids, note_entities, n_clusters=15)
    rag_engine = ClinicalRAG(doc_ids, doc_texts, note_entities)
    
    # Save training metrics
    metrics_summary = {
        "ner_metrics": {
            "precision": float(ner_metrics["precision"]),
            "recall": float(ner_metrics["recall"]),
            "f1_micro": float(ner_metrics["f1_micro"]),
            "f1_macro": float(ner_metrics["f1_macro"])
        },
        "clustering_metrics": {
            "silhouette_score": clustering_res["silhouette_score"],
            "davies_bouldin_index": clustering_res["davies_bouldin_index"],
            "n_clusters": clustering_res["n_clusters"]
        }
    }
    with open(os.path.join(output_dir, "model_performance.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    # 1. NER Evaluation on Test Set or Corpus Test Split
    print(">>> 2. Generating NER Predictions...")
    pred_rows = []
    if test_corpus_csv and os.path.exists(test_corpus_csv):
        test_df = pd.read_csv(test_corpus_csv)
    else:
        # Use last 80 notes of our corpus as evaluation sample
        test_df = df[df["note_id"].isin(doc_ids[-80:])]
        
    for nid, group in test_df.groupby("note_id", sort=False):
        tokens = group["token"].astype(str).tolist()
        dummy_sent = [(t, "O") for t in tokens]
        feats = sent2features(dummy_sent)
        preds = crf_model.predict_single(feats)
        for tok, p_tag in zip(tokens, preds):
            pred_rows.append({"note_id": nid, "token": tok, "predicted_tag": p_tag})
            
    pd.DataFrame(pred_rows).to_csv(os.path.join(output_dir, "predictions_ner.csv"), index=False, encoding="utf-8")
    print(f"Saved NER predictions to {os.path.join(output_dir, 'predictions_ner.csv')}")

    # 2. Phenotype Cluster Assignment
    print(">>> 3. Generating Cluster Assignments...")
    cluster_assignments = []
    for nid, c_id in zip(doc_ids, clustering_res["cluster_labels"]):
        cluster_assignments.append({"note_id": nid, "cluster_id": int(c_id)})
        
    pd.DataFrame(cluster_assignments).to_csv(os.path.join(output_dir, "cluster_assignments.csv"), index=False, encoding="utf-8")
    print(f"Saved cluster assignments to {os.path.join(output_dir, 'cluster_assignments.csv')}")

    # 3. RAG Query Answering
    print(">>> 4. Executing Grounded RAG on Test Queries...")
    default_queries = [
        "টাইপ ২ ডায়াবেটিস রোগীর লক্ষণ ও ব্যবস্থাপত্র কি?",
        "শিশুর পাতলা পায়খানা ও বমির ক্ষেত্রে কি স্যালাইন ও ওষুধ দেওয়া হয়?",
        "বুকে তীব্র ব্যথা এবং হার্ট অ্যাটাকের ক্ষেত্রে কি জরুরি চিকিৎসা প্রয়োজন?",
        "টাইফয়েড জ্বরের উপসর্গ এবং কি অ্যান্টিবায়োটিক নির্দেশিত?",
        "কিডনিতে পাথরের উপসর্গ এবং কি ওষুধ দেওয়া হয়েছে?"
    ]
    if test_queries_json and os.path.exists(test_queries_json):
        with open(test_queries_json, "r", encoding="utf-8") as f:
            queries = json.load(f)
    else:
        queries = default_queries

    rag_results = []
    for q in queries:
        ans, docs = rag_engine.answer_query(q)
        rag_results.append({
            "query": q,
            "synthesized_answer": ans,
            "retrieved_passages": docs
        })
        
    with open(os.path.join(output_dir, "rag_answers.json"), "w", encoding="utf-8") as f:
        json.dump(rag_results, f, ensure_ascii=False, indent=2)
    print(f"Saved RAG answers to {os.path.join(output_dir, 'rag_answers.json')}")
    print("\nAll deliverables generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_corpus", default=None, help="Path to hidden test notes CSV")
    parser.add_argument("--test_queries", default=None, help="Path to hidden test queries JSON")
    parser.add_argument("--output_dir", default="output/round2_deliverables", help="Output directory")
    args = parser.parse_args()
    
    run_test_eval(args.test_corpus, args.test_queries, args.output_dir)
