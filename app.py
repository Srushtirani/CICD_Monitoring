
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head><title>CI/CD Demo</title></head>
        <body style="font-family: Arial; text-align: center;">
            <h1>CI/CD Pipeline Demo</h1>
            <h2>Flask Application is Running!</h2>
            <p>Deployed using Docker and Jenkins.</p>
            <p>Monitoring: Application is available.</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "CICD_Monitoring"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
