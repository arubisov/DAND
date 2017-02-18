#!/usr/bin/env python2
# -*- coding: utf-8 -*-

s = '{1.01787e+08|1.019e+08}'
print s[1:-1]
out = s[1:-1].split('|')
out1 = out[0]
out2 = out[1]
print out[0][::-1].find('.') - out[0][::-1].find('e') - 1
print out2[::-1].find('.') - out2[::-1].find('e') - 1
print float('1.01787e+08')
