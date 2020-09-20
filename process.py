#!/usr/bin/env python3

import argparse
import csv
import pathlib

topdir = pathlib.Path(__file__).parent

import matplotlib.pyplot as plt

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
    maxreceipts = 0
    for d in csv_dict(args.data / "totals-2020-09-20T07_40_42.csv", {'receipts': float}):
        maxreceipts = max(maxreceipts, d['receipts'])
        if d['party'] == "REP":
            continue
        entry = statedict.setdefault(d['state'], {'fec': None, '538': None})
        if entry['fec'] is None or entry['fec']['receipts'] < d['receipts']:
            entry['fec'] = d
    for d in csv_dict(args.data / "election-forecasts-2020" / "senate_state_toplines_2020.csv", {'winner_Dparty': float}):
        if d['expression'] != '_deluxe':
            continue
        state = d['district'][:2]
        entry = statedict.setdefault(state, {'fec': None, '538': None})
        if entry['538'] is None:
            entry['538'] = d
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.autoscale(False)
    ax.set_xbound([0, 1])
    ax.set_ybound([0, 1.1 * maxreceipts/1E6])
    ax.set_title("Senate seats, neglectedness and tractability")
    ax.set_xlabel("538 deluxe model probability of winning seat")
    ax.set_ylabel("FEC receipts by top non-GOP candidate")
    for k, v in statedict.items():
        if v['538'] is not None:
            ax.text(v['538']['winner_Dparty'], v['fec']['receipts']/1E6, k,
                ha="center", va="center")
    plt.show()

if __name__ == "__main__":
    main()