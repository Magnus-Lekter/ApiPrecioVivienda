import os
from flask import Flask
from flask import request, jsonify
import traceback
import pandas as pd
import numpy as np
import sys
import joblib
import logging
from flask_cors import CORS, cross_origin

def create_app():
    app=Flask(__name__)
    CORS(app) 
    return app