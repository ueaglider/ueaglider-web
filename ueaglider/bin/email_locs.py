import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import datetime
import json
import os
import numpy as np
import pandas as pd

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Dives
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


def main():
    session = Session()
    start = datetime.datetime.now() - datetime.timedelta(hours=36)
    dives = session.query(Dives)\
        .filter(Dives.ReceivedDate > start)\
        .all()
    glider, divenum, times, lon, lat = [], [], [], [], []
    session.close()
    for dive in dives:
        glider.append(dive.GliderID)
        divenum.append(dive.DiveNo)
        times.append(dive.ReceivedDate)
        lat.append(dive.Latitude)
        lon.append(dive.Longitude)
    df = pd.DataFrame({"glider": glider, "dive": divenum, "datetime":times, "lon": lon, "lat": lat})
    df["lon"] = np.round(df.lon.values, 4)
    df["lat"] = np.round(df.lat.values, 4)
    df.to_csv('/apps/glider_locs.csv', index=False)

if __name__ == '__main__':
    main()
