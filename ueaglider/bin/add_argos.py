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
    tag_number = "60281"
    mission_num = 1
    add_tag_location(tag_number, mission_num)
    pass


def add_tag_location(tag_number, mission_num):
    print('start')
    wsdl = "http://ws-argos.cls.fr/argosDws/services/DixService?wsdl"

    client = zeep.Client(wsdl=wsdl)
    resp_xml = client.service.getXml(username=secrets["argo_user"], password=secrets["argo_pwd"], nbPassByPtt=100, nbDaysFromNow=20,
                                     displayLocation="true", displayRawData="true",
                                     mostRecentPassages="true", platformId=tag_number)

    resp_dict = xmltodict.parse(resp_xml)
    bar = resp_dict['data']
    print(bar)
    if 'program' not in bar.keys():
        return
    baz = bar['program']
    b = baz['platform']
    b0 = b['satellitePass']
    b1 = b0[0]
    argo_dict = b1['location']
    print('parsing')
    location = ArgosLocations()
    location.Number = int(tag_number)
    location.Longitude = float(argo_dict['longitude'])
    location.Latitude = float(argo_dict['latitude'])
    location.Date = datetime.datetime.strptime(argo_dict['locationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
    location.Quality = argo_dict['locationClass']
    location.Altitude = float(argo_dict['altitude'])
    location.MissionID = mission_num
    print('adding')
    session = Session()
    session.add(location)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
