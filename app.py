# Import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import numpy as np
from flask import Flask,  jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()


# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    """List of all routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startenddate<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    prcp_avg = [measurement.date,
           func.avg(measurement.prcp)]

    precipitation = session.query(*prcp_avg).\
    filter(measurement.date >= '2016-08-23').\
    group_by(measurement.date).\
    order_by(measurement.date).all()

    session.close()

    # Convert
    query1 = list(np.ravel(precipitation))

    return jsonify(query1)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    stations = session.query(station.station, station.name).all()

    session.close()

    # Convert
    query2 = list(np.ravel(stations))

    return jsonify(query2)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    temp_obs = session.query(measurement.tobs).\
    filter(measurement.date >= '2016-08-23', measurement.station == 'USC00519281').all()

    session.close()

    # Convert
    query3 = list(np.ravel(temp_obs))

    return jsonify(query3)

@app.route("/api/v1.0/startdate")
def startdate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

      # Query
    startdate = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date == '2017-07-01').all()

    session.close()

    # Convert
    query4 = list(np.ravel(startdate))

    return jsonify(query4)

@app.route("/api/v1.0/startenddate")
def startenddate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

      # Query
    startenddate = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= '2017-07-01').\
        filter(measurement.date <= '2017-07-15').\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    # Convert
    query5 = list(np.ravel(startenddate))

    return jsonify(query5)


if __name__ == '__main__':
    app.run(debug=True)