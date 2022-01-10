// ------------ Global Vars ---------------
var host = document.location.host;
var course = 0.0;
var controlPanel;
var gps; // current ship's positoin (global so we can use it in multiple places)
var dasngTrackline; // ship trackline based on dasNG on hermes
var realtimeTrackline; // ship trackline realtime in-browser data
var shipMarker;  // marker for the ship
var wptMarker;  // waypoint for the marker for the ship
var showControls = false; // bool to show the map controls or not
var fallowShip = false; // whether to keep the map centerd on the ship during refresh
var autozoom = false; // bool whether to zoom to the ship and the next waypoint
var lyrEEZ; // EEZ layer
var graticules;  // lat/lon grid lines

function getParameterByName(name, url)
// Get URL query parameters
// Name is the name of the URL paramter you want to get the value for, and URL is a URL (will use the current page if null)
{
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    decoded = decodeURIComponent(results[2].replace(/\+/g, " "));
    if (decoded.toUpperCase() == 'TRUE') return true;
    if (decoded.toUpperCase() == 'FASLE') return false;
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getCurrentPosition()
// Get the ship's current position, and return a L.LatLng object
{
                var lat = $.getData("NBPs330Lat",6);
                var lng = $.getData("NBPs330Lon",6);
                // if longitude is negative, move it to 0-360 instead of -180 to 180 range
                // Disabled NBP1707 - found a better way!
                //if (lng < 0) {lng = (parseFloat(lng) + 180) + 180;}
                gps = new L.LatLng(parseFloat(lat),parseFloat(lng));
                return gps;
}


function getTrackline()
// Get the ship's current trackline
{
    var json;
    $.getJSON( "https://dasng.nbp.usap.gov/map_custom/sqlite-geojson-trackline4.php", function( data ) {
        // Add realtime polyline
        var myStyle = {
            "color": "#ff7800",
            "weight": 5,
            "opacity": 0.65
        };
    dasngTrackline = L.geoJson(data, { style: myStyle });
    dasngTrackline.addTo(map);

    //Add realtime trackline
    var mp = dasngTrackline.toMultiPoint();
    var lastpoint = mp.geometry.coordinates[mp.geometry.coordinates.length-1][mp.geometry.coordinates[mp.geometry.coordinates.length-1].length-1]
    var llLastPoint = L.latLng(lastpoint[1],lastpoint[0]);

    });
}

function UpdateRemoteShip()
// This function is for USAP HQ - not used on the ships...
{
    // parse the .data file
    $.get('https://maps.nbp.usap.gov/NBP-1497325201.data', function(data)
    {
        var lines = data.split('\n');
        var shipInfo = {};
        var shipTooltip = "<table>"
        for (var i=0; i<lines.length; i++)
        {
            var linevalues = lines[i].split(':')
            if (linevalues.length > 1)
            {
                var value = linevalues[1];
                // Try to parse it as a number
                numbervalue = parseFloat(value)
                if (isNaN(numbervalue)) { value = value.trim()} else {value = numbervalue}
                shipInfo[linevalues[0]] = value
                shipTooltip += "<tr><td><strong>" + linevalues[0] +"</strong></td><td>" + value +"</td></tr>"

            }
        }
        shipTooltip += "</table>"
        // now ShipInfo is an object that contains all our data
        // Add a marker to the map
        var shipPosition = L.latLng([shipInfo["Lat"],shipInfo["Lon"]]);
        shipMarker = L.marker(shipPosition);
        shipMarker.bindTooltip(shipTooltip, {permanent: true});
        shipMarker.addTo(map);
    });


}
function UpdateMap()
// Update the map with realtime data
{
    //
//    console.log(data)Remove the existing ship icon and set a new one
    shipMarker.remove();
    gps = getCurrentPosition();
    var shipIcon = new L.BoatIcon();
    // Set the new icon to a boaticon with heading and wind info
    shipIcon.setHeadingWind($.getData("NBPGyroHeading",1),$.getData("NBPSUSTrueWindSpdKn",1),$.getData("NBPSUSTrueWindDir",1));
    shipMarker = new L.marker(gps, {icon: shipIcon});
    shipMarker.addTo(map);
    realtimeTrackline.addLatLng(gps); // pop our position into the realtime trackline
    // Update the waypoint marker
    wptMarker.remove();
    wptMarker = getNextWaypoint();
    wptMarker.addTo(map);
    if (followShip == true)
    {
        CenterOnShip();
        // If followship is set, set the view to the ship and the next waypoint
        //map.fitBounds([gps,wptMarker._latlng]);
        // Now zoom out one level to make sure it's all in view
        //map.zoomOut();  // actually, this seems to make the map zoom out every refresh. not cool.
    }

}

function getNextWaypoint()
// Get the next waypoint as an L.marker object
{
    var lat = $.getData("NBPDestLat",6);
    var lng = $.getData("NBPDestLon",6);
    var name = $.getData("NBPDestinationName");
    var wptLatLng = new L.LatLng(parseFloat(lat),parseFloat(lng));
    var wptMarker = new L.marker(wptLatLng);
    // Show the waypoint text, and set the tooltip to permanent so it always is visible
    wptMarker.bindTooltip(name, {direction: 'bottom', permanent: true});
    return wptMarker;
}

function onMouseMove(e)
// Function to update the infobox with the cursor's lat/lon
{
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;
    // if the lon is > 180, show it as a neg. (West) value
    // This is to account for the way leaflet handles scrolling past the antimeridian (180 longitude)
    if (Math.abs(lon) > 180)
    {
        if (lon > 0) lon = (180-(Math.abs(lon)-180))*-1;
        else lon = 180-(Math.abs(lon)-180);
    }
    // Calculate the distance from the mouse cursor position and the ship
    var latlng = L.latLng(lat,lon);
    var distance_meters = latlng.distanceTo(gps);
    var distance_nm = distance_meters * 0.00054;
    // Update the text in the infobox
    $("#mouseposition").html(convertDMS(latlng) + "<br />" + latlng.lat.toFixed(5) + ", " + latlng.lng.toFixed(5) + "<br />Distance from ship: " + distance_nm.toFixed(1) + "nm" );
}

function onZoomEnd(e)
// Function to handle zoom end event
{
        //Check zoom level
        zoom = map.getZoom();
        map.attributionControl.setPrefix("Zoom: " + zoom);
}

function CenterOnShip()
// Function to re-center the map to the ship's position
{
    gps = getCurrentPosition()
    map.panTo(gps);
}


/**
 * Convert longitude/latitude decimal degrees to degrees and minutes
 * DDD to DMS, no seconds
 * @param latlng, L.LatLng object
 */
function convertDMS( latlng ) {
        lat = latlng.lat;
        lng = latlng.lng;
        var convertLat = Math.abs(lat);
        var LatDeg = Math.floor(convertLat);
        var LatMin = ((convertLat - LatDeg) * 60).toFixed(4);
        var LatCardinal = ((lat > 0) ? "N" : "S");
        var convertLng = Math.abs(lng);
        var LngDeg = Math.floor(convertLng);
        var LngMin = ((convertLng - LngDeg) * 60).toFixed(4);
        var LngCardinal = ((lng > 0) ? "E" : "W");
        return LatDeg + "&deg; " + LatMin + LatCardinal  + ", " + LngDeg + "&deg; " + LngMin + LngCardinal;
}

//update an element on the page with a DAS varible
function updateElement(element,DASvariable,precision)
{
    // precision is an optional argument, default to 2 decimal places
    precision = precision || 2;
    // get the data from dasNG
    var data = $.getData(DASvariable,precision);
    try
    {
        // set the value
        document.getElementById(element).innerHTML = data;
    }
    catch(ex) {}
}

/****  Context Menu handlers aka what to do when the user right-clicks *****/
function showCoordinates (e) {
    lat = e.latlng.lat;
    lon = e.latlng.lng;
    text = "Cursor Position (in waypoint.txt format):\n" + lat.toFixed(5) + "," + lon.toFixed(5) + ",WAYPONTTEXT";
alert(text);
}

function centerMap (e) {
    map.panTo(e.latlng);
}

function zoomIn (e) {
    map.zoomIn();
}

function zoomOut (e) {
    map.zoomOut();
}
