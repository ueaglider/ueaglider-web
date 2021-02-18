import sqlalchemy
from sqlalchemy.orm import sessionmaker
import re
import sys
import datetime
import json
import os
import xarray as xr

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Dives, Gliders, Missions, Targets, Pins

# Store credentials in a external file that is never added to git or shared over insecure channels
#folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


def main():
    # get glider num from bash script. Gliders are linux users named sgXXX where XXX is the glider number
    glider_num = sys.argv[1][2:]
    add_dive(glider_num)
    #add_depths()


def add_dive(glider_num):
    session = Session()
    dive_num, dive_datetime, lat, lon, status_str = get_dive_data(glider_num)
    elevation = gebco_depth(lat, lon)
    dive = Dives()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    mission_num = session.query(Missions.Number).filter(Missions.MissionID == glider.MissionID).first()
    dive.MissionID = mission_num[0]
    dive.GliderID = glider.GliderID
    dive.Longitude = coord_db_decimal(lon)
    dive.Latitude = coord_db_decimal(lat)
    dive.DiveNo = dive_num
    dive.Status = status_str
    dive.ReceivedDate = dive_datetime
    dive.Elevation = elevation
    session.add(dive)
    session.commit()
    session.close()


#########   GET DIVE DATA ###################

def get_dive_data(glider_num):
    glider_dir = "/home/sg" + str(int(glider_num))
    comm_log = glider_dir + '/comm.log'
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
        dive_datetime = datetime.datetime.strptime(date + time, "%d%m%y%H%M%S")
        lat = float(gps_list[3]) / 100
        lon = float(gps_list[4]) / 100
        status = status_str.split(' ')[0]
        status_identities = ['dive num', 'call cycle', 'calls made', 'no-comm count', 'internal mission number',
                             'reboot count', 'error code', 'AD pitch', 'AD roll', 'AD VBD', 'Pitch', 'Depth',
                             '10 V voltage', '24 V voltage', 'internal pressure', 'internal RH']
        dive_num = int(status.split(':')[0])
    return dive_num, dive_datetime, lat, lon, status


def add_depths():
    session = Session()
    dives = session.query(Dives)
    for dive in dives:
        print(dive.DiveInfoID)
        dive.Elevation = gebco_depth(dive.Latitude, dive.Longitude)
    session.commit()
    session.close()


def gebco_depth(lat_in, lon_in):
    # Find the GEBCO water depth underneath where the glider surfaced
    gebco_path = secrets['gebco_path']
    gebco = xr.open_dataset(gebco_path)
    gebco_elevation = float(gebco.sel(lon=lon_in, lat=lat_in, method='nearest').elevation)
    return gebco_elevation


def coord_db_decimal(coord_in):
    # convert from kongsberg style degree-mins to decimal degrees
    deg = int(coord_in)
    minutes = coord_in - deg
    decimal_degrees = deg + minutes / 0.6
    return decimal_degrees


def convert_dives(overwrite_db=False):
    # WARNING! This will overwrite data in the db in place. Only run once and be sure what you're doing
    if not overwrite_db:
        return
    session = Session()
    dives = session.query(Dives)
    for dive in dives:
        print(dive.DiveInfoID)
        dive.Latitude = coord_db_decimal(dive.Latitude)
        dive.Longitude = coord_db_decimal(dive.Longitude)
    session.commit()
    session.close()


def convert_targets(overwrite_db=False):
    # WARNING! This will overwrite data in the db in place. Only run once and be sure what you're doing
    if not overwrite_db:
        return
    session = Session()
    targets = session.query(Targets)
    for target in targets:
        print(target.TargetsID)
        target.Latitude = coord_db_decimal(target.Latitude)
        target.Longitude = coord_db_decimal(target.Longitude)
    session.commit()
    session.close()


def convert_pins(overwrite_db=False):
    # WARNING! This will overwrite data in the db in place. Only run once and be sure what you're doing
    if not overwrite_db:
        return
    session = Session()
    pins = session.query(Pins)
    for pin in pins:
        print(pin.WaypointsID)
        pin.Latitude = coord_db_decimal(pin.Latitude)
        pin.Longitude = coord_db_decimal(pin.Longitude)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
