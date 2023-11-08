# cdrSummarization
This is a Python Script that will take CDR records from Cisco Communications Manager and provide a summarization of the CDR data. 


# Prerequistes
Due to the size of the CDR data files, this file uses Pandas as the processing library behind the scenes.   We also use the openpyxl library to assist in formating the output spreadhseet.

The prerequisites of the script is get the CDR records from CUCM in .csv format.   In addition, we are requiring another file called phonedb.csv. This file has the following format:


```commandline
phonename,model,branch
SEP111111111111,Cisco 7961,Branch1
SEP222222222222,Cisco 7962,Branch2
SEP333333333333,Cisco 7962,Branch3
.
.
.

```

# Script Details
This script will use the phonedb.csv to correlate each branch location to the CDR records.

The summarization includes will create an Excel Spreadsheet with multiple tabs.   The following describes each Tab:

CDR Summary Tab - This tab shows a report broken down by branch and phone type within the branch and number of calls and duration.
```commandline
CDR Summary Report

Dates: Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55

Branch  Phone Model     Phone Device ID     Total Call
                                            Duration        Number of
                                            (seconds)         Calls
                                            
Branch1 Cisco 7962      SEP111111111111         100             2
        Cisco 7961      SEP999999999999          20             1
Branch2 Cisco 8531      SEP888888888888         200             5        
```

CDR Summary By Day - This tab shows a report that is broken down by branch and the number of calls and duration by day.
```
 CDR Summary Report By Day
Dates: Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55

Branch  Day         Total Call
                    Duration        Number of
                    (seconds)         Calls
                                            
Branch1 Monday         10              2
        Tuesday        12              1
        Wednesday      10              3
        Thursday       20              4
        Friday         30              1
Branch2 Monday          5              2
        Tuesday         2              1
        Wednesday       3              3
        Thursday       10              4
        Friday          3              1      
```

Unknown CDR Records - This tab shows a report that reports on phone devices that are in the CDR records but not in the phonedb.csv file.
```
Unknown CDR Records
Dates: Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55

Branch  Day         Total Call
                    Duration        Number of
                    (seconds)         Calls
                                            
SEP888888888888       10              2
SEPABABABABABAB       11              10
SEP1B1B1B1B1B1B       200             11   
```


The current version is hardcoded with two CDR files. In my customer, we had two clusters, so there would be two CDR Files to be generated.  You can name the two files the following:

```commandline
Cluster1CDR.txt
Cluster2CDR.txt
```

Once the script will run, it will produce a single Excel summary report with the following output name:

```commandline
CDRSummary.xlsx
```