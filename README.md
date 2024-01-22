# cdrSummarization
This is a Python Script that will take CDR records from Cisco Communications Manager and provide a summarization of the CDR data. 

## Requirements
This module leverages python 3 and pandas and openpyxl libraries are required.

You can install the required libraries by:

```
pip -f requirements.txt
```

## Prerequistes
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
The phonedb.csv file has three fields:
* **phonename** - This field is the phone identifier
* **model** - This field allows you to specify the type of phone 
* **branch** - This field allows you to identify a location of where the phone is placed


## Script Details
This script will use the phonedb.csv to correlate each branch location to the CDR records.

The summarization includes will create an Excel Spreadsheet with multiple tabs.   The following describes each Tab:

**CDR Summary Tab** - This tab shows a report broken down by branch and phone type within the branch and number of calls and duration.
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

**CDR Summary By Day** - This tab shows a report that is broken down by branch and the number of calls and duration by day.
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

**Unknown CDR Records** - This tab shows a report that reports on phone devices that are in the CDR records but not in the phonedb.csv file.
```
Unknown CDR Records
Dates: Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55

Phone Device ID     Total Call
                    Duration        Number of
                    (seconds)         Calls
                                            
SEP888888888888       10              2
SEPABABABABABAB       11              10
SEP1B1B1B1B1B1B       200             11   
```

**Inbound Breakdown** - This tab shows a report that presents the inbound calls.   In our cluster the inbound calls are identified from the source: SIP-TRUNK-TO-SME. This tab breaks down these calls.
```
Inbound Breakdown
Dates: Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55


Branch          Phone Model     Source of Call    Destination Phone    Total Call
                                                                        Duration        Number of
                                                                        (seconds)         Calls
                                            
Branch1            7962         SIP-TRUNK-TO-SME      SEP888888888888       10              2
                                                      SEPABABABABABAB       11              10
                                                      SEP1B1B1B1B1B1B       200             11   
```


The current version allows you to specify the number of CDR files. In my customer, we had two clusters, so there would be two CDR Files to be generated.  The following is an example of the script when it is run.

```commandline
Cisco CDR Summarization
For more details, please look at the github repository at: https://github.com/chrisbog/cdrSummarization

Enter the Phone Data Base Filename [phonedb.csv]: 
How many CDR files do you have [1]?:  2
Enter CDR File #1: Cluster1CDR.txt
Enter CDR File #2: Cluster2CDR.txt
===================================================================================
Reading in phone database from phonedb.csv
Total Number of Phones in Database: 28551
Loading in the CDR Records - Original File: Cluster1CDR.txt
Total Number of CDR Records: 1998829
Loading in the CDR Records - Original File: Cluster2CDR.txt
Total Number of CDR Records: 1775983
CDR Summary from Tuesday 2023-08-22 09:02:51 to Friday 2023-10-20 09:56:55
Total Number of original CDR Entries: 3774812
Total Number of known CDR Entries: 1999775
Total Number of Unknown CDR Entries: 1775037
Writing Output File: CDRSummary.xlsx
Formatting Final Spreadsheet

```

Once the script will run, it will produce a single Excel summary report with the following output name:

```commandline
CDRSummary.xlsx
```