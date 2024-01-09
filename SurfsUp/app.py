# SQLalchemy toolkit
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
absolute_path = "C:\Repos\My_Repo\sqlalchemy-challenge\Resources\hawaii.sqlite"
engine = create_engine(f"sqlite:///{absolute_path}")

# # reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)


# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Sup bruh, welcome to the Hawai'i Climate API"""
    return (
        f"Welcome! Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/temp/start/end <br/>"
            f"format date: as mmddyyyy, example: 07092016 <br/>"
           
    )

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= precip_date).\
        order_by(measurement.date.desc()).all()
    prcp_dict = {date: prcp for date, prcp in precipitation}
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list = stations_list)

@app.route("/api/v1.0/tobs")
def temperature():
        active_temps = dt.date(2017,8,23) - dt.timedelta(days=365)
        results = session.query(measurement.tobs).\
                  filter(measurement.station == 'USC00519281').\
                  filter(measurement.date >= active_temps).all()
        tobs_route = list(np.ravel(results))
        return jsonify(tobs_route = tobs_route)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    #Return Tmin, Tavg, Tmax
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]       
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps = temps)
    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date < end).all()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

    
session.close()

if __name__ == '__main__':
    app.run(debug=True)
