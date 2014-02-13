import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    with open("armodel.data") as fp:
        df = pd.read_table(fp)
        df.plot()
