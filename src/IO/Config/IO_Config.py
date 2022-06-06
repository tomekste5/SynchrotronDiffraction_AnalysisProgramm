from IO.Parser import CsvParser, PickleParser

loadModes = {"single_pickle":PickleParser.preloadPickle_eachDirectory,"multipleD_pickle":PickleParser.preloadPickle_eachDirectory,
             "single_csv":PickleParser.preloadPickle_eachDirectory,
             "multiple_csv":CsvParser.writeCSV_eachFile,
             "multipleD_csv":CsvParser.preloadPickle_eachDirectory
             }#put into settings
 
SaveFunctions = {"single_pickle":PickleParser.writePickle_single,"multipleD_pickle":PickleParser.writePickle_eachDirectory,
    "single_csv":CsvParser.writeCSV_single,
    "multiple_csv":CsvParser.writeCSV_eachFile,
    "multipleD_csv":CsvParser.writeCSV_eachDirectory
 }#put into settings