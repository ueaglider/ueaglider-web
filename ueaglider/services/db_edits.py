from datetime import datetime

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Pins, Audit, Missions, Targets
from ueaglider.services.user_service import find_user_by_id


def edit_waypoint_info(waypoint_id, info_txt):
    if not waypoint_id:
        return None
    session = create_session()
    waypoint = session.query(Pins).filter(Pins.WaypointsID == waypoint_id).first()
    waypoint.Info = info_txt
    session.commit()
    session.close()
    return


def create_waypoint(missionid, name, lat, lon, info):
    session = create_session()
    waypoint = Pins()
    waypoint.MissionID = missionid
    waypoint.Name = name
    waypoint.Latitude = lat
    waypoint.Longitude = lon
    waypoint.Info = info
    session.add(waypoint)
    session.commit()
    session.close()
    return waypoint


def create_target(missionid, name, lat, lon, radius, goto):
    session = create_session()
    target = Targets()
    target.MissionID = missionid
    target.Name = name
    target.Latitude = lat
    target.Longitude = lon
    target.Radius = radius
    target.Goto = goto
    session.add(target)
    session.commit()
    session.close()
    return target


def create_mission(number, name, start, end, info):

    mission = Missions()
    mission.Number = number
    mission.Name = name
    mission.StartDate = start
    mission.EndDate = end
    mission.Info = info
    session = create_session()
    session.add(mission)
    session.commit()
    session.close()
    return mission


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
