# API Endpoints for Profiling

There are two sets of endpoints which work with similar API calls. One endpoint runs a profiling program written in python, the other in R.  They are similar and will be congruent in the near future.

Note, the system has a queuing service to handle multiple requests.  Therefore, the response from the API endpoints includes a callback url which is used to retrieve the actual data.

## R Preprocess

1. Send the file for preprocessing
    ```
    # Local
    curl  -X POST -i -F source_file=@/path/to/datafile/fearonLaitin.csv http://127.0.0.1:8080/r-preprocess/api-run-in-queue    

    # Service
    curl  -X POST -i -F source_file=@/path/to/datafile/fearonLaitin.csv http://metadata.2ravens.org/r-preprocess/api-run-in-queue    
    ```
2. Use the callback url returned in the JSON response.  Sample response:
    ```
    {
      "success":true,
      "message":"In progress",
      "callback_url":"http://127.0.0.1:8080/preprocess/job-info-json/179",
      "data":{
        "id":179,
        "state":"RECEIVED",
        "is_success":false,
        (etc)
      }
    }
    ```
3.  Check the value of the `data.state` which may have the following values:
    ```
    "RECEIVED" - The data profiling is in process

    "FAILURE" - The profiling failed

    "SUCCESS" - There will be a `data.summary_metadata` attribute containing the summary statistics
    ```
4. If the `data.state` is "RECEIVED", try the callback_url periodically until the state is either "FAILURE" or "SUCCESS":
    ```
    # Try the callback url
    # Example:
    curl http://127.0.0.1:8080/preprocess/job-info-json/179
    ```

## Python Preprocess

For the python preprocessing, the steps are similar to R (above).  The first step has a different url but steps 2 through 4 are the same

1. Send the file for preprocessing
    ```
    # Local
    curl  -X POST -i -F source_file=@/path/to/datafile/fearonLaitin.csv http://127.0.0.1:8080/preprocess/api/process-single-file

    # Service
    curl  -X POST -i -F source_file=@/path/to/datafile/fearonLaitin.csv http://metadata.2ravens.org/api/process-single-file
    ```
2.  Follow steps 2 to 4 above in **R Preprocess**
