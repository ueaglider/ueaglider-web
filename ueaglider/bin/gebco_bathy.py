import sys
from pathlib import Path
import xarray as xr
import numpy as np
import os
import matplotlib.pyplot as plt
import json
from shapely.geometry import LineString
import geopandas as gpd

path_to_gebco_nc = '/media/callum/storage/Documents/global_datasets/GEBCO_2019/GEBCO_2019.nc'


def main():
    lon = float(sys.argv[1])
    lat = float(sys.argv[2])
    mission = sys.argv[3]
    rad = 300  # radius in km from point to grab bathy data. Will return a square, not a circle though
    north = lat + rad / 111
    south = lat - rad / 111
    west = lon - rad / (111 * np.cos(np.deg2rad(lat)))
    east = lon + rad / (111 * np.cos(np.deg2rad(lat)))
    if north > 90:
        north = 90
    if south < -90:
        south = -90
    if west < -180:
        west = -180
    if east > 180:
        east = 180
    gebco_to_geojson(extent=[south, north, west, east], depths=[-50, -200, -1000],
                     directory='static/json/Mission' + str(mission))


def gebco_to_geojson(extent=(58, 55, -2, 5), depths=(-50, -200, -1000), directory='Mission'):
    """
    Extracts isobaths from gebco bathymetric grid and writes them to geoJSON format
    :param extent: lon - lat square defines region of interest[S, N, W, E]
    NOTE: making this bigger than around 90 * 90 degrees may cause excess memory use and termination of process
    :param depths: depth levels to extract, make +ve for above sea level topography
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
        lines = []
        print("extracting geometries")
        for shape in shapes:
            v = shape.vertices
            x = v[:, 0]
            y = v[:, 1]
            if len(x) < 2:
                # Trying to write a single point to a LineString throws an error
                continue
            coord_pairs = []
            for i, j in zip(x, y):
                coord_pairs.append((i, j))
            lines.append(LineString(coord_pairs))
        # create geopandas dataframe and write it to json
        line_gdf = gpd.GeoDataFrame(geometry=lines)
        geo_json = line_gdf.to_json()
        print("writing to file")
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/isobaths_' + str(abs(depth)) + 'm.json', 'w', encoding='utf-8') as f:
            json.dump(geo_json, f)


def gebco_subset(path_to_folder_str, extent):
    """
    Extracts bathy data from a global GEBCO .nc file from an area specified by the use
    :param path_to_folder_str: string of path to the folder or file of gebco data
    :param extent: list with four items which are extent of desired geotiff [South, North, West, East]
    e.g. [49. 50.5, -5, 2] (if using gebco or emodnet)
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
