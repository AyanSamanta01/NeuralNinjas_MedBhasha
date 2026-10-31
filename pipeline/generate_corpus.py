# -*- coding: utf-8 -*-
"""
MedBhasha Clinical Corpus Generator - Expanded Version
Generates a diverse, multi-specialty clinical corpus across:
1. Internal Medicine / Infectious Disease
2. Cardiology & Vascular
3. Pulmonology & Critical Care
4. Gastroenterology & Hepatology
5. Endocrinology & Metabolic
6. Nephrology & Urology
7. Neurology & Neurosurgery
8. Dermatology & Venerology
9. Orthopedics, Trauma & Rheumatology
10. Pediatrics & Neonatology
11. Psychiatry & Behavioral Health
12. Ophthalmology
13. ENT (Otolaryngology)
14. Oncology & Hematology
15. Obstetrics & Gynecology

Strictly conforming to the 10 BIO entities:
1. DIAGNOSIS
2. SYMPTOM
3. MEDICATION
4. DOSAGE
5. TEST
6. TEST_RESULT
7. BODY_SITE
8. PROCEDURE
9. TEMPORAL
10. NEGATION_UNCERTAINTY
"""

import csv
import json
import random
import re

random.seed(42)

# Comprehensive repository of distinct clinical cases
CLINICAL_CASES = [
    # --- Category 1: General Medicine & Infectious Disease ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("তীব্র", None), ("জ্বর", "SYMPTOM"), ("এবং", None), ("মাথা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("আছে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথার", "SYMPTOM"), ("কোনো", None), ("অভিযোগ", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("সিবিসি", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("প্লাটিলেট", "TEST"), ("কাউন্ট", "TEST"), ("স্বাভাবিক", "TEST_RESULT"), ("।", None),
        ("প্যারাসিটামল", "MEDICATION"), ("৬৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"),
        ("খাওয়ার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("ভাইরাল", "DIAGNOSIS"), ("ফিভার", "DIAGNOSIS"), ("।", None),
        ("স্যালাইন", "PROCEDURE"), ("পুশ", "PROCEDURE"), ("করা", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("গত", "TEMPORAL"), ("পাঁচ", "TEMPORAL"), ("দিন", "TEMPORAL"), ("যাবত", "TEMPORAL"),
        ("রোগীর", None), ("শুকনো", None), ("কাশি", "SYMPTOM"), ("ও", None), ("গলা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("চলছে", None), ("।", None),
        ("শ্বাসকষ্ট", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("রক্ত", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ডব্লিউবিসি", "TEST"), ("কাউন্ট", "TEST"), ("১১০০০", "TEST_RESULT"), ("।", None),
        ("রোগীর", None), ("ফ্যারিঞ্জাইটিস", "DIAGNOSIS"), ("হওয়ার", None), ("সম্ভাবনা", "NEGATION_UNCERTAINTY"), ("।", None),
        ("এজিথ্রোমাইসিন", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("পাঁচ", "DOSAGE"), ("দিনের", "DOSAGE"), ("জন্য", "DOSAGE"), ("ব্যবস্থাপত্র", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("নেবুলাইজেশন", "PROCEDURE"), ("করা", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("রোগী", None), ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("শারীরিক", None), ("দুর্বলতা", "SYMPTOM"), ("এবং", None), ("অরুচি", "SYMPTOM"), ("অনুভব", None), ("করছেন", None), ("।", None),
        ("বমি", "SYMPTOM"), ("ভাব", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("হিমোগ্লোবিন", "TEST"), ("পরীক্ষায়", "TEST"), ("ফলাফল", None), ("৯.২", "TEST_RESULT"), ("গ্রাম/ডিএল", "TEST_RESULT"), ("।", None),
        ("রোগী", None), ("রক্তস্বল্পতা", "DIAGNOSIS"), ("রোগে", None), ("ভুগছেন", None), ("।", None),
        ("আয়রন", "MEDICATION"), ("ট্যাবলেট", "MEDICATION"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("মুখে", "DOSAGE"), ("খাওয়ার", "DOSAGE"), ("পরামর্শ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("পর", "TEMPORAL"), ("পুনরায়", None), ("দেখা", None), ("করতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("তীব্র", None), ("শীত", "SYMPTOM"), ("দিয়ে", None), ("কাঁপুনির", "SYMPTOM"), ("সাথে", None), ("জ্বর", "SYMPTOM"), ("আসছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("প্রচণ্ড", None), ("ঘাম", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("ম্যালেরিয়া", "TEST"), ("র‌্যাপিড", "TEST"), ("টেস্ট", "TEST"), ("পজিটিভ", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("রোগী", None), ("ম্যালেরিয়া", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("ক্লোরোকুইন", "MEDICATION"), ("ট্যাবলেট", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"),
        ("প্রথম", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],
    [
        ("রোগীর", None), ("চোখের", "BODY_SITE"), ("পেছনে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("ও", None), ("মাংসপেশিতে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("রয়েছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("চার", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("উচ্চ", None), ("জ্বর", "SYMPTOM"), ("।", None),
        ("ডেঙ্গু", "TEST"), ("এনএস১", "TEST"), ("অ্যান্টিজেন", "TEST"), ("পরীক্ষা", "TEST"), ("পজিটিভ", "TEST_RESULT"), ("।", None),
        ("রোগী", None), ("ডেঙ্গু", "DIAGNOSIS"), ("জ্বরে", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("রক্তক্ষরণ", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("প্যারাসিটামল", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("জ্বর", None), ("আসলে", None), ("খাবেন", None), ("।", None),
        ("প্রচুর", None), ("তরল", "MEDICATION"), ("ও", None), ("স্যালাইন", "MEDICATION"), ("পান", None), ("করতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("প্রস্রাবের", "BODY_SITE"), ("সাথে", None), ("জ্বালা", "SYMPTOM"), ("ও", None), ("তলপেটে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("হালকা", None), ("জ্বর", "SYMPTOM"), ("আছে", None), ("।", None),
        ("ইউরিন", "TEST"), ("আর/এম/ই", "TEST"), ("পরীক্ষায়", "TEST"), ("পুঁজ", "TEST_RESULT"), ("কোষ", "TEST_RESULT"), ("১০-১৫", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("রোগীর", None), ("ইউটিআই", "DIAGNOSIS"), ("বা", None), ("মূত্রনালীর", "DIAGNOSIS"), ("সংক্রমণ", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("।", None),
        ("সিপ্রোফ্লক্সাসিন", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("প্রস্রাবে", "BODY_SITE"), ("রক্ত", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 2: Cardiology & Vascular ---
    [
        ("রোগীর", None), ("বুকে", "BODY_SITE"), ("চাপ", "SYMPTOM"), ("ও", None), ("বাম", "BODY_SITE"), ("হাতে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("শুরু", None), ("হয়েছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("ঘণ্টা", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("প্রচণ্ড", None), ("ঘাম", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("ইসিজি", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ফলাফলে", None), ("এসটি", "TEST_RESULT"), ("এলিভেশন", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("রোগী", None), ("মায়োকার্ডিয়াল", "DIAGNOSIS"), ("ইনফার্কশন", "DIAGNOSIS"), ("বা", None), ("হার্ট", "DIAGNOSIS"), ("অ্যাটাক", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("অ্যাসপিরিন", "MEDICATION"), ("৩০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("তাৎক্ষণিক", None), ("খাওয়ানো", None), ("হয়েছে", None), ("।", None),
        ("ইকোকার্ডিওগ্রাফি", "TEST"), ("রিপোর্টে", None), ("বাম", "BODY_SITE"), ("নিলয়ের", "BODY_SITE"), ("দুর্বলতা", "TEST_RESULT"), ("স্পষ্ট", None), ("।", None),
        ("রোগীর", None), ("জরুরি", None), ("অ্যাঞ্জিওপ্লাস্টি", "PROCEDURE"), ("সম্পন্ন", None), ("করা", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("উচ্চ", "DIAGNOSIS"), ("রক্তচাপ", "DIAGNOSIS"), ("নিয়ন্ত্রণে", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("মাথা", "BODY_SITE"), ("ঘোরা", "SYMPTOM"), ("এবং", None), ("বুক", "BODY_SITE"), ("ধড়ফড়", "SYMPTOM"), ("করার", None), ("সমস্যা", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("চলছে", None), ("।", None),
        ("রক্তচাপ", "TEST"), ("পরিমাপ", "TEST"), ("করে", None), ("পাওয়া", None), ("গেল", None), ("১৬০/১০০", "TEST_RESULT"), ("মিমি", "TEST_RESULT"), ("এইচজি", "TEST_RESULT"), ("।", None),
        ("অ্যামলোডিপিন", "MEDICATION"), ("৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("সকালে", "DOSAGE"),
        ("এবং", None), ("অ্যাটেনোলল", "MEDICATION"), ("৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("লিপিড", "TEST"), ("প্রোফাইল", "TEST"), ("পরীক্ষা", "TEST"), ("করাতে", None), ("বলা", None), ("হয়েছে", None), ("।", None),
        ("রোগীর", None), ("হৃদযন্ত্রে", "BODY_SITE"), ("কোনো", None), ("অস্বাভাবিক", None), ("শব্দ", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],
    [
        ("বৃদ্ধ", None), ("রোগীর", None), ("পায়ে", "BODY_SITE"), ("ফোলা", "SYMPTOM"), ("ও", None), ("শুয়ে", None), ("থাকলে", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("বাড়ে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("অস্বীকার", "NEGATION_UNCERTAINTY"), ("করে", "NEGATION_UNCERTAINTY"), ("।", None),
        ("কনজেস্টিভ", "DIAGNOSIS"), ("হার্ট", "DIAGNOSIS"), ("ফেইলিউর", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("করা", None), ("হচ্ছে", None), ("।", None),
        ("বুকের", "BODY_SITE"), ("এক্স-রে", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("হৃদযন্ত্রের", "BODY_SITE"), ("আকার", None), ("বৃদ্ধি", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("ফ্রুসেমাইড", "MEDICATION"), ("৪০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("আইভি", "DOSAGE"), ("ইনজেকশন", "PROCEDURE"), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("পরবর্তীতে", "TEMPORAL"), ("স্পাইরোনোল্যাকটোন", "MEDICATION"), ("২৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"), ("চলবে", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("হাঁটার", None), ("সময়", None), ("বুকে", "BODY_SITE"), ("চাপ", "SYMPTOM"), ("অনুবাদ", None), ("হয়", None), ("ও", None), ("বিশ্রামে", None), ("কমে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("এই", None), ("কষ্ট", None), ("।", None),
        ("রোগীর", None), ("স্টেবল", "DIAGNOSIS"), ("এনজাইনা", "DIAGNOSIS"), ("চিহ্নিত", None), ("হলো", None), ("।", None),
        ("নাইট্রোগ্লিসারিন", "MEDICATION"), ("০.৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("জিহ্বার", "DOSAGE"), ("নিচে", "DOSAGE"), ("রাখার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("করোনারি", "TEST"), ("অ্যাঞ্জিওগ্রাম", "TEST"), ("পরীক্ষা", "TEST"), ("করার", None), ("সিদ্ধান্ত", None), ("নেওয়া", None), ("হলো", None), ("।", None),
        ("বমি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 3: Pulmonology & Respiratory ---
    [
        ("রোগী", None), ("ব্রঙ্কিয়াল", "DIAGNOSIS"), ("অ্যাজমা", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("গত", "TEMPORAL"), ("চার", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("তীব্র", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("এবং", None), ("বুকে", "BODY_SITE"), ("বাঁশির", None), ("মতো", None), ("শব্দ", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("পালস", "TEST"), ("অক্সিমিটারে", "TEST"), ("অক্সিজেন", "TEST"), ("স্যাচুরেশন", "TEST"), ("৮৯%", "TEST_RESULT"), ("।", None),
        ("রোগীকে", None), ("অক্সিজেন", "PROCEDURE"), ("থেরাপি", "PROCEDURE"), ("এবং", None),
        ("সালবিউটামল", "MEDICATION"), ("ইনহেলার", "MEDICATION"), ("দুই", "DOSAGE"), ("পাফ", "DOSAGE"),
        ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("নিতে", None), ("বলা", None), ("হয়েছে", None), ("।", None),
        ("বুডেসোনাইড", "MEDICATION"), ("নেবুলাইজার", "PROCEDURE"), ("দেওয়া", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("দীর্ঘদিনের", "TEMPORAL"), ("ধূমপায়ী", None), ("রোগীর", None), ("সিওপিডি", "DIAGNOSIS"), ("বা", None), ("ক্রনিক", "DIAGNOSIS"), ("অবস্ট্রাকটিভ", "DIAGNOSIS"), ("পালমোনারি", "DIAGNOSIS"), ("ডিজিজ", "DIAGNOSIS"), ("রয়েছে", None), ("।", None),
        ("কাশি", "SYMPTOM"), ("এবং", None), ("কফে", "BODY_SITE"), ("রক্ত", "SYMPTOM"), ("পড়ার", None), ("সমস্যা", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("বাড়ছে", None), ("।", None),
        ("বুকের", "BODY_SITE"), ("সিটি", "TEST"), ("স্ক্যান", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ফুসফুসে", "BODY_SITE"), ("সংক্রমণের", "TEST_RESULT"), ("চিহ্ন", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("ডক্সিসাইক্লিন", "MEDICATION"), ("১০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("রোগীর", None), ("ব্রঙ্কোস্কপি", "PROCEDURE"), ("করার", None), ("প্রস্তাব", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],
    [
        ("গত", "TEMPORAL"), ("দশ", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("রোগীর", None), ("উচ্চমাত্রার", None), ("জ্বর", "SYMPTOM"), (",", None), ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("কাশি", "SYMPTOM"), ("আছে", None), ("।", None),
        ("বুকের", "BODY_SITE"), ("এক্স-রে", "TEST"), ("পরীক্ষায়", "TEST"), ("ডান", "BODY_SITE"), ("ফুসফুসে", "BODY_SITE"), ("কনসোলিডেশন", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("রোগীর", None), ("নিউমোনিয়া", "DIAGNOSIS"), ("নিশ্চিত", None), ("হয়েছে", None), ("।", None),
        ("সেফট্রিয়াক্সন", "MEDICATION"), ("১", "DOSAGE"), ("গ্রাম", "DOSAGE"), ("আইভি", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("ইনজেকশন", "PROCEDURE"), ("শুরু", None), ("করা", None), ("হলো", None), ("।", None),
        ("কাশির", "SYMPTOM"), ("কফ", "BODY_SITE"), ("কালচার", "TEST"), ("পরীক্ষার", "TEST"), ("নির্দেশ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("তিন", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("ক্রমাগত", None), ("কাশি", "SYMPTOM"), (",", None), ("রাতে", "TEMPORAL"), ("ঘাম", "SYMPTOM"), ("এবং", None), ("ওজন", "SYMPTOM"), ("কমে", "SYMPTOM"), ("যাচ্ছে", None), ("।", None),
        ("কফে", "BODY_SITE"), ("রক্ত", "SYMPTOM"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("জিনএক্সপার্ট", "TEST"), ("পরীক্ষায়", "TEST"), ("এমটিবি", "TEST_RESULT"), ("পজিটিভ", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("পালমোনারি", "DIAGNOSIS"), ("টিউবারকিউলোসিস", "DIAGNOSIS"), ("বা", None), ("যক্ষ্মা", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("অ্যান্টি-টিবি", "MEDICATION"), ("ওষুধ", "MEDICATION"), ("চার", "DOSAGE"), ("ট্যাবলেট", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("সকালে", "DOSAGE"), ("খালি", "DOSAGE"), ("পেটে", "DOSAGE"), ("চলবে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 4: Gastroenterology & Hepatology ---
    [
        ("রোগী", None), ("পেপটিক", "DIAGNOSIS"), ("আলসার", "DIAGNOSIS"), ("রোগে", None), ("ভুগছেন", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("পেটের", "BODY_SITE"), ("উপরের", "BODY_SITE"), ("অংশে", "BODY_SITE"), ("জ্বালাপোড়া", "SYMPTOM"), ("ব্যথা", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("বমির", "SYMPTOM"), ("লক্ষণ", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("রোগীর", None), ("এন্ডোস্কপি", "PROCEDURE"), ("করা", None), ("হয়েছে", None), (",", None),
        ("পাকস্থলীতে", "BODY_SITE"), ("ক্ষতচিহ্ন", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("এসোমিপ্রাজল", "MEDICATION"), ("২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("খাবারের", "DOSAGE"), ("আগে", "DOSAGE"),
        ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("সেবনের", None), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("তীব্র", None), ("পেটে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("হলুদ", None), ("চোখ", "BODY_SITE"), ("ও", None), ("প্রস্রাব", "BODY_SITE"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("চার", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("বমি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("লিভার", "TEST"), ("ফাংশন", "TEST"), ("টেস্ট", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("সিরাম", "TEST"), ("বিলিরুবিন", "TEST"), ("৪.৮", "TEST_RESULT"), ("মিগ্রা/ডিএল", "TEST_RESULT"), ("এবং", None),
        ("এসজিপিটি", "TEST"), ("২৮০", "TEST_RESULT"), ("ইউ/এল", "TEST_RESULT"), ("।", None),
        ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("তীব্র", "DIAGNOSIS"), ("হেপাটাইটিস", "DIAGNOSIS"), ("বা", None), ("জন্ডিস", "DIAGNOSIS"), ("।", None),
        ("পেটের", "BODY_SITE"), ("আল্ট্রাসনোগ্রাফি", "TEST"), ("সম্পন্ন", None), ("করা", None), ("হলো", None), ("।", None),
        ("রোগীকে", None), ("পর্যাপ্ত", None), ("বিশ্রাম", None), ("ও", None), ("আইভি", "DOSAGE"), ("ফ্লুইড", "PROCEDURE"), ("দেওয়া", None), ("হচ্ছে", None), ("।", None)
    ],
    [
        ("তলপেটে", "BODY_SITE"), ("প্রচণ্ড", None), ("ব্যথা", "SYMPTOM"), ("নিয়ে", None), ("রোগী", None), ("জরুরি", None), ("বিভাগে", None), ("এসেছেন", None), ("।", None),
        ("ডান", "BODY_SITE"), ("পাশে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("বেশি", None), ("এবং", None), ("জ্বর", "SYMPTOM"), ("আছে", None), ("।", None),
        ("ডায়রিয়া", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("তীব্র", "DIAGNOSIS"), ("অ্যাপেন্ডিসাইটিস", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("করা", None), ("হচ্ছে", None), ("।", None),
        ("পেটের", "BODY_SITE"), ("ইউএসজি", "TEST"), ("রিপোর্টে", None), ("অ্যাপেন্ডিক্স", "BODY_SITE"), ("প্রদাহযুক্ত", "TEST_RESULT"), ("।", None),
        ("রোগীর", None), ("জরুরি", None), ("অ্যাপেনডিসেক্টমি", "PROCEDURE"), ("অস্ত্রোপচার", "PROCEDURE"), ("করা", None), ("হয়েছে", None), ("।", None),
        ("মেট্রোনিডাজল", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("আইভি", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("পেটের", "BODY_SITE"), ("ডান", "BODY_SITE"), ("পাশে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("চর্বিযুক্ত", None), ("খাবারের", None), ("পর", None), ("বাড়ে", None), ("।", None),
        ("বমির", "SYMPTOM"), ("অভিযোগ", None), ("আছে", None), ("।", None),
        ("পেটের", "BODY_SITE"), ("আল্ট্রাসাউন্ড", "TEST"), ("পরীক্ষায়", "TEST"), ("পিত্তথলিতে", "BODY_SITE"), ("পাথর", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("কোলেলিথিয়াসিস", "DIAGNOSIS"), ("নির্ণয়", None), ("হয়েছে", None), ("।", None),
        ("জন্ডিস", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ল্যাপারোস্কোপিক", "PROCEDURE"), ("কোলেসিস্টেক্টমি", "PROCEDURE"), ("অস্ত্রোপচারের", "PROCEDURE"), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],

    # --- Category 5: Endocrinology & Metabolism ---
    [
        ("রোগীর", None), ("টাইপ", "DIAGNOSIS"), ("২", "DIAGNOSIS"), ("ডায়াবেটিস", "DIAGNOSIS"), ("মেলাইটাস", "DIAGNOSIS"), ("ধরা", None), ("পড়েছে", None), ("।", None),
        ("অতিরিক্ত", None), ("পিপাসা", "SYMPTOM"), (",", None), ("ঘনঘন", None), ("প্রস্রাব", "SYMPTOM"), ("এবং", None), ("ওজন", "SYMPTOM"), ("হ্রাস", "SYMPTOM"),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("চলছে", None), ("।", None),
        ("রক্তে", "BODY_SITE"), ("শর্করার", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হলো", None), (",", None),
        ("ফাস্টিং", "TEST"), ("ব্লাড", "TEST"), ("সুগার", "TEST"), ("১১.৪", "TEST_RESULT"), ("মিমি/লি", "TEST_RESULT"), ("এবং", None),
        ("এইচবিএ১সি", "TEST"), ("৮.৯%", "TEST_RESULT"), ("।", None),
        ("মেটফরমিন", "MEDICATION"), ("৮৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("খাওয়ার", "DOSAGE"), ("পর", "DOSAGE"),
        ("এবং", None), ("গ্লাইমেপিরিড", "MEDICATION"), ("১", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("সকালে", "DOSAGE"), ("চলবে", None), ("।", None),
        ("পায়ে", "BODY_SITE"), ("কোনো", None), ("ক্ষত", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],
    [
        ("রোগী", None), ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("যাবত", "TEMPORAL"),
        ("ওজন", "SYMPTOM"), ("বৃদ্ধি", "SYMPTOM"), (",", None), ("অতিরিক্ত", None), ("ক্লান্তি", "SYMPTOM"), ("এবং", None), ("শীতলতা", "SYMPTOM"), ("অনুভব", None), ("করছেন", None), ("।", None),
        ("গলায়", "BODY_SITE"), ("ফোলাভাব", "SYMPTOM"), ("আছে", None), ("।", None),
        ("থাইরয়েড", "TEST"), ("ফাংশন", "TEST"), ("টেস্ট", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("টিএসএইচ", "TEST"), ("১২.৫", "TEST_RESULT"), ("এমআইইউ/এল", "TEST_RESULT"), ("যা", None), ("উচ্চ", "TEST_RESULT"), ("।", None),
        ("রোগীর", None), ("হাইপোথাইরয়েডিজম", "DIAGNOSIS"), ("নিশ্চিত", None), ("হয়েছে", None), ("।", None),
        ("লেভোথাইরক্সিন", "MEDICATION"), ("৫০", "DOSAGE"), ("মাইক্রোগ্রাম", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("সকালে", "DOSAGE"),
        ("খালি", "DOSAGE"), ("পেটে", "DOSAGE"), ("খাওয়ার", "DOSAGE"), ("নির্দেশ", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("হঠাৎ", "TEMPORAL"), ("হাত", "BODY_SITE"), ("কাঁপা", "SYMPTOM"), (",", None), ("অতিরিক্ত", None), ("ঘাম", "SYMPTOM"), ("এবং", None), ("ওজন", "SYMPTOM"), ("হ্রাস", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("চোখ", "BODY_SITE"), ("সামনে", "BODY_SITE"), ("বেরিয়ে", "SYMPTOM"), ("আসার", "SYMPTOM"), ("লক্ষণ", None), ("আছে", None), ("।", None),
        ("সেরাম", "TEST"), ("এফটি৪", "TEST"), ("উচ্চ", "TEST_RESULT"), ("এবং", None),
        ("টিএসএইচ", "TEST"), ("কম", "TEST_RESULT"), ("০.০১", "TEST_RESULT"), ("।", None),
        ("গ্রেভস", "DIAGNOSIS"), ("ডিজিজ", "DIAGNOSIS"), ("বা", None), ("হাইপারথাইরয়েডিজম", "DIAGNOSIS"), ("চিহ্নিত", None), ("হলো", None), ("।", None),
        ("কার্বিমাজোল", "MEDICATION"), ("২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("এবং", None), ("প্রোপ্রানোলল", "MEDICATION"), ("২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 6: Nephrology & Urology ---
    [
        ("রোগীর", None), ("কোমরের", "BODY_SITE"), ("পেছনে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("প্রস্রাবে", "BODY_SITE"), ("জ্বালাপোড়া", "SYMPTOM"), ("আছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("প্রস্রাবের", "BODY_SITE"), ("সাথে", None), ("রক্ত", "SYMPTOM"), ("গেছে", None), ("।", None),
        ("কিডনি", "TEST"), ("ইউএসজি", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ডান", "BODY_SITE"), ("কিডনিতে", "BODY_SITE"), ("৬", "TEST_RESULT"), ("মিমি", "TEST_RESULT"), ("পাথর", "TEST_RESULT"), ("চিহ্নিত", None), ("হয়েছে", None), ("।", None),
        ("রোগী", None), ("নেফ্রোলিথিয়াসিস", "DIAGNOSIS"), ("বা", None), ("কিডনি", "DIAGNOSIS"), ("পাথর", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("কিটোোরোল্যাক", "MEDICATION"), ("১০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("ব্যথানাশক", None), ("হিসেবে", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("প্রস্রাব", "TEST"), ("পরীক্ষায়", "TEST"), ("পুঁজ", "TEST_RESULT"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("লিথোট্রিপসি", "PROCEDURE"), ("পদ্ধতি", "PROCEDURE"), ("বিবেচনা", None), ("করা", None), ("হচ্ছে", None), ("।", None)
    ],
    [
        ("দীর্ঘদিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("উচ্চ", "DIAGNOSIS"), ("রক্তচাপ", "DIAGNOSIS"), ("থাকায়", None), ("রোগীর", None),
        ("মুখ", "BODY_SITE"), ("ও", None), ("পা", "BODY_SITE"), ("ফুলে", "SYMPTOM"), ("গেছে", None), ("।", None),
        ("সিরাম", "TEST"), ("ক্রিয়েটিনিন", "TEST"), ("পরীক্ষার", "TEST"), ("ফলাফল", None), ("৩.৪", "TEST_RESULT"), ("মিগ্রা/ডিএল", "TEST_RESULT"), ("।", None),
        ("রোগী", None), ("ক্রনিক", "DIAGNOSIS"), ("কিডনি", "DIAGNOSIS"), ("ডিজিজ", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("হিমোডায়ালাইসিস", "PROCEDURE"), ("শুরু", None), ("করার", None), ("সিদ্ধান্ত", None), ("নেওয়া", None), ("হলো", None), ("।", None),
        ("এরিথ্রোপয়েটিন", "MEDICATION"), ("৪০০০", "DOSAGE"), ("ইউনিট", "DOSAGE"), ("ইনজেকশন", "PROCEDURE"), ("সপ্তাহে", "DOSAGE"), ("একবার", "DOSAGE"), ("দেওয়া", None), ("হবে", None), ("।", None)
    ],
    [
        ("প্রবীণ", None), ("পুরুষ", None), ("রোগীর", None), ("প্রস্রাব", "BODY_SITE"), ("আটকে", "SYMPTOM"), ("যাওয়া", "SYMPTOM"), ("এবং", None), ("ফোটা", "SYMPTOM"), ("ফোটা", "SYMPTOM"), ("পড়ার", "SYMPTOM"), ("সমস্যা", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("রাতে", "TEMPORAL"), ("ঘনঘন", None), ("প্রস্রাব", "SYMPTOM"), ("হয়", None), ("।", None),
        ("প্রস্টেট", "TEST"), ("ইউএসজি", "TEST"), ("পরীক্ষায়", "TEST"), ("প্রস্টেটের", "BODY_SITE"), ("আকার", None), ("৫০", "TEST_RESULT"), ("গ্রাম", "TEST_RESULT"), ("বৃদ্ধি", "TEST_RESULT"), ("।", None),
        ("বেনাইন", "DIAGNOSIS"), ("প্রস্টেটিক", "DIAGNOSIS"), ("হাইপারপ্লাসিয়া", "DIAGNOSIS"), ("বা", None), ("বিপিএইচ", "DIAGNOSIS"), ("নির্ণয়", None), ("হলো", None), ("।", None),
        ("ট্যামসুলোসিন", "MEDICATION"), ("০.৪", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("খাওয়ার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("ক্যাথেটারাইজেশন", "PROCEDURE"), ("করা", None), ("হলো", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 7: Neurology & Neurosurgery ---
    [
        ("রোগীর", None), ("মাথার", "BODY_SITE"), ("একপাশে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("আলোতে", None), ("অস্বস্তি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("বারো", "TEMPORAL"), ("ঘণ্টা", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("বমি", "SYMPTOM"), ("বমি", "SYMPTOM"), ("ভাব", "SYMPTOM"), ("রয়েছে", None), ("।", None),
        ("ঘাড়", "BODY_SITE"), ("শক্ত", "SYMPTOM"), ("হওয়ার", None), ("লক্ষণ", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("মস্তিষ্কের", "BODY_SITE"), ("এমআরআই", "TEST"), ("স্বাভাবিক", "TEST_RESULT"), ("।", None),
        ("রোগীর", None), ("মাইগ্রেন", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হয়েছে", None), ("।", None),
        ("সুমাট্রিপটান", "MEDICATION"), ("৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("ব্যথা", None), ("শুরুতে", None), ("খাওয়ার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("ডোমপেরিডন", "MEDICATION"), ("১০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("বমির", None), ("জন্য", None), ("প্রেসক্রাইব", None), ("করা", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("বৃদ্ধ", None), ("রোগীর", None), ("হঠাৎ", "TEMPORAL"), ("করে", None), ("ডান", "BODY_SITE"), ("হাত", "BODY_SITE"), ("ও", None), ("পা", "BODY_SITE"), ("অবশ", "SYMPTOM"), ("হয়ে", None), ("গেছে", None), ("।", None),
        ("কথা", None), ("বলতে", None), ("অসুবিধা", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("মস্তিষ্কের", "BODY_SITE"), ("সিটি", "TEST"), ("স্ক্যান", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("বাম", "BODY_SITE"), ("হেমিস্ফিয়ারে", "BODY_SITE"), ("ইস্কেমিক", "TEST_RESULT"), ("পরিবর্তন", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("রোগী", None), ("ইস্কেমিক", "DIAGNOSIS"), ("স্ট্রোক", "DIAGNOSIS"), ("শিকার", None), ("।", None),
        ("খিঁচুনি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ক্লোপিডোগ্রেল", "MEDICATION"), ("৭৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("এবং", None), ("অ্যাটোরভাস্ট্যাটিন", "MEDICATION"), ("২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("চলবে", None), ("।", None),
        ("ফিজিওথেরাপি", "PROCEDURE"), ("চিকিৎসা", "PROCEDURE"), ("চালু", None), ("করা", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("হঠাৎ", "TEMPORAL"), ("শরীর", "BODY_SITE"), ("শক্ত", "SYMPTOM"), ("হয়ে", None), ("তীব্র", None), ("খিঁচুনি", "SYMPTOM"), ("হয়েছে", None), ("।", None),
        ("মুখ", "BODY_SITE"), ("দিয়ে", None), ("ফেনা", "SYMPTOM"), ("বেরিয়েছিল", None), ("।", None),
        ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("এমন", None), ("ঘটনা", None), ("তিনবার", None), ("ঘটেছে", None), ("।", None),
        ("ইইজি", "TEST"), ("পরীক্ষায়", "TEST"), ("মস্তিষ্কে", "BODY_SITE"), ("অস্বাভাবিক", "TEST_RESULT"), ("তরঙ্গ", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("রোগীর", None), ("এপিলেপসি", "DIAGNOSIS"), ("বা", None), ("মৃগীরোগ", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("লেভেটিরাসিটাম", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("নিয়মিত", None), ("চলবে", None), ("।", None),
        ("মাথা", "BODY_SITE"), ("ঘোরা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 8: Dermatology & Venerology ---
    [
        ("রোগীর", None), ("ত্বকে", "BODY_SITE"), ("লালচে", "SYMPTOM"), ("দাগ", "SYMPTOM"), ("এবং", None), ("তীব্র", None), ("চুলকানি", "SYMPTOM"), ("রয়েছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("হাত", "BODY_SITE"), ("ও", None), ("বুকে", "BODY_SITE"), ("ফুসকুড়ি", "SYMPTOM"), ("দেখা", None), ("দিচ্ছে", None), ("।", None),
        ("পুঁজ", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("স্কিন", "TEST"), ("স্ক্র্যাপিং", "TEST"), ("পরীক্ষায়", "TEST"), ("ছত্রাক", "TEST_RESULT"), ("সংক্রমণ", "TEST_RESULT"), ("ধরা", None), ("পড়েছে", None), ("।", None),
        ("টিনিয়া", "DIAGNOSIS"), ("কর্পোরিস", "DIAGNOSIS"), ("বা", None), ("দাদ", "DIAGNOSIS"), ("রোগ", None), ("নিশ্চিত", None), ("।", None),
        ("টারবিনাফিন", "MEDICATION"), ("ক্রিম", "MEDICATION"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("ত্বকে", "DOSAGE"), ("লাগান", None), ("।", None),
        ("ফেওক্সোফেনাডিন", "MEDICATION"), ("১২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("খাওয়ার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],
    [
        ("কনুই", "BODY_SITE"), ("ও", None), ("হাঁটুতে", "BODY_SITE"), ("রূপালি", "SYMPTOM"), ("আঁশযুক্ত", "SYMPTOM"), ("ত্বকের", "BODY_SITE"), ("প্রলেপ", "SYMPTOM"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("মাস", "TEMPORAL"), ("যাবত", "TEMPORAL"), ("এই", None), ("সমস্যা", None), ("বাড়ছে", None), ("।", None),
        ("রোগীর", None), ("সোরিয়াসিস", "DIAGNOSIS"), ("রোগ", None), ("নির্ণয়", None), ("হয়েছে", None), ("।", None),
        ("জয়েন্টে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("স্কিন", "PROCEDURE"), ("বায়োপসি", "PROCEDURE"), ("সম্পন্ন", None), ("করা", None), ("হয়েছে", None), ("।", None),
        ("ক্লোবেটাসল", "MEDICATION"), ("মলম", "MEDICATION"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"), ("ব্যবহার", None), ("করতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],
    [
        ("মুখে", "BODY_SITE"), ("ও", None), ("গালে", "BODY_SITE"), ("তীব্র", None), ("ব্রণ", "SYMPTOM"), ("এবং", None), ("প্রদাহযুক্ত", "SYMPTOM"), ("দানা", "SYMPTOM"), ("উঠেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("ব্যথা", "SYMPTOM"), ("করছে", None), ("।", None),
        ("অ্যাকনি", "DIAGNOSIS"), ("ভালগারিস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("ক্লিন্ডামাইসিন", "MEDICATION"), ("জেল", "MEDICATION"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("লাগান", None), ("।", None),
        ("আইসোট্রেটিনয়েন", "MEDICATION"), ("১০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 9: Orthopedics, Trauma & Rheumatology ---
    [
        ("রোগীর", None), ("উভয়", "BODY_SITE"), ("হাঁটুতে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("ফোলাভাব", "SYMPTOM"), ("আছে", None), ("।", None),
        ("হাঁটাচলা", None), ("করলে", None), ("ব্যথা", "SYMPTOM"), ("বাড়ে", None), ("।", None),
        ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("এই", None), ("কষ্ট", None), ("চলছে", None), ("।", None),
        ("হাঁটুর", "BODY_SITE"), ("এক্স-রে", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হলো", None), (",", None),
        ("জয়েন্ট", "BODY_SITE"), ("স্পেস", "BODY_SITE"), ("হ্রাস", "TEST_RESULT"), ("পেয়েছে", None), ("।", None),
        ("রোগী", None), ("অস্টিওআর্থ্রাইটিস", "DIAGNOSIS"), ("রোগে", None), ("ভুগছেন", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ন্যাপ্রোক্সেন", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("ভরা", "DOSAGE"), ("পেটে", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("হাঁটুতে", "BODY_SITE"), ("ইন্ট্রা-আর্টিকুলার", "DOSAGE"), ("ইনজেকশন", "PROCEDURE"), ("দেওয়া", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("সকালে", "TEMPORAL"), ("ঘুম", None), ("থেকে", None), ("উঠলে", None), ("হাতের", "BODY_SITE"), ("আঙুলে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("ও", None), ("আড়ষ্টতা", "SYMPTOM"), ("থাকে", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("বছর", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("লক্ষণগুলো", None), ("বিদ্যমান", None), ("।", None),
        ("আরএ", "TEST"), ("ফ্যাক্টর", "TEST"), ("পজিটিভ", "TEST_RESULT"), ("এবং", None),
        ("অ্যান্টি-সিসিপি", "TEST"), ("উচ্চ", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("রিউমাটয়েড", "DIAGNOSIS"), ("আর্থ্রাইটিস", "DIAGNOSIS"), ("নিশ্চিত", None), ("হয়েছে", None), ("।", None),
        ("মিথোট্রেক্সেট", "MEDICATION"), ("৭.৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("সপ্তাহে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("এবং", None), ("ফলিক", "MEDICATION"), ("অ্যাসিড", "MEDICATION"), ("৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("চোখে", "BODY_SITE"), ("ঝাপসা", "SYMPTOM"), ("দেখা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],
    [
        ("রোগী", None), ("সিঁড়ি", None), ("থেকে", None), ("পড়ে", None), ("গিয়ে", None), ("ডান", "BODY_SITE"), ("পায়ে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("ও", None), ("ফোলা", "SYMPTOM"), ("।", None),
        ("পা", "BODY_SITE"), ("নাড়াতে", None), ("পারছেন", None), ("না", "NEGATION_UNCERTAINTY"), ("।", None),
        ("পায়ের", "BODY_SITE"), ("এক্স-রে", "TEST"), ("করে", None), ("টিবিয়া", "BODY_SITE"), ("হাড়ে", "BODY_SITE"), ("ফ্র্যাকচার", "TEST_RESULT"), ("চিহ্নিত", None), ("হলো", None), ("।", None),
        ("টিবিয়াল", "DIAGNOSIS"), ("ফ্র্যাকচার", "DIAGNOSIS"), ("নিশ্চিত", None), ("।", None),
        ("প্লাস্টার", "PROCEDURE"), ("কাস্ট", "PROCEDURE"), ("পরানো", None), ("হয়েছে", None), ("।", None),
        ("ট্রামাডল", "MEDICATION"), ("৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("ব্যথার", None), ("জন্য", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],

    # --- Category 10: Pediatrics & Neonatology ---
    [
        ("শিশুর", None), ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("পাতলা", "SYMPTOM"), ("পায়খানা", "SYMPTOM"), ("এবং", None), ("বমি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("প্রচণ্ড", None), ("পানিশূন্যতা", "SYMPTOM"), ("ও", None), ("দুর্বলতা", "SYMPTOM"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("পেটে", "BODY_SITE"), ("চাপ", None), ("দিলে", None), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("মল", "TEST"), ("পরীক্ষায়", "TEST"), ("রোটাভাইরাস", "TEST_RESULT"), ("চিহ্নিত", None), ("হয়েছে", None), ("।", None),
        ("তীব্র", "DIAGNOSIS"), ("গ্যাস্ট্রোএন্টেরাইটিস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("ওআরএস", "MEDICATION"), ("স্যালাইন", "MEDICATION"), ("বারবার", "DOSAGE"), ("খাওয়ানো", None), ("এবং", None),
        ("জিংক", "MEDICATION"), ("সিরাপ", "MEDICATION"), ("২০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"),
        ("চৌদ্দ", "DOSAGE"), ("দিন", "DOSAGE"), ("খাওয়ার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("ক্যানুলা", "PROCEDURE"), ("স্থাপন", "PROCEDURE"), ("করে", None), ("আইভি", "DOSAGE"), ("স্যালাইন", "PROCEDURE"), ("চালু", None), ("করা", None), ("হলো", None), ("।", None)
    ],
    [
        ("গত", "TEMPORAL"), ("চার", "TEMPORAL"), ("দিন", "TEMPORAL"), ("যাবত", "TEMPORAL"),
        ("বাচ্চার", None), ("উচ্চ", None), ("তাপমাত্রার", None), ("জ্বর", "SYMPTOM"), ("ও", None), ("কানে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("চলছে", None), ("।", None),
        ("কান", "BODY_SITE"), ("দিয়ে", None), ("পানি", "SYMPTOM"), ("পড়ার", "SYMPTOM"), ("অভিযোগ", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ওটোস্কোপি", "TEST"), ("পরীক্ষায়", "TEST"), ("টিম্প্যানিক", "BODY_SITE"), ("মেমব্রেন", "BODY_SITE"), ("লালচে", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("অ্যাকিউট", "DIAGNOSIS"), ("ওটাইটিস", "DIAGNOSIS"), ("মিডিয়া", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("।", None),
        ("অ্যামোক্সিসিলিন", "MEDICATION"), ("সিরাপ", "MEDICATION"), ("২৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"),
        ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None)
    ],

    # --- Category 11: Psychiatry & Behavioral Health ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("তীব্র", None), ("বিষণ্ণতা", "SYMPTOM"), (",", None), ("অনিদ্রা", "SYMPTOM"), ("এবং", None), ("কাজে", None), ("উৎসাহহীনতা", "SYMPTOM"), ("রয়েছে", None), ("।", None),
        ("আত্মহত্যার", "SYMPTOM"), ("চিন্তাভাবনা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("সাইকিয়াট্রিক", "TEST"), ("মূল্যায়নে", "TEST"), ("মেজর", "DIAGNOSIS"), ("ডিপ্রেসিভ", "DIAGNOSIS"), ("ডিসঅর্ডার", "DIAGNOSIS"), ("চিহ্নিত", None), ("হলো", None), ("।", None),
        ("এসসিটালোপ্রাম", "MEDICATION"), ("১০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("সকালে", "DOSAGE"),
        ("এবং", None), ("ক্লোনাজিপাম", "MEDICATION"), ("০.৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("ঘুমের", None), ("জন্য", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("কাউন্সেলিং", "PROCEDURE"), ("সেশন", "PROCEDURE"), ("শুরু", None), ("করা", None), ("হয়েছে", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("হঠাৎ", "TEMPORAL"), ("করে", None), ("বুক", "BODY_SITE"), ("ধড়ফড়", "SYMPTOM"), (",", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("ও", None), ("মৃত্যুভয়", "SYMPTOM"), ("শুরু", None), ("হয়েছিল", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("সপ্তাহে", "TEMPORAL"), ("দুইবার", None), ("এমন", None), ("হয়েছে", None), ("।", None),
        ("ইসিজি", "TEST"), ("ও", None), ("ইকো", "TEST"), ("স্বাভাবিক", "TEST_RESULT"), ("।", None),
        ("প্যানিক", "DIAGNOSIS"), ("অ্যাটাক", "DIAGNOSIS"), ("বা", None), ("প্যানিক", "DIAGNOSIS"), ("ডিসঅর্ডার", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("করা", None), ("হলো", None), ("।", None),
        ("সার্ট্রালিন", "MEDICATION"), ("৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("একবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("কোনো", None), ("ক্ষত", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 12: Ophthalmology (Eye) ---
    [
        ("বৃদ্ধ", None), ("রোগীর", None), ("ডান", "BODY_SITE"), ("চোখে", "BODY_SITE"), ("ঝাপসা", "SYMPTOM"), ("দৃষ্টি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("সমস্যা", None), ("বাড়ছে", None), ("।", None),
        ("চোখে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("স্লিট", "TEST"), ("ল্যাম্প", "TEST"), ("পরীক্ষায়", "TEST"), ("চোখের", "BODY_SITE"), ("লেন্সে", "BODY_SITE"), ("অস্বচ্ছতা", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("রোগীর", None), ("ছানি", "DIAGNOSIS"), ("বা", None), ("ক্যাটারাক্ট", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("ফ্যাকো", "PROCEDURE"), ("সার্জারি", "PROCEDURE"), ("ও", None), ("আইওএল", "PROCEDURE"), ("প্রতিস্থাপন", "PROCEDURE"), ("করার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("মক্সিফ্লক্সাসিন", "MEDICATION"), ("আই", "MEDICATION"), ("ড্রপ", "MEDICATION"), ("এক", "DOSAGE"), ("ফোঁটা", "DOSAGE"), ("দিনে", "DOSAGE"), ("চারবার", "DOSAGE"), ("ব্যবহার্য", None), ("।", None)
    ],
    [
        ("রোগীর", None), ("চোখে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), (",", None), ("মাথা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("আলোর", None), ("চারপাশে", None), ("রংধনু", "SYMPTOM"), ("দেখছেন", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("এই", None), ("অবস্থা", None), ("।", None),
        ("টোনোমেট্রি", "TEST"), ("পরীক্ষায়", "TEST"), ("চোখের", "BODY_SITE"), ("চাপ", "TEST"), ("৪০", "TEST_RESULT"), ("মিমি", "TEST_RESULT"), ("এইচজি", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("অ্যাকিউট", "DIAGNOSIS"), ("গ্লুকোমা", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("টিমোলল", "MEDICATION"), ("ড্রপ", "MEDICATION"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("ম্যানিটল", "MEDICATION"), ("আইভি", "DOSAGE"), ("ইনফিউশন", "PROCEDURE"), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("বমি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- Category 13: ENT (Otolaryngology) ---
    [
        ("রোগীর", None), ("নাক", "BODY_SITE"), ("বন্ধ", "SYMPTOM"), (",", None), ("মাথা", "BODY_SITE"), ("ভারী", "SYMPTOM"), ("ভাব", "SYMPTOM"), ("এবং", None), ("হলুদ", None), ("সর্দি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("মুখের", "BODY_SITE"), ("হাড়ে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("নাকের", "BODY_SITE"), ("এক্স-রে", "TEST"), ("পিএনএস", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ম্যাক্সিলারি", "BODY_SITE"), ("সাইনাসে", "BODY_SITE"), ("তরল", "TEST_RESULT"), ("জমেছে", "TEST_RESULT"), ("।", None),
        ("ক্রনিক", "DIAGNOSIS"), ("সাইনোসাইটিস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("অ্যামোক্সিক্ল্যাভ", "MEDICATION"), ("৬২৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("ফ্লুটিকাসোন", "MEDICATION"), ("নেজাল", "MEDICATION"), ("স্প্রে", "MEDICATION"), ("দুই", "DOSAGE"), ("পাফ", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("সাইনাস", "PROCEDURE"), ("অ্যানট্রাল", "PROCEDURE"), ("ওয়াশ", "PROCEDURE"), ("বিবেচনা", None), ("করা", None), ("হচ্ছে", None), ("।", None)
    ],

    # --- Category 14: Oncology & Hematology ---
    [
        ("রোগীর", None), ("ঘাড়ে", "BODY_SITE"), ("ব্যথাহীন", None), ("গোটা", "SYMPTOM"), ("বা", None), ("ফোলা", "SYMPTOM"), ("দেখা", None), ("দিয়েছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("রাতে", "TEMPORAL"), ("জ্বর", "SYMPTOM"), ("ও", None), ("ঘাম", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("কাশির", "SYMPTOM"), ("সমস্যা", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("লিম্ফ", "BODY_SITE"), ("নোড", "BODY_SITE"), ("এফএনএসি", "TEST"), ("পরীক্ষা", "TEST"), ("করা", None), ("হয়েছে", None), (",", None),
        ("ম্যালিগন্যান্ট", "TEST_RESULT"), ("কোষ", "TEST_RESULT"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("।", None),
        ("পরবর্তীতে", "TEMPORAL"), ("এক্সিশনাল", "PROCEDURE"), ("বায়োপসি", "PROCEDURE"), ("সম্পন্ন", None), ("করা", None), ("হলো", None), ("।", None),
        ("হজকিন্স", "DIAGNOSIS"), ("লিম্ফোমা", "DIAGNOSIS"), ("নিশ্চিত", None), ("হয়েছে", None), ("।", None),
        ("কেমোথেরাপির", "PROCEDURE"), ("জন্য", None), ("অনকোলজি", None), ("রেফার", None), ("করা", None), ("হলো", None), ("।", None)
    ],

    # --- Category 15: Obstetrics & Gynecology ---
    [
        ("গর্ভবতী", None), ("রোগীর", None), ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("মাথা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("ও", None), ("চোখে", "BODY_SITE"), ("ঝাপসা", "SYMPTOM"), ("দেখা", "SYMPTOM"), ("শুরু", None), ("হয়েছে", None), ("।", None),
        ("রক্তচাপ", "TEST"), ("মেপে", None), ("পাওয়া", None), ("গেল", None), ("১৬০/১১০", "TEST_RESULT"), ("মিমি", "TEST_RESULT"), ("এইচজি", "TEST_RESULT"), ("।", None),
        ("ইউরিন", "TEST"), ("প্রোটিন", "TEST"), ("৩+", "TEST_RESULT"), ("পজিটিভ", "TEST_RESULT"), ("।", None),
        ("প্রি-এক্লাম্পসিয়া", "DIAGNOSIS"), ("রোগ", None), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("খিঁচুনি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ম্যাগনেসিয়াম", "MEDICATION"), ("সালফেট", "MEDICATION"), ("আইভি", "DOSAGE"), ("ইনফিউশন", "PROCEDURE"), ("লোডিং", "DOSAGE"), ("ডোজ", "DOSAGE"), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("ল্যাবেটালোল", "MEDICATION"), ("১০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("মুখে", "DOSAGE"), ("খাওয়ানো", None), ("হয়েছে", None), ("।", None),
        ("জরুরি", None), ("সিজারিয়ান", "PROCEDURE"), ("ডেলিভারি", "PROCEDURE"), ("সম্পন্ন", None), ("করা", None), ("হলো", None), ("।", None)
    ],

    # ================================================================
    # NEW CASES — Additional conditions for corpus diversity
    # ================================================================

    # --- NEW: Typhoid Fever (General Medicine) ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("ধাপে", None), ("ধাপে", None), ("বাড়তে", None), ("থাকা", None), ("জ্বর", "SYMPTOM"), ("আছে", None), ("।", None),
        ("পেটে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("ডায়রিয়া", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("উইডাল", "TEST"), ("টেস্ট", "TEST"), ("পজিটিভ", "TEST_RESULT"), ("এসেছে", None), ("।", None),
        ("রোগী", None), ("টাইফয়েড", "DIAGNOSIS"), ("জ্বরে", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("সেফিক্সিম", "MEDICATION"), ("২০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("চৌদ্দ", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("বমি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Chickenpox / Varicella (General Medicine) ---
    [
        ("রোগীর", None), ("সারা", "BODY_SITE"), ("শরীরে", "BODY_SITE"), ("পানিভরা", "SYMPTOM"), ("ফোসকা", "SYMPTOM"), ("উঠেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("জ্বর", "SYMPTOM"), ("ও", None), ("চুলকানি", "SYMPTOM"), ("আছে", None), ("।", None),
        ("রোগী", None), ("চিকেনপক্স", "DIAGNOSIS"), ("বা", None), ("জলবসন্ত", "DIAGNOSIS"), ("আক্রান্ত", None), ("।", None),
        ("অ্যাসাইক্লোভির", "MEDICATION"), ("৮০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("পাঁচবার", "DOSAGE"),
        ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("ক্যালামাইন", "MEDICATION"), ("লোশন", "MEDICATION"), ("ত্বকে", "BODY_SITE"), ("লাগাতে", None), ("বলা", None), ("হলো", None), ("।", None),
        ("শ্বাসকষ্ট", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Atrial Fibrillation (Cardiology) ---
    [
        ("রোগীর", None), ("অনিয়মিত", None), ("বুক", "BODY_SITE"), ("ধড়ফড়", "SYMPTOM"), ("এবং", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("মাথা", "BODY_SITE"), ("ঘোরা", "SYMPTOM"), ("আছে", None), ("।", None),
        ("ইসিজি", "TEST"), ("পরীক্ষায়", "TEST"), ("অ্যাট্রিয়াল", "TEST_RESULT"), ("ফিব্রিলেশন", "TEST_RESULT"), ("ধরা", None), ("পড়েছে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ওয়ারফারিন", "MEDICATION"), ("৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("প্রতিদিন", "DOSAGE"),
        ("এবং", None), ("ডিগক্সিন", "MEDICATION"), ("০.২৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("আইএনআর", "TEST"), ("মনিটরিং", "TEST"), ("প্রতি", "TEMPORAL"), ("সপ্তাহে", "TEMPORAL"), ("করতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Pleural Effusion (Pulmonology) ---
    [
        ("রোগীর", None), ("তীব্র", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("এবং", None), ("বুকের", "BODY_SITE"), ("ডান", "BODY_SITE"), ("পাশে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("আছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("কাশি", "SYMPTOM"), ("চলছে", None), ("।", None),
        ("বুকের", "BODY_SITE"), ("এক্স-রে", "TEST"), ("পরীক্ষায়", "TEST"), ("ডান", "BODY_SITE"), ("ফুসফুসে", "BODY_SITE"), ("তরল", "TEST_RESULT"), ("জমেছে", "TEST_RESULT"), ("।", None),
        ("প্লুরাল", "DIAGNOSIS"), ("ইফিউশন", "DIAGNOSIS"), ("নিশ্চিত", None), ("হয়েছে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("থোরাসেন্টেসিস", "PROCEDURE"), ("করে", None), ("তরল", None), ("বের", None), ("করা", None), ("হয়েছে", None), ("।", None),
        ("প্লুরাল", "TEST"), ("ফ্লুইড", "TEST"), ("বিশ্লেষণের", "TEST"), ("জন্য", None), ("পাঠানো", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Acute Pancreatitis (Gastroenterology) ---
    [
        ("রোগীর", None), ("পেটের", "BODY_SITE"), ("উপরের", "BODY_SITE"), ("অংশে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("পিঠে", "BODY_SITE"), ("ছড়িয়ে", None), ("যাচ্ছে", None), ("।", None),
        ("বারবার", None), ("বমি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("কিছু", None), ("খেতে", None), ("পারছেন", None), ("না", "NEGATION_UNCERTAINTY"), ("।", None),
        ("সিরাম", "TEST"), ("অ্যামাইলেজ", "TEST"), ("১২০০", "TEST_RESULT"), ("ইউ/এল", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("তীব্র", "DIAGNOSIS"), ("প্যানক্রিয়াটাইটিস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("রোগীকে", None), ("এনপিও", None), ("রেখে", None), ("আইভি", "DOSAGE"), ("ফ্লুইড", "PROCEDURE"), ("ও", None),
        ("ট্রামাডল", "MEDICATION"), ("৫০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("আইভি", "DOSAGE"), ("ব্যথানাশক", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("পেটের", "BODY_SITE"), ("সিটি", "TEST"), ("স্ক্যান", "TEST"), ("করার", None), ("নির্দেশ", None), ("দেওয়া", None), ("হয়েছে", None), ("।", None)
    ],

    # --- NEW: Diabetic Ketoacidosis / DKA (Endocrinology) ---
    [
        ("ডায়াবেটিক", "DIAGNOSIS"), ("রোগীর", None), ("তীব্র", None), ("বমি", "SYMPTOM"), (",", None), ("পেটে", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("অতিরিক্ত", None), ("তৃষ্ণা", "SYMPTOM"), ("আছে", None), ("।", None),
        ("শ্বাসকষ্ট", "SYMPTOM"), ("ও", None), ("ঝিমুনি", "SYMPTOM"), ("দেখা", None), ("দিয়েছে", None), ("।", None),
        ("রক্তের", "BODY_SITE"), ("সুগার", "TEST"), ("পরীক্ষায়", "TEST"), ("৪৫০", "TEST_RESULT"), ("মিগ্রা/ডিএল", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("ইউরিনে", "BODY_SITE"), ("কিটোন", "TEST"), ("৩+", "TEST_RESULT"), ("পজিটিভ", "TEST_RESULT"), ("।", None),
        ("ডায়াবেটিক", "DIAGNOSIS"), ("কিটোঅ্যাসিডোসিস", "DIAGNOSIS"), ("বা", None), ("ডিকেএ", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("ইনসুলিন", "MEDICATION"), ("আইভি", "DOSAGE"), ("ইনফিউশন", "PROCEDURE"), ("এবং", None),
        ("নরমাল", "MEDICATION"), ("স্যালাইন", "MEDICATION"), ("আইভি", "DOSAGE"), ("দ্রুত", None), ("চালু", None), ("করা", None), ("হলো", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Nephrotic Syndrome (Nephrology) ---
    [
        ("রোগীর", None), ("সারা", "BODY_SITE"), ("শরীর", "BODY_SITE"), ("ফুলে", "SYMPTOM"), ("গেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("চোখের", "BODY_SITE"), ("নিচে", "BODY_SITE"), ("ফোলা", "SYMPTOM"), ("বাড়ছে", None), ("।", None),
        ("ইউরিন", "TEST"), ("পরীক্ষায়", "TEST"), ("প্রোটিন", "TEST_RESULT"), ("৪+", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("সিরাম", "TEST"), ("অ্যালবুমিন", "TEST"), ("১.৮", "TEST_RESULT"), ("গ্রাম/ডিএল", "TEST_RESULT"), ("যা", None), ("কম", "TEST_RESULT"), ("।", None),
        ("নেফ্রোটিক", "DIAGNOSIS"), ("সিনড্রোম", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("করা", None), ("হচ্ছে", None), ("।", None),
        ("প্রেডনিসোলোন", "MEDICATION"), ("৪০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("প্রতিদিন", "DOSAGE"), ("সকালে", "DOSAGE"), ("চলবে", None), ("।", None),
        ("ফ্রুসেমাইড", "MEDICATION"), ("৪০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("একবার", "DOSAGE"), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("রেনাল", "TEST"), ("বায়োপসি", "PROCEDURE"), ("বিবেচনা", None), ("করা", None), ("হচ্ছে", None), ("।", None)
    ],

    # --- NEW: Meningitis (Neurology) ---
    [
        ("রোগীর", None), ("তীব্র", None), ("মাথা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), (",", None), ("উচ্চ", None), ("জ্বর", "SYMPTOM"), ("এবং", None), ("ঘাড়", "BODY_SITE"), ("শক্ত", "SYMPTOM"), ("হয়ে", None), ("গেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("বমি", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("আলোতে", None), ("অস্বস্তি", "SYMPTOM"), ("আছে", None), ("।", None),
        ("সিএসএফ", "TEST"), ("বিশ্লেষণে", "TEST"), ("কোষ", "TEST_RESULT"), ("সংখ্যা", "TEST_RESULT"), ("বৃদ্ধি", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("ব্যাকটেরিয়াল", "DIAGNOSIS"), ("মেনিনজাইটিস", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("।", None),
        ("সেফট্রিয়াক্সন", "MEDICATION"), ("২", "DOSAGE"), ("গ্রাম", "DOSAGE"), ("আইভি", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("ইনজেকশন", "PROCEDURE"), ("শুরু", None), ("করা", None), ("হলো", None), ("।", None),
        ("খিঁচুনি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("লাম্বার", "PROCEDURE"), ("পাংচার", "PROCEDURE"), ("করা", None), ("হয়েছে", None), ("।", None)
    ],

    # --- NEW: Herpes Zoster / Shingles (Dermatology) ---
    [
        ("রোগীর", None), ("বুকের", "BODY_SITE"), ("একপাশে", "BODY_SITE"), ("জ্বালাযুক্ত", "SYMPTOM"), ("ফোসকা", "SYMPTOM"), ("দেখা", None), ("দিয়েছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("পাঁচ", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("ও", None), ("জ্বালাপোড়া", "SYMPTOM"), ("আছে", None), ("।", None),
        ("হার্পিস", "DIAGNOSIS"), ("জোস্টার", "DIAGNOSIS"), ("বা", None), ("শিঙ্গলস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("ভ্যালাসাইক্লোভির", "MEDICATION"), ("১০০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"),
        ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("গ্যাবাপেন্টিন", "MEDICATION"), ("৩০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("রাতে", "DOSAGE"), ("ব্যথার", None), ("জন্য", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Gout (Orthopedics / Rheumatology) ---
    [
        ("রোগীর", None), ("পায়ের", "BODY_SITE"), ("বুড়ো", "BODY_SITE"), ("আঙুল", "BODY_SITE"), ("তীব্র", None), ("লাল", "SYMPTOM"), ("ও", None), ("ফোলা", "SYMPTOM"), ("হয়ে", None), ("গেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("হাঁটতে", None), ("পারছেন", None), ("না", "NEGATION_UNCERTAINTY"), ("।", None),
        ("রক্তে", "BODY_SITE"), ("ইউরিক", "TEST"), ("অ্যাসিড", "TEST"), ("পরীক্ষায়", "TEST"), ("৯.৮", "TEST_RESULT"), ("মিগ্রা/ডিএল", "TEST_RESULT"), ("।", None),
        ("গাউট", "DIAGNOSIS"), ("বা", None), ("গেঁটে", "DIAGNOSIS"), ("বাত", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("কোলচিসিন", "MEDICATION"), ("০.৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("ইন্ডোমেথাসিন", "MEDICATION"), ("২৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Febrile Seizure (Pediatrics) ---
    [
        ("শিশুর", None), ("উচ্চ", None), ("জ্বরের", "SYMPTOM"), ("সাথে", None), ("হঠাৎ", "TEMPORAL"), ("খিঁচুনি", "SYMPTOM"), ("হয়েছে", None), ("।", None),
        ("খিঁচুনি", "SYMPTOM"), ("প্রায়", None), ("দুই", "TEMPORAL"), ("মিনিট", "TEMPORAL"), ("স্থায়ী", None), ("ছিল", None), ("।", None),
        ("শরীরের", "BODY_SITE"), ("তাপমাত্রা", "TEST"), ("১০৩", "TEST_RESULT"), ("ডিগ্রি", "TEST_RESULT"), ("ফারেনহাইট", "TEST_RESULT"), ("।", None),
        ("ফেব্রাইল", "DIAGNOSIS"), ("সিজার", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("প্যারাসিটামল", "MEDICATION"), ("সিরাপ", "MEDICATION"), ("১৫", "DOSAGE"), ("মিগ্রা/কেজি", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("দেওয়া", None), ("হয়েছে", None), ("।", None),
        ("মস্তিষ্কের", "BODY_SITE"), ("কোনো", None), ("অস্বাভাবিকতা", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Bronchiolitis (Pediatrics) ---
    [
        ("ছোট", None), ("শিশুর", None), ("গত", "TEMPORAL"), ("চার", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("সর্দি", "SYMPTOM"), (",", None), ("কাশি", "SYMPTOM"), ("এবং", None), ("শ্বাসকষ্ট", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("বুকে", "BODY_SITE"), ("শব্দ", "SYMPTOM"), ("শোনা", None), ("যাচ্ছে", None), ("।", None),
        ("অক্সিজেন", "TEST"), ("স্যাচুরেশন", "TEST"), ("৯১%", "TEST_RESULT"), ("।", None),
        ("তীব্র", "DIAGNOSIS"), ("ব্রঙ্কিওলাইটিস", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("অক্সিজেন", "PROCEDURE"), ("মাস্ক", "PROCEDURE"), ("দিয়ে", None), ("চিকিৎসা", None), ("চলছে", None), ("।", None),
        ("নেবুলাইজেশন", "PROCEDURE"), ("সালবিউটামল", "MEDICATION"), ("দিয়ে", None), ("করা", None), ("হয়েছে", None), ("।", None),
        ("বমি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ],

    # --- NEW: Generalized Anxiety Disorder (Psychiatry) ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("অতিরিক্ত", None), ("দুশ্চিন্তা", "SYMPTOM"), (",", None), ("অস্থিরতা", "SYMPTOM"), ("এবং", None), ("ঘুমের", None), ("সমস্যা", "SYMPTOM"), ("চলছে", None), ("।", None),
        ("বুক", "BODY_SITE"), ("ধড়ফড়", "SYMPTOM"), ("ও", None), ("মাংসপেশিতে", "BODY_SITE"), ("টান", "SYMPTOM"), ("অনুভব", None), ("করেন", None), ("।", None),
        ("থাইরয়েড", "TEST"), ("টেস্ট", "TEST"), ("স্বাভাবিক", "TEST_RESULT"), ("।", None),
        ("জেনারেলাইজড", "DIAGNOSIS"), ("অ্যাংজাইটি", "DIAGNOSIS"), ("ডিসঅর্ডার", "DIAGNOSIS"), ("চিহ্নিত", None), ("হলো", None), ("।", None),
        ("আত্মহত্যার", "SYMPTOM"), ("চিন্তা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("বুসপাইরন", "MEDICATION"), ("৫", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("কগনিটিভ", "PROCEDURE"), ("বিহেভিয়রাল", "PROCEDURE"), ("থেরাপি", "PROCEDURE"), ("শুরু", None), ("করার", None), ("পরামর্শ", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Schizophrenia (Psychiatry) ---
    [
        ("রোগী", None), ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("একা", None), ("একা", None), ("কথা", None), ("বলেন", None), ("এবং", None), ("সন্দেহপ্রবণ", "SYMPTOM"), ("হয়ে", None), ("গেছেন", None), ("।", None),
        ("গায়েবি", None), ("আওয়াজ", "SYMPTOM"), ("শোনেন", None), ("বলে", None), ("জানান", None), ("।", None),
        ("ঘুমের", None), ("সমস্যা", "SYMPTOM"), ("আছে", None), ("।", None),
        ("সাইকিয়াট্রিক", "TEST"), ("মূল্যায়নে", "TEST"), ("সিজোফ্রেনিয়া", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হয়েছে", None), ("।", None),
        ("শারীরিক", None), ("আঘাতের", None), ("ইতিহাস", None), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("রিসপেরিডন", "MEDICATION"), ("২", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("শুরু", None), ("করা", None), ("হলো", None), ("।", None),
        ("পরবর্তী", "TEMPORAL"), ("সাক্ষাতের", None), ("তারিখ", None), ("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("পর", "TEMPORAL"), ("।", None)
    ],

    # --- NEW: Conjunctivitis (Ophthalmology) ---
    [
        ("রোগীর", None), ("উভয়", "BODY_SITE"), ("চোখ", "BODY_SITE"), ("লাল", "SYMPTOM"), ("হয়ে", None), ("গেছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("চোখ", "BODY_SITE"), ("থেকে", None), ("পানি", "SYMPTOM"), ("পড়ছে", None), ("ও", None), ("চুলকানি", "SYMPTOM"), ("আছে", None), ("।", None),
        ("দৃষ্টি", None), ("ঝাপসা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("অ্যালার্জিক", "DIAGNOSIS"), ("কনজাংটিভাইটিস", "DIAGNOSIS"), ("নির্ণয়", None), ("করা", None), ("হলো", None), ("।", None),
        ("ওলোপ্যাটাডিন", "MEDICATION"), ("আই", "MEDICATION"), ("ড্রপ", "MEDICATION"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("কোল্ড", None), ("কম্প্রেস", None), ("দিতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Tonsillitis (ENT) ---
    [
        ("রোগীর", None), ("গলা", "BODY_SITE"), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("খাবার", None), ("গিলতে", None), ("কষ্ট", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("তিন", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("উচ্চ", None), ("জ্বর", "SYMPTOM"), ("আছে", None), ("।", None),
        ("গলার", "BODY_SITE"), ("পরীক্ষায়", "TEST"), ("টনসিল", "BODY_SITE"), ("ফোলা", "TEST_RESULT"), ("ও", None), ("পুঁজ", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("তীব্র", "DIAGNOSIS"), ("টনসিলাইটিস", "DIAGNOSIS"), ("নির্ণয়", None), ("হলো", None), ("।", None),
        ("কাশি", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("অ্যামোক্সিসিলিন", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"),
        ("সাত", "DOSAGE"), ("দিন", "DOSAGE"), ("চলবে", None), ("।", None),
        ("আইবুপ্রোফেন", "MEDICATION"), ("৪০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("ব্যথার", None), ("জন্য", None), ("দেওয়া", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Otitis Externa (ENT) ---
    [
        ("রোগীর", None), ("কানে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("ও", None), ("চুলকানি", "SYMPTOM"), ("আছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("পাঁচ", "TEMPORAL"), ("দিন", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("কান", "BODY_SITE"), ("থেকে", None), ("পুঁজ", "SYMPTOM"), ("বের", None), ("হচ্ছে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ওটোস্কোপি", "TEST"), ("পরীক্ষায়", "TEST"), ("কানের", "BODY_SITE"), ("বহিঃপথে", "BODY_SITE"), ("প্রদাহ", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("ওটাইটিস", "DIAGNOSIS"), ("এক্সটার্না", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("সিপ্রোফ্লক্সাসিন", "MEDICATION"), ("ইয়ার", "MEDICATION"), ("ড্রপ", "MEDICATION"), ("দিনে", "DOSAGE"), ("তিনবার", "DOSAGE"), ("চলবে", None), ("।", None),
        ("কান", "BODY_SITE"), ("শুকনো", None), ("রাখতে", None), ("বলা", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Breast Cancer (Oncology) ---
    [
        ("রোগীর", None), ("ডান", "BODY_SITE"), ("স্তনে", "BODY_SITE"), ("শক্ত", None), ("গোটা", "SYMPTOM"), ("অনুভূত", None), ("হচ্ছে", None), ("।", None),
        ("গত", "TEMPORAL"), ("দুই", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"), ("ক্রমশ", None), ("বড়", None), ("হচ্ছে", None), ("।", None),
        ("ব্যথা", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None),
        ("ম্যামোগ্রাফি", "TEST"), ("পরীক্ষায়", "TEST"), ("সন্দেহজনক", "TEST_RESULT"), ("মাস", "TEST_RESULT"), ("চিহ্নিত", None), ("হয়েছে", None), ("।", None),
        ("এফএনএসি", "TEST"), ("রিপোর্টে", None), ("ম্যালিগন্যান্ট", "TEST_RESULT"), ("কোষ", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("স্তন", "DIAGNOSIS"), ("ক্যান্সার", "DIAGNOSIS"), ("নিশ্চিত", None), ("হলো", None), ("।", None),
        ("সার্জারি", "PROCEDURE"), ("ও", None), ("কেমোথেরাপির", "PROCEDURE"), ("জন্য", None), ("অনকোলজি", None), ("বিভাগে", None), ("রেফার", None), ("করা", None), ("হলো", None), ("।", None)
    ],

    # --- NEW: Leukemia (Oncology) ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("এক", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("দুর্বলতা", "SYMPTOM"), (",", None), ("ফ্যাকাশে", "SYMPTOM"), ("ভাব", None), ("এবং", None), ("বারবার", None), ("জ্বর", "SYMPTOM"), ("আসছে", None), ("।", None),
        ("মাড়ি", "BODY_SITE"), ("থেকে", None), ("রক্তক্ষরণ", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("সিবিসি", "TEST"), ("রিপোর্টে", None), ("ডব্লিউবিসি", "TEST"), ("৮৫০০০", "TEST_RESULT"), ("এবং", None),
        ("হিমোগ্লোবিন", "TEST"), ("৬.২", "TEST_RESULT"), ("গ্রাম/ডিএল", "TEST_RESULT"), ("।", None),
        ("পেরিফেরাল", "TEST"), ("ব্লাড", "TEST"), ("স্মিয়ারে", "TEST"), ("ব্লাস্ট", "TEST_RESULT"), ("কোষ", "TEST_RESULT"), ("দেখা", None), ("গেছে", None), ("।", None),
        ("লিউকেমিয়া", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("করা", None), ("হচ্ছে", None), ("।", None),
        ("বোন", "PROCEDURE"), ("ম্যারো", "PROCEDURE"), ("বায়োপসি", "PROCEDURE"), ("করার", None), ("নির্দেশ", None), ("দেওয়া", None), ("হলো", None), ("।", None),
        ("রক্ত", "PROCEDURE"), ("সঞ্চালন", "PROCEDURE"), ("দেওয়া", None), ("হয়েছে", None), ("।", None)
    ],

    # --- NEW: Ectopic Pregnancy (OB-GYN) ---
    [
        ("রোগীর", None), ("তলপেটে", "BODY_SITE"), ("তীব্র", None), ("ব্যথা", "SYMPTOM"), ("এবং", None), ("যোনিপথে", "BODY_SITE"), ("রক্তপাত", "SYMPTOM"), ("হচ্ছে", None), ("।", None),
        ("শেষ", "TEMPORAL"), ("মাসিকের", "TEMPORAL"), ("পর", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL"), ("হয়েছে", None), ("।", None),
        ("ইউরিন", "TEST"), ("প্রেগন্যান্সি", "TEST"), ("টেস্ট", "TEST"), ("পজিটিভ", "TEST_RESULT"), ("।", None),
        ("পেটের", "BODY_SITE"), ("ইউএসজি", "TEST"), ("করে", None), ("জরায়ুতে", "BODY_SITE"), ("ভ্রূণ", None), ("পাওয়া", None), ("যায়নি", "NEGATION_UNCERTAINTY"), ("।", None),
        ("এক্টোপিক", "DIAGNOSIS"), ("প্রেগন্যান্সি", "DIAGNOSIS"), ("বা", None), ("জরায়ুর", "BODY_SITE"), ("বাইরে", "BODY_SITE"), ("গর্ভধারণ", "DIAGNOSIS"), ("সন্দেহ", "NEGATION_UNCERTAINTY"), ("।", None),
        ("জরুরি", None), ("ল্যাপারোস্কোপিক", "PROCEDURE"), ("সার্জারি", "PROCEDURE"), ("সম্পন্ন", None), ("করা", None), ("হলো", None), ("।", None),
        ("সিরাম", "TEST"), ("বিটা-এইচসিজি", "TEST"), ("মনিটরিং", None), ("চলছে", None), ("।", None)
    ],

    # --- NEW: PCOS / Polycystic Ovarian Syndrome (OB-GYN) ---
    [
        ("রোগীর", None), ("গত", "TEMPORAL"), ("ছয়", "TEMPORAL"), ("মাস", "TEMPORAL"), ("ধরে", "TEMPORAL"),
        ("অনিয়মিত", "SYMPTOM"), ("মাসিক", "SYMPTOM"), ("চলছে", None), ("।", None),
        ("মুখে", "BODY_SITE"), ("ব্রণ", "SYMPTOM"), ("এবং", None), ("অবাঞ্ছিত", None), ("লোম", "SYMPTOM"), ("বৃদ্ধি", "SYMPTOM"), ("পেয়েছে", None), ("।", None),
        ("পেটের", "BODY_SITE"), ("আল্ট্রাসাউন্ড", "TEST"), ("পরীক্ষায়", "TEST"), ("ডিম্বাশয়ে", "BODY_SITE"), ("একাধিক", "TEST_RESULT"), ("সিস্ট", "TEST_RESULT"), ("পাওয়া", None), ("গেছে", None), ("।", None),
        ("পিসিওএস", "DIAGNOSIS"), ("বা", None), ("পলিসিস্টিক", "DIAGNOSIS"), ("ওভারিয়ান", "DIAGNOSIS"), ("সিনড্রোম", "DIAGNOSIS"), ("নির্ণয়", None), ("হলো", None), ("।", None),
        ("ওজন", "SYMPTOM"), ("বেড়ে", "SYMPTOM"), ("গেছে", None), ("।", None),
        ("মেটফরমিন", "MEDICATION"), ("৫০০", "DOSAGE"), ("মিগ্রা", "DOSAGE"), ("দিনে", "DOSAGE"), ("দুইবার", "DOSAGE"),
        ("এবং", None), ("জন্মনিয়ন্ত্রণ", "MEDICATION"), ("বড়ি", "MEDICATION"), ("চলবে", None), ("।", None),
        ("জ্বর", "SYMPTOM"), ("নেই", "NEGATION_UNCERTAINTY"), ("।", None)
    ]
]

# Variations bank to expand corpus size realistically while maintaining diverse clinical scenarios
AGE_GENDER_PREFIXES = [
    [("রোগীর", None)],
    [("৫০", None), ("বছর", None), ("বয়সী", None), ("পুরুষ", None), ("রোগীর", None)],
    [("৪৫", None), ("বছর", None), ("বয়সী", None), ("মহিলা", None), ("রোগীর", None)],
    [("বৃদ্ধ", None), ("রোগীর", None)],
    [("যুবক", None), ("রোগীর", None)],
    [("একজন", None), ("৩৫", None), ("বছর", None), ("বয়সী", None), ("রোগীর", None)],
    [("হাসপাতালে", None), ("ভর্তি", None), ("রোগীর", None)],
    [("বহির্বিভাগে", None), ("আগত", None), ("রোগীর", None)],
    [("জরুরি", None), ("বিভাগে", None), ("উপস্থিত", None), ("রোগীর", None)],
    [("২৮", None), ("বছর", None), ("বয়সী", None), ("তরুণীর", None)],
    [("৬০", None), ("বছর", None), ("বয়সী", None), ("বৃদ্ধার", None)],
]

TEMPORAL_SUBS = {
    "তিন দিন": [("তিন", "TEMPORAL"), ("দিন", "TEMPORAL")],
    "চার দিন": [("চার", "TEMPORAL"), ("দিন", "TEMPORAL")],
    "পাঁচ দিন": [("পাঁচ", "TEMPORAL"), ("দিন", "TEMPORAL")],
    "এক সপ্তাহ": [("এক", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL")],
    "দুই সপ্তাহ": [("দুই", "TEMPORAL"), ("সপ্তাহ", "TEMPORAL")],
    "এক মাস": [("এক", "TEMPORAL"), ("মাস", "TEMPORAL")],
}

def generate_corpus(target_notes=400):
    notes = []
    note_id_counter = 1
    
    # Base cases expansion
    while len(notes) < target_notes:
        for base_case in CLINICAL_CASES:
            if len(notes) >= target_notes:
                break
            
            note_tokens = []
            
            # Prepend demographics variation
            if random.random() > 0.3:
                prefix = random.choice(AGE_GENDER_PREFIXES)
                note_tokens.extend(prefix)
            
            # Incorporate case tokens
            for tok, tag in base_case:
                note_tokens.append((tok, tag))
                
            note_id = f"note_{note_id_counter:04d}"
            notes.append((note_id, note_tokens))
            note_id_counter += 1
            
    return notes


def convert_to_bio_rows(notes):
    rows = []
    for note_id, tokens in notes:
        prev_tag = None
        for tok, tag in tokens:
            if not tok or not tok.strip():
                continue
            
            tok_clean = tok.strip()
            if tag is None or tag == "O":
                bio_tag = "O"
                prev_tag = None
            else:
                if prev_tag == tag:
                    bio_tag = f"I-{tag}"
                else:
                    bio_tag = f"B-{tag}"
                prev_tag = tag
            rows.append({"note_id": note_id, "token": tok_clean, "tag": bio_tag})
    return rows


def main():
    # Generating 400 notes representing comprehensive clinical encounters
    notes = generate_corpus(target_notes=400)
    rows = convert_to_bio_rows(notes)
    
    out_csv = "output/annotated_corpus.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["note_id", "token", "tag"])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Generated {len(notes)} notes with {len(rows)} tokens in {out_csv}")

if __name__ == "__main__":
    main()
