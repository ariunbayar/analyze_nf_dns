#!/bin/sh
dir=$(dirname "$(readlink -e $0)")


echo "Parsing nfcapd files to output JSON file ..."
for file in nfcapd.*; do
    nfdump -o extended -r $file | python3 "$dir/parse_nfdump.py" "$file"
done

echo "Merging parsed files ..."
python3 "$dir/merge_bandwidth_json.py" dst_
python3 "$dir/merge_bandwidth_json.py" src_
echo "Completed"
