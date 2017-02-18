#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from pprint import pprint
import re
import codecs
import json

from audit_streetnames import *
from format_hours import *
from format_phones import *
"""
Output looks like:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):

    if element.tag == "node" or element.tag == "way":

        node = {k: v for k, v in element.attrib.items()
                if k not in CREATED + ['lat', 'lon']}
        node['type'] = element.tag

        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.get('lat')),
                           float(element.get('lon'))]

        created = {k: v for k, v in element.attrib.items() if k in CREATED}
        node['created'] = created

        for tag in element.findall('tag'):
            k = tag.get('k')
            if problemchars.search(k):
                continue

            if lower.match(k):
                node[k] = parse_tag(k, tag.get('v'))

            if lower_colon.match(k):
                colonkey = k.split(':')
                prefix = colonkey[0]
                suffix = colonkey[1]
                if prefix == 'addr':
                    prefix = 'address'
                if prefix not in node:
                    node[prefix] = {}
                try:
                    node[prefix][suffix] = parse_tag(suffix, tag.get('v'))
                except:
                    node[prefix + '_' + suffix] = tag.get('v')

        # Way-specific.
        if element.tag == 'way':
            for tag in element.findall('nd'):
                if 'node_refs' not in node:
                    node['node_refs'] = []
                node['node_refs'].append(tag.get('ref'))

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in, events=("start",)):
            el = shape_element(element)
            if el:
                # data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
            element.clear()
    return data


def parse_tag(key, val):
    if key == 'city':
        try:
            city = re.search(r'^city of ([\w. ]+)',
                             val, re.IGNORECASE).group(1)
            return city
        except:
            return val
    elif key == 'street':
        return parse_street_name(val)
    elif key == 'province':
        return 'ON'
    elif key == 'country':
        return 'CA'
    elif key == 'phone':
        return parse_phone_number(val)
    elif key == 'opening_hours':
        return parse_opening_hours(val)
    else:
        return val


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('toronto_canada.osm', False)
    #data_mini = [
    #    x for x in data if 'address' in x or 'phone' in x or 'opening_hours' in x]
    #pprint(data_mini)


if __name__ == "__main__":
    test()
