import sys
from glob import glob
from ueaglider.services.glider_service import glider_info
import os
import xarray as xr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import cmocean as cmo


def main():
    # get glider num from bash script. Gliders are linux users named sgXXX where XXX is the glider number
    glider_num = sys.argv[1][2:]
    glider, __ = glider_info(glider_num)
    mission_num = glider.MissionID
    create_plots(glider_num, mission_num)


def create_plots(glider_num, mission_num):
    plots_dir = f'/mnt/gliderstore/dives/Mission{mission_num}/{glider_num}/Science_python'

    #Check if plots_dir exists, if not, create it
    CHECK_DIR = os.path.isdir(plots_dir)
    # If folder doesn't exist, then create it.
    if not CHECK_DIR:
        os.makedirs(plots_dir)

#    mission_nc = glob(f'/home/sg{glider_num}*_timeseries.nc')[0]
    # Beth plotting stuff here
    mission_nc = glob(f'/home/sg{glider_num}*_up_and_down_profile.nc')[0]
    ds = xr.open_dataset(mission_nc)

    profile_time = ds.ctd_time.mean(axis=1).data  # average time per profile
    ds = ds.assign_coords(profile_time=("profile", profile_time))  # assign this as a new coordinate called profile_time
    ds.profile_time.attrs = {'comment': 'Mean time of CTD profile',  # add essential metadata, or xarray won't plot it
                             'standard_name': 'time',
                             'axis': 'profile'}
    measuredvariables = list(ds.keys())  # list data variables in ds

    # list of variables from old matlab script that may come from glider
    #tbi, update list of variables, particularly check for revE seagliders
    glider_variables = ('temp', 'temperature', 'conductivity', 'salinity', 'sigma_theta', 'dissolved_oxygen_sat',
                        'eng_aa4330_O2', 'eng_aa4330F_O2', 'eng_aa1_O2', 'eng_aa807_O2', 'eng_aa4831_O2',
                        'contopt_instrument_dissolved_oxygen', 'contopt_dissolved_oxygen',
                        'eng_aa4330_Temp', 'eng_aa4330F_Temp', 'eng_aa1_Temp', 'eng_aa807_Temp', 'eng_aa4831_Temp',
                        'eng_contopt_Temp', 'eng_contopt_pO2',
                        'eng_wl_sig1', 'eng_wl1_sig1', 'eng_wl_Chlsig1', 'eng_wl1_Chlsig1', 'eng_wl_Cdomsig1',
                        'eng_wl1_Cdomsig1',
                        'eng_phfl_raw_data', 'eng_phfl_pHcalib', 'eng_phfl_Temp',
                        'eng_ph_pH', 'eng_ph_pCO2', 'eng_ph_temp_pH',
                        'eng_qsp144_PARuV', 'eng_qsp1_PARuV', 'eng_qsp_PARuV', 'eng_qsp_PARuV', 'eng_qsp1_PARuv',
                        'eng_wlbbfl2vmt_wl600sig', 'eng_wlbbfl2vmt_wl650sig', 'eng_wlbbfl2vmt_Cdomsig',
                        'eng_wlbbfl2vmt_Chlsig',
                        'eng_wl1_sig1', 'eng_wl1_Chlsig1', 'eng_wl1_Cdomsig1',
                        'eng_wl836_sig1', 'eng_wl836_Chlsig1', 'eng_wl836_Cdomsig1',
                        'eng_wlbb2fl_BB1sig', 'eng_wlbb2fl_BB2sig', 'eng_wlbb2fl_FL1sig',
                        'eng_wlbbfl2_BB1sig', 'eng_wlbbfl2_FL1sig', 'eng_wlbbfl2_FL2sig',
                        'eng_wlseaowl_FL1sig', 'eng_wlseaowl_BB1sig', 'eng_wlseaowl_FDOMsig', 'eng_wlbbfl2_temp')

    # create dictionary to match each variable in glider_variables to a colourmap
    default_cmap = "viridis"
    dict = {}
    for j in range(len(glider_variables)):
        dict[glider_variables[j]] = default_cmap

    # update certain variables colourmaps
    #dict['temp'] = cmo.cm.thermal
    #dict['temperature'] = cmo.cm.thermal
    #dict['conductivity'] = cmo.cm.haline
    #dict['salinity'] = cmo.cm.haline
    #dict['sigma_theta'] = cmo.cm.dense
    #dict['eng_aa4330_Temp'] = cmo.cm.thermal
    #dict['eng_aa4330F_Temp'] = cmo.cm.thermal
    #dict['eng_aa1_Temp'] = cmo.cm.thermal
    #dict['eng_aa807_Temp'] = cmo.cm.thermal
    #dict['eng_aa4831_Temp'] = cmo.cm.thermal
    #dict['eng_contopt_Temp'] = cmo.cm.thermal
    #dict['eng_wl_Chlsig1'] = cmo.cm.algae
    #dict['eng_wl1_Chlsig1'] = cmo.cm.algae

    to_plot = list(set(measuredvariables).intersection(glider_variables))  # find elements in glider_variables relevant to this dataset

    for i in range(len(to_plot)):
        plotter(ds, to_plot[i], dict[to_plot[i]], to_plot[i])
    return

#define a basic quality control function
def prepare_for_plotting(dataset, variable):
    """Prepare variable for plotting by:
    1. Removing outliers more than 2 std dev from the mean
    2. Interpolating over nans
    """
    data = dataset[variable].data
    # Copy some of the cleaning functionality from GliderTools and use it here
    # https://github.com/GliderToolsCommunity/GliderTools/blob/master/glidertools/cleaning.py
    # e.g. remove data more than 2 standard deviations from the mean

    from numpy import array, nan, nanmean, nanstd
    arr = data
    # standard deviation
    mean = nanmean(arr)
    std = nanstd(arr)

    multiplier = 2
    ll = mean - std * multiplier
    ul = mean + std * multiplier

    mask = (arr < ll) | (arr > ul)
    arr[mask] = nan
    dataset[variable].data = data

    # nanpercentile
    #ll = np.nanpercentile(arr, 0.5)
    #ul = np.nanpercentile(arr, 99.5)
    # tbi

    return dataset


# define a basic plotting function for the profiles
def plotter(dataset, variable, colourmap, title):
    """Create time depth profile coloured by desired variable

    Input:
    dataset: the name of the xarray dataset
    variable: the name of the data variable to be plotted
    colourmap: name of the colourmap to be used in profile
    title: variable name included as title to easily identify plot

    The intended use of the plotter function is to iterate over a list of variables,
    plotting a pcolormesh style plot for each variable, where each variable has a colourmap assigned using a dictionary"""

    # find max depth the given variable was measures to
    var_sum = np.nansum(dataset[variable].data, 0)
    valid_depths = dataset[variable].depth.data[var_sum != 0.0]

    fig, ax = plt.subplots()
    dataset = prepare_for_plotting(dataset, variable)
    dataset[variable].T.plot(yincrease=False, y="depth", x="profile_time", cmap=colourmap)
    ax.set_ylim(valid_depths.max(), valid_depths.min())
    ax.set_title(str(title))
    plt.tight_layout()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))  # sets x tick format
    fig.savefig(plots_dir + '/' + variable + '.jpeg', format='jpeg')
    matplotlib.pyplot.close()
    return


if __name__ == '__main__':
    main()