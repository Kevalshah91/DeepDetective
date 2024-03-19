import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BartForConditionalGeneration
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="")

# Initialize Generative Model
det = genai.GenerativeModel("gemini-pro")

def content_auth(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = [paragraph.get_text() for paragraph in soup.find_all('p')]
        content = ' '.join(text_content)
        user_input = "Check if the content is authentic or not: " + content
        response = det.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def bart_summarize(text):
    tokenizer = BertTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        auth_result = content_auth(url)
        if len(auth_result) > 800:
            summary = bart_summarize(auth_result)
            return render_template('index.html', auth_result=auth_result, summary=summary)
        else:
            return render_template('index.html', auth_result=auth_result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
