# Import the dependencies.
import datetime as dt
from flask import Flask,jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.session import Session
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
#################################################
# Database Setup
#################################################
#data_path= Path('Resources/hawaii.db')
data_path= Path('../SurfsUp/Resources/hawaii.db')
engine = create_engine(f"sqlite:///{data_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route('/')
def availableroutes():
    return ( """/api/v1.0/precipitation<br/>
            /api/v1.0/station<br/>
            /api/v1.0/tobs<br/>
            /api/v1.0/<start><>br/
            /api/v1.0/<start>/<end><br/>
            """)



@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(bind=engine)
    year_ago_dt = dt.date(2016,8,23)
    data = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date>=year_ago_dt).all()
    session.close()
    json_dic = {}
    for date, prcp in data:
        json_dic[date] = prcp
    return jsonify(json_dic)
    



if __name__ == "__main__":
    app.run(debug=True)

@app.route('/api/v1.0/station')
def stations():
    session=Session(bind=engine)
    station_data = session.query(Station.station,Station.name).all()
    session.close()
    json_dic_1={}
    for station,name in station_data:
        json_dic_1[name]=station
    return jsonify(json_dic_1)

if __name__ == "__main__":
    app.run(debug=True)
    

@app.route('/api/v1.0/tobs')
def tobs():
    session=Session(bind=engine)
    first_day = dt.date(2016,1,1)
    last_day = dt.date(2016,12,31)
    most_active_previous_year = session.query(Measurements.prcp,Measurements.date).filter(Measurements.station=="USC00519281").filter(Measurements.date>=first_day).filter(Measurements.date<=last_day).all()
    most_active_previous_year
    session.close()
    json_dict_2={}
    for prcp,date in most_active_previous_year:
        json_dict_2[date]=prcp
    return jsonify(json_dict_2)
if __name__ == "__main__":
    app.run(debug=True)

   


