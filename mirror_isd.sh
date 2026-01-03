#!/bin/bash
# arguments: target-dir USAF-WBAN1 USAF-WBAN2 ...

if [[ "$ISD_LATEST" == 1 ]]; then
    #YEAR=$(date -u +"%Y")
    # get most recent year of data on ftp (don't assume that 2026 data is available on 1/1/2026!)
    YEAR=$(lftp ftp://ftp.ncdc.noaa.gov/pub/data/noaa -e "cls -1; bye" | grep "^[0-9]\\+/" | sort | tail -1 | sed 's/\///')
    REGEX="("`python3 -c "import sys; print(str.join('|', sys.argv[2:]))" $@`")"
    echo $REGEX
    for i in $(seq $((YEAR-2)) $YEAR); do
        lftp -e "mirror --recursion=newer --parallel=4 --only-newer -i '$REGEX' . $1/$i; quit" "ftp.ncdc.noaa.gov/pub/data/noaa/"$i
    done
else 
    if [[ "$ISD_QUICK" == 1 ]]; then
        echo "Quick!"
        # for quick build only use the first station and 2020s
        REGEX="^[0-9]+/("`python3 -c "import sys; print(str.join('|', sys.argv[2:]))" $@`")"
        EXCLUDE="^([^2]|2[^0]|20[^2])"
    else
        REGEX="^[0-9]+/("`python3 -c "import sys; print(str.join('|', sys.argv[2:]))" $@`")"
        EXCLUDE="^[a-zA-Z]" # ignore the non data files
    fi

    echo $REGEX
    echo $EXCLUDE

    # create regex by joining USAF-WBAN arguments using pipe
    lftp -e "mirror --recursion=newer --parallel=4 --only-newer -i '$REGEX' -x '$EXCLUDE' . $1; quit" "ftp.ncdc.noaa.gov/pub/data/noaa/"
fi
