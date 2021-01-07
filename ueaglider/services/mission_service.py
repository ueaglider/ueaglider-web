from typing import List

import sqlalchemy

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Gliders, Missions, Dives, Targets


def get_glider_count() -> int:
    session = create_session()
    return session.query(Gliders).count()
def get_mission_count() -> int:
    session = create_session()
    return session.query(Missions).count()

def get_dive_count() -> int:
    session = create_session()
    return session.query(Dives).count()

def list_missions() -> dict:
    session = create_session()
    missions = session.query(Missions).order_by(Missions.MissionID.desc()).all()
    session.close()
    return missions


def get_mission_by_id(mission_id):
    if not mission_id:
        return None
    session = create_session()
    mission = session.query(Missions).filter(Missions.MissionID == mission_id).first()
    session.close()
    return mission

def get_mission_targets(mission_id) -> List[Targets]:
        if not mission_id:
            return None

        mission_id = int(mission_id)

        session = create_session()

        targets = session.query(Targets) \
            .filter(Targets.MissionID == mission_id) \
            .all()

        session.close()

        return targets
