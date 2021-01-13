from typing import Optional, Any, Tuple

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Gliders, Missions, Dives, Targets, Waypoints


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


def get_dive_count() -> int:
    session = create_session()
    dives = session.query(Dives).filter(Dives.MissionID.notin_(non_uea_mission_numbers)).count()
    session.close()
    return dives


def list_missions() -> dict:
    session = create_session()
    missions = session.query(Missions).order_by(Missions.MissionID.desc()).all()
    session.close()
    return missions

def list_gliders() -> dict:
    session = create_session()
    gliders = session.query(Gliders).order_by(Gliders.Number.asc()).all()
    session.close()
    return gliders



def glider_info(glider_num):
    session = create_session()
    glider_info = session.query(Gliders).filter(Gliders.Number == glider_num).first()
    session.close()
    return glider_info


def coord_db_decimal(coord_in):
    # convert from kongsberg style degree-mins in table to decimal degrees
    deg = int(coord_in)
    minutes = coord_in - deg
    decimal_degrees = deg + minutes / 0.6
    return decimal_degrees


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
    for glider_id in glider_ids:
        dive = session.query(Dives) \
            .filter(Dives.MissionID == mission_id) \
            .filter(Dives.GliderID == glider_id) \
            .order_by(Dives.DiveNo.desc()) \
            .first()
        most_recent_dives.append(dive)

    session.close()
    return dives, gliders, most_recent_dives


def dives_to_json(dives, gliders) -> Tuple:
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
    dive_page_links = []
    for i, dive in enumerate(dives):
        dive_page_link = "/mission" + str(dive.MissionID) + "/glider" + str(glider_number_dict[dive.GliderID]) \
                         + "/dive" + str(dive.DiveNo).zfill(4)
        dive_page_links.append(dive_page_link)
        tgt_popup = 'SG ' + str(glider_number_dict[dive.GliderID]) + ' ' + gliders_name_dict[
            dive.GliderID] + "<br><a href=" + dive_page_link + ">Dive " + str(dive.DiveNo) + "</a>" + "<br>Lat: " + str(
            dive.Latitude) + "<br>Lon: " + str(dive.Longitude)
        dive_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
                    coord_db_decimal(dive.Longitude),
                    coord_db_decimal(dive.Latitude)
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup,
                "gliderOrder": glider_order_dict[dive.GliderID],
            },
            "id": i
        }
        features.append(dive_item)
    dive_page_links.sort(reverse=True)
    divedict = {
        "type": "FeatureCollection",
        "features": features
    }
    return divedict, dive_page_links


def targets_to_json(targets, mission_tgt=False) -> dict:
    features = []
    for i, target in enumerate(targets):
        if mission_tgt:
            tgt_popup = "Mission " + str(target.MissionID) + "<br><a href=/mission" + str(
                target.MissionID) + ">" + target.Name
        else:
            tgt_popup = "Target: " + target.Name + "<br>Lat: " + str(target.Latitude) + "<br>Lon: " + str(
                target.Longitude) + "<br>GOTO: " + target.Goto + "<br>Radius: " + str(target.Radius) + ' m'
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
                    coord_db_decimal(target.Longitude),
                    coord_db_decimal(target.Latitude)
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


def waypoints_to_json(waypoints) -> dict:
    features = []
    for i, waypoint in enumerate(waypoints):
        tgt_popup = "Waypoint: " + waypoint.Name + "<br>Lat: " + str(waypoint.Latitude) + "<br>Lon: " + str(
            waypoint.Longitude)
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
                    coord_db_decimal(waypoint.Longitude),
                    coord_db_decimal(waypoint.Latitude)
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup
            },
            "id": i
        }
        features.append(target_item)

    waypointdict = {
        "type": "FeatureCollection",
        "features": features
    }
    return waypointdict


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
