from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="")
det = genai.GenerativeModel("gemini-pro")

def check_authenticity(text):
    try:
        user_input = "Check if the content is authentic or not: " + text
        response = det.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['text']
        if url:
            result = check_authenticity(url)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
