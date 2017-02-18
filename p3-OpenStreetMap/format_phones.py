#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions to properly format a phone number to the international standard.
Adapted from https://www.quora.com/What-is-the-best-way-to-parse-and-standardize-phone-numbers-in-Python/answer/Stuart-Woodward?srid=1FEf
'''

import re
testData = [
    "",
    "garbage",
    "garbage1231moregarbage",
    "0120-24-3343",
    "046-824-3721",
    "0468243721",
    "+1-222-333-4444",
    "(222) 333-4444",
    "222.333.4444",
    "1-222-333-4444",
    "222.333.4444 ex55",
    "222.333.4444 ex55",
    "222.333.4444 ex.55",
    "222.333.4444 ex.  55",
    "222.333.4444 extension 55",
    "222.333.4444 extension. 55",
    "222.333.4444 x55",
    "222.333.4444 x 55",
    "222.333.4444 x.55",
    "222.333.4444ex.55",
    "222.333.4444ex55",
    "222.333.4444ex 55",
    "222.333.4444ex. 55",
    "222.333.4444extension 55",
    "222.333.4444extension. 55",
    "222.333.4444x55",
    "222.333.4444x 55",
    "222.333.4444x.55"
]
# Match Country Code


def match_phone_number(telephoneNo, defaultCountryCode="1"):
    # match phones starting with +, and split by + sign followed by repetitions
    # of digits
    parts = re.split(r'^\+(\d+)', telephoneNo)
    if len(parts) > 1:
        return parts[1], parts[2]
    # special case where there is a single 1, split on 1 followed by nondigit
    # followed by everything else
    parts = re.split(r'^(1)(\D.*)', telephoneNo)
    if len(parts) > 1:
        return parts[1], parts[2]
    else:
        # could return a default country code here
        return defaultCountryCode, telephoneNo


def match_extension(telephoneNo):
    # match and number following a word at the end of a string
    matched = re.match(r'([^a-zA-Z]+)([a-zA-Z]+\D*)(\d+)', telephoneNo)
    if matched:
        parts = matched.groups()
        if len(parts) > 1:
            return parts[2], parts[0]
    return "", telephoneNo


def parse_numbers(telephoneNo):
    # find all repetitions of digits
    parts = re.findall(r'(\d+)', telephoneNo)
    return parts


def split_number_by_parts(telephoneNo):
    countryCode = ""
    areaCode = ""
    phoneNumber = ""
    extension = ""
    countryCode, phoneNumber = match_phone_number(telephoneNo)
    extension, phoneNumber = match_extension(phoneNumber)
    numbers = parse_numbers(phoneNumber)
    numberOfParts = len(numbers)
    if numberOfParts > 1:
        areaCode = numbers[0]
        phoneNumber = " ".join(numbers[1:])
    elif numberOfParts == 1 and len(numbers[0]) == 10:
        areaCode = "{}".format(numbers[0][0:3])
        phoneNumber = "{} {}".format(numbers[0][3:6], numbers[0][6:])
    else:
        phoneNumber = " ".join(numbers)
    return countryCode, areaCode, phoneNumber, extension


def parse_phone_number(phone):
    cntry, area, phone_num, ext = split_number_by_parts(phone)
    if ext:
        return "+{} {} {} Ext. {}".format(cntry, area, phone_num, ext)
    else:
        return "+{} {} {}".format(cntry, area, phone_num)


if __name__ == '__main__':
    for telephoneNo in testData:
        print(telephoneNo)
        countryCode, areaCode, phoneNumber, extension = split_number_by_parts(
            telephoneNo)
        print("Country Code:", countryCode)
        print("Area Code", areaCode)
        print("Phone Number", phoneNumber)
        print("Extension", extension)
        print(" ")
