import torch
import pickle
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaTokenizer, RobertaForSequenceClassification, get_scheduler
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report

print("Loading tokenized data...")
with open('data/tokenized_small.pkl', 'rb') as f:
    data = pickle.load(f)

input_ids = data['input_ids']
attention_masks = data['attention_mask']
labels = data['labels']

indices = list(range(len(labels)))
from sklearn.model_selection import train_test_split
train_idx, val_idx = train_test_split(indices, test_size=0.2, random_state=42)

print(f'Train: {len(train_idx)} | Val: {len(val_idx)}')

class CodeDataset(Dataset):
    def __init__(self, indices):
        self.indices = indices

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, i):
        idx = self.indices[i]
        return {
            'input_ids': torch.tensor(input_ids[idx]),
            'attention_mask': torch.tensor(attention_masks[idx]),
            'label': torch.tensor(labels[idx], dtype=torch.long)
        }

train_loader = DataLoader(CodeDataset(train_idx), batch_size=4, shuffle=True, num_workers=0)
val_loader = DataLoader(CodeDataset(val_idx), batch_size=4, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

model = RobertaForSequenceClassification.from_pretrained('microsoft/codebert-base', num_labels=2)
model.to(device)

optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
num_epochs = 5
num_training_steps = num_epochs * len(train_loader)
scheduler = get_scheduler('linear', optimizer=optimizer, num_warmup_steps=100, num_training_steps=num_training_steps)

best_f1 = 0.0

for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for i, batch in enumerate(train_loader):
        input_ids_b = batch['input_ids'].to(device)
        attention_mask_b = batch['attention_mask'].to(device)
        labels_b = batch['label'].to(device)

        outputs = model(input_ids=input_ids_b, attention_mask=attention_mask_b, labels=labels_b)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

        if i % 20 == 0:
            print(f'Epoch {epoch+1} | Step {i}/{len(train_loader)} | Loss: {loss.item():.4f}')

    model.eval()
    all_preds, all_labels = [], []

    with torch.no_grad():
        for batch in val_loader:
            input_ids_b = batch['input_ids'].to(device)
            attention_mask_b = batch['attention_mask'].to(device)

            outputs = model(input_ids=input_ids_b, attention_mask=attention_mask_b)
            preds = outputs.logits.argmax(dim=1)

            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(batch['label'].tolist())

    f1 = f1_score(all_labels, all_preds, average='binary')
    print(f'Epoch {epoch+1} | Val F1: {f1:.4f} | Avg Loss: {total_loss/len(train_loader):.4f}')
    print(classification_report(all_labels, all_preds))

    if f1 > best_f1:
        best_f1 = f1
        from transformers import RobertaTokenizer
        tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
        model.save_pretrained('model/saved')
        tokenizer.save_pretrained('model/saved')
        print(f'New best model saved - F1: {best_f1:.4f}')

print(f'Training complete. Best F1: {best_f1:.4f}')
