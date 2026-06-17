from flask import Flask, jsonify
import torch
from lstm_model import FailurePredictor

app = Flask(__name__)

model = FailurePredictor()
model.load_state_dict(
    torch.load(
        "ml/models/failure_predictor.pt",
        map_location="cpu"
    )
)

model.eval()

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model": "lstm-v1"
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5050
    )