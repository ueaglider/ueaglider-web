#!/bin/bash
cd /home/callum/Documents/web/output
rm /home/callum/Documents/web/output/data.zip
rsync "webadmin@139.162.215.209:/apps/ueaglider_repo/output/data.zip" /home/callum/Documents/web/output/data.zip
rm /home/callum/Documents/web/output/*.csv
unzip /home/callum/Documents/web/output/data.zip
printf '\n%s' "$(date "+%Y-%m-%dT%H:%M:%S")" >> /home/callum/Documents/web/output/transfer.log
/home/callum/Documents/web/venv/bin/python /home/callum/Documents/web/ueaglider/bin/add_from_csv.py

