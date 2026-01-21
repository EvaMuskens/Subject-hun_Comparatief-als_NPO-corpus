"""
Last version: Jan 15 2026
Author: EvaMuskens
Assisted by AI (ChatGPT)
"""

from pathlib import Path
from jiwer import wer
import re


def load_text(path):
    return Path(path).read_text(encoding="cp1252")


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# === bestanden ===
gold_file = "test_45min_golden_standard.txt"

model_files = {
    "model_1": "test_45min_small.txt",
    "model_2": "test_45min_medium.txt",
    "model_3": "test_45min_amberscript.txt",
}

# === gold standard ===
gold_text = normalize(load_text(gold_file))

# === WER per model ===
for model_name, file_path in model_files.items():
    hyp_text = normalize(load_text(file_path))
    score = wer(gold_text, hyp_text)
    print(f"{model_name}: WER = {score:.3f}")