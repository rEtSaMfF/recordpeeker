import csv
from pkg_resources import resource_stream
import heapq
import json

import command_line

def json_decode(string):
    """Windows likely does not have utf8 as the system encoding and Python is
    too stubborn to provide a sensible default."""
    return json.loads(string.decode('utf-8-sig'))


def anonymize_data(data):
    """
    Remove the user_id from the data.
    """
    battle = data.get("battle")
    if battle is not None:
        for buddy in battle["buddy"]:
            buddy["ability_panels"][0]["uid"] = 0

    party = data.get("party")
    if party is not None:
        party["uid"] = 0

    user = data.get("user")
    if user is not None:
        user["id"] = 0

class Equipment(dict):
    def __init__(self, sourcedict):
        dict.__init__(self, **sourcedict)

    def rs(self, series):
        if self["series_id"] == int(series):
            return {"name": self["name"], "acc": self["series_acc"], "atk": self["series_atk"],
                    "def": self["series_def"], "eva": self["series_eva"], "matk": self["series_matk"],
                    "mdef":self["series_mdef"], "mnd":self["series_mnd"]}
        else:
            return slicedict(self, "name acc atk def eva matk mdef mnd".split())

def slicedict(d, s):
    return {k:v for k,v in d.iteritems() if k in s}

def best_equipment(series, heap, stat, n=3):
    return [y.rs(series) for y in heapq.nlargest(n, heap, lambda x: x.rs(series)[stat])]

def load_dict(path):
    res = dict()
    rfile = resource_stream("recordpeeker", path)
    reader = csv.reader(rfile)
    for row in reader:
        res[row[0]] = row[1]
    return res

ITEMS = load_dict("data/items.csv")
BATTLES = load_dict("data/battles.csv")
DUNGEONS = load_dict("data/dungeons.csv")
