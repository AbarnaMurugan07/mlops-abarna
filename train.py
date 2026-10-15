import os
import joblib
from sklearn.tree import DecisionTreeClassifier

MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0")

X = [
    [1, 50, 10], [2, 60, 15],
    [3, 70, 20], [4, 80, 25],
    [5, 90, 30], [1, 40, 5],
    [2, 45, 8], [6, 95, 35]
]
y = ["Fail", "Fail", "Pass", "Pass",
     "Pass", "Fail", "Fail", "Pass"]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

joblib.dump(
    {"model": model, "version": MODEL_VERSION},
    "model.joblib"
)

print("Model trained successfully:", MODEL_VERSION)
