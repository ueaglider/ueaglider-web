from datetime import datetime

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Waypoints, Audit
from ueaglider.services.user_service import find_user_by_id


def edit_waypoint_info(waypoint_id, info_txt):
    if not waypoint_id:
        return None
    session = create_session()
    waypoint = session.query(Waypoints).filter(Waypoints.WaypointsID == waypoint_id).first()
    waypoint.Info = info_txt
    session.commit()
    session.close()
    return


def create_waypoint(missionid, name, lat, lon, info):
    session = create_session()
    waypoint = Waypoints()
    waypoint.MissionID = missionid
    waypoint.Name = name
    waypoint.Latitude = lat
    waypoint.Longitude = lon
    waypoint.Info = info
    session.add(waypoint)
    session.commit()
    session.close()
    return waypoint


def audit_entry(user_id: int, message: str):
    user = find_user_by_id(user_id)
    if not user:
        return None
    audit = Audit()
    audit.UserID = user_id
    audit.Date = datetime.now()
    audit.Info = message

    session = create_session()
    session.add(audit)
    session.commit()
    session.close()
    return audit
