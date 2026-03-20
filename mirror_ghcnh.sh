#!/bin/bash
# downloads GHCNh parquet files for the given station IDs to the target directory
# relies on aria2 for downloading only files that have been modified

# arguments: target-dir GHCNh_ID1 GHCNh_ID2 ...
# target-dir: the directory to download the parquet files to (typically www/)
# GHCNh_IDs: the stations to download data for

# download the ghcnh inventory to know which years exist for which stations
aria2c --conditional-get --continue --dir=$1 "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh-inventory.txt"

# if ITWW_LATEST is set, only download the latest 2 years of data for each station
if [[ "$ITWW_LATEST" == 1 ]]; then
   for station in "${@:2}"; do    
      grep "^$station" $1/ghcnh-inventory.txt | tail -2
   done |\
      awk '{print "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/" $2 "/parquet/GHCNh_" $1 "_" $2 ".parquet"}' |\
      aria2c --conditional-get --continue --dir=$1 --input-file=-

# otherwise, download all years of data for each station
else
   # turns GHCNh_IDs into a regex matching any of them
   REGEX=`echo "\\\\(""${@:2}""\\\\)" | sed 's/ /\\\\|/g'`

   cat $1/ghcnh-inventory.txt |\
      grep $REGEX |\
      awk '{print "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/" $2 "/parquet/GHCNh_" $1 "_" $2 ".parquet"}' |\
      aria2c --conditional-get --continue --dir=$1 --input-file=-
fi
