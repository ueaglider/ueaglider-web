import sys
from glob import glob
from ueaglider.services.glider_service import glider_info


def main():
    # get glider num from bash script. Gliders are linux users named sgXXX where XXX is the glider number
    glider_num = sys.argv[1][2:]
    glider, __ = glider_info(glider_num)
    mission_num = glider.MissionID
    create_plots(glider_num, mission_num)


def create_plots(glider_num, mission_num):
    plots_dir = f'/mnt/gliderstore/dives/Mission{mission_num}/{glider_num}/Science_python'
    # TODO create plots_dir if it does not exist
    mission_nc = glob(f'home/sg{glider_num}*_timeseries.nc')[0]
    # Beth plotting stuff here
    return
