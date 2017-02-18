#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow


def create_reduced_dataset(in_file, out_file="sample.osm", k=10):
    '''
    Take as input an OSM file, return back a sized-down version of the file
    taking only every kth top level element.

    Source: Udacity Data Analysis Nanodegree, Project 3, Project Details
    '''

    def get_element(in_file, tags=('node', 'way', 'relation')):
        """Yield element if it is the right type of tag

        Reference:
        http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
        """
        context = iter(ET.iterparse(in_file, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()

    with open(out_file, 'wb') as output:
        output.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            .encode(encoding='utf-8'))
        output.write('<osm>\n  '.encode(encoding='utf-8'))

        # Write every kth top level element
        for i, element in enumerate(get_element(in_file)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>'.encode(encoding='utf-8'))


if __name__ == '__main__':
    create_reduced_dataset('toronto_canada.osm', out_file="toronto-sample.osm", k=500)
