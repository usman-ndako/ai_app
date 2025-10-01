# Week 1 Project: Newborn Health Insights
# Author: Usman
# Date: 2025-09-27
# Goal: Load newborn health dataset and generate simple insights

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Step 1: Load dataset
# -----------------------------
df = pd.read_csv("newborn_health.csv")

# Step 2: Preview data
print("✅ Data loaded successfully!")
print(df.head())
print("\n--- Columns ---")
print(df.columns.tolist())

# -----------------------------
# Step 3: Basic Variables & Sample Data
# -----------------------------
hospital_name = "City Neonatal Center"
report_year = 2025
print(f"\n📢 Report for {hospital_name}, Year: {report_year}")

# Sample birth weights (first 10)
birth_weights = df["birth_weight_kg"].dropna().tolist()[:10]

def manual_average(numbers):
    """Calculate average using a loop (not built-in mean)."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print("\nSample Birth Weights:", birth_weights)
print("Manual Average (first 10):", manual_average(birth_weights))
print("Pandas Average (all babies):", df["birth_weight_kg"].mean())

# -----------------------------
# Step 4: Key Statistics
# -----------------------------
avg_weight = df["birth_weight_kg"].mean()
avg_gestation = df["gestational_age_weeks"].mean()
avg_apgar = df["apgar_score"].mean()
most_common_risk = df["risk_level"].value_counts().idxmax()

print(f"\n👶 Average Gestational Age: {avg_gestation:.1f} weeks")
print(f"🚨 Most Common Risk Level: {most_common_risk}")
print("\nRisk Level Distribution:")
print(df["risk_level"].value_counts())
print(f"\n🩺 Average APGAR Score: {avg_apgar:.1f}")

# -----------------------------
# Step 5: Visualizations
# -----------------------------
# Risk Level Distribution
plt.figure(figsize=(7,5))
ax = sns.countplot(data=df, x="risk_level", palette="coolwarm")
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=10, color='black', xytext=(0,5),
                textcoords='offset points')
plt.title("🍼 Risk Level Distribution", fontsize=14, weight="bold")
plt.xlabel("Risk Level", fontsize=12)
plt.ylabel("Number of Babies", fontsize=12)
plt.tight_layout()
plt.savefig("risk_distribution.png")
plt.show()

# Birth Weight Distribution
plt.figure(figsize=(7,5))
sns.histplot(df["birth_weight_kg"], bins=20, kde=True, color="skyblue")
plt.axvline(avg_weight, color="red", linestyle="--", label=f"Avg: {avg_weight:.2f} kg")
plt.title("⚖️ Birth Weight Distribution", fontsize=14, weight="bold")
plt.xlabel("Birth Weight (kg)", fontsize=12)
plt.ylabel("Number of Babies", fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig("birth_weight_hist.png")
plt.show()

# -----------------------------
# Step 6: Automated Markdown Report
# -----------------------------
def generate_report(df, report_file="health_insights_report.md"):
    avg_weight = df["birth_weight_kg"].mean()
    avg_gestation = df["gestational_age_weeks"].mean()
    avg_apgar = df["apgar_score"].mean()
    top_risk = df["risk_level"].value_counts().idxmax()
    risk_counts = df["risk_level"].value_counts()

    # Write Markdown report with UTF-8 encoding
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# 🍼 Newborn Health Insights Report\n\n")
        f.write(f"*Hospital:* **{hospital_name}**  \n")
        f.write(f"*Year:* **{report_year}**\n\n")
        f.write("This report summarizes key findings from the newborn dataset.\n\n")
        
        f.write("## 📊 Key Statistics\n")
        f.write(f"- Total cases: **{len(df)}**\n")
        f.write(f"- Average birth weight: **{avg_weight:.2f} kg**\n")
        f.write(f"- Average gestational age: **{avg_gestation:.1f} weeks**\n")
        f.write(f"- Average APGAR score: **{avg_apgar:.1f}**\n")
        f.write(f"- Most common risk level: **{top_risk}**\n\n")
        
        f.write("## 🧾 Risk Level Distribution\n")
        f.write("| Risk Level | Count |\n")
        f.write("|-----------|-------|\n")
        for level, count in risk_counts.items():
            f.write(f"| {level} | {count} |\n")
        f.write("\n")
        
        f.write("## 📈 Visualizations\n")
        f.write("![Risk Distribution](risk_distribution.png)\n\n")
        f.write("![Birth Weight Histogram](birth_weight_hist.png)\n\n")

    print(f"✅ Report saved as {report_file}")

# Generate the report
generate_report(df)

