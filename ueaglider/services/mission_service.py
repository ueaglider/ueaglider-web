from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Gliders, Missions, Dives



def get_glider_count() -> int:
    session = create_session()
    return session.query(Gliders).count()
def get_mission_count() -> int:
    session = create_session()
    return session.query(Missions).count()

def get_dive_count() -> int:
    session = create_session()
    return session.query(Dives).count()
