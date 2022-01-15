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


def add_dives(dive_csv):
    df = pd.read_csv(dive_csv)
    session = Session()
    for i, row in df.iterrows():
        dive = Dives()
        for key, val in row.items():
            setattr(dive, key, val)
        dive_exists = session.query(Dives) \
            .filter(Dives.GliderID == int(row['GliderID'])) \
            .filter(Dives.DiveNo == row['DiveNo']) \
            .filter(Dives.MissionID == row['MissionID']) \
            .first()
        # stop if dive already exists
        if dive_exists:
            return
        session.add(dive)
    session.commit()
    session.close()


def add_targets(target_csv):
    df = pd.read_csv(target_csv)
    session = Session()
    for i, row in df.iterrows():
        tgt = Targets()
        for key, val in row.items():
            setattr(tgt, key, val)
        tgt_exists = session.query(Targets) \
            .filter(Targets.Name == int(row['Name'])) \
            .filter(Targets.MissionID == row['MissionID']) \
            .first()
        # stop if dive already exists
        if tgt_exists:
            return
        session.add(tgt)
    session.commit()
    session.close()


if __name__ == '__main__':
    input_dir = folder + '/output'
    add_dives(f'{input_dir}/dives.csv')
    add_targets(f'{input_dir}/targets.csv')
    add_argos(f'{input_dir}/argos.csv')
