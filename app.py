from flask import Flask, request, render_template_string
from sklearn.tree import DecisionTreeClassifier
import os

app = Flask(__name__)

# Sample student data
X = [
    [1, 50, 10],
    [2, 60, 15],
    [3, 70, 20],
    [4, 80, 25],
    [5, 90, 30],
    [1, 40, 5],
    [2, 45, 8],
    [6, 95, 35]
]

y = [
    "Fail", "Fail", "Pass", "Pass",
    "Pass", "Fail", "Fail", "Pass"
]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

VERSION = os.getenv("MODEL_VERSION", "1.0")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Result Predictor</title>
</head>
<body>
    <h1>Student Result Predictor</h1>
    <p>Model Version: {{ version }}</p>

    <form method="POST">
        Study Hours:
        <input type="number" name="hours" min="0"
               max="24" step="0.5" required><br><br>

        Attendance (%):
        <input type="number" name="attendance" min="0"
               max="100" required><br><br>

        Internal Marks (out of 40):
        <input type="number" name="marks" min="0"
               max="40" required><br><br>

        <button type="submit">Predict Result</button>
    </form>

    {% if result %}
        <h2>Predicted Result: {{ result }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        hours = float(request.form["hours"])
        attendance = float(request.form["attendance"])
        marks = float(request.form["marks"])

        result = model.predict(
            [[hours, attendance, marks]]
        )[0]

    return render_template_string(
        HTML, result=result, version=VERSION
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
