To run preprocess locally:

```R
setwd('[path to]/raven-metadata-service/preprocess/input')
source('preprocess.R')
preprocess(filename='[path to]data/fearonLaitin.csv')
```

- Notes on NA

```
import pandas as pd
import numpy as np
df = pd.DataFrame([[np.nan, 2, np.nan, 0],
                  [3, 4, np.nan, 1],
                  [np.nan, np.nan, np.nan, 5]],
                  columns=list('ABCD'))
```
