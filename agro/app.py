from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from flask_cors import CORS # CORS for handling Cross-Origin Resource Sharing
import pickle

# Create a Flask application instance
app = Flask(__name__)

# Enable CORS for all routes, allowing requests from any origin
CORS(app,resources={r"/*":{"origins":"*"}})

crop_model = pickle.load(open('crop_recommendation_model.pkl', 'rb'))
fertilizer_model = pickle.load(open('fertilizer.pkl', 'rb'))
classifier_model = pickle.load(open('classifier.pkl', 'rb'))
soil_quality_model=pickle.load(open('soil_quality.pkl' ,'rb'))



# Define a route for handling HTTP GET requests to the root URL
@app.route('/', methods=['GET'])
def get_data():
    data = {
        "message":"API is Running"
    }
    return jsonify(data)
  
# Define a route for making predictions
@app.route('/crop_predict', methods=['POST'])
def crop_predict():
    try:
        data = request.get_json()
        query_df = pd.DataFrame([data])
        prediction = crop_model.predict(query_df)
        return jsonify({'Prediction': list(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/fertilizer_predict', methods=['POST'])
def fertilizer_predict():
    try:
        data = request.get_json()
        query_df = pd.DataFrame([data])
        prediction = fertilizer_model.classes_[classifier_model.predict(query_df)]
        return jsonify({'Prediction': str(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/soil_quality_predict', methods=['POST'])
def soil_quality_predict():
    data = request.get_json()
    features = np.array([
        data['N'], data['P'], data['K'], data['pH'], data['EC'],
        data['OC'], data['S'], data['Zn'], data['Fe'], data['Cu'],
        data['Mn'], data['B']
    ]).reshape(1, -1)  # Convert to 2D array
    prediction = soil_quality_model.predict(features)
    return jsonify({'prediction': str(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)