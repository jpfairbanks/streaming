import matplotlib.pyplot as plt
import pandas as pd
import sys

for filename in sys.argv[1:]:
    df = pd.read_table(filename)
    df.plot()
