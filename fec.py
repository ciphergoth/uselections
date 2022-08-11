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

import itertools

def fetch(ctx, url, params):
    for page in itertools.count(start=1):
        rp = params.copy()
        rp['api_key'] = ctx.config['fec']['api_key']
        rp['per_page'] = "100"
        rp['page'] = str(page)
        r = ctx.session.get(url, params=rp)
        r.raise_for_status()
        d = r.json()
        #with open(f"/tmp/fec_{page:03}.json", "w") as f:
        #    json.dump(d, f, indent=4)
        yield from d['results']
        if page >= d['pagination']['pages']:
            break

def totals(ctx):
    yield from fetch(ctx, "https://api.open.fec.gov/v1/candidates/totals/", {
        'has_raised_funds': 'true',
        'office': 'S',
        'is_active_candidate': 'true',
        'election_full': 'true',
        'election_year': '2022',
        'sort': 'candidate_id',
    })

def main():
    import json
    import context

    ctx = context.get()
    t = list(totals(ctx))
    t.sort(key=lambda c: c["receipts"], reverse=True)
    print(json.dumps(t, indent=4))

if __name__ == "__main__":
    main()
