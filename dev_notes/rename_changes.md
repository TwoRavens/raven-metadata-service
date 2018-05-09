

# Metadata/Preprocess file

### Self section

- `preprocess_id` -> `preprocessId`

### Dataset

- `data_source` -> `dataSource`

- `row_cnt` -> `rowCnt`

- `variable_count` -> `variableCount`

## Variables section

- `varnameSumStat` -> `variableName`

- `invalid` -> `invalidCount`

- `valid` -> `validCount`

- `uniques` -> `uniqueCount`

- `freqmode` -> `modeFreq`

- `fewest` -> `fewestValues`

- `freqfewest` -> `fewestFreq`

- `mid` -> `midpoint`

- `freqmid` -> `midpointFreq`

- `sd` -> `stdDev`

- `herfindahl` -> `herfindahlIndex`

- `plotvalues` -> `plotValues`

- `plottype` -> `plotType`

- `plotx` -> `plotX`

- `ploty` -> `plotY`

- `cdfplottype` -> `cdfPlotType`

- `cdfplotx` -> `cdfPlotX`

- `cdfploty` -> `cdfPlotY`


## Variable display section

- `variable_display` -> `variableDisplay`


# Retrieve Rows Request (peek)

- `preprocess_id` -> `preprocessId`
- `start_row` -> `startRow`
- `number_rows` -> `numberRows`

- Example of a request:
  - Note: Only `preprocessId` is required.  All other fields are optional

    ```json
    {
        "preprocessId": 5,
        "startRow": 1,
        "numberRows": 100,
        "format":"json"
    }
    ```

# Variable Update Requests

- `preprocess_id` -> `preprocessId`

- `variable_updates` -> `variableUpdates`

- `valueUpdates` -> `valueUpdates`

- `labl` -> `label`

- Example of an update call:

    ```json
    {
       "preprocessId":5,
       "variableUpdates":{
          "ccode":{
             "viewable":true,
             "omit":[
                "time"
             ],
             "valueUpdates":{
                "label":"Code Book"
             }
          }
       }
    }
    ```
