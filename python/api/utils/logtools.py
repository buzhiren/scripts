#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging



def Log(loginfo):
    logging.basicConfig(level=logging.DEBUG,
              format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
              datefmt='%m-%d %H:%M',
              filename='../../logs/dvdcmdb.log',
              filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info(loginfo)