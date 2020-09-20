#!/usr/bin/env python3

import argparse
import csv
import pathlib

topdir = pathlib.Path(__file__).parent

def identity(x):
    return x

def csv_dict(p, conversions={}): # conversions is never modified
    with p.open() as f:
        r = csv.reader(f)
        headings = None
        for row in r:
            if headings is None:
                headings = row
            else:
                yield {k: conversions.get(k, identity)(v) for k, v in zip(headings, row)}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=pathlib.Path, default=(topdir / "data"))
    return parser.parse_args()

def main():
    args = parse_args()
    statedict = {}
    for d in csv_dict(args.data / "totals-2020-09-20T07_40_42.csv", {'receipts': float}):
        if d['party'] == "REP":
            continue
        entry = statedict.setdefault(d['state'], {'fec': None, '538': None})
        if entry['fec'] is None or entry['fec']['receipts'] < d['receipts']:
            entry['fec'] = d
    for d in csv_dict(args.data / "election-forecasts-2020" / "senate_state_toplines_2020.csv", {'winner_Dparty': float}):
        state = d['district'][:2]
        entry = statedict.setdefault(state, {'fec': None, '538': None})
        if entry['538'] is None:
            entry['538'] = d
    with open("/tmp/out.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(['state', 'receipts', 'winner_Dparty'])
        for k, v in statedict.items():
            if v['538'] is not None:
                w.writerow([k, v['fec']['receipts'], v['538']['winner_Dparty']])
                #print(f"{k} {v['fec']['receipts']:13.2f} {v['538']['winner_Dparty']:7.5f} {v['538']['mean_predicted_turnout']} {v['fec']['name']} ")

if __name__ == "__main__":
    main()