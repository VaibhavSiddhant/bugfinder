import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = RobertaTokenizer.from_pretrained('model/saved')
model = RobertaForSequenceClassification.from_pretrained('model/saved')
model.to(device)
model.eval()

def ml_predict(code):
    # Input validation
    if not code.strip():
        return {'bug': False, 'confidence': 0.0, 'type': 'Empty input'}

    enc = tokenizer(
        code,
        truncation=True,
        padding='max_length',
        max_length=512,
        return_tensors='pt'
    )
    input_ids = enc['input_ids'].to(device)
    attention_mask = enc['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        probs = torch.softmax(outputs.logits, dim=1)
        bug_confidence = probs[0][1].item()

    # Threshold control — only flag if confidence > 0.7
    bug_detected = bug_confidence > 0.7

    return {
        'bug': bug_detected,
        'confidence': round(bug_confidence, 2),
        'type': 'Potential vulnerability detected' if bug_detected else 'No vulnerability detected'
    }
