from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from transformers import pipeline

app = Flask(__name__)

# Load pre-trained transformer model for the chatbot
chatbot = pipeline("text-generation", model="distilgpt2", cache_dir="/dev/null")
# Function to search Google
def google_search(query, num_results=3):
    results = []
    for url in search(query, num=num_results, stop=num_results, lang="en"):
        results.append(url)
    return results

# Function to scrape text from a website
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        
        text = " ".join([para.get_text() for para in paragraphs[:5]])  
        return text if text else "No content found."
    
    except requests.exceptions.RequestException as e:
        return f"Error scraping {url}: {e}"

@app.route("/chat", methods=["GET"])
def chat():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # If the user wants web search
    if "search" in query.lower():
        search_results = google_search(query)
        search_texts = [scrape_website(url) for url in search_results]
        return jsonify(search_texts)

    # Otherwise, use the chatbot model
    response = chatbot(query, max_length=100, do_sample=True)[0]["generated_text"]
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
