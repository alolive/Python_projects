#!/usr/bin/python

MyJson = {}

import grp_feeder as fct

def main ():

  # Feed with bullshit
  MyJson['stuff1'] = "bullshit"

  print 'Before feeidng'
  print MyJson

  fct.MyFeeder( MyJson )

  print 'After feeidng'
  print MyJson


if __name__ == '__main__':
    main()

