from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Waypoints


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
    return
