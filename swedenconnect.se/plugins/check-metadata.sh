#!/bin/bash

crt=$1; shift

declare -a on_exit_items

function on_exit()
{
    for i in "${on_exit_items[@]}"
    do
        eval $i
    done
}

function add_on_exit()
{
    local n=${#on_exit_items[*]}
    on_exit_items[$n]="$*"
    if [[ $n -eq 0 ]]; then
        trap on_exit EXIT
    fi
}

for url in $*; do
   tmp=`mktemp`; add_on_exit rm -f $tmp
   samlsign -v -u $url -c $crt >$tmp 2>&1
   if [ $? -ne 0 ]; then
      echo "CRITICAL - failed to verify metadata $url using $crt [`paste -s -d"," $tmp`]"
      exit 2
   fi
done
echo "OK - all metadata validated ok"
exit 0
