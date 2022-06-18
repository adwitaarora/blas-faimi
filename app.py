from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv

from sqlalchemy import false
from sentimentAnalysis import analyseEnglish, analyseHindi
from googletrans import Translator

translator = Translator()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # label = db.Column(db.String(200))

    def __repr__(self):
        return '<Post %r>' % self.content


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_content = request.form['textContent']
        new_post = Post(content=post_content)
        try:
            db.session.add(new_post)
            db.session.commit()
            post = [post_content]
            language = translator.detect(post_content).lang

            with open('input_posts.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(post)
            print(language)
            try:
                if language == 'en' :
                    prediction, certainity = analyseEnglish(post_content)
                elif language == 'hi':
                    prediction, certainity = analyseHindi(post_content)
                else:
                    post_content = translator.translate(post_content, dest='en')
                    prediction, certainity = analyseEnglish(post_content)
            except:
                prediction = "Could Not Predict"
            print(prediction)
            return render_template ('index.html')
        except:
            return "Error Occurred"
    else:
        posts = Post.query.all()
        return render_template('index.html', posts=posts, predicted = False)


if __name__ == "__main__":
    app.run(debug=True)
