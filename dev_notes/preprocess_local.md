To run preprocess locally:

```R
setwd('[path to]/raven-metadata-service/preprocess/input')
source('preprocess.R')
preprocess(filename='[path to]data/fearonLaitin.csv')
```

Dframe

```
import pandas as pd
import numpy as np

s = pd.Series([1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, np.nan, 5, 5, 5])
s.dropna(inplace=True)

hhi_elements = []
for val, cnt in s.value_counts(normalize=True).items():
    print(val, '%d%%' % (cnt*100))
    hhi_elements.append(cnt**2) # square the "share"

print(sum(hhi_elements))
```
