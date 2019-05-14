#!/bin/bash

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

uri=$1
tmp=`mktemp`
add_on_exit rm -f $tmp

wget --no-check-certificate -qO$tmp $uri
nfailed=$(jq '.["last execution result"]["failed"] | length' $tmp)
npassed=$(jq '.["last execution result"]["passed"] | length' $tmp)
passed=$(jq -r '.["last execution result"]["passed"][]."result"' $tmp | tr '\n' ' ')
failed=$(jq -r '.["last execution result"]["failed"][]."result"' $tmp | tr '\n' ' ')
target=$(jq -r '.["last execution result"]["target"]' $tmp)
if [ $nfailed -eq 0 ]; then
   echo "OK - $npassed tests successful in $target"
   exit 0
else
   reason=$(jq -r '.["last execution result"]["reason"][]' $tmp )
   if [ "x$reason" = "x" ]; then
      reason="unknown"
   fi
   echo "CRITICAL - $failed FAILED in $target (reason: \"$reason\") ($passed still ok)"
   exit 2
fi
