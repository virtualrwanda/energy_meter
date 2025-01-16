from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    energy_meter_serial = db.Column(db.String(100), nullable=False)
    previous_month_payment = db.Column(db.Float, nullable=False)
    two_months_ago_payment = db.Column(db.Float, nullable=False)
    predicted_payment = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Prediction {self.id}>'
