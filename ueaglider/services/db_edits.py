from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Waypoints


def get_mission_by_id(mission_id):
    if not mission_id:
        return None
    session = create_session()
    mission = session.query(Waypoints).filter(Waypoints.MissionID == mission_id).first()
    session.close()
    return mission