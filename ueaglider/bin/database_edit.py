import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from ueaglider.data.db_classes import Dives, Gliders

import json
import os
folder = os.path.abspath(os.path.dirname(__file__))
# Store credentials in a external file that is never added to git or shared over insecure channels
with open(folder+'/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

#from ueaglider.data.db_session import create_session

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sa.create_engine(conn_str, echo=False)

__factory = orm.sessionmaker(bind=engine)
session: Session = __factory()
session.expire_on_commit = False

def add_dive(mission_num, glider_num, dive_no, lon, lat):
    dive = Dives()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    dive.MissionID = mission_num
    dive.GliderID = glider.GliderID
    dive.Longitude = lon
    dive.Latitude = lat
    dive.DiveNo = dive_no
    session.add(dive)
    session.commit()
    session.close()


add_dive(60,637,1,30,30)
