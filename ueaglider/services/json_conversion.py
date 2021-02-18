from typing import Tuple

from ueaglider.services.mission_service import degree_sign


def coord_dec_to_pretty(coord_in):
    # convert from decimal degrees to pretty formatted string for popup text
    deg = int(coord_in)
    minutes = abs(coord_in - deg) * 60
    coord_str = str(deg) + degree_sign + " " + str(round(minutes, 2)) + "'"
    return coord_str
    
    
def dives_to_json(dives, gliders) -> Tuple:
    # Extract the glider names and numbers corresponding to the GliderID that is included in DiveInfo table
    gliders_name_dict = {}
    glider_number_dict = {}
    for glider in gliders:
        gliders_name_dict[glider.Number] = glider.Name
        glider_number_dict[glider.Number] = glider.Number
    # Make a sorted dictionary of ascending integers per gliderID for colouring the map dive icons
    glider_ids = list(glider_number_dict.keys())
    glider_ids.sort()
    glider_order_dict = {val: i for i, val in enumerate(glider_ids)}
    features = []
    dive_page_links = []
    coords = []
    i = 0
    dive = []
    for i, dive in enumerate(dives):
        coords.append([dive.Longitude, dive.Latitude])
        dive_page_link = "/mission" + str(dive.MissionID) + "/glider" + str(dive.GliderID) \
                         + "/dive" + str(dive.DiveNo).zfill(4)
        dive_page_links.append(dive_page_link)
        tgt_popup = 'SG ' + str(dive.GliderID) + ' ' + gliders_name_dict[
            dive.GliderID] + "<br><a href=" + dive_page_link + ">Dive " + str(dive.DiveNo) + "</a>" + "<br>Lat: " \
            + coord_dec_to_pretty(dive.Latitude) + "<br>Lon: " + coord_dec_to_pretty(dive.Longitude)
        dive_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
                    dive.Longitude,
                    dive.Latitude
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup,
                "gliderOrder": glider_order_dict[dive.GliderID],
                "gliderNum": dive.GliderID,
                "diveLink": dive_page_link,
                "diveNum": str(dive.DiveNo),
            },
            "id": i
        }
        features.append(dive_item)
    dive_page_links.sort(reverse=True)
    divedict = {
        "type": "FeatureCollection",
        "features": features
    }
    linedict = {
        "type": "FeatureCollection",
        "features": [{
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "type": "Feature",
            "properties": {
                "gliderOrder": glider_order_dict[dive.GliderID],
            },
            "id": i
        }]
    }

    return divedict, dive_page_links, linedict


def targets_to_json(targets, mission_tgt=False) -> dict:
    features = []
    for i, target in enumerate(targets):
        if mission_tgt:
            tgt_popup = "Mission " + str(target.MissionID) + "<br><a href=/mission" + str(
                target.MissionID) + ">" + str(target.Name)
        else:
            tgt_popup = "Target: " + str(target.Name) + "<br>Lat: " + coord_dec_to_pretty(
                target.Latitude) + "<br>Lon: " + coord_dec_to_pretty(
                target.Longitude) + "<br>GOTO: " + str(target.Goto) + "<br>Radius: " + str(target.Radius) + ' m'
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
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


def pins_to_json(waypoints) -> dict:
    features = []
    for i, waypoint in enumerate(waypoints):
        tgt_popup = "Target: " + str(waypoint.Name) + "<br>Lat: " + coord_dec_to_pretty(
            waypoint.Latitude) + "<br>Lon: " + coord_dec_to_pretty(waypoint.Longitude) + "<br>" + str(waypoint.Info)
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # convert from kongsberg style degree-mins in table to decimal degrees
                    waypoint.Longitude,
                    waypoint.Latitude
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
