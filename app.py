import os
import joblib
from flask import Flask, request, render_template_string

app = Flask(__name__)

saved = joblib.load("model.joblib")
model = saved["model"]

VERSION = os.getenv("MODEL_VERSION", saved["version"])

PAGE = """
<html>
<head>
<title>Student Result Predictor</title>
</head>
<body style="font-family:Arial;text-align:center;margin:40px">
<h1>Student Result Predictor</h1>
<p>Model Version: {{ version }}</p>

<form method="post">
Study Hours: <input type="number" name="hours"
min="0" max="24" step="0.5" required><br><br>

Attendance (%): <input type="number" name="attendance"
min="0" max="100" required><br><br>

Internal Marks (out of 40):
<input type="number" name="marks"
min="0" max="40" required><br><br>

<button type="submit">Predict Result</button>
</form>

<h2>{{ result }}</h2>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        try:
            values = [[
                float(request.form["hours"]),
                float(request.form["attendance"]),
                float(request.form["marks"])
            ]]
            result = "Prediction: " + str(model.predict(values)[0])
        except (ValueError, KeyError):
            result = "Please enter valid values"

    return render_template_string(
        PAGE, version=VERSION, result=result
    )
