import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

app2 = Flask(__name__)
CORS(app2)