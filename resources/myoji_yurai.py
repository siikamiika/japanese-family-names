#!/usr/bin/env python3
import csv

class Names(object):

    def __init__(self, filename):
        self.filename = filename
        self.names = dict(
            (
                n[0],
                dict(
                    rank=i+1,
                    readings=n[1].split('|'),
                    people=int(n[2]),
                    nandokudo=float(n[3]),
                )
            )
            for i, n in enumerate(self._read_names())
        )

    def get(self, name):
        return self.names[name]

    def _read_names(self):
        with open(self.filename, newline='') as f:
            reader = csv.reader(f)
            return [tuple(row) for row in reader]
