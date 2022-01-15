import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import json
import os
import pandas as pd

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Dives, Targets, ArgosLocations, Pins, SealDive
from sqlalchemy import MetaData
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
            if str(val) == 'nan':
                val = None
            setattr(dive, key, val)
        dive_exists = session.query(Dives) \
            .filter(Dives.GliderID == int(row['GliderID'])) \
            .filter(Dives.DiveNo == row['DiveNo']) \
            .filter(Dives.MissionID == row['MissionID']) \
            .first()
        # stop if dive already exists
        if dive_exists:
            continue
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
            .filter(Targets.Name == row['Name']) \
            .filter(Targets.MissionID == row['MissionID']) \
            .first()
        # stop if dive already exists
        if tgt_exists:
            continue
        session.add(tgt)
    session.commit()
    session.close()


def add_argos(argos_csv):
    df = pd.read_csv(argos_csv)
    session = Session()
    for i, row in df.iterrows():
        tgt = ArgosLocations()
        for key, val in row.items():
            setattr(tgt, key, val)
        tgt_exists = session.query(ArgosLocations) \
            .filter(ArgosLocations.Date == row['Date']) \
            .filter(ArgosLocations.TagNumber == row['TagNumber']) \
            .first()
        # stop if dive already exists
        if tgt_exists:
            continue
        session.add(tgt)
    session.commit()
    session.close()


def add_seals(seals_csv):
    df = pd.read_csv(seals_csv)
    df = df[:1000]
    session = Session()
    meta = MetaData()
    meta.create_all(engine)
    for i, row in df.iterrows():
        seal = SealDive()
        for key, val in row.items():
            setattr(seal, key, val)
        seal.Latitude = round(seal.Latitude, 3)
        seal.Longitude = round(seal.Longitude, 3)
        seal.TagNumber = 1
        tgt_exists = session.query(SealDive) \
            .filter(SealDive.TagNumber == seal.TagNumber) \
            .filter(SealDive.Latitude == seal.Latitude) \
            .filter(SealDive.Longitude == seal.Longitude) \
            .first()
        # stop if dive already exists
        if tgt_exists:
            continue
        session.add(seal)
    session.commit()
    session.close()


def add_new_table():
    from sqlalchemy import MetaData, Table, Column, Integer, Numeric
    meta = MetaData()
    SealDives = Table(
        'SealDive', meta,
        Column('LocationID', Integer, primary_key=True, autoincrement=True),
        Column('TagNumber', Integer, nullable=True),
        Column('Depth', Integer),
        Column('Latitude', Numeric(10, 3)),
        Column('Longitude', Numeric(10, 3)),
    )
    meta.create_all(engine)




if __name__ == '__main__':
    folder = '/home/callum/Documents/tarsan/on-board/data-to-ship/uea/2022-01-15'
    add_dives(f'{folder}/dives.csv')
    add_targets(f'{folder}/targets.csv')
    add_argos(f'{folder}/argos.csv')
