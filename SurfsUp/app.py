# Import the dependencies.
import datetime as dt
from flask import Flask,jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.session import Session
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
#################################################
# Database Setup
#################################################
data_path = Path("hawaii.db")
engine = create_engine(f"sqlite:///{data_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station
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
    return jsonify(data)
    



if __name__ == "__main__":
    app.run(debug=True)


df = pd.DataFrame(data,columns=['',''])

df.sort_values(df['date'],inplace=True)

plt.plot(df['date'],df['prcp'])

df['prcp'].describe()



    