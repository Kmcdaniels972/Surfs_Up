# Import dependancies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import Flask

# Set up the Database Connection
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the Database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creat a session link
session = Session(engine)

# Set up Flask
app = Flask(__name__)
@app.route("/")
def welcome():
        return(
                '''
                Welcome to the Climate Analysis API! <br>
                Available Routes: <br>
                /api/v1.0/precipitation<br>
                /api/v1.0/stations<br>
                /api/v1.0/tobs<br>
                /api/v1.0/temp/start/end<br>
                ''')

# Add Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   session.close() 
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Add Stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Add Tobs route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Add Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)