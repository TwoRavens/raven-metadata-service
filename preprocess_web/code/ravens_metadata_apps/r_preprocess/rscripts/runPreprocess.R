

# --------------------------------
# Run preprocess and output lines
# for the python subprocess
# --------------------------------
runPreprocess <- function(filename){

  ppJSON<-preprocess(filename=filename);

  writeLines("---START-PREPROCESS-JSON---")
  writeLines(ppJSON);
  writeLines("---STOP-PREPROCESS-JSON---")

}

# --------------------------------
# Check for a filename argument
# --------------------------------
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).", call.=FALSE)
} else if (length(args)==2) {
  # default output file
  input_file <- args[1]
  r_script_directory <- args[2]
  if(!dir.exists(r_script_directory)){
    stop(paste("This directory does not exist or could not be reached: ", r_script_directory), call.=FALSE)

  }else if(!file.exists(input_file)){
    stop(paste("This file does not exist or could not be reached: ", input_file), call.=FALSE)

  }else{
      source(paste(r_script_directory, '/preprocess.R', sep=""))

      runPreprocess(input_file)
  }
}else{
  stop("Please supply a *single* argument giving the file location", call.=FALSE)

}
#ppJSON<- list()

#ppJSON<-preprocess(filename='../test_data/fearonLaitin.csv')
#ppJSON<-preprocess(filename='../test_data/editor_test.tab')

#writeLines("---START-PREPROCESS-JSON---")
#writeLines(ppJSON)
# print(paste("ppJSON: ", ppJSON, sep=""))

print(args)
