import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv("healthcare_dataset.csv")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Normalize case for names and genders
df['Name'] = df['Name'].str.title()
df['Gender'] = df['Gender'].str.capitalize()

# Convert dates to datetime
df['Date_of_Admission'] = pd.to_datetime(df['Date_of_Admission'], errors='coerce')
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'], errors='coerce')

# Calculate stay duration
df['Stay_Duration'] = (df['Discharge_Date'] - df['Date_of_Admission']).dt.days

# Convert Billing_Amount to numeric
df['Billing_Amount'] = pd.to_numeric(df['Billing_Amount'], errors='coerce')

sns.set(style="whitegrid")

# Gender Distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Gender', palette='Set2')
plt.title("Gender Distribution", fontsize=14)
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

# Age Distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['Age'], bins=20, kde=True, color='skyblue')
plt.title("Age Distribution", fontsize=14)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Billing Amount Distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['Billing_Amount'], bins=30, kde=True, color='orange')
plt.title("Billing Amount Distribution", fontsize=14)
plt.xlabel("Billing Amount")
plt.ylabel("Frequency")
plt.show()

# Hospital Stay Duration
plt.figure(figsize=(8, 4))
sns.histplot(df['Stay_Duration'], bins=20, kde=True, color='green')
plt.title("Hospital Stay Duration (Days)", fontsize=14)
plt.xlabel("Days")
plt.ylabel("Frequency")
plt.show()

# Admission Type Distribution
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Admission_Type', palette='coolwarm')
plt.title("Admission Type Distribution", fontsize=14)
plt.xlabel("Admission Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()
