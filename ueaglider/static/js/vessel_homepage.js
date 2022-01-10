// Function to get data from dasNG
jQuery.extend({
getData: function(varname,precision) {

	// precision is an optional argument, default to 2 decimal places
	precision = precision || 2;
	var result = null;
//AC 26/10/20	var geturl = 'http://hermes.nbp.usap.gov/rvdas/' + varname
  	var geturl = 'https://dasng.nbp.usap.gov/rvdas/' + varname
	// detect IE CORS transport
	// IE8 does not allow cross-domain requests via the standard xmlhttp request,
	// so we have to use XDomainRequest instead.
	try
	{
	if ('XDomainRequest' in window && window.XDomainRequest !== null)
	{
		var xdr = new XDomainRequest();
		xdr.open("get", geturl);
		xdr.onload = function() { result = xdr.responseText; }
		xdr.send();
	}
	else //we're using a browser that actually handles XDRs like it should
	{
    $.ajax({
        url: geturl,
        type: 'get',
        dataType: 'html',
        async: false,
        success: function(data) {
            result = data;
        }
    });
	}
	}
	catch(err) {};
	// Return the data, if precision is set, format the number
	// if not a number, just return the data (prob. a string value)
	var data = result;
	if (!isNaN(Number(data))) { data = Number(data).toFixed(precision);}
    return data;
}
});

//update an element on the page with a DASvarible
function updateElement(element,DASvariable,precision)
{
	// precision is an option argument
	precision = precision || 2;
	// get the data from dasNG
	var data = $.getData(DASvariable,precision);
	//alert(DASvariable + " " + data);
	//var textElement = document.getElementById(element);
	//textElement.html = data;
	try
	{
	document.getElementById(element).innerHTML = data; //data;
	}
	catch(ex) {}
}
function updateSidebar()
{
	 //get DAS data variables and update their page elements

    updateElement("windspeed","NBPPUSTrueWindSpdKn",1);
	updateElement("winddir","NBPSUSTrueWindDir",1);
	updateElement("airTemp", "NBPmwxAirTemp", 1);
	updateElement("windchill","NBPCalcWindChill",1);
	updateElement("seaTemp","NBPRtmprtemp",1);
	updateElement("shipLat", "NBPs330Lat", 4);
    updateElement("shipLng", "NBPs330Lon", 4);
	updateElement("wpName", "NBPDestinationName",0);
    updateElement("wpDist", "NBPnMilesToDest",1);
	updateElement("wpTime", "NBPTravelTime",1);
	updateElement("speed", "NBPs330SOGkn",1);
	updateElement("gyroHeading", "NBPGyroHeading",1);
	updateElement("gpsCOG", "NBPseapCOG",1);


	var IsCTDout = false; // Check if CTD is in operation
	var CurrentWinch = $.getData("NBPWinchSource", 0);

	if (CurrentWinch == 'BALTIC')
	{
		var CTD_Depth = $.getData("NBPCTDDepthm",1);
		var CTD_WireOut = $.getData("NBPWnc1MetersOut",1);
		var CTD_WireSpeed = $.getData("NBPWnc1Speed",1);
		if ((CTD_Depth > 0) && (CTD_WireOut > 0))
		{
			ISCTDout = true;
			$("#ctdwinch").show();
			updateElement("ctd_depth", "NBPCTDDepthm",1);
			updateElement("ctd_wireout", "NBPWnc1MetersOut",1);
			updateElement("ctd_speed", "NBPWnc1Speed",1);
		}
		else { $("#ctdwinch").hide(); }

	}
	var Sunriseset = SunriseSunset();
	document.getElementById("Sunrise").innerHTML = FormatTime(Sunriseset['Sunrise']);
	document.getElementById("Sunset").innerHTML = FormatTime(Sunriseset['Sunset']);
	document.getElementById("civildusk").innerHTML = FormatTime(Sunriseset['civildusk']);
	document.getElementById("civildawn").innerHTML = FormatTime(Sunriseset['civildawn']);
	document.getElementById("nauticaldusk").innerHTML = FormatTime(Sunriseset['nauticaldusk']);
	document.getElementById("nauticaldawn").innerHTML = FormatTime(Sunriseset['nauticaldawn']);

}
function FormatTime(thisTime)
// Format the moment time object to be HH:mm or '---' if invalid (i.e. the sun doens't rise today)
{
	if (thisTime.isValid())
	{
		return thisTime.format("HH:mm");
	}
	else return "---";
}
function SunriseSunset()
/*	Function to calculate the sunrise and sunset times based on the Lat/Long of where you are.

	REQUIREMENTS:
	SunCalc.js library
	Moment.js library

	ATTENTION: function is called by the following files:
	\\winfs\web\vessel-website\include\sidebar.shtml (intranet sidebar)

	RETURN VALUE:
	Object 	{
			Sunrise: Moment Object,
			Sunset: Moment Object,
			}
*/
{
	// Sunrise & Sunset
	var sunToday = SunCalc.getTimes(new Date(), $.getData('NBPs330Lat',5), $.getData('NBPs330Lon',5)); // NBP Lat/Lon
	var sunriseTime = moment(sunToday.sunrise);
	var sunsetTime = moment(sunToday.sunset);
	var civilduskTime = moment(sunToday.dusk);
	var civildawnTime = moment(sunToday.dawn);
	var nauticalduskTime = moment(sunToday.nauticalDusk);
	var nauticaldawnTime = moment(sunToday.nauticalDawn);
	// Wrap it all up in an object
	var retValue = {}; // define object to contain returned values
	retValue['Sunrise'] = sunriseTime;
	retValue['Sunset'] = sunsetTime;
	retValue['civildusk'] = civilduskTime;
	retValue['civildawn'] = civildawnTime;
	retValue['nauticaldusk'] = nauticalduskTime;
	retValue['nauticaldawn'] = nauticaldawnTime;
	// Return the value
	return retValue;
}
$(function($)
// This function sets the clocks on the homepage
// to adjust the the time for a clock, just change the utc_offset varible
{
    try
    {
        var optionsMcMurdo = {
            format: '%H:%M:%S %a, %d %b %Y',
		    utc: true,
            utc_offset: 13
        }
        $('#clock_McMurdo').jclock(optionsMcMurdo);
        var optionsUTC = {
            format: '%H:%M:%S %a, %d %b %Y',
            utc: true,
            utc_offset: 0
        }
        $('#clock_UTC').jclock(optionsUTC);
        var optionsChile = {
            format: '%H:%M:%S %a, %d %b %Y',
		    utc: true,
            utc_offset: -3
        }
        $('#clock_Chile').jclock(optionsChile);
        var optionsDenver = {
		    format: '%H:%M:%S %a, %d %b %Y',
            utc: true,
            utc_offset: -7
        }
        $('#clock_Denver').jclock(optionsDenver);
    } catch(err) {};

});
function init(interval)
{
	updateSidebar();
	window.setInterval(function(){updateSidebar()},interval);
}
