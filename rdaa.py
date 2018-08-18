#!/usr/bin/env python
#================================================================
# rdaa: Convert right ascension/declination to azimuth/altitude
#   For documentation, see:
#     ims/
#----------------------------------------------------------------

# - - - - -   I m p o r t s

from __future__ import print_function
import sys
import re
import sidereal

# - - - - -   M a n i f e s t   c o n s t a n t s

SIGN_PAT = re.compile(r'[\-+]')

# - - - - -   m a i n

def main():
    """Main program for rdaa.
    """

    #-- 1 --
    # [ if sys.argv contains a valid set of command line
    #   arguments ->
    #     raDec  :=  the right ascension and declination as
    #                a sidereal.RADec instance
    #     latLon  :=  the observer's location as a
    #                 sidereal.LatLon instance
    #     dt  :=  the observer's date and time as a
    #             datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    raDec, latLon, dt = checkArgs()
    #-- 2 --
    # [ if dt has no time zone information ->
    #     utc  :=  dt
    #   else ->
    #     utc  :=  the UTC equivalent to dt ]
    if ((dt.tzinfo is None) or
        (dt.utcoffset() is None)):
        utc = dt
    else:
        utc = dt - dt.utcoffset()
    #-- 3 --
    # [ sys.stdout  +:=  local sidereal time for dt and latLon ]
    gst = sidereal.SiderealTime.fromDatetime(utc)
    lst = gst.lst(latLon.lon)
    print("Equatorial coordinates: {0}".format(raDec))
    print("Observer's location: {0}".format(latLon))
    print("Observer's time: {0}".format(dt))
    print("Local sidereal time is {0}".format(lst))
    #-- 4 --
    # [ h  :=  hour angle for raDec at time (utc) and longitude
    #          (latLon.lon) ]
    h = raDec.hourAngle(utc, latLon.lon)

    #-- 5 --
    # [ aa  :=  horizon coordinates of raDec at hour angle h
    #           as a sidereal.AltAz instance ]
    aa = raDec.altAz(h, latLon.lat)

    #-- 6 --
    print("Horizon coordinates: {0}".format(aa))

# - - -   c h e c k A r g s

def checkArgs():
    """Process all command line arguments.

      [ if sys.argv[1:] is a valid set of command line arguments ->
          return (raDec, latLon, dt) where raDec is a set of
          celestial coordinates as a sidereal.RADec instance,
          latLon is position as a sidereal.LatLon instance, and
          dt is a datetime.datetime instance
        else ->
          sys.stderr  +:=  error message
          stop execution ]
    """
    #-- 1 --
    # [ if sys.argv[1:] has exactly four elements ->
    #     rawRADec, rawLat, rawLon, rawDT  :=  those elements
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    argList = sys.argv[1:]
    if  len(argList) != 4:
        usage ("Incorrect command line argument count.")
    else:
        rawRADec, rawLat, rawLon, rawDT = argList
    #-- 2 --
    # [ if rawRADec is a valid set of equatorial coordinates ->
    #     raDec  :=  those coordinates as a sidereal.RADec instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    raDec = checkRADec(rawRADec)

    #-- 3 --
    # [ if rawLat is a valid latitude ->
    #     lat  :=  that latitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lat = sidereal.parseLat(rawLat)
    except SyntaxError, detail:
        usage("Invalid latitude: {0}".format(detail))

    #-- 4 --
    # [ if rawLon is a valid longitude ->
    #     lon  :=  that longitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lon = sidereal.parseLon(rawLon)
    except SyntaxError, detail:
        usage("Invalid longitude: {0}".format(detail))

    #-- 5 --
    # [ if rawDT is a valid date-time string ->
    #     dt  :=  that date-time as a datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        dt = sidereal.parseDatetime(rawDT)
    except SyntaxError, detail:
        usage("Invalid timestamp: {0}".format(detail))

    #-- 6 --
    latLon = sidereal.LatLon(lat, lon)
    return  (raDec, latLon, dt)

# - - -   u s a g e

def usage(*L):
    """Print a usage message and stop.

      [ L is a list of strings ->
          sys.stderr  +:=  (usage message) + (elements of L,
                           concatenated)
          stop execution ]
    """
    print("*** Usage:", file=sys.stderr)
    print("***   rdaa RA+dec lat lon datetime", file=sys.stderr)
    print("*** Or:", file=sys.stderr)
    print("***   rdaa RA-dec lat lon datetime", file=sys.stderr)
    print("*** Error: {0}".format("".join(L)), file=sys.stderr)
    raise SystemExit

# - - -   c h e c k R A D e c

def checkRADec(rawRADec):
    """Check and convert a pair of equatorial coordinates.

      [ rawRADec is a string ->
          if rawRADec is a valid set of equatorial coordinates ->
            return those coordinates as a sidereal.RADec instance
          else ->
            sys.stderr  +:=  error message
            stop execution ]
    """
    #-- 1 --
    # [ if rawRADec contains either a '+' or a '-' ->
    #     m  :=  a re.match instance describing the first matching
    #            character
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    m = SIGN_PAT.search(rawRADec)
    if  m is None:
        usage("Equatorial coordinates must be separated by "
                "'+' or '-'.")
    #-- 2 --
    # [ rawRA  :=  rawRADec up to the match described by m
    #   sign  :=  characters matched by m
    #   rawDec  :=  rawRADec past the match described by m ]
    rawRA = rawRADec[:m.start()]
    sign = m.group()
    rawDec = rawRADec[m.end():]
    #-- 3 --
    # [ if rawRA is a valid hours expression ->
    #     ra  :=  rawRA as radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        raHours = sidereal.parseHours(rawRA)
        ra = sidereal.hoursToRadians(raHours)
    except SyntaxError, detail:
        usage("Right ascension '{0}' should have the form "
                "'NNh[NNm[NN.NNNs]]'.".format(rawRA))
    #-- 4 --
    # [ if rawDec is a valid angle expression ->
    #     absDec  :=  that angle in radians
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        absDec = sidereal.parseAngle(rawDec)
    except SyntaxError, detail:
        usage("Right ascension '{0}' should have the form "
                "'NNd[NNm[NN.NNNs]]'.".format(rawDec))
    #-- 5 --
    if  sign == '-':   dec = - absDec
    else:              dec = absDec

    #-- 6 --
    return sidereal.RADec(ra, dec)

# - - - - -   E p i l o g u e

if  __name__ == "__main__":
    main()
