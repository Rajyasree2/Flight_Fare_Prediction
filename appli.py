from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_pred.pkl", "rb"))  # Load your trained RandomForestRegressor model

@app.route("/")
@cross_origin()
def home():
    return render_template("Home_page.html")

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Extracting features from the form
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        Total_stops = int(request.form["stops"])

        airline = request.form['airline']
        Airline_IndiGo = 1 if airline == 'IndiGo' else 0
        Airline_Jet_Airways = 1 if airline == 'Jet Airways' else 0

        Source = request.form["Source"]
        Source_Delhi = 1 if Source == 'Delhi' else 0

        # Making prediction using the model
        prediction_data = [[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Airline_IndiGo,
            Airline_Jet_Airways,
            Source_Delhi
        ]]

        prediction = model.predict(prediction_data)
        output = round(prediction[0], 2)

        return render_template('Home_page.html', prediction_text="Your Flight Price is Rs. {}".format(output))

    return render_template("Home_page.html")

if __name__ == "__main__":
    app.run(debug=True)
