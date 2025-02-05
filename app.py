from flask import Flask, send_file, send_from_directory, render_template, request
from routes.main_routes import main_bp
import numpy as np
import joblib, pickle, jsonify
import pandas as pd
from dotenv import load_dotenv
import os

# 
load_dotenv()  # Load environment variables from .env file
secret_key = os.getenv("SECRET_KEY")
print(secret_key)

# Create an instance of the Flask class
app = Flask(__name__)

# register a route
app.register_blueprint(main_bp)

# Load the ML model
base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, 'models')
model_path = os.path.join(model_dir, 'random_forest_model.pkl')
model = joblib.load(model_path)

print("Model Loaded: ",type(model).__name__) # inspect the type of the model


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input data from the form
        name = request.form['name']
        age = float(request.form['age'])
        gender = int(request.form['gender'])
        systolic_bp = float(request.form['systolic_bp'])
        diastolic_bp = float(request.form['diastolic_bp'])
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        family_diabetes = int(request.form['family_diabetes'])
        hypertensive = int(request.form['hypertensive'])

        # Make a prediction using the model
        input_data = pd.DataFrame({
            'age': [age],
            'gender': [gender],
            'systolic_bp': [systolic_bp], 
            'diastolic_bp': [diastolic_bp],
            'glucose': [glucose],
            'bmi': [bmi],
            'family_diabetes': [family_diabetes],
            'hypertensive': [hypertensive],
        })
        prediction = model.predict(input_data)
        # input_data = pd.DataFrame()
        
        # Convert the prediction to a string
        prediction_str = 'Positive' if prediction == 1 else 'Negative'
        
        # Return the prediction as a JSON response
        return render_template('result.html', result=prediction_str, name=name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

print("Flask app for Diabetes Diagnosis System is ready!")