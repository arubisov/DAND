#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it,
clean it, come up with a data model, insert it into MongoDB and then run some
queries against your database. The set contains data about Arachnid class
animals.

Your task in this exercise is to parse the file, process only the fields that
are listed in the FIELDS dictionary as keys, and return a list of dictionaries
of cleaned values.

The following things should be done:
- the output structure should be as follows:

[ { 'label': 'Argiope',
    'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
    'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
    'name': 'Argiope',
    'synonym': ["One", "Two"],
    'classification': {
                      'family': 'Orb-weaver spider',
                      'class': 'Arachnid',
                      'phylum': 'Arthropod',
                      'order': 'Spider',
                      'kingdom': 'Animal',
                      'genus': None
                      }
  },
  { 'label': ... , }, ...
]

  * Note that the value associated with the classification key is a dictionary
    with taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re
import os
import sys

DATAFILE = './arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(os.path.join(sys.path[0], filename), "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            entry = dict()
            classification = dict()

            # - trim out redundant description in parenthesis from the 'rdf-schema#label'
            #   field, like "(spider)"
            line['rdf-schema#label'] = strip_parentheses(line['rdf-schema#label'])

            # - if 'name' is "NULL" or contains non-alphanumeric characters, set it to the
            #   same value as 'label'.
            if line['name'] == 'NULL' or not line['name'].isalnum():
                line['name'] = line['rdf-schema#label']

            class_fields = ['family_label', 'class_label', 'phylum_label', 'order_label', 'kingdom_label', 'genus_label']

            # - keys of the dictionary changed according to the mapping in FIELDS dictionary
            for field in list(set(process_fields) - set(class_fields)):
                # - if a value of a field is "NULL", convert it to None
                if line[field] == 'NULL':
                    entry[fields[field]] = None
                else:
                    # - strip leading and ending whitespace from all fields, if there is any
                    print field
                    entry[fields[field]] = line[field].strip()

            for field in class_fields:
                if line[field] == 'NULL':
                    classification[fields[field]] = None
                else:
                    # - strip leading and ending whitespace from all fields, if there is any
                    classification[fields[field]] = line[field].strip()

            # - if there is a value in 'synonym', it should be converted to an array (list)
            #   by stripping the "{}" characters and splitting the string on "|". Rest of the
            #   cleanup is up to you, e.g. removing "*" prefixes etc. If there is a singular
            #   synonym, the value should still be formatted in a list.
            if entry['synonym'] is not None:
                entry['synonym'] = parse_array(entry['synonym'])

            entry['classification'] = classification

            data.append(entry)
    pprint.pprint(data)
    print process_fields
    return data

def strip_parentheses(string):
    return re.sub(r'\([^)]*\)', '', string)

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()
