# Dependencies
from flask import Flask, request, jsonify
#from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np
import sys
import joblib
import logging
from flask_cors import CORS, cross_origin
from app import create_app

app = create_app()

@app.route('/')
def home():
    return jsonify({'mensaje':"API para prediccion de precios de vivienda"})

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    global model
    global model_columns
    if model:
        try:
            if request.method == 'POST':
                        
                json_ = request.json
                if isinstance(json_, list) and all(isinstance(i, dict) for i in json_):
                    query = pd.get_dummies(pd.DataFrame(json_))
                else:
                    return jsonify({'error': 'Invalid input format. Expected a list of dictionaries.'})
                query = query.reindex(columns=model_columns, fill_value=0)

                prediction = list(model.predict(query))

                return jsonify({'prediction': prediction})
            else:
                return jsonify({'error': 'No se encontró el método POST'})
        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        logging.error('Train the model first')
        return ('No model here to use')

    




