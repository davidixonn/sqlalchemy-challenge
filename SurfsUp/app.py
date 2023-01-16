from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite://///Users/David/Documents/BootCamp/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)


Base.classes.keys()


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    
    return (
        f"Welcome! Here are all the available API routes. <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    names = list(np.ravel(results))

    return jsonify(names)


@app.route("/api/v1.0/stations")
def stations():

    station_results = session.query(Measurement.station).all()
    station_names = list(np.ravel(station_results))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tob():

    current = dt.date(2017, 8, 23)
    year_prior = current - dt.timedelta(days=365)

    act_station_tmp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_prior).\
        filter(Measurement.date <= current).\
        order_by(Measurement.date).all()

    session.close()

    active = dict(act_station_tmp)
    return jsonify(active)


@app.route("/api/v1.0/<start>")
def start(start=None):

    start1 = session.query(func.min(Measurement.tobs)\
        , func.max(Measurement.tobs)\
        , func.round(func.avg(Measurement.tobs),2), Station.name).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date >= start).\
        group_by(Measurement.station).all()

    session.close()

    beg = []
    for min, max, avg, name in start1:
        start_dict = {}
        start_dict['min'] = min
        start_dict['max'] = max
        start_dict['avg'] = avg
        start_dict['name'] = name
        beg.append(start_dict)

    return jsonify(beg)

@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):

    range = session.query(func.min(Measurement.tobs)\
        , func.max(Measurement.tobs)\
        , func.round(func.avg(Measurement.tobs),2), Station.name).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.station).all()

    session.close()

    range_data = []
    for min, max, avg, name in range:
        range_dict = {}
        range_dict['min'] = min
        range_dict['max'] = max
        range_dict['avg'] = avg
        range_dict['name'] = name
        range_data.append(range_dict)

    return jsonify(range_data)


if __name__ == '__main__':
    app.run(debug=True)




