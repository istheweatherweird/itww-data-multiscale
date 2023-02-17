#!/bin/sh
# arguments: target-dir USAF-WBAN1 USAF-WBAN2 ...

# create regex by joining USAF-WBAN arguments using pipe
REGEX=`python -c "import sys; print(str.join('|', sys.argv[2:]))" $@`
lftp -e "mirror --recursion=newer --parallel=4 --only-newer -i '^[0-9]+/($REGEX)' -x '^[a-zA-Z]' . $1; quit" ftp.ncdc.noaa.gov/pub/data/noaa/
