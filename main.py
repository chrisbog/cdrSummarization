import pandas as pd
import openpyxl
from openpyxl.styles import Color, Fill, Font, Alignment
import time
import os



def process_spreadsheet(phonedbname,filenames):
    print('===================================================================================')
    print (f"Reading in phone database from {phonedbname}")
    db = pd.read_csv(phonedbname, usecols=['phonename', 'model','branch'])
    # Example on How to Search search = db[db['phonename'] == 'SEP88755651F5D5']
    print(f'Total Number of Phones in Database: {db.shape[0]}')

    cdr_df =[]
    for cdr in filenames:
        print(f'Loading in the CDR Records - Original File: {cdr}')
        df = pd.read_csv(cdr,usecols=['origDeviceName','duration','dateTimeOrigination'])
        print(f'Total Number of CDR Records: {df.shape[0]}')
        cdr_df.append(df)

    # Concatenate the multiple CDR files
    cdrs = pd.concat(cdr_df)

    minepoch = cdrs['dateTimeOrigination'].min()
    maxepoch = cdrs['dateTimeOrigination'].max()

    min = time.strftime('%A %Y-%m-%d %H:%M:%S', time.localtime(int(minepoch)))
    max = time.strftime('%A %Y-%m-%d %H:%M:%S', time.localtime(int(maxepoch)))

    daymin = time.strftime('%A', time.localtime(int(minepoch)))
    daymax = time.strftime('%A', time.localtime(int(maxepoch)))

    print (f'CDR Summary from {min} to {max}')


    # Let's Merge the CDR record with the Database of phones
    mergeddf = pd.merge(cdrs,db,left_on='origDeviceName',right_on='phonename')

    notmerged = cdrs[~cdrs['origDeviceName'].isin(db['phonename'])]
    #print (notmerged)



    print(f'Total Number of original CDR Entries: {cdrs.shape[0]}')
    print(f'Total Number of known CDR Entries: {mergeddf.shape[0]}')
    print(f'Total Number of Unknown CDR Entries: {notmerged.shape[0]}')

    mergeddf['datetime'] = pd.to_datetime(mergeddf['dateTimeOrigination'], unit='s')

    mergeddf['day'] = mergeddf['datetime'].dt.day_name()

    # Let's drop the duplicate column
    mergeddf = mergeddf.drop('phonename',axis=1)
    mergeddf = mergeddf.drop('datetime',axis=1)

    newdf = mergeddf.groupby(['branch','model','origDeviceName'])['duration'].agg(['sum','count'])
    sorteddf = newdf.sort_values(by=['branch','model'])

    groupedbyday = mergeddf.groupby(['branch','day'])['duration'].agg(['sum','count'])
    groupedbyday = groupedbyday.sort_values(by=['branch','day'])

    unknown = notmerged.groupby(['origDeviceName'])['duration'].agg(['sum','count'])
    #print (unknown)

    headertext = "Dates: " + min + ' to '+ max

    outputfile = 'CDRSummary.xlsx'
    print ('Writing Output File: '+outputfile)

    with pd.ExcelWriter(outputfile) as writer:
        sorteddf.to_excel(writer,sheet_name='CDR Summary',startrow=4)
        groupedbyday.to_excel(writer,sheet_name='CDR Summary By Day',startrow=4)
        unknown.to_excel(writer,sheet_name='Unknown CDR Records', startrow=4)
    print ("Formatting Final Spreadsheet")
    workbook = openpyxl.load_workbook(outputfile)
    sheet = workbook['CDR Summary']
    sheet['A1'] = " CDR Summary Report"
    sheet['A3'] = headertext
    sheet['A1'].font = Font(size=16, bold=True)
    sheet['A3'].font = Font(size=16, bold=True)
    sheet['A5'] = "Branch"
    sheet['A5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['A'].width = 12
    sheet['B5'] = "Phone Model"
    sheet.column_dimensions['B'].width = 12
    sheet['B5'].font = Font(size=12,bold=True)
    sheet['C5'] = "Phone Device ID"
    sheet['C5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['C'].width = 20
    sheet['D5'] = 'Total Call Duration (seconds)'
    sheet['D5'].font = Font(size=12,bold=True)
    sheet['D5'].alignment = Alignment(wrap_text=True,horizontal='center')
    sheet.column_dimensions['D'].width = 12
    sheet['E5'] = 'Number of Calls'
    sheet['E5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['E'].width = 12
    sheet['E5'].alignment = Alignment(wrap_text=True,horizontal='center')

    sheet = workbook['CDR Summary By Day']
    sheet['A1'] = " CDR Summary Report By Day"
    sheet['A3'] = headertext
    sheet['A1'].font = Font(size=16, bold=True)
    sheet['A3'].font = Font(size=16, bold=True)
    sheet['A5'] = "Branch"
    sheet['A5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['A'].width = 12
    sheet['B5'] = "Day"
    sheet['B5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['B'].width = 12
    sheet['C5'] = 'Total Call Duration (seconds)'
    sheet['C5'].font = Font(size=12,bold=True)
    sheet['C5'].alignment = Alignment(wrap_text=True,horizontal='center')
    sheet.column_dimensions['C'].width = 12
    sheet['D5'] = 'Number of Calls'
    sheet['D5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['D'].width = 12
    sheet['D5'].alignment = Alignment(wrap_text=True,horizontal='center')

    sheet = workbook['Unknown CDR Records']
    sheet['A1'] = " Unknown CDR Records"
    sheet['A3'] = headertext
    sheet['A1'].font = Font(size=16, bold=True)
    sheet['A3'].font = Font(size=16, bold=True)
    sheet['A5'] = "Phone Device ID"
    sheet['A5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['A'].width = 20
    sheet['B5'] = 'Total Call Duration (seconds)'
    sheet['B5'].font = Font(size=12,bold=True)
    sheet['B5'].alignment = Alignment(wrap_text=True,horizontal='center')
    sheet.column_dimensions['B'].width = 12
    sheet['B5'] = 'Number of Calls'
    sheet['B5'].font = Font(size=12,bold=True)
    sheet.column_dimensions['B'].width = 12
    sheet['B5'].alignment = Alignment(wrap_text=True,horizontal='center')

    workbook.save(filename=outputfile)

if __name__ == '__main__':

    print("Cisco CDR Summarization")
    print("For more details, please look at the github repository at: https://github.com/chrisbog/cdrSummarization")
    print("")

    filenames=["Cluster1CDR.txt","Cluster2CDR.txt"]

    phonedbname = input("Enter the Phone Data Base Filename [phonedb.csv]: ")
    if phonedbname == "":
        phonedbname = 'phonedb.csv'

    if os.path.isfile(phonedbname) == False:
        print (f"ERROR: {phonedbname} does not exist, please correct.")
        exit()

    numberofcdr = input("How many CDR files do you have [1]?:  ")
    if numberofcdr.isdigit():
        numberofcdr = int(numberofcdr)
    else:
        numberofcdr = 1

    filenames=[]
    for count in range(numberofcdr):
        filename = input("Enter CDR File #"+str(count+1)+": ")

        if os.path.isfile(filename) == False:
            print(f"ERROR: {filename} does not exist, please correct.")
            exit()
        else:
            filenames.append(filename)

    process_spreadsheet(phonedbname, filenames)


