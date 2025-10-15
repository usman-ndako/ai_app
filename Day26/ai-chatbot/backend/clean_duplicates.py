import pandas as pd
import os

# Path to your FAQ CSV
faq_path = os.path.join(os.path.dirname(__file__), "faq.csv")

if not os.path.exists(faq_path):
    print("❌ faq.csv not found!")
    exit(1)

# Load CSV
df = pd.read_csv(faq_path)
print(f"Loaded {len(df)} rows from faq.csv")

if 'question' not in df.columns or 'answer' not in df.columns:
    print("❌ CSV must have 'question' and 'answer' columns!")
    exit(1)

# Create key for deduplication (question + answer)
df['key'] = df['question'].astype(str) + '|||' + df['answer'].astype(str)

# Drop duplicates based on key, keeping first occurrence
df_clean = df.drop_duplicates(subset=['key'], keep='first')

# Remove the temp key and embedding column if present
if 'key' in df_clean.columns:
    df_clean = df_clean.drop(columns=['key'])
if 'embedding' in df_clean.columns:
    df_clean = df_clean.drop(columns=['embedding'])

# Save back to CSV
df_clean.to_csv(faq_path, index=False)

# Stats
duplicates_removed = len(df) - len(df_clean)
print(f"✅ Cleanup complete! Removed {duplicates_removed} duplicates.")
print(f"New total: {len(df_clean)} rows.")
print("Restart your FastAPI server to reload embeddings.")