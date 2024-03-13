#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import csv



def main():

    positions_ = []

    fname_ = 'sample003.csv'
    with open(fname_, encoding = 'utf-8', newline = '') as f_:
        csv_ = csv.reader(f_)
        positions_ = [row_ for row_ in csv_]

    for item_ in positions_:
        if '#' == item_[0]:
            print('comment: {}'.format(item_[1]))
        else:
            print('position: ({}, {})'.format(item_[0], item_[1]))

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
