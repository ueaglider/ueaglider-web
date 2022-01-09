import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import datetime
import json
import os
import pandas as pd

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Dives, Targets, ArgosLocations, Pins
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


def get_dives():
    session = Session()
    start = datetime.datetime.now() - datetime.timedelta(hours=3006)
    rows = session.query(Dives)\
        .filter(Dives.ReceivedDate > start)\
        .all()
    session.close()
    if not rows:
        return
    df = rows_to_df(rows)
    df.to_csv(folder + '/output/glider_locs.csv', index=False)


def rows_to_df(rows):
    inst_dict = rows[0].__dict__
    inst_dict.pop('_sa_instance_state')
    keys = inst_dict.keys()
    data_dict = {}
    for key in keys:
        data = []
        for row in rows:
            data.append(getattr(row, key))
        data_dict[key] = data
    df = pd.DataFrame(data_dict)
    return df


def get_tgts():
    session = Session()
    rows = session.query(Targets)\
        .filter(Targets.MissionID == 64)\
        .all()
    session.close()
    if not rows:
        return
    df = rows_to_df(rows)
    df.to_csv(f'{folder}/output/targets.csv', index=False)


if __name__ == '__main__':
    get_tgts()
    get_dives()
