#!/usr/bin/env python
#================================================================
# conjd:  Convert Julian date to date and time
#   For documentation, see:
#     ims/
#----------------------------------------------------------------

# - - - - -   I m p o r t s

from __future__ import print_function
import sys
import sidereal

# - - -   m a i n

def main():
    """conjd main program.
    """

    #-- 1 --
    # [ if  sys.argv[1:] is a single float ->
    #     j  :=  that float
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    argList = sys.argv[1:]
    if  len(argList) != 1:
        usage("Wrong argument count.")
    else:
        try:
            j = float(argList[0])
        except ValueError, detail:
            usage("Invalid argument: {0}".format(detail))
    #-- 2 --
    # [ jd  :=  a JulianDate instance for Julian date j ]
    jd = sidereal.JulianDate(j)

    #-- 3 --
    # [ dt  :=  jd as a datetime.datetime instance ]
    dt = jd.datetime()

    #-- 4 --
    # [ sys.stdout  +:=  dt in ISO form ]
    print(str(dt))

# - - -   u s a g e

def usage(*L):
    """Write a usage message and stop.

      [ L is a list of strings ->
          sys.stderr  +:=  (usage message) + (joined elements of L)
          stop execution ]
    """
    print("*** Usage:", file=sys.stderr)
    print("***   conjd NNNNNNN.NN...", file=sys.stderr)
    print("*** where NNNNNNN.NN is the Julian date.", file=sys.stderr)
    print("*** Error: {0}".format("".join(L)), file=sys.stderr)
    raise SystemExit

# - - - - -   E p i l o g u e

if __name__ == "__main__":
    main()
