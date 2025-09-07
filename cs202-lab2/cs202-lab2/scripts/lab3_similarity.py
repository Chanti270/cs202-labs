import pandas as pd, numpy as np, torch, pathlib
from transformers import AutoTokenizer, AutoModel
from sacrebleu import sentence_bleu

IN  = "data/lab3_metrics.csv"
OUT = "data/lab3_metrics_similarity.csv"
pathlib.Path("data").mkdir(parents=True, exist_ok=True)

df = pd.read_csv(IN)
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def embed(text: str):
    text = "" if not isinstance(text, str) else text
    if not text.strip():
        return None
    inputs = tokenizer(text, max_length=256, truncation=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model(**inputs).last_hidden_state  # [1, L, H]
        mask = inputs["attention_mask"].unsqueeze(-1)  # [1, L, 1]
        summed = (out * mask).sum(dim=1)               # [1, H]
        counts = mask.sum(dim=1).clamp(min=1)          # [1, 1]
        emb = (summed / counts).squeeze(0).cpu().numpy()
        return emb

def cos(a, b):
    if a is None or b is None: return np.nan
    an, bn = np.linalg.norm(a), np.linalg.norm(b)
    if an == 0 or bn == 0: return np.nan
    return float(np.dot(a, b) / (an * bn))

sem_sims = []
tok_sims = []

for _, row in df.iterrows():
    old = row.get("old_code", "")
    new = row.get("new_code", "")
    # Semantic (CodeBERT cosine)
    e1, e2 = embed(str(old)), embed(str(new))
    sem_sims.append(cos(e1, e2))
    # Token BLEU (0..1)
    try:
        bleu = sentence_bleu(str(new), [str(old)]).score / 100.0
    except Exception:
        bleu = np.nan
    tok_sims.append(bleu)

df["Semantic_Similarity"] = sem_sims
df["Token_Similarity"]    = tok_sims

df.to_csv(OUT, index=False)
print(f"✅ Similarity metrics saved to {OUT}")
