from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
import keras as K
import numpy as np
from keras.datasets import imdb
from keras.preprocessing import sequence
import tensorflow as tf
from keras.datasets import imdb
from keras.models import load_model
from tensorflow.python.framework import ops
from tensorflow.keras.models import Sequential

app = Flask(__name__,static_url_path='/static')
Bootstrap(app)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def image(): 
    return render_template('index.html')

def init():
    global model
    # load the pre-trained Keras model
    model = load_model('sentiment_analysis.h5')


@app.route('/analyse',methods=['POST'])
def analyse():
    if request.method == 'POST':
        analysis=''
        rawtext = request.form['rawtext']
        d = imdb.get_word_index()
        print(rawtext)
        words = rawtext.split()
        review = []
        for word in words:
            if word not in d:
                review.append(2)
            else:
                review.append(d[word] + 3)
        review = sequence.pad_sequences([review], truncating='pre', padding='pre', maxlen=80)
        prediction = model.predict(review)
        print(prediction)
        if prediction >=0.8:
            analysis='VERY POSITIVE :-)'
        elif prediction>=0.5 and prediction<0.8:
            analysis='POSITIVE :-)'
        elif prediction>=0.35 and prediction<0.5:
            analysis= 'SLIGHTLY POSITIVE'
        elif prediction>=0.26 and prediction<0.35:
            analysis= 'NEUTRAL'
        else:
            analysis='NEGATIVE :-('

    return render_template('index.html',received_text =rawtext,analysis=analysis)
















if __name__ == '__main__':
    init()
    app.run()