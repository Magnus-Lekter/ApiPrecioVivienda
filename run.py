import logging
import sys
import joblib
from app import create_app
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import numpy as np
from flask_cors import CORS



if __name__ == '__main__':
    app = create_app()
    CORS(app)
   
    model = joblib.load('modelo_vivienda.pkl') # Load "modelo_vivienda.pkl"
    logging.info('Modelo cargado')
    model_columns = joblib.load('model_columns.pkl') # Load "model_columns.pkl"
    logging.info('Columnas cargadas')
    #app.run(port=port, debug=True)
    app.run()