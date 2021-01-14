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
