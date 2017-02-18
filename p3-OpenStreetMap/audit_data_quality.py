#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def audit_key_types(file_in):

    data = {}

    for _, element in ET.iterparse(file_in):

        if element.tag == "node" or element.tag == "way":
            for tag in element.findall('tag'):
                k = tag.get('k')

                if k not in data:
                    data[k] = {'count': 1, 'vals': set([tag.get('v')])}
                else:
                    data[k]['count'] += 1
                    data[k]['vals'].add(tag.get('v'))
    return data


def display_address_counts(data):
    addresses = {k: v for k, v in data.items() if k[0:4] == 'addr'}
    addr_counts = {}
    for k, v in addresses.items():
        addr_counts[k] = v['count']
    pprint.pprint(addr_counts)


def test():
    data = audit_key_types('toronto-sample.osm')
    pprint.pprint(data)
    print(len(list(data.keys())), "unique tag keys.")


if __name__ == "__main__":
    test()
