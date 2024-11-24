# Dependencies
from flask import Flask, request, jsonify
#from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np
import sys
import joblib
import logging
# Your API definition

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return jsonify({'mensaje':"API para prediccion de precios de vivienda"}) # Modify this message to whatever you like

    @app.route('/predict', methods=['POST'])
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

    return app

#app = create_app()
if __name__ == '__main__':
    app = create_app()
    #try:
    #    port = int(sys.argv[1]) # This is for a command-line input
    #except:
    #    port = 12345 # If you don't provide any port the port will be set to 12345
    model = joblib.load('modelo_vivienda.pkl') # Load "modelo_vivienda.pkl"
    logging.info('Modelo cargado')
    model_columns = joblib.load('model_columns.pkl') # Load "model_columns.pkl"
    logging.info('Columnas cargadas')
    #app.run(port=port, debug=True)
    app.run()
