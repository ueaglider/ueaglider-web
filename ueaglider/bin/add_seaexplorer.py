import sys
import os
import xarray as xr
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import imaplib
import re
import email
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
from ueaglider.data.db_classes import Dives, Gliders, Missions

# Store credentials in a external file that is never added to git or shared over insecure channels
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)

conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string'] \
           + '/' + secrets['db_name']

engine = sqlalchemy.create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)


class GliderHTMLParser(HTMLParser):
    def handle_data(self, data):
        if 'Latitude' in data:
            result = re.findall(r'[-+]?\d*\.\d+|\d+', data)
            try:
                self.latitude = result[0]
            except:
                pass
        if 'Longitude' in data:
            result = re.findall(r'[-+]?\d*\.\d+|\d+', data)
            try:
                self.longitude = result[0]
            except:
                pass
        if 'Glider' in data:
            result = re.findall(r'[-+]?\d*\.\d+|\d+', data)
            try:
                self.glider = result[0]
            except:
                pass
        if 'Cycle' in data:
            result = re.findall(r'[-+]?\d*\.\d+|\d+', data)
            try:
                self.dive = result[0]
            except:
                pass


def read_email_from_gmail():
    # check what time email was last checked
    timefile = Path("lastcheck.log")
    if timefile.exists():
        with open("lastcheck.log", "r") as variable_file:
            for line in variable_file.readlines():
                last_check = datetime.fromisoformat((line.strip()))
    else:
        last_check = datetime(1970, 1, 1)
    last_check = datetime(1970, 1, 1)
    # Write the time of this run
    with open('lastcheck.log', 'w') as f:
        f.write(str(datetime.now()))
    # Check gmail account for emails
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(secrets['uea_email'], secrets['email_pwd'])
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    # Cut to last 10 emails
    if len(id_list) > 10:
        first_email_id = int(id_list[-10])

    # Check which emails have arrived since the last run of this script
    unread_emails = []
    for i in range(first_email_id, latest_email_id + 1):
        result, data = mail.fetch(str(i), '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                date_tuple = email.utils.parsedate_tz(msg['Date'])
                if date_tuple:
                    local_date = datetime.fromtimestamp(
                        email.utils.mktime_tz(date_tuple))
                    if local_date > last_check:
                        unread_emails.append(i)
    # Exit if no new emails
    if not unread_emails:
        with open('seaexplorer.log', 'a') as f:
            f.write(str(datetime.now()) + ' no new mail' + '\n')
        exit(0)

    # Check new emails
    for i in unread_emails:
        result, data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                # If email is from UEA domain and subject is GPS, pass to glider_loc script
                if 'administrateur@alseamar' in email_from and 'SEA' in email_subject:
                    email_parser = parse_glider_email(data, email_from)
                    if not email_parser:
                        continue
                    print(email_parser.glider)
                    add_dive(email_parser)


def parse_glider_email(message, email_from):
    body = None
    # Get the body of the message, surprisingly complicated
    raw_email = message[0][1]
    mail_content = raw_email.decode('utf-8')
    b = email.message_from_string(mail_content)
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = b.get_payload(decode=True)
    if not body:
        return None
    body_text = body.decode("utf-8")
    # parse email
    glider_email_parser = GliderHTMLParser()
    glider_email_parser.feed(body_text)
    return glider_email_parser


def add_dive(glider_email):
    glider_num = int(glider_email.glider)
    dive_num = int(glider_email.dive)
    dive_datetime = datetime.now()
    lat = float(glider_email.latitude)
    lon = float(glider_email.longitude)
    status_str = ""
    session = Session()
    elevation = gebco_depth(lat, lon)

    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    if not glider:
        return
    mission_num = session.query(Missions).filter(Missions.Number == glider.MissionID).first().Number
    dive_exists = session.query(Dives) \
        .filter(Dives.GliderID == int(glider_num)) \
        .filter(Dives.DiveNo == dive_num) \
        .filter(Dives.MissionID == mission_num) \
        .first()
    # stop if dive already exists
    if dive_exists:
        return
    dive = Dives()
    dive.MissionID = mission_num
    dive.GliderID = glider_num
    dive.Longitude = lon
    dive.Latitude = lat
    dive.DiveNo = dive_num
    dive.Status = status_str
    dive.ReceivedDate = dive_datetime
    dive.Elevation = elevation
    session.add(dive)
    session.commit()
    session.close()


def gebco_depth(lat_in, lon_in):
    # Find the GEBCO water depth underneath where the glider surfaced
    gebco_path = secrets['gebco_path']
    gebco = xr.open_dataset(gebco_path)
    gebco_elevation = int(gebco.sel(lon=lon_in, lat=lat_in, method='nearest').elevation)
    return gebco_elevation


if __name__ == '__main__':
    read_email_from_gmail()
