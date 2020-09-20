import csv

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
