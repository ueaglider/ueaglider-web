from typing import Optional, Any
import datetime
from ueaglider.data.db_session import create_session
from ueaglider.data.db_classes import Gliders, Missions, Dives, Targets, Pins, ArgosLocations, ArgosTags

degree_sign = u'\N{DEGREE SIGN}'
# Add more non-UEA assets and missions here so they don't inflate our front page statistics
non_uea_mission_numbers = [1, 2, 16, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 53]


def get_mission_count() -> int:
    session = create_session()
    missions = session.query(Missions).filter(Missions.Number.notin_(non_uea_mission_numbers)).count()
    session.close()
    return missions


def mission_ids() -> list:
    session = create_session()
    missions = session.query(Missions.Number) \
        .order_by(Missions.Number.desc()) \
        .all()
    session.close()
    return missions


def get_dive(glider_num, dive_num, mission_num):
    session = create_session()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    if not glider:
        return None
    glider_id = glider.Number
    dive = session.query(Dives)\
        .filter(Dives.GliderID == glider_id)\
        .filter(Dives.DiveNo == dive_num)\
        .filter(Dives.MissionID == mission_num)\
        .first()
    session.close()
    if not dive:
        return None
    return dive


def adjacent_dives(glider_num, dive_num, mission_num):
    session = create_session()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    if not glider:
        return None
    glider_id = glider.Number
    prev_dive = session.query(Dives.DiveNo) \
        .filter(Dives.GliderID == glider_id) \
        .filter(Dives.MissionID == mission_num) \
        .filter(Dives.DiveNo < dive_num) \
        .order_by(Dives.DiveNo.desc()) \
        .first()
    session.close()
    if not prev_dive:
        prev_dive = None
    next_dive = session.query(Dives.DiveNo) \
        .filter(Dives.GliderID == glider_id) \
        .filter(Dives.MissionID == mission_num) \
        .filter(Dives.DiveNo > dive_num) \
        .order_by(Dives.DiveNo.asc()) \
        .first()
    session.close()
    if not next_dive:
        next_dive = None
    return prev_dive, next_dive


def get_dive_nums(glider_num, mission_num):
    session = create_session()
    glider = session.query(Gliders).filter(Gliders.Number == int(glider_num)).first()
    if not glider:
        return None
    glider_id = glider.Number
    dives = session.query(Dives.DiveNo) \
        .filter(Dives.GliderID == glider_id) \
        .filter(Dives.MissionID == mission_num) \
        .all()
    session.close()
    if not dives:
        return None
    return dives


def get_dive_count(filter_glider=False) -> int:
    session = create_session()
    if filter_glider:
        dives = session.query(Dives) \
            .filter(Dives.GliderID == filter_glider) \
            .filter(Dives.MissionID.notin_(non_uea_mission_numbers)).count()
    else:
        non_uea_gliders_list = session.query(Gliders.Number)\
            .filter(Gliders.UEAGlider == 0) \
            .all()
        non_uea_gliders = [y for x in non_uea_gliders_list for y in x]
        dives = session.query(Dives)\
            .filter(Dives.GliderID.notin_(non_uea_gliders)) \
            .filter(Dives.MissionID.notin_(non_uea_mission_numbers)).count()
    session.close()
    return dives


def list_missions(filter_missions=False, mission_id_list=()) -> dict:
    session = create_session()
    if filter_missions:
        missions = session.query(Missions) \
            .filter(Missions.Number.in_(mission_id_list)) \
            .filter(Missions.Number.notin_(non_uea_mission_numbers)) \
            .order_by(Missions.Number.desc()) \
            .all()
    else:
        missions = session.query(Missions) \
            .filter(Missions.Number.notin_(mission_id_list)) \
            .order_by(Missions.Number.desc()).all()
    session.close()
    return missions


def get_mission_by_id(mission_id):
    if not mission_id:
        return None
    session = create_session()
    mission = session.query(Missions).filter(Missions.Number == mission_id).first()
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


def get_mission_pins(mission_id) -> Optional[Any]:
    if not mission_id:
        return None
    mission_id = int(mission_id)
    session = create_session()
    pins = session.query(Pins) \
        .filter(Pins.MissionID == mission_id) \
        .all()
    session.close()
    return pins


def get_pins() -> Optional[Any]:
    session = create_session()
    pins = session.query(Pins).order_by(Pins.WaypointsID.desc()).all()
    pin_ids = session.query(Pins.WaypointsID).all()
    session.close()
    return pins, pin_ids


def get_targets() -> Optional[Any]:
    session = create_session()
    targets = session.query(Targets).order_by(Targets.TargetsID.desc()).all()
    target_ids = session.query(Targets.TargetsID).all()
    session.close()
    return targets, target_ids


def get_missions() -> Optional[Any]:
    session = create_session()
    missions = session.query(Missions).order_by(Missions.Number.desc()).all()
    missions_ids = session.query(Missions.Number).all()
    session.close()
    return missions, missions_ids


def get_dives() -> Optional[Any]:
    session = create_session()
    dives = session.query(Dives).order_by(Dives.DiveInfoID.desc()).all()[:100]
    dive_ids = session.query(Dives.DiveInfoID).all()
    session.close()
    return dives, dive_ids

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
    query = session.query(Gliders).filter(Gliders.Number.in_(glider_ids))
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
        # Correct for GPS rollover if present
        for dive in dives:
            if not dive.ReceivedDate:
                continue
            if dive.ReceivedDate < datetime.datetime(2010, 1, 1):
                dive.ReceivedDate = dive.ReceivedDate + datetime.timedelta(weeks=1024)
        dives_by_glider.append(dives)
        most_recent_dives.append(dives[0])

    session.close()
    return dives, gliders, dives_by_glider, most_recent_dives


def get_mission_tag_locs(mission_id, qualities=('G', '3', '2', '1', '0', 'A', 'B', 'Z')) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    tag_locations = session.query(ArgosLocations) \
        .filter(ArgosLocations.MissionID == mission_id) \
        .all()
    # Necessary because ArgosTags table records only them most recent mission for each tag
    tag_numbers = []
    for value in session.query(ArgosLocations.TagNumber) \
            .filter(ArgosLocations.MissionID == mission_id) \
            .distinct():
        tag_numbers.append(value[0])
    query = session.query(ArgosTags).filter(ArgosTags.TagNumber.in_(tag_numbers))
    tags = query.all()
    # Get most recent locations from each tag
    most_recent_locs = []
    # Group locs by tag
    locs_by_tag = []
    for tag_num in tag_numbers:
        tag_locations = session.query(ArgosLocations) \
            .filter(ArgosLocations.MissionID == mission_id) \
            .filter(ArgosLocations.TagNumber == tag_num) \
            .order_by(ArgosLocations.Date.desc()) \
            .all()
        good_tag_locs = []
        for loc in tag_locations:
            if loc.Quality in qualities:
                good_tag_locs.append(loc)
        if good_tag_locs:
            locs_by_tag.append(good_tag_locs)
            most_recent_locs.append(good_tag_locs[0])

    session.close()
    return tag_locations, tags, locs_by_tag, most_recent_locs


def mission_loc(filter_missions=False, mission_no=None):
    session = create_session()
    if filter_missions:
        missions = session.query(Missions).filter(Missions.Number.notin_(non_uea_mission_numbers)).all()
    elif mission_no:
        missions = session.query(Missions).filter(Missions.Number == mission_no)
    else:
        missions = session.query(Missions).all()
    mission_locs = []
    for mission in missions:
        dive = session.query(Dives).filter(Dives.MissionID == mission.Number).order_by(Dives.DiveNo.asc()).first()
        if dive:
            tgt_template = Targets()
            tgt_template.Longitude = dive.Longitude
            tgt_template.Latitude = dive.Latitude
            tgt_template.Name = mission.Name
            tgt_template.MissionID = mission.Number
            mission_locs.append(tgt_template)
            continue
        target = session.query(Targets).filter(Targets.MissionID == mission.Number).first()
        if target:
            target.Name = mission.Number
            mission_locs.append(target)
    session.close()
    return mission_locs
