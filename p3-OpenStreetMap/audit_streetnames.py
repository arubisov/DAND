#!/usr/bin/env python

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "toronto_canada.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Crescent", "Drive", "Court",
            "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons",
            'Circle', 'Way', 'Terrace', 'Mews', 'Gate', 'Hollow', 'Queensway',
            'Heights', 'Promenade', 'Park', 'Sideroad', 'Line', 'Manor',
            'Meadoway', 'Millway', 'Passage', 'Path', 'Pathway', 'Point',
            'Ridge', 'Rise', 'Row', 'Roseway', 'Run', 'Shepway', 'Sideline',
            'Starway', 'Townline', 'Vineway', 'Walk', 'Wood', 'Landing',
            'Hill', 'Highway', 'Hawkway', 'Grove', 'Green', 'Gardens', 'Garden',
            'Fernway', 'Crossing', 'Concession', 'Common', 'Close', 'Circuit',
            'Chase', 'Gateway', 'Golfway', 'Grassway', 'Greenway']

CARDINALS = ['North', 'South', 'East', 'West']

CARD_MAP = {'E': 'East', 'W': 'West', 'N': 'North', 'S': 'South',
            'E.': 'East', 'W.': 'West', 'N.': 'North', 'S.': 'South'}

# UPDATE THIS VARIABLE
STREET_MAPPING = {"St": "Street",
                  "St.": "Street",
                  "ST": "Street",
                  "street": "Street",
                  "Ave": "Avenue",
                  "Ave.": "Avenue",
                  'avenue': 'Avenue',
                  'ave,': 'Avenue',
                  "Rd.": "Road",
                  "Rd": "Road",
                  'road': 'Road',
                  "Ave": "Avenue",
                  "Blvd": "Boulevard",
                  "By-pass": "Bypass",
                  "Dr": "Drive",
                  "Dr.": "Drive",
                  'Trl': 'Trail'
                  }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in CARDINALS:
            audit_street_type(street_types, street_name[
                              :-(len(street_type) + 1)])
        elif street_type in CARD_MAP.keys():
            audit_street_type(street_types, street_name[
                              :-len(street_type)] + CARD_MAP[street_type])
        elif street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    # osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    for event, elem in ET.iterparse(osmfile, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        elem.clear()
    return street_types


def parse_street_name(name):
    m = street_type_re.search(name)
    if m:
        ending = m.group()
        if ending in CARDINALS:
            return parse_street_name(name[:-(len(ending) + 1)]) + ' ' + ending
        elif ending in CARD_MAP:
            return parse_street_name(name[:-(len(ending) + 1)]) + ' ' + CARD_MAP[ending]
        elif ending in STREET_MAPPING:
            return name[:-(len(ending) + 1)] + ' ' + STREET_MAPPING[ending]
        else:
            return name


def test():
    st_types = audit(OSMFILE)
    ugly = {k: v for k, v in dict(st_types).items() if not k.isdigit()}
    pprint.pprint(ugly)
    # assert len(st_types) == 3

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = parse_street_name(name)
            print(name, "=>", better_name)


if __name__ == '__main__':
    test()
