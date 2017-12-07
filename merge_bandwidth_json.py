import json
import os
import sys


files = os.listdir('.')

nvd3_data = {}

timestamps = []

prefix = sys.argv[1]

for filename in sorted(files):
    if not filename.endswith('.json'):
        continue
    if not filename.startswith(prefix):
        continue

    timestamp_js = int(filename[len(prefix):].split('.')[0]) * 1000
    timestamps.append(timestamp_js)

    with open(filename) as f:
        data = json.load(f)

    for ip, speed in data.items():
        nvd3_data[ip] = nvd3_data.get(ip, {})
        nvd3_data[ip][timestamp_js] = speed

data_js = []
for ip, values in nvd3_data.items():
    v = []
    data_js.append({
        'key': ip,
        'values': v,
        })
    n = 0
    num_min = 5
    last_value = 0
    for timestamp_js in timestamps:
        n = n % num_min + 1
        if n == 1:
            max_value = 0
        # if int((timestamp_js - timestamps[0]) / 1000 / 60) > 20:
            # continue

        max_value = max(max_value, values.get(timestamp_js, 0))

        if n == num_min or timestamp_js == timestamps[-1]:
            # v.append({'x': timestamp_js, 'y': max_value})
            v.append([timestamp_js - 60000, last_value])
            v.append([timestamp_js, max_value])
            last_value = max_value


cur_dir = os.path.dirname(os.path.realpath(__file__))
with open(cur_dir + '/' + prefix + 'data.js', 'w') as f:
    f.write('var data=')
    json.dump(data_js, f, indent=4, sort_keys=True)
