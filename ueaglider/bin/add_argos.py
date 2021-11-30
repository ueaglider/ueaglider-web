import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import datetime
import json
import os
import zeep
import xmltodict

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Missions, ArgosTags, ArgosLocations
from ueaglider.services import argos_service

LocationClasses = {
    'G': 'within 100 m',
    '3': 'within 250 m',
    '2': 'within 500 m',
    '1': 'within 1500 m',
    '0': 'greater than 1500 m',
    'A': 'No accuracy estimation',
    'B': 'No accuracy estimation',
    'Z': 'Invalid location'
}
# Store credentials in a external file that is never added to git or shared over insecure channels
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

# Can switch echo to True for debug, SQL actions print out to terminal
engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


def main():
    session = Session()
    tags = session.query(ArgosTags).all()
    session.close()
    tag_numbers = []
    tag_missions = []
    for tag in tags:
        tag_numbers.append(tag.TagNumber)
        tag_missions.append(tag.MissionID)
    for tag_num, mission_num in zip(tag_numbers, tag_missions):
        add_tag_location(tag_num, mission_num)
    pass


def add_tag_location(tag_number, mission_num):
    wsdl = "http://ws-argos.cls.fr/argosDws/services/DixService?wsdl"

    client = zeep.Client(wsdl=wsdl)
    resp_xml = client.service.getXml(username=secrets["argo_user"], password=secrets["argo_pwd"], nbPassByPtt=100,
                                     nbDaysFromNow=20,
                                     displayLocation="true", displayRawData="true",
                                     mostRecentPassages="true", platformId=str(tag_number))

    resp_dict = xmltodict.parse(resp_xml)
    bar = resp_dict['data']
    if 'program' not in bar.keys():
        return
    baz = bar['program']
    b = baz['platform']
    b0 = b['satellitePass']
    session = Session()
    existing_loc_dates_lists = session.query(ArgosLocations.Date) \
        .filter(ArgosLocations.TagNumber == tag_number) \
        .all()
    existing_loc_dates = [y for x in existing_loc_dates_lists for y in x]
    for b1 in b0:
        if 'location' not in b1.keys():
            continue
        argo_dict = b1['location']
        location = ArgosLocations()
        location.Date = datetime.datetime.strptime(argo_dict['locationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if location.Date in existing_loc_dates:
            # If this location has already been logged, skip it
            continue
        location.TagNumber = int(tag_number)
        location.Longitude = float(argo_dict['longitude'])
        location.Latitude = float(argo_dict['latitude'])
        location.Quality = argo_dict['locationClass']
        location.Altitude = float(argo_dict['altitude'])
        location.MissionID = mission_num
        session.add(location)
        session.commit()
    session.close()


if __name__ == '__main__':
    main()
