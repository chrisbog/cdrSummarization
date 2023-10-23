# cdrSummarization
This is a simple Python Script that will take CDR records from Cisco Communications Manager and provide a summarization of the CDR data.

The summarization includes, the Phone Identifier and the number of calls and the total number of minutes that was made from that device.

In my customer, we had two clusters, so there would be two CDR Files required.   All you need to do is copy the files to the directory of the script and name them:

```commandline
Cluster1CDR.txt
Cluster2CDR.txt
```

Once the script will run, it will produce two Excel spreadsheets with the name:

```commandline
Cluster1CDR-output.xlsx
Cluster2CDR-output.xlsx
```