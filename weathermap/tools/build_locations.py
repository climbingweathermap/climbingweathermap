""" Combine open beta location (area) files"""
import json
import jsonlines
import os
import glob

locations = {}
sourcepath = ".\\weathermap\\tools"
outpath = ".\\instance\\locations.json"

data_files = glob.glob(f"{sourcepath}/*.jsonlines")

for file in data_files:
    with jsonlines.open(file) as reader:
        for loc in reader.iter(type=dict, skip_invalid=True):
            _temp = {
                "lat": loc["lnglat"][1],
                "long": loc["lnglat"][0],
                "url": loc["url"],
            }
            locations[loc["area_name"]] = _temp

with open(outpath, "w+") as f:
    json.dump(locations, f)
