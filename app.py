# Import relevant libraries
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from flask import Flask, request, jsonify, render_template, send_file
from pyngrok import ngrok
from flask_cors import CORS


# Initialize your Flask app and enable CORS
app = Flask(__name__, template_folder='/content/templates', static_folder='/content/static')
CORS(app)

# Define your routes (home, static files)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(os.path.join('static', filename) if not filename.startswith('static/') else filename)

# Load your dataset (replace 'your_dataset.csv' with the actual file path)
data = pd.read_csv('duplicate1.csv')

# Assuming your dataset has columns 'Q1' to 'Q40' for the 40 questionnaire responses
# For each category, X represents the features (questionnaire responses)
X_well_being = data[['wb_q1', 'wb_q2', 'wb_q3', 'wb_q4', 'wb_q5', 'wb_q6', 'wb_q7', 'wb_q8', 'wb_q9', 'wb_10']].values
X_sociality = data[['soc_q1', 'soc_q2', 'soc_q3', 'soc_q4', 'soc_q5', 'soc_q6', 'soc_q7', 'soc_q8', 'soc_q9', 'soc_q10']].values
X_emotionality = data[['emo_q1', 'emo_q2', 'emo_q3', 'emo_q4', 'emo_q5', 'emo_q6', 'emo_q7', 'emo_q8', 'emo_q9', 'emo_q10']].values
X_self_control = data[['sc_q1', 'sc_q2', 'sc_q3', 'sc_q4', 'sc_q5', 'sc_q6', 'sc_q7', 'sc_q8', 'sc_q9', 'sc_q10']].values

# Y represents the target variables for each category (the final numerical values)
Y_well_being = data['Final Well-Being Value']
Y_sociality = data['Final Sociality Value']
Y_emotionality = data['Final Emotionality Value']
Y_self_control = data['Final Self-Control Value']

# Perform imputation for missing values
imputer = SimpleImputer(strategy='mean')
X_well_being = imputer.fit_transform(X_well_being)
X_sociality = imputer.fit_transform(X_sociality)
X_emotionality = imputer.fit_transform(X_emotionality)
X_self_control = imputer.fit_transform(X_self_control)

# Split each category's data into training and testing sets
X_wb_train, X_wb_test, Y_wb_train, Y_wb_test = train_test_split(X_well_being, Y_well_being, test_size=0.2, random_state=42)
X_so_train, X_so_test, Y_so_train, Y_so_test = train_test_split(X_sociality, Y_sociality, test_size=0.2, random_state=42)
X_em_train, X_em_test, Y_em_train, Y_em_test = train_test_split(X_emotionality, Y_emotionality, test_size=0.2, random_state=42)
X_sc_train, X_sc_test, Y_sc_train, Y_sc_test = train_test_split(X_self_control, Y_self_control, test_size=0.2, random_state=42)

# Create Linear Regression models for each category
model_well_being = LinearRegression()
model_sociality = LinearRegression()
model_emotionality = LinearRegression()
model_self_control = LinearRegression()

# Fit each model to its respective training data
model_well_being.fit(X_wb_train, Y_wb_train)
model_sociality.fit(X_so_train, Y_so_train)
model_emotionality.fit(X_em_train, Y_em_train)
model_self_control.fit(X_sc_train, Y_sc_train)

# Define a prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json(force=True)  # Expecting JSON data from the frontend

        # Extract user responses and cast them to numeric values with a default of 1
        user_well_being = [float(data.get('wb_q1', 1)), float(data.get('wb_q2', 1)), float(data.get('wb_q3', 1)), float(data.get('wb_q4', 1)), float(data.get('wb_q5', 1)), float(data.get('wb_q6', 1)), float(data.get('wb_q7', 1)), float(data.get('wb_q8', 1)), float(data.get('wb_q9', 1)), float(data.get('wb_q10', 1))]
        user_sociality = [float(data.get('soc_q1', 1)), float(data.get('soc_q2', 1)), float(data.get('soc_q3', 1)), float(data.get('soc_q4', 1)), float(data.get('soc_q5', 1)), float(data.get('soc_q6', 1)), float(data.get('soc_q7', 1)), float(data.get('soc_q8', 1)), float(data.get('soc_q9', 1)), float(data.get('soc_q10', 1))]
        user_emotionality = [float(data.get('emo_q1', 1)), float(data.get('emo_q2', 1)), float(data.get('emo_q3', 1)), float(data.get('emo_q4', 1)), float(data.get('emo_q5', 1)), float(data.get('emo_q6', 1)), float(data.get('emo_q7', 1)), float(data.get('emo_q8', 1)), float(data.get('emo_q9', 1)), float(data.get('emo_q10', 1))]
        user_self_control = [float(data.get('sc_q1', 1)), float(data.get('sc_q2', 1)), float(data.get('sc_q3', 1)), float(data.get('sc_q4', 1)), float(data.get('sc_q5', 1)), float(data.get('sc_q6', 1)), float(data.get('sc_q7', 1)), float(data.get('sc_q8', 1)), float(data.get('sc_q9', 1)), float(data.get('sc_q10', 1))]

        # Make predictions using the respective models
        well_being_pred = model_well_being.predict([user_well_being])
        sociality_pred = model_sociality.predict([user_sociality])
        emotionality_pred = model_emotionality.predict([user_emotionality])
        self_control_pred = model_self_control.predict([user_self_control])

        # Prepare and return predictions as JSON
        predictions = {
            'well_being': well_being_pred[0],
            'sociality': sociality_pred[0],
            'emotionality': emotionality_pred[0],
            'self_control': self_control_pred[0]
        }

        return jsonify(predictions)
    else:
        return "This is a POST request to /predict"

if __name__ == '__main__':
    public_url = ngrok.connect(addr='5000', proto='http')
    print(' * ngrok tunnel "{}" -> "http://127.0.0.1:{}/"'.format(public_url, 5000))
    app.run(port=5000)
