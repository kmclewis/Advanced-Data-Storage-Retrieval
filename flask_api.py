import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# engine = create_engine('sqlite:////var/www/homepage/blog.db?check_same_thread=False')
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/single_date/<br/>"
        f"<br/>"
        f"Enter a date in the format YYYY-MM-DD.<br/>"  
        f"For example:  /api/v1.0/start_date/2012-01-01<br/>"
        f"<br/>"
        f"/api/v1.0/date_range/<br/>"
        f"<br/>"
        f"Enter a starting date followed by / and an ending date.<br/>"
        f"For example:  /api/v1.0/date_range/2012-01-01/2014-12-31"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = []
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").all()
    for row in results:
        precipitation.append({row[0]:row[1]})
    return jsonify(precipitation) 

@app.route("/api/v1.0/stations")
def stations():
    stations = []
    results = session.query(Measurement.station,).group_by(Measurement.station)\
        .order_by(Measurement.station).all()
    for row in results:
        stations.append(row)    
    return jsonify(stations) 

@app.route("/api/v1.0/tobs")
def temp_observations():
    temp = []
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").all()
    for row in results:
        temp.append({row[0]:row[1]})
    return jsonify(temp) 

@app.route("/api/v1.0/single_date/<start_date>")
def start_date(start_date):
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    if start_date <= "2017-08-23" and start_date >= "2010-01-01": 
        return jsonify(results) 

    return jsonify({"error": f"The date {start_date} isn't in the dataset.  The dataset begins at 2010-01-01 and ends at 2017-08-23.  Please enter a valid date."}), 404


@app.route("/api/v1.0/date_range/<range_start>/<range_end>")
def range(range_start, range_end):
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= range_start).filter(Measurement.date <= range_end).all()
    if range_start >= "2010-01-01" and range_start <= "2017-08-23" and range_end <= "2017-08-23" and range_end >= "2010-01-01" and range_start <= range_end and range_end >= range_start: 
        return jsonify(results) 

    return jsonify({"error": f"A value entered isn't in the dataset or start date is greater than end date.  The dataset begins at 2010-01-01 and ends at 2017-08-23.  Please enter valid dates."}), 404

if __name__ == "__main__":
    app.run(debug=True)    