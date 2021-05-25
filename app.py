import numpy as np

import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
session = Session(engine)
app = Flask(__name__)


# List all routes that are available.
@app.route("/")
def home_page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prec():

# Perform a query to retrieve the data and precipitation scores
    year_data = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    annual_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_data).all()

    Prec_list = []
    for x in annual_prcp:
        prec_dict = {}
        prec_dict["date"] = x[0]
        prec_dict["prcp"] = x[1]
        Prec_list.append(prec_dict)

    #results = list(np.ravel(annual_prcp))

    return jsonify(Prec_list)
    
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_result = session.query(Measurement.station).group_by(Measurement.station).all()

    Stn_list = []
    for y in stations_result:
        Stn_dict = {}
        Stn_dict["station"] = y[0]
        Stn_list.append(Stn_dict)


    return jsonify(Stn_list)

# Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_data = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    annual_tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= year_data).filter(Measurement.station == 'USC00519281').all()

    Tobs_list = []
    for temp in annual_tobs:
        Tobs_dict = {}
        Tobs_dict["date"] = temp[0]
        Tobs_dict["tobs"] = temp[1]
        Tobs_list.append(Tobs_dict)


    return jsonify(Tobs_list)


if __name__ == '__main__':
    app.run(debug=True)