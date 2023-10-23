import pandas as pd
import openpyxl


def process_spreadsheet(filename):
    print('===================================================================================')
    print('Loading in the CDR Records - Original File'+filename+'.txt')
    df1 = pd.read_csv(filename+'.txt',usecols=['origDeviceName','duration'])

#    for row in df1.iterrows():
#        print(row[1]['origDeviceName'], row[1]['duration'], row[1]['destDeviceName'])

    newdf = df1.groupby(["origDeviceName"]).agg(['sum','count'])
    sorteddf = newdf.sort_values(by=['origDeviceName'])
    #print(sorteddf)
    print ('Writing Output File: '+filename+'-output.xlsx')
    with pd.ExcelWriter(filename+'-output.xlsx') as writer:
        sorteddf.to_excel(writer)
#    old_list = df1[['origDeviceName', 'duration']].values.tolist()


if __name__ == '__main__':
    filenames=["Cluster1CDR","Cluster2CDR"]
    for name in filenames:
        process_spreadsheet(name)


