from flask import Flask, send_file, send_from_directory, render_template, request
from routes.main_routes import main_bp
import numpy as np
import joblib, os, pickle, jsonify

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
        systolic = float(request.form['systolic'])
        diastolic = float(request.form['diastolic'])
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        family_diabetes = int(request.form['family_diabetes'])
        hypertension = int(request.form['hypertension'])

        # Make a prediction using the model
        input_data = np.array([[age, gender, systolic, diastolic, glucose, bmi, family_diabetes, hypertension]])
        prediction = model.predict(input_data)[0]

        # Return the prediction as a JSON response
        return render_template('result.html', result=prediction, name=name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

print("Flask app for Diabetes Diagnosis System is ready!")