import sys
from pathlib import Path
import xarray as xr
import numpy as np
import os
import matplotlib.pyplot as plt
import json
from shapely.geometry import LineString
import geopandas as gpd
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
with open(folder+'/secrets.txt') as json_file:
    secrets = json.load(json_file)
path_to_gebco_nc = secrets["gebco_path"]
json_dir = secrets["json_dir"]


def main():
    # get lon, lat and mission number from the app when it calls this script with argv
    lon = float(sys.argv[1])
    lat = float(sys.argv[2])
    mission = sys.argv[3]
    rad = 300  # radius in km from point to grab bathy data. Will return a square, not a circle though
    # Create limits with the center point and the distance, approx converted to degrees lon and lat
    north = lat + rad / 111
    south = lat - rad / 111
    west = lon - rad / (111 * np.cos(np.deg2rad(lat)))
    east = lon + rad / (111 * np.cos(np.deg2rad(lat)))
    # Hard block to keep limits within the surface of the earth. xarray doesn't like being indexed to 92 degrees North
    if north > 90:
        north = 90
    if south < -90:
        south = -90
    if west < -180:
        west = -180
    if east > 180:
        east = 180
    gebco_to_geojson(extent=[south, north, west, east], depths=[-50, -200, -500, -1000],
                     directory=json_dir + 'Mission' + str(mission))


def gebco_to_geojson(extent=(58, 55, -2, 5), depths=(0, -1000), directory='Mission'):
    """
    Extracts isobaths from gebco bathymetric grid and writes them to geoJSON format
    :param extent: lon - lat square defines region of interest[S, N, W, E]
    NOTE: making this bigger than around 90 * 90 degrees may cause excess memory use and termination of process
    with a small web server, I avoig going more than 10 * 10
    :param depths: topographic levels to extract, make -ve for bathy +ve for topo
    :param directory: name of directory to write json files to
    :return: None
    """
    # extract bathy from region of interest
    lon, lat, topo = gebco_subset(path_to_gebco_nc, extent)
    for depth in depths:
        print(str(directory) + "depth " + str(depth))
        # create single contour level plot
        fig, ax = plt.subplots()
        cs = ax.contour(lon, lat, topo, [depth])
        shapes = cs.collections[0].get_paths()
        # some inefficient loops to extract the data and convert it to shapely LineStrings
        # we only run this once per mission then save the files so not really worth optimising
        lines = []
        print("extracting geometries")
        for shape in shapes:
            v = shape.vertices
            x = v[:, 0]
            y = v[:, 1]
            if len(x) < 2:
                # Trying to write a single point to a LineString throws an error so skip those
                continue
            coord_pairs = []
            for i, j in zip(x, y):
                coord_pairs.append((i, j))
            lines.append(LineString(coord_pairs))
        # create geopandas dataframe and write it to json
        line_gdf = gpd.GeoDataFrame(geometry=lines)
        geo_json = line_gdf.to_json()
        print("writing to file")
        # create mission directory if it doesn't exist already
        if not os.path.exists(directory):
            os.makedirs(directory)
        # write geojson to file
        with open(directory + '/isobaths_' + str(abs(depth)) + 'm.json', 'w', encoding='utf-8') as f:
            json.dump(geo_json, f)


def gebco_subset(path_to_folder_str, extent):
    """
    Extracts bathy data from a global GEBCO .nc file from an area specified by the use
    :param path_to_folder_str: string of path to the folder or file of gebco data
    :param extent: list with four items which are extent of desired bathy [South, North, West, East]
    :return: numpy arrays of lon, lat and bathymetry
    """
    extent = list(extent)
    if extent[2] > 180:
        extent[2] = extent[2] - 360
    if extent[3] > 180:
        extent[3] = extent[3] - 360
    path_to_folder = Path(path_to_folder_str)
    if path_to_folder.is_file():
        gebco = xr.open_dataset(path_to_folder)
    else:
        path_to_gebco = list(Path(path_to_folder).joinpath().glob("*.nc"))
        if not path_to_gebco:
            print(
                'No netcdf files found in location supplied. Check that you pointed to a .nc file or a folder '
                'containing one. Aborting')
            exit(1)
        gebco = xr.open_dataset(path_to_gebco[0])
    print("Subsettting GEBCO data")
    subset = gebco.sel(lon=slice(extent[2], extent[3]), lat=slice(extent[0], extent[1]))
    return np.array(subset.lon), np.array(subset.lat), np.array(subset.elevation)


if __name__ == '__main__':
    main()
