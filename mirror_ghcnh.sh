#!/bin/bash
# downloads GHCNh parquet files for the given station IDs to the target directory
# relies on aria2 for downloading only files that have been modified

# arguments: target-dir GHCNh_ID1 GHCNh_ID2 ...
# target-dir: the directory to download the parquet files to (typically www/)
# GHCNh_IDs: the stations to download data for

# download the ghcnh inventory to know which years exist for which stations
#aria2c --conditional-get --dir=$1 "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh-inventory.txt"

# turns GHCNh_IDs into a regex matching any of them
REGEX=`echo "\\\\(""${@:2}""\\\\)" | sed 's/ /\\\\|/g'`

# download the parquet files
cat $1/ghcnh-inventory.txt |\
	grep $REGEX |\
   awk '{print "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/" $2 "/parquet/GHCNh_" $1 "_" $2 ".parquet"}' |\
   aria2c --conditional-get --continue --dir=$1 --input-file=-

# or to download the station CSV files, which are 10x larger but appear more reliable:
# cd $1
# BASE_URL="https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-station/"
# for GHCN_ID in "${@:2}"; do
#     curl -s $BASE_URL"/GHCNh_"$GHCN_ID"_por.psv" |\
#         ([ "$ITWW_FAST" = "1" ] && head -n 10000 || cat)  >\
#         $GHCN_ID.psv.tmp && mv $GHCN_ID.psv.tmp $GHCN_ID.psv
# done