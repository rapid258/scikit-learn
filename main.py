import sys
import os
import shutil
import time
import traceback
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib

app = Flask(__name__)

# inputs
training_data = 'data/ListaFiltrada.csv'
include = ["Nombres"]
dependent_variable = ["Sexo"]

model_directory = 'model'
model_file_pipe = '%s/modelpip.pkl' % model_directory
def Word_low(txt):
    return txt.lower()

# These will be populated at training time

pipeline = None

@app.route('/predict', methods=['POST'])
def predict():
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    if pipeline:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            query["Name"]=query["Name"].apply(Word_low)
            Nom = query["Name"].values
            print(Nom)
            prediction = list(pipeline.predict(Nom))

            # Converting to int from int64
            return jsonify({"prediction": list(prediction)})

        except Exception as e:

            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        print('train first')
        return 'no model here'


@app.route('/train', methods=['GET'])
def train():
    from sklearn.pipeline import Pipeline
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    global pipeline
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])
    Lista=pd.read_csv(training_data)

    
    start = time.time()

    pipeline.fit(Lista["Nombres"].values, Lista.Sexo)
    joblib.dump(pipeline, model_file_pipe)


    message1 = 'Trained in %.5f seconds' % (time.time() - start)
    
    return message1


@app.route('/wipe', methods=['GET'])
def wipe():
    try:
        shutil.rmtree('model')
        os.makedirs(model_directory)
        return 'Model wiped'

    except Exception as e:
        print(str(e))
        return 'Could not remove and recreate the model directory'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 80

    try:
        pipeline = joblib.load(model_file_pipe)


    except Exception as e:
        print('No model here')
        print('Train first')
        print(str(e))
        clf = None

    app.run( debug=True, host='0.0.0.0', port=port)
