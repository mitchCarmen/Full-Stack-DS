# -----------------------------------------------------------
# Import Libraries
# -----------------------------------------------------------

import pandas as pd
from flask import Flask, request, render_template,jsonify
from wtforms import Form, FloatField, StringField
from io import StringIO
import pickle
import os
import numpy as np

# -----------------------------------------------------------
# Forms
# -----------------------------------------------------------

# Form Class
class MyForm(Form):
    FlightDate = StringField('FlightDate', default = '2010-01-09')
    DepTime = StringField('DepTime', default = '14:25')
    UniqueCarrier = StringField('UniqueCarrier', default = '9E')
    Origin = StringField('Origin', default = 'ATL')
    Dest = StringField('Dest', default = 'AUS')
    Distance = FloatField('Distance', default = 813.0)

sample_input = """FlightDate,DepTime,UniqueCarrier,Origin,Dest,Distance\n
{},{},{},{},{},{}"""

# -----------------------------------------------------------
# Custom Inference Class
# -----------------------------------------------------------
class CustomInferenceModel():
    """
    This is a template for Python inference model scoring code.
    It loads the custom model pickle, performs any necessary preprocessing or feature engineering,
    and then performs predictions.
    Note: If your model is a binary classification model, you will likely want your predict
           function to use `predict_proba`, whereas for regression you will want to use `predict`
    """

    def __init__(self, path_to_model="{}/LGBM_gridCV_flights_model.pkl".format(os.getcwd())):
        """Load the model pickle file."""

        with open(path_to_model, "rb") as picklefile:
            self.model = pickle.load(picklefile)

    def preprocess_features(self, X):
        """Add any required feature preprocessing here, if it's not handled by the pickled model"""
        """Takes a raw airline df and engineers new date time features that will be used for modeling"""
                
        X['FlightDate'] = pd.to_datetime(X['FlightDate'])
        X['Day_of_Week'] = X['FlightDate'].dt.day_name()
        X['Year'] = pd.DatetimeIndex(X['FlightDate']).year.astype('category')
        X['Month'] = pd.DatetimeIndex(X['FlightDate']).month.astype('category')
        X['Day'] = pd.DatetimeIndex(X['FlightDate']).day.astype('category')
        X['Hour'] = pd.to_datetime(X['DepTime'], format='%H:%M').dt.hour.astype('category')
        X['Minutes'] = pd.to_datetime(X['DepTime'], format='%H:%M').dt.minute.astype('category')
        X['DepTime'] = pd.to_datetime(X['DepTime'], format='%H:%M').dt.time

        return X

    def predict(self, X, positive_class_label=None, negative_class_label=None, **kwargs):
        """
        Predict with the pickled custom model.
        If your model is for classification, you likely want to ensure this function
        calls `predict_proba()`, whereas for regression it should use `predict()`
        """
        X = self.preprocess_features(X)
        prediction = self.model.predict_proba(X)
        return prediction

custom_model = CustomInferenceModel()

# -----------------------------------------------------------
# Route Function for predictions
# -----------------------------------------------------------

app = Flask(__name__, template_folder= 'frontend/templates', static_folder= 'frontend/static')

@app.route('/',methods=['GET', 'POST'])
def predict_outcome():
    """Renders a template with a form that asks for data.
       Uses that data to predict."""

    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            to_send = sample_input.format(form.FlightDate.data,
                                          form.DepTime.data,
                                          form.UniqueCarrier.data,
                                          form.Origin.data,
                                          form.Dest.data,
                                          form.Distance.data
                                          )

            data = StringIO(to_send)
            X = pd.read_csv(data)
            prediction = custom_model.predict(X)
            return render_template('apis/form.html', form = form,
                                pred = prediction)

        except ValueError:
            return render_template('apis//form.html', form=form)
    else:
        return render_template('apis//form.html', form=form)


#The code below needs to change so that we are getting results from Sagemaker, not the model saved within this application!

@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    data_df = pd.DataFrame.from_dict(data)
    prediction = custom_model.predict(data_df)

    return str(prediction)