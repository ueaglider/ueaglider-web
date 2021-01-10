from typing import Optional, Any

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


def get_mission_dives(mission_id) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    dives = session.query(Dives) \
        .filter(Dives.MissionID == mission_id) \
        .all()
    gliders = session.query(Gliders) \
        .filter(Gliders.MissionID == mission_id) \
        .all()
    session.close()

    return dives, gliders


def dives_to_json(dives, gliders) -> dict:
    # Extract the glider names and numbers corresponding to the GliderID that is included in DiveInfo table
    gliders_name_dict = {}
    glider_number_dict = {}
    for glider in gliders:
        gliders_name_dict[glider.GliderID] = glider.Name
        glider_number_dict[glider.GliderID] = glider.Number
    # Make a sorted dictionary of ascending integers per gliderID for colouring the map dive icons
    glider_ids = list(glider_number_dict.keys())
    glider_ids.sort()
    glider_order_dict = {val: i for i, val in enumerate(glider_ids)}
    features = []
    for i, dive in enumerate(dives):
        tgt_popup = 'SG ' + str(glider_number_dict[dive.GliderID]) + ' ' + gliders_name_dict[dive.GliderID] + "<br>Dive " + str(
            dive.DiveNo) + "<br>Lat: " + str(dive.Latitude) + "<br>Lon: " + str(dive.Longitude)
        dive_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    dive.Longitude,
                    dive.Latitude
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup,
                "gliderOrder":glider_order_dict[dive.GliderID]
            },
            "id": i
        }
        features.append(dive_item)

    divedict = {
        "type": "FeatureCollection",
        "features": features
    }
    return divedict


def targets_to_json(targets) -> dict:
    features = []
    for i, target in enumerate(targets):
        tgt_popup = "Target: " + target.Name + "<br>Lat: " + str(target.Latitude) + "<br>Lon: " + str(
            target.Longitude) + "<br>GOTO: " + target.Goto + "<br>Radius: " + str(target.Radius) + ' m'
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    target.Longitude,
                    target.Latitude
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup
            },
            "id": i
        }
        features.append(target_item)

    tgtdict = {
        "type": "FeatureCollection",
        "features": features
    }
    return tgtdict
