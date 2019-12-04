from flask import Flask,render_template,url_for,request

# Package Imports
import pandas as pd
import json
import myutils

from tensorflow.keras.layers import *

from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from tensorflow.keras.models import load_model
from keras_preprocessing.text import tokenizer_from_json


# Data Path
dataPath = "../data"    #you can change this datapath
MAX_NB_WORDS = 100000    # max no. of words for tokenizer
MAX_SEQUENCE_LENGTH = 200 # max length of each entry (sentence), including padding
VALIDATION_SPLIT = 0.2   # data for validation (not used in training)
EMBEDDING_DIM = 100      # embedding dimensions for word vectors (word2vec/GloVe)
#you can download glove with this website: https://www.kaggle.com/terenceliu4444/glove6b100dtxt
GLOVE_DIR = "../data/glove/glove.6B."+str(EMBEDDING_DIM)+"d.txt"  #glove path
labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

#load saved model ltsm_model.h5
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    model = load_model('doc/ltsm_model.h5')

#load tokenizer model tokenizer.json
with open('doc/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

app = Flask(__name__)


@app.route('/')
def home():
    result = [0,0,0,0,0,0]
    my_prediction = dict(zip(labels, result))

    return render_template('home.html',result=my_prediction)


@app.route('/predict', methods=['POST'])
def predict():

    comments = []
    if request.method == 'POST':
        message = request.form['message']
        data = pd.Series(message)
        vect = myutils.preprocessing_test(data, tokenizer)
        pred = model.predict(vect)
        result = []
        for p in pred:
            result.append(round(float(p[0]),4))
        my_prediction = dict(zip(labels, result))

    for l, p in my_prediction.items():
        if p > 0.5:
            comments.append(l)

    return render_template('home.html', result=my_prediction, comments = comments)


if __name__ == '__main__':
    app.run(debug=True)