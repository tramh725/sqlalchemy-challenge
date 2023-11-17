# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np

#################################################
# Database Setup
#################################################
setup = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
database = automap_base()
# reflect the tables
database.prepare(autoload_with=setup)

# Save references to each table
measurement = database.classes.measurement
station = database.classes.station

# Create our session (link) from Python to the DB
session = Session(setup)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return(
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= last_year).all()
    session.close()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    new_station = session.query(station.station).all()
    session.close()
    
    stations=list(np.ravel(new_station))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    new_temp = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= last_year).all()
    session.close()
    
    temperature=list(np.ravel(new_temp))
    return jsonify(temps=temperature)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        result= session.query(*select).\
            filter(measurement.date >= start).all()
        session.close()
        
        temp=list(np.ravel(result))
        return jsonify(temp)
    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    result = session.query(*select).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    session.close()
    
    temp = list(np.ravel(result))
    return jsonify(temps=temp)


if __name__ == '__main__':
    app.run()

    
    
    