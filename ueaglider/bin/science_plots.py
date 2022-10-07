import sys
from glob import glob
from ueaglider.services.glider_service import glider_info
import os


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
    return

if __name__ == '__main__':
    main()