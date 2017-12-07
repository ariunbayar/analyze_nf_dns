from datetime import datetime
import json
import re
import sys


filename = sys.argv[1]
v = filename.split('.')[1]
date = datetime(int(v[0:4]), int(v[4:6]), int(v[6:8]), int(v[8:10]), int(v[10:12]), 0)
timestamp = int(date.timestamp())


# nfdump -o extended -r netmon/nfcapd.201711031411 | python3 parse_nfdump.py

re_traffic = re.compile(
        r'^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'
        r' +'
        r'(?P<duration>[^ ]+)'
        r' +'
        r'(?P<protocol>[^ ]+)'
        r' +'
        r'(?P<source_ip>[^:]+)'
        r':'
        r'(?P<source_port>[^ ]+)'
        r' +-> +'
        r'(?P<destination_ip>[^:]+)'
        r':'
        r'(?P<destination_port>[^ ]+)'
        r' +'
        r'(?P<flags>[^ ]+)'
        r' +'
        r'(?P<tos>[^ ]+)'
        r' +'
        r'(?P<packets>[^ ]+)'
        r' +'
        r'(?P<bytes>[^ ]+)'
        r' +'
        r'(?P<pps>[^ ]+)'
        r' +'
        r'(?P<bps>[^ ]+)'
        r' +'
        r'(?P<bpp>[^ ]+)'
        r' +'
        r'(?P<flows>[^ ]+)'
        r'$'
        )

bandwidth_dst = dict()
bandwidth_src = dict()

for line in sys.stdin:
    match = re_traffic.match(line)
    if not match:
        # print(line)
        continue

    dst_ip = match.group('destination_ip')
    src_ip = match.group('source_ip')

    if src_ip.startswith('10.10.'):
        continue
    if not dst_ip.startswith('10.10.'):
        continue

    mbps = int(match.group('bps')) / 1000000.0

    # stats by destination
    if dst_ip not in bandwidth_dst:
        bandwidth_dst[dst_ip] = mbps
    else:
        bandwidth_dst[dst_ip] += mbps

    # stats by source
    if mbps > 0.5:
        if src_ip not in bandwidth_src:
            bandwidth_src[src_ip] = mbps
        else:
            bandwidth_src[src_ip] += mbps



with open('dst_%s.json' % timestamp, 'w') as f:
    json.dump(bandwidth_dst, f, indent=4, sort_keys=True)

with open('src_%s.json' % timestamp, 'w') as f:
    json.dump(bandwidth_src, f, indent=4, sort_keys=True)
