#   Copyright 2020 Google LLC

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       https://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import codecs
import csv

def senate_toplines_deluxe(ctx):
    url = "https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv"
    with ctx.session.get(url, stream=True) as r:
        r.raise_for_status()
        done = set()
        for d in csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8')):
            if d['expression'] != '_deluxe':
                continue
            district = d['district']
            if district in done:
                continue
            done.add(district)
            yield d

def main():
    import json
    import context

    ctx = context.get()
    t = list(senate_toplines_deluxe(ctx))
    print(json.dumps(t, indent=4))

if __name__ == "__main__":
    main()
