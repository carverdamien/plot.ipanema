#!/usr/bin/env python3
import sys
import pandas as pd

output = sys.argv[1]
csv = sys.argv[2:]

pd.concat([pd.read_csv(i) for i in csv]).to_csv(output)
