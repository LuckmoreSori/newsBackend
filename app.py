from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app, origins=["https://news-article-system.vercel.app"])  # Corrected origin (no trailing slash)

# Load your data
data_path = os.path.join(os.path.dirname(__file__), 'article.csv')
try:
    data = pd.read_csv(data_path)
except FileNotFoundError:
    print(f"Error: {data_path} not found.")
    data = pd.DataFrame()

@app.route('/api/articles', methods=['GET'])
def get_articles():
    if data.empty:
        return jsonify({"error": "No articles found."}), 404

    try:
        # Only select the necessary columns and drop NaNs to be safe
        required_columns = ['title','url', 'category', 'source','picture']
        articles = data[required_columns].fillna("").to_dict(orient='records')
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

