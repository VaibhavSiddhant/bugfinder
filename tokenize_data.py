import pandas as pd
import torch
from transformers import RobertaTokenizer
import pickle

print("Loading data...")
df = pd.read_csv('data/clean.csv')
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')

print("Tokenizing... this takes a few minutes but only once")
encodings = tokenizer(
    df['code'].tolist(),
    truncation=True,
    padding='max_length',
    max_length=512
)

print("Saving tokenized data...")
with open('data/tokenized.pkl', 'wb') as f:
    pickle.dump({
        'input_ids': encodings['input_ids'],
        'attention_mask': encodings['attention_mask'],
        'labels': df['label'].tolist()
    }, f)

print("Done")
