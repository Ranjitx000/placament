
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# CSV file load कर
df = pd.read_csv('submissions.csv')

# Rename columns (तुझ्या CSV च्या columns प्रमाणे adjust कर)
df.rename(columns={
    'CGPA': 'cgpa',
    'Expected Salary': 'salary',
    'attended': 'attended',
    'preferred Shift': 'shift',
    'how many year do you want work': 'work_duration',
    'placement': 'placement'
}, inplace=True)

# Categorical data convert
df['preferred-shift'] = df['preferred-shift'].map({'Day': 0, 'Night': 1})
df['attended'] = df['attended'].map({'yes': 1, 'no': 0})

# Features and target split
X = df[['cgpa', 'salary', 'attended', 'shift', 'work_duration']]
y = df['placement']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'model.pkl')
print("✅ model.pkl created successfully!")
