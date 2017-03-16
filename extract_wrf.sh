#!/bin/bash

# Test script to extract basic forecast variables from grib2
# model output for particular location using GrADS

YYYY=$1
MM=$2
DD=$3
HH=$4

INIT="$YYYY-$MM-$DD $HH:00:00Z"

locname=Maksimir
lat=45.822
lon=16.034

if [ "$HH" == "06" ] ; then
  start=16
  end=39
TOMORROW0=`date --date="$INIT + 18 hours"`
fi
if [ "$HH" == "18" ] ; then
  start=4
  end=27
TOMORROW0=`date --date="$INIT + 6 hours"`
fi

UNIX0=`date -d "$TOMORROW0" +"%s"`
UNIX=UNIX0

start=$((start+1))
end=$((end+1))

mkdir -p marwec/data/input/tmp
cd marwec/data/input/tmp

ctlfile=marwec/data/input/wrf_d02.grib2.ctl
vars="tmp2m u10m v10m dswrad dlwrad uswrad ulwrad rh2m"
for var in $vars ; do
cat > plotgrads << EOF
'reinit'
'open $ctlfile'
'set lat $lat'
'set lon $lon'
'set t $start $end'
'set gxout print'
'set undef 0'
'set prnopts %0.1f 1 1'
'define tmp2m=(TMP2m)'
'define u10m=UGRD10m'
'define v10m=VGRD10m'
'define dswrad=DSWRFsfc'
'define dlwrad=DLWRFsfc'
'define uswrad=USWRFsfc'
'define ulwrad=ULWRFsfc'
'define rh2m=RH2m'
'd $var'
dummy=write('marwec/data/input/tmp/$var',result)
'quit'
EOF
grads -bpc "run plotgrads"
done

for var in $vars ; do
    sed '1d' $var > $var.tmp
    mv $var.tmp $var
done

UNIX=$((UNIX - 3600))
for i in {1..24} ; do
    UNIX=$((UNIX + 3600))
    echo $UNIX >> UNIX.list
done


paste UNIX.list tmp2m u10m v10m dswrad dlwrad uswrad ulwrad rh2m | awk 'BEGIN {print"timestamp\ttmp2m\tu10m\tv10m\tdswrad\tdlwrad\tuswrad\tulwrad\trh2m";}
            {print $1,"\t",$2,"\t",$3,"\t",$4,"\t",$5,"\t",$6,"\t",$7,"\t",$8,"\t",$9;}
            END{}' > $locname.list

rm tmp2m u10m v10m dswrad dlwrad uswrad ulwrad rh2m

# delete first line, not needed anymore after first run:
files=*.list
for file in $files ; do
    sed '1d' $file > $file.tmp
    mv $file.tmp $file
done

# delete last line:
files=*.list
for file in $files ; do
    sed '$d' $file > $file.tmp
    mv $file.tmp $file
done

cat $locname.list >> marwec/data/input/$locname.wrf.csv

# Append contents of file into joined data file on server:
cat marwec/data/input/$locname.wrf.csv | ssh -p 22222 maps@gamma.meteoadriatic.net 'cat >> /usr/local/nginx/html/meteoadriatic/irb/arw/learn/Maksimir.wrf.csv'

cd $locname.list marwec/data/input
rm .rf tmp

