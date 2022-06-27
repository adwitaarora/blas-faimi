from flask import Flask, render_template, url_for, request, redirect
import csv

from sentimentAnalysis import analyseEnglish, analyseHindi
from googletrans import Translator

translator = Translator()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_content = request.form['textContent']
        try:
            language = translator.detect(post_content).lang
            try:
                if language == 'en' :
                    prediction, certainity = analyseEnglish([post_content])
                elif language == 'hi':
                    prediction, certainity = analyseHindi([post_content])
                else:
                    post_content = translator.translate(post_content, dest='en').text
                    prediction, certainity = analyseEnglish([post_content])
            except:
                prediction = "Could Not Predict"
                certainity = 0
            post = [post_content, prediction]
    
            return render_template ('index.html', prediction = prediction, post = post_content, certainity = certainity, predicted = True)
        except:
            return "Error Occurred"
    else:
        return render_template('index.html', predicted = False)


if __name__ == "__main__":
    app.run(debug=True)
