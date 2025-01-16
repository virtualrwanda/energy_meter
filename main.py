from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
from models import db, Prediction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Load the trained model
model = joblib.load('optimized_customer_payment_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input data from the form
    energy_meter_serial = request.form['energy_meter_serial']
    previous_month_payment = float(request.form['previous_month_payment'])
    two_months_ago_payment = float(request.form['two_months_ago_payment'])

    # Prepare the data for prediction
    input_data = np.array([[previous_month_payment, two_months_ago_payment]])

    # Predict using the model
    predicted_payment = model.predict(input_data)[0]

    # Store the prediction in the database
    new_prediction = Prediction(
        energy_meter_serial=energy_meter_serial,
        previous_month_payment=previous_month_payment,
        two_months_ago_payment=two_months_ago_payment,
        predicted_payment=predicted_payment
    )
    db.session.add(new_prediction)
    db.session.commit()

    return render_template('index.html', predicted_payment=predicted_payment)

if __name__ == '__main__':
    app.run(debug=True)
