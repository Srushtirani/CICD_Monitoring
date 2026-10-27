
from flask import Flask, request, jsonify, render_template_string
import pickle
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]
target_names = saved_data["target_names"]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ML Prediction Application</title>
</head>
<body style="font-family: Arial; text-align: center; margin: 50px;">
    <h1>Machine Learning Web Application</h1>
    <p>Enter Iris flower measurements to predict its species.</p>

    <form action="/predict" method="post">
        Sepal length (cm):
        <input type="number" name="sepal_length"
               step="any" min="0" required><br><br>

        Sepal width (cm):
        <input type="number" name="sepal_width"
               step="any" min="0" required><br><br>

        Petal length (cm):
        <input type="number" name="petal_length"
               step="any" min="0" required><br><br>

        Petal width (cm):
        <input type="number" name="petal_width"
               step="any" min="0" required><br><br>

        <button type="submit">Predict Species</button>
    </form>

    {% if prediction %}
        <h2>Predicted Species: {{ prediction }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, prediction=None)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return jsonify({
            "message": "Send four flower measurements using POST."
        })

    try:
        features = [
            float(request.form["sepal_length"]),
            float(request.form["sepal_width"]),
            float(request.form["petal_length"]),
            float(request.form["petal_width"])
        ]

        if any(value <= 0 for value in features):
            return "Measurements must be positive.", 400

        result = model.predict([features])[0]
        prediction = target_names[int(result)]

        return render_template_string(
            HTML, prediction=prediction
        )

    except (ValueError, KeyError):
        return "Invalid flower measurements.", 400

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "ML Prediction App",
        "model_loaded": model is not None
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
