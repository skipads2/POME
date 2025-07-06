# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load your promotions data
df = pd.read_csv("promotions_data.csv")

# 2. Preprocess: Encode categorical features
df['Promotion Type'] = LabelEncoder().fit_transform(df['Promotion Type'])
df['Region'] = LabelEncoder().fit_transform(df['Region'])
df['Season'] = LabelEncoder().fit_transform(df['Season'])

# Features and label
X = df[['Promotion Type', 'Region', 'Season', 'Price Elasticity']]
y = df['Successful']

# 3. Split data for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. Evaluate accuracy
print("Model accuracy:", model.score(X_test, y_test))

# 6. Save the trained model with joblib
joblib.dump(model, "promotions_model.pkl")
print("✅ Model saved as promotions_model.pkl")
