import sys
import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
##session = Session(engine)

app = Flask (__name__)

@app.route("/")
def welcome ():
    return(
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/YYYY-MM-DD<br/>"
        f"/api/v1.0/temp/YYYY-MM-DD/YYYY-MM-DD\n"
)

@app.route("/api/v1.0/precipitation")
def precipitation ():
    session = Session(engine)
    last_one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_one_year).all()
    precip = {date:prcp for date, prcp in precipitation_scores}
    return jsonify (precip)

@app.route("/api/v1.0/stations")
def stations ():
    session = Session(engine)
    stat_no = session.query(Station.station).all()
    stat = list(np.ravel(stat_no))
    return jsonify (stat) 

@app.route("/api/v1.0/tobs")
def temperature ():
    session = Session(engine)
    last_one_year_2 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_temp = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_one_year_2 ).all()
    temp = list(np.ravel(station_temp))
    return jsonify (temp) 


#@app.route("/api/v1.0/temp/<start><br/>")
#def start(start=None):
@app.route("/api/v1.0/temp/<start_date>")
def start(start_date):
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)]
    precipitation_results = session.query(*sel).filter(Measurement.station == Station.station).filter(Measurement.date >= start_date).all()
    temp_start= list(np.ravel(precipitation_results))
    return jsonify (temp_start)

#@app.route("/api/v1.0/temp/<start>/<end>")
#def start(start=None):
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def start_end(start_date, end_date):
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)]
    precipitation_results = session.query(*sel).filter(Measurement.station == Station.station).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temp_start= list(np.ravel(precipitation_results))
    return jsonify (temp_start) 


if __name__ == '__main__':
    app.run()