from ueaglider.data.db_session import create_session
from ueaglider.data.db_classes import Dives


def add_dive(mission_num):
    dive = Dives
    dive.MissionID = mission_num
    dive.GliderID


def edit_waypoint_info(waypoint_id, info_txt):
    if not waypoint_id:
        return None
    session = create_session()
    waypoint = session.query(Pins).filter(Pins.WaypointsID == waypoint_id).first()
    waypoint.Info = info_txt
    session.commit()
    session.close()
    retur