from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
from transformers import pipeline

app = Flask(__name__)

# Use a compact HF sentiment model (downloads on first run or can be baked into image)
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error":"No message provided"}), 400

    # TextBlob sentiment score (-1 to 1)
    blob = TextBlob(user_message)
    tb_score = round(blob.sentiment.polarity, 3)

    # Transformer sentiment (POSITIVE/NEGATIVE) and confidence
    hf = sentiment_model(user_message)[0]
    hf_label = hf.get("label")
    hf_score = round(hf.get("score", 0), 3)

    # Map to richer emotions (basic mapping; expand as needed)
    if hf_label == "POSITIVE":
        if tb_score >= 0.6:
            emotion = "joy"
            bot_response = "That's wonderful — I'm so happy for you! 🌟"
        elif tb_score >= 0.2:
            emotion = "contentment"
            bot_response = "That sounds nice. Tell me more! 🙂"
        else:
            emotion = "calm"
            bot_response = "Good to hear. What's next on your mind?"
    else:  # NEGATIVE
        if tb_score <= -0.6:
            emotion = "sadness"
            bot_response = "I'm really sorry. Do you want to talk about it? 💔"
        elif tb_score <= -0.2:
            emotion = "frustration"
            bot_response = "That sounds tough. I’m here to listen. 🙏"
        else:
            emotion = "annoyance"
            bot_response = "Hmm — I hear you. Want to elaborate?"

    return jsonify({
        "user_message": user_message,
        "textblob_score": tb_score,
        "transformer_label": hf_label,
        "transformer_confidence": hf_score,
        "emotion": emotion,
        "bot_response": bot_response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
