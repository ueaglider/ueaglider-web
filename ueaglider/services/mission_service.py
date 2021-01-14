from typing import Optional, Any

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Gliders, Missions, Dives, Targets, Waypoints

degree_sign = u'\N{DEGREE SIGN}'
# Add more non-UEA assets and missions here so they don't inflate our front page statistics
non_uea_mission_numbers = [1, 2, 16, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 53]
non_uea_gliders = [503, 539, 546, 566, 533, 565, 524, 999, 532, 534, 550, 602, 621, 643, 640]

def get_glider_count() -> int:
    session = create_session()
    gliders = session.query(Gliders).filter(Gliders.Number.notin_(non_uea_gliders)).count()
    session.close()
    return gliders


def get_mission_count() -> int:
    session = create_session()
    missions = session.query(Missions).filter(Missions.MissionID.notin_(non_uea_mission_numbers)).count()
    session.close()
    return missions


def get_dive_count(filter_glider=False) -> int:
    session = create_session()
    if filter_glider:
        dives = session.query(Dives) \
            .filter(Dives.GliderID == filter_glider) \
            .filter(Dives.MissionID.notin_(non_uea_mission_numbers)).count()
    else:
        dives = session.query(Dives).filter(Dives.MissionID.notin_(non_uea_mission_numbers)).count()
    session.close()
    return dives


def list_missions(filter_missions=False, mission_ids=[]) -> dict:
    session = create_session()
    if filter_missions:
        missions = session.query(Missions) \
            .filter(Missions.MissionID.in_(mission_ids)) \
            .filter(Missions.MissionID.notin_(non_uea_mission_numbers)) \
            .order_by(Missions.MissionID.desc()) \
            .all()
    else:
        missions = session.query(Missions).order_by(Missions.MissionID.desc()).all()
    session.close()
    return missions


def list_gliders() -> dict:
    session = create_session()
    gliders = session.query(Gliders).filter(Gliders.Number.notin_(non_uea_gliders)).order_by(Gliders.Number.asc()).all()
    session.close()
    return gliders


def glider_info(glider_num):
    session = create_session()
    glider_instance = session.query(Gliders).filter(Gliders.Number == glider_num).first()
    mission_ids = []
    for value in session.query(Dives.MissionID) \
            .filter(Dives.GliderID == glider_instance.GliderID) \
            .distinct():
        mission_ids.append(value[0])
    session.close()
    return glider_instance, mission_ids


def get_mission_by_id(mission_id):
    if not mission_id:
        return None
    session = create_session()
    mission = session.query(Missions).filter(Missions.MissionID == mission_id).first()
    session.close()
    return mission


def get_mission_targets(mission_id) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    targets = session.query(Targets) \
        .filter(Targets.MissionID == mission_id) \
        .all()

    session.close()

    return targets


def get_mission_waypoints(mission_id) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    waypoints = session.query(Waypoints) \
        .filter(Waypoints.MissionID == mission_id) \
        .all()

    session.close()

    return waypoints


def get_mission_dives(mission_id) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    dives = session.query(Dives) \
        .filter(Dives.MissionID == mission_id) \
        .all()
    # Necessary because Gliders table records only them most recent mission for each glider
    glider_ids = []
    for value in session.query(Dives.GliderID) \
            .filter(Dives.MissionID == mission_id) \
            .distinct():
        glider_ids.append(value[0])
    query = session.query(Gliders).filter(Gliders.GliderID.in_(glider_ids))
    gliders = query.all()
    # Get most recent dive from each glider
    most_recent_dives = []
    # Group dives by glider
    dives_by_glider = []
    for glider_id in glider_ids:
        dives = session.query(Dives) \
            .filter(Dives.MissionID == mission_id) \
            .filter(Dives.GliderID == glider_id) \
            .order_by(Dives.DiveNo.desc()) \
            .all()
        dives_by_glider.append(dives)
        most_recent_dives.append(dives[0])

    session.close()
    return dives, gliders, dives_by_glider, most_recent_dives


def mission_av_loc():
    session = create_session()
    targets = session.query(Targets) \
        .all()
    session.close()
    missions = []
    mission_tgts = []
    for tgt in targets:
        if tgt.MissionID not in missions:
            missions.append(tgt.MissionID)
            mission_tgts.append(tgt)
            session = create_session()
            mission = session.query(Missions.Name).filter(Missions.MissionID == tgt.MissionID).first()
            session.close()
            tgt.Name = mission[0]
    return mission_tgts
