import sqlalchemy
from sqlalchemy.orm import sessionmaker
from ueaglider.data.db_classes import Dives, Gliders, Missions
import re
import datetime
import json
import os
folder = os.path.abspath(os.path.dirname(__file__))
# Store credentials in a external file that is never added to git or shared over insecure channels
with open(folder+'/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


def add_dive(glider_num):
    session = Session()
    dive_num, dive_datetime, lat, lon, status_str = get_dive_data(glider_num)
    dive = Dives()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    mission_num = session.query(Missions.Number).filter(Missions.MissionID == glider.MissionID).first()
    dive.MissionID = mission_num[0]
    dive.GliderID = glider.GliderID
    dive.Longitude = lon
    dive.Latitude = lat
    dive.DiveNo = dive_num
    dive.Status = status_str
    dive.ReceivedDate = dive_datetime
    session.add(dive)
    session.commit()
    session.close()


#########   GET DIVE DATA ###################

def get_dive_data(glider_num):
    glider_dir = "/home/sg" + str(glider_num)
    comm_log = glider_dir + '/p' + str(glider_num) + '.log'
    with open(comm_log) as origin_file:
        # Go through comm log looking for GPS lines
        for line in origin_file:
            sel_line = re.findall(r'GPS', line)
            if sel_line:
                # Keep only most recent GPS line
                gps_line = line
        gps_list = gps_line.split(',')
        status_str = gps_list[0]
        date = gps_list[1]
        time = gps_list[2]
        dive_datetime = datetime.datetime.strptime(date+time, "%d%m%y%H%M%S")
        lat = float(gps_list[3]) / 100
        lon = float(gps_list[4]) / 100
        status = status_str.split(' ')[0]
        status_identities = ['dive num', 'call cycle', 'calls made', 'no-comm count', 'internal mission number',
                             'reboot count', 'error code', 'AD pitch', 'AD roll', 'AD VBD', 'Pitch', 'Depth',
                             '10 V voltage', '24 V voltage', 'internal pressure', 'internal RH']
        dive_num = int(status.split(':')[0])
    return dive_num, dive_datetime, lat, lon, status

