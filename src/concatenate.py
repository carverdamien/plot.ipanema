#!/usr/bin/env python3
import sys
import pandas as pd

output = sys.argv[1]
csv = sys.argv[2:]

pd.concat([df for df in [pd.read_csv(i) for i in csv] if len(df) > 0]).to_csv(output)
