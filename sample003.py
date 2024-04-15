#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import csv




def read_csv(csv_fpath_):
    """
    引数 file_ で指定される CSV ファイルを解析して，
    リストを返します．

    Parameter
    ---------
    csv_fpath_ : string
        CSV ファイルへのパス文字列．

    Return
    ------
    lines : list
        CSV から読み出したデータ (2 次元リスト) ．
    """

    read_data = []
    with open(csv_fpath_, encoding = 'utf-8', newline = '') as f_:
        csv_ = csv.reader(f_)
        read_data = [row_ for row_ in csv_]

    return read_data



def main():

    lines = read_csv('sample003.csv')

    i = 0
    for item in lines:
        val_ = input('HIT ENTER KEY TO NEXT..')
        if '#' == item[0]:
            print('[{}] comment: {}'.format(i, item[1]))
        else:
            print('[{}] position: ({}, {})'.format(i, item[0], item[1]))
        i += 1

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
