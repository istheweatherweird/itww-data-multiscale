#!/usr/bin/bash
# args: www_dir station_id
GZ_FILES=`ls $1/*/$2*.gz`

echo 'date,source,temp,temp_quality'
for file in $GZ_FILES
do
    filename=`basename $file`
    zcat $file | cut --output-delimiter=, -c 16-27,28,88-92,93
done
