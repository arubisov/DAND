#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions to format opening hours into a consistent standard.

Schedule formatting inspired by:
http://stackoverflow.com/questions/5906984/combine-days-where-opening-hours-are-similar

LEFT TODO: Replace pm times with 24h, replace hyphens with spaces, remap names.
'''
import xml.etree.cElementTree as ET
import re
from pprint import pprint
from collections import defaultdict

test_data = ['24/7',
             'Minday-Friday : 08:00-19:00',
             'Mo-Fr 06:30-18:00; Sa-Su 10:00-16:00',
             'Mo-Fr 07:00-23:00',
             'Mo-Fr 08:00-18:00; Tu,Th 08:00-19:00; Sa 09:00-13:00',
             'Mo-Fr 6:30-19:00; Sa-Su 8:00-18:00',
             'Mo-Fr 7:45-17:00; Sa-Su off',
             'Mo-Fr 8:00-17:00',
             'Mo-Fr 9:00-19:00; Sa-Su off',
             'Mo-Sa 10:00-18:00; Su off',
             'Mo-Su 11:00-22:00',
             'Mo-Th 00:00-01:00,11:00-24:00; Fr-Su 00:00-02:00,11:00-24:00',
             'We-Mo 07:00-20:00, Tu 07:00-19:00, Fr 00:00-01:00',
             'We-Mo 07:00-20:00, Tu 7:00-19:00, Fr 00:00-3:00',
             'Thu-Sat - 6pm - 2am',
             'Tue-Thu 4pm – midnight | Fri-Sat 4pm – 2am']

days_week = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su', 'PubHolBuffer', 'PH']

days_map = {'Minday': 'Mo', 'Monday': 'Mo', 'Friday': 'Fr'}
# 'Mon': 'Mo', 'Tue': 'Tu', 'Wed': 'We', 'Thu': 'Th', 'Fri': 'Fr',
# 'Sat': 'Sa', 'Sun': 'Su'}


def clean_sched_string(input_str):
    output = input_str
    # if there are commas separating entries instead of semicolons:
    pattern = re.compile(r'[\d]+(, )[\w]+')
    iterator = pattern.finditer(output)
    for match in iterator:
        output = "{}; {}".format(output[:match.span()[0] + 2],
                                 output[match.span()[1] - 2:])

    # make sure all times have leading zero if before 10am
    pattern = re.compile(r'[ ,-]\d{1}:')
    iterator = pattern.finditer(output)
    i = 0
    for match in iterator:
        i = i + 1
        output = "{}0{}".format(output[:match.span()[0] + i],
                                output[match.span()[0] + i:])

    # any weird colons laying around?
    output = output.replace(" : ", " ")

    # pipes instead of semi-colons?
    output = output.replace(" | ", "; ")
    return output


def abbrev_days(input_str):
    pattern = re.compile(r'\b(' + '|'.join(days_map.keys()) + r')\b')
    result = pattern.sub(lambda x: days_map[x.group()], input_str)
    return result


def build_hours_dict(input_str):
    daily_schedule = {}

    if input_str == '24/7':
        for day in days_week[:7]:
            daily_schedule[day] = '00:00-24:00'

        return daily_schedule

    entries = input_str.split('; ')

    for entry in entries:
        days, hours = split_entry(entry)
        days = parse_days(days)

        if hours == 'off':
            continue

        for day in days:
            daily_schedule[day] = hours

    return daily_schedule


def split_entry(input_str):
    parts = re.split(r'^([\w,-]+) (.*)', input_str)
    if len(parts) == 4:
        return parts[1], parts[2]


def parse_days(input_str):
    list_days = []
    if ',' in input_str:
        parts = input_str.split(',')
    else:
        parts = [input_str]

    for part in parts:
        if '-' in part:
            dayrange = part.split('-')
            begin = days_week.index(dayrange[0])
            end = days_week.index(dayrange[1])
            if begin <= end:
                list_days = list_days + days_week[begin:end + 1]
            elif begin > end:
                list_days = list_days + \
                    days_week[begin:7] + days_week[:end + 1]

        else:
            list_days.append(part)

    return list_days


def format_days_list(input_list):
    if len(input_list) == 1:
        return input_list[0]

    num_list = [days_week.index(x) for x in input_list]
    diffs = [y - x for x, y in zip(num_list[0:-1], num_list[1:])]

    output = input_list[0]
    for day, diff, i in zip(input_list[1:], diffs, range(len(diffs))):
        if diff == 1:
            if i == len(diffs) - 1 or diffs[i + 1] != 1:
                output = output + '-' + day

        if diff > 1:
            output = output + ',' + day
    return output


def format_schedule(input_dict):
    groupby_hours = defaultdict(list)

    for key, value in sorted(input_dict.items()):
        groupby_hours[value].append(key)

    for k in groupby_hours:
        groupby_hours[k] = sorted(
            groupby_hours[k], key=lambda x: days_week.index(x))

        groupby_hours[k] = format_days_list(groupby_hours[k])

    sched_list = []
    for k, v in groupby_hours.items():
        sched_list.append('{} {}'.format(v, k))

    sched_list = sorted(sched_list, key=lambda x: days_week.index(x[:2]))

    return "; ".join(sched_list)


def parse_opening_hours(input_str):
    try:
        cleaned = clean_sched_string(input_str)
        abbrev = abbrev_days(cleaned)
        hours_dict = build_hours_dict(abbrev)
        sched = format_schedule(hours_dict)
        return sched
    except:
        return input_str


def show_unformattable_hours(file_in):
    bad_strings = []

    for _, element in ET.iterparse(file_in):

        if element.tag == "node" or element.tag == "way":
            for tag in element.findall('tag'):
                if tag.get('k') == 'opening_hours':
                    k = tag.get('k')
                    try:
                        # print("   ", tag.get('v'))
                        # print("-> ", parse_opening_hours(tag.get('v')))
                        parse_opening_hours(tag.get('v'))
                    except:
                        bad_strings.append(tag.get('v'))
    pprint(bad_strings)


if __name__ == '__main__':
    # for s in test_data:
    #     print(s)
    #     pprint(parse_opening_hours(s))

    file_in = 'financial_district.osm'
    show_unformattable_hours(file_in)
