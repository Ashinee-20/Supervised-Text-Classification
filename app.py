from flask import Flask, request, render_template
import joblib
#import pandas as pd

app = Flask(__name__)


model = joblib.load('model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')


def preprocess_text(text):
    return [text]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']

    # Check if the input text matches the default placeholder
    if text.strip() == "Enter a text for category prediction":
        return render_template('index.html', prediction='Please enter a text for category prediction.')

    input_data = preprocess_text(text)
    input_tfidf = tfidf_vectorizer.transform(input_data)
    predicted_category = model.predict(input_tfidf)[0]
    category_name = {
        1: "Business",
        2: "Technology",
        3: "Politics",
        4: "Sports",
        5: "Entertainment"
    }[predicted_category]

    return render_template('index.html', prediction=f'Predicted Category: {category_name}')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
