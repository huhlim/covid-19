import numpy as np
import datetime

START_DATE = datetime.datetime.strptime('2020-01-21', "%Y-%m-%d")
OUTPUT='./data'
HIGHLIGHT = ['Michigan', 'New York', 'New Jersey']

def time_delta(date):
    return np.array([x.days for x in date-START_DATE], dtype=int)

def smooth(date, data, smooth=3):
    ddays = time_delta(date)
    #
    out = []
    for x in ddays:
        n = data[np.abs(ddays-x) <= smooth]
        z = (n-np.mean(n))/np.maximum(0.1,np.std(n))
        n = n[np.abs(z)<2.]
        out.append(np.mean(n))
    return np.array(out)
