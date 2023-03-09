# imports 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Set up data base 
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

#Save references
Measurement = Base.classes.measurement
Station = Base.classes.station 

#Set up Flask
app = Flask(__name__)

#Set up Flask Routes
@app.route("/")
def welcome(): 
    """List all available api routes."""
    return(
         f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #Create filter to select data after 8/24/2016 (one year from the latest result)
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()
    
    session.close()

    #Create a dictionary with the date and prcp 
    all_prcp = []
    for date, prcp in prcp_results:
                prcp_dict = {}
                prcp_dict["date"] = date
                prcp_dict["precipitation"] = prcp

                all_prcp.append(prcp_dict)
     
    return jsonify(all_prcp)          

@app.route("/api/v1.0/stations")
def stations():
       session = Session(engine)
       station_results = session.query(Station.station, Station.id).all()
       
       session.close()

       #Create a station dictionary with the date and prcp
       station_values = []
       for station, id in station_results: 
                station_dict = {}
                station_dict["station"] = station
                station_dict["id"] = id
                
                station_values.append(station_dict)

       return jsonify(station_values)

@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)
        tobs_results = session.query(Measurement.prcp, Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= '2016-08-23').\
                    filter(Measurement.station == 'USC00519281').\
                    order_by(Measurement.date).all()

        session.close()

        #Create a tobs dictionary with the date and prcp 
        all_tobs = []
        for prcp, date, tobs in tobs_results: 
               tobs_dict = {}
               tobs_dict["prcp"]= prcp
               tobs_dict["date"]= date 
               tobs_dict["tobs"]= tobs

               all_tobs.append(tobs_dict)
        return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine) 

    start_date_tobs_results = session.query(func.min(Measurement.tobs),\
                                            func.avg(Measurement.tobs),
                                            func.max(Measurement.tobs)).\
                                filter(Measurement.date >= start).all()
    
    session.close() 
    #Create a start date tobs dictionary with the min, average, and max 
    start_date_tobs_values =[]
    for min, avg, max in start_date_tobs_results:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["average"] = avg
        start_date_dict["max"] = max
        start_date_tobs_values.append(start_date_dict)
    
    return jsonify(start_date_tobs_values)

@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    session = Session(engine)

    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
  
    start_end_values = []
    for min, avg, max in start_end_results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["avg"] = avg
        start_end_dict["max"] = max
        start_end_values.append(start_end_dict) 
    

    return jsonify(start_end_values)

if __name__ == '__main__':
    app.run(debug=True) 