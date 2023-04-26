#!/usr/bin/env python3

from cmath import tau
from msilib.schema import Error
from operator import ge
from tkinter import Y, Variable
import scipy.io
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import csv

# import originpro as op


### Find all of the files in the directory and add them to a list to be analysed ###
mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath,f))]
datapoints.sort()
# print(datapoints)

Time_Plot = False


### Lists possible subsection in the matlab folder/data structure ###
def list_subsections():
    print("subsections (I'm using zerod by default):")
    print(full_dataset['post'].dtype)

### Lists the indexs in the cell arrays to choose from i.e the variables to be read from metis e.g Ip, pnbi ###
def list_indexes(subsection='z0dinput'):
    print("indexes in subsection " + subsection + ":")
    print(full_dataset['post']['z0dinput'][0][0].dtype)

### Opens up the file to be read and then reads the certain subsection and index and outputs the data ###
def get_variable(index, subsection='zerod'):
    a = full_dataset['post'][subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a

 
def get_B0_variable(index, subsection='z0dinput',NextSection="geo"):
    a = full_dataset['post'][subsection][0][0][NextSection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a
### gets the stated variable and between the two points specified averages them out for 1 value for a range ###
def get_average(start, end, index, subsection='zerod'):
    a = get_variable(index, subsection=subsection)
    return np.mean(a[start:end]),np.std(a[start:end])

def get_List(start, end, index, subsection='zerod'):
    a = get_variable(index, subsection=subsection)
    return (a[start:end])

def get_B0_List(start, end, index, subsection='z0dinput'):
    a = get_B0_variable(index, subsection=subsection)
    return (a[start:end])

def get_variable_new(file_path,variables,start=44,end=104,chosen_subsection="zerod"):
    full_dataset = scipy.io.loadmat(file_path)
    results = []
    for variable in variables:
        if variable == "b0":
            a = full_dataset['post']["z0dinput"][0][0]["geo"][0][0]["b0"][0][0]
            a = [float(x[0]) for x in a]
            results.append([variable, a[start:end]])
        elif variable == "nTtau":
            a = get_triple_product(file_path,start,end)
        
            results.append(a)
        else:
            a = full_dataset["post"][chosen_subsection][0][0][variable][0][0]
            a = [float(x[0]) for x in a]
            results.append([variable, a[start:end]])
    return results

def get_triple_product(file_path, start, end, average=False):
    full_dataset = scipy.io.loadmat(file_path)
    triple_product_variables = ["ni0", "te0", "taue"]
    triple_product = []
    avg_results = []
    results = get_variable_new(file_path,triple_product_variables,start,end)
    
    for i in range(len(results[0][1])):
        triple_product.append((results[0][1][i]) * results[1][1][i] * results[2][1][i])
   
    if average:
        avg_results = get_average(file_path,start,end,triple_product_variables)
        triple_product_avg = avg_results[0][1] * avg_results[1][1] * avg_results[2][1]
        triple_product_std = triple_product_avg * np.sqrt(
        (avg_results[0][2] / avg_results[0][1]) ** 2
        + (avg_results[1][2] / avg_results[1][1]) ** 2
        + (avg_results[2][2] / avg_results[2][1]) ** 2
        )
        return ["nTtau",triple_product_avg, triple_product_std]
    else:
        return ["nTtau", triple_product]

### creating empty lists ###
te0_List = []
ne0_List = []
taue_List = []
NTtau_List = []
NTtau_Err_List = []
pnbi_List = []
Nbar_List = []
Nbar_List2 = [[],[]]


pnbi_Err_List = []
te0_Err_List = []
ne0_Err_List = []
taue_Err_List = []
hmode_Err_List = []
Ip_Err_List = []
Nbar_Err_List = []


modeh_List = []
Ip_List = []
B0_List = []
B0_List2 = []
Nbar_List = []
hmode_List = []
q0_List = []

NTtau_Max_List = [[],[]]
Nbar_Max_List = [[],[]]
Ip_Max_List = [[],[]]
Pnbi_Max_List = [[],[]]
B0_Max_List = []
taue_Max_List =[[],[]]
te0_Max_List = [[],[]]
ne0_Max_List = [[],[]]
hmode_Max_List = []


# Errorpercent = 0.09224468889	#0-3MW
Errorpercent = 0.09224468889	


### Finds and fills the lists for all required data variables ###




for i in range((len(datapoints))):
    full_dataset = scipy.io.loadmat(mypath + datapoints[i])
    # pnbi_List.append(get_List(44,104,"pnbi"))
    # print(list_indexes())
    # pnbi_List = pnbi_List[0]
    te0_List = (get_List(44,104,"te0"))
    ne0_List = (get_List(44,104,"ne0"))
    taue_List = (get_List(44,104,"taue"))
    hmode_List = (get_List(44,104,"modeh"))
    Ip_List = (get_List(44,104,"ip"))
    pnbi_List = (get_List(44,104,"pnbi"))
    b0_List = get_B0_List(44,104,"b0")
    Nbar_List = (get_List(44,104,"nbar"))
    Nbar_List2.append(get_average(44,104,"nbar")[0])
    # print(b0_List)
    for j in range(len(get_List(44,104,"pnbi"))):

        # y = get_List(44,104, 'taue')
        # x = get_List(44,104, 'pnbi')
        # x = x[0]
        # y = y[0]
        # # print(x)
        # # print(y
        # print(str(datapoints[i]) + "  Index: "+ str(y.index(max(y))) + "  - Value: " + str(max(y)))
        # print(str(datapoints[i]) + "  PNBI value for index: " + str(y.index(max(y))) + " is " + str(x[y.index(max(y))]))
        # plt.plot(x,y)
        # plt.show()
        # print(mypath + datapoints[i])
        # B0_List.append((str(datapoints[i]).split('T'))[0])
        # te0_List.append(get_average(44, 104, 'te0'))
        # ne0_List.append(get_average(44, 104, 'ne0'))
        # taue_List.append(get_average(44, 104, 'taue'))
        # pnbi_List.append(get_average(44,104, 'pnbi'))
        # Ip_List.append(get_average(44, 104, 'ip'))
        # Nbar_List.append(get_average(44, 104, 'nbar'))
        # hmode_List.append(get_average(44,104, "modeh"))

        if len(te0_Err_List) < 60:
            # pnbi_Err_List.append((pnbi_List[j]*Errorpercent))
            te0_Err_List.append((np.std(te0_List)))
            ne0_Err_List.append((np.std(ne0_List)))
            taue_Err_List.append((np.std(taue_List)))
            hmode_Err_List.append((np.std(hmode_List)))
            Ip_Err_List.append((np.std(Ip_List)))
            pnbi_Err_List.append((np.std(pnbi_List)))
            Nbar_Err_List.append((np.std(Nbar_List)))
        else:
            pass

    pnbi_List = [pnbi_List,pnbi_Err_List]
    te0_List = [te0_List,te0_Err_List]
    ne0_List = [ne0_List,ne0_Err_List]
    taue_List = [taue_List,taue_Err_List]
    hmode_List = [hmode_List,hmode_Err_List]
    Ip_List = [Ip_List,Ip_Err_List]
    Nbar_List = [Nbar_List,Nbar_Err_List]




        
    NTtau_List = []
    NTtau_Err_List = []
    # print(len(Ip_List[1]))    
    if len(NTtau_Err_List) < 60:
        for i in range(len(te0_List[0])):
            NTtau_List.append(te0_List[0][i] * ne0_List[0][i] * taue_List[0][i])
            # print((NTtau_List[0][i]*np.sqrt((te0_List[i][0]/te0_List[i][1]**2)+(ne0_List[i][0]/ne0_List[i][0])**2 + (taue_List[i][0]/taue_List[i][1])**2)))
            NTtau_Err_List.append(NTtau_List[i]*np.sqrt(((te0_List[0][i]*Errorpercent) /te0_List[0][i]**2)+((ne0_List[0][i]*Errorpercent)/ne0_List[0][i])**2 + ((taue_List[0][i]*Errorpercent)/taue_List[0][i])**2))
    # print(len(NTtau_List))
    # print(max(NTtau_List))
    # print(NTtau_List.index(max(NTtau_List)))
    # print(NTtau_Err_List[NTtau_List.index(max(NTtau_List))])
    NTtau_Max_List[0].append(max(NTtau_List))
    NTtau_Max_List[1].append(NTtau_Err_List[NTtau_List.index(max(NTtau_List))])
    # print(NTtau_Err_List[NTtau_List.index(max(NTtau_List))])
    Ip_Max_List[0].append(Ip_List[0][NTtau_List.index(max(NTtau_List))])
    Ip_Max_List[1].append(Ip_List[1][NTtau_List.index(max(NTtau_List))])
    Pnbi_Max_List[0].append(pnbi_List[0][NTtau_List.index(max(NTtau_List))])
    Pnbi_Max_List[1].append(pnbi_List[1][NTtau_List.index(max(NTtau_List))])
    Nbar_Max_List[0].append(Nbar_List[0][NTtau_List.index(max(NTtau_List))])
    Nbar_Max_List[1].append(Nbar_List[1][NTtau_List.index(max(NTtau_List))])
    taue_Max_List[0].append(taue_List[0][NTtau_List.index(max(NTtau_List))])
    taue_Max_List[1].append(taue_List[1][NTtau_List.index(max(NTtau_List))])
    ne0_Max_List[0].append(ne0_List[0][NTtau_List.index(max(NTtau_List))])
    ne0_Max_List[1].append(ne0_List[1][NTtau_List.index(max(NTtau_List))])
    te0_Max_List[0].append(te0_List[0][NTtau_List.index(max(NTtau_List))])
    te0_Max_List[1].append(te0_List[1][NTtau_List.index(max(NTtau_List))])
    # print(NTtau_List.index(max(NTtau_List)),len(b0_List))
    B0_Max_List.append(b0_List[NTtau_List.index(max(NTtau_List))])
    hmode_Max_List.append(hmode_List[0][NTtau_List.index(max(NTtau_List))])

x = Nbar_Max_List[0]
y = NTtau_Max_List[0]

MaxVal = NTtau_Max_List[0].index(max(NTtau_Max_List[0]))
print(MaxVal)
print(str(Nbar_Max_List[0][MaxVal]) + ", Max NTtau - " + str(NTtau_Max_List[0][MaxVal]),datapoints[MaxVal])
    # y = Ip_List[0]

plt.scatter(x,y)
# plt.show()

###Checks lengths ###
# print(str(len(pnbi_List[1]))+"," +str(len(te0_List[1]))+","+ str(len(ne0_List[1]))+","+str(len(taue_List[1]))+","+str(len(hmode_List[1])))


### calculates NTtau ###


# print(str(len(Ip_List[0]))+"," +str(len(te0_List[1]))+","+ str(len(ne0_List[1]))+","+str(len(taue_List[1]))+","+str(len(hmode_List[0])) + "," + str(len(NTtau_Err_List)))

### Gets max values ###



### Prints the listed variables below for the range of Values ###

Results = open("H:\Desktop\Results.txt", "w")
PlasmaRow = []
TempRow = []
DensRow = [] 
TauRow = []
HmodeRow = []
NTtauRow = []
PnbiRow = []
NbarRow = []
NTtauErrRow = []
B0Row = []

Ip_Max_Row = []
NTtau_Max_Row = []
Pnbi_Max_Row = []
Nbar_Max_Row = []
taue_Max_Row = []
te0_Max_Row = []
ne0_Max_Row = []
TestRow = []
Time_row = []




if not Time_Plot:
    writer = csv.writer(Results) 
    # Results.write(("Plasma Current" + "," + "Plasma Current Err" + "," + "P(NBI)" + "," + "P(NBI) Err" + "," +"Central Line Density"+"," +"Central Line Density Error"+",Confinement Time,"+"Tau E error"+",Central Electron Density"+",Central Electron Density Err"+",Central Electron Temperature"+",Te0 Err" +",Magnetic Field" +","+"hmode" +","+ "NTtau Maximum" +"," + "NTtau Err" + "," + "\n"))
    Results.write("Pnbi"+","+"Pnbi err"+","+"Temp"+","+"temp err,"+"hmode"+","+"hmode err"+"," +"\n")
    # + "," + "Plasma Current Err"
    
    # print(str(Ip_List[0]))
    for i in range(len(Pnbi_Max_List[0])):
        Row = 0
        full_dataset = scipy.io.loadmat(mypath + datapoints[i])
        # PlasmaRow.append(str(Ip_List[0][i]) + "," + str(Ip_List[1][i]) + ",")
        pnbi_mean, pnbi_err = get_average(44,104,"pnbi")
        te0_mean, te0_err = get_average(44,104,"te0")
        hmode_mean, Hmode_err = get_average(44,104,"modeh")
        PnbiRow = str(pnbi_mean) + "," + str(pnbi_err) + ","
        # print(PnbiRow)
        TempRow = str(te0_mean) + "," + str(te0_err) + ","
        hmode_row = str(hmode_mean) + "," + str(Hmode_err) + ","
        # DensRow.append(str(ne0_List[0][i]) + "," + str(ne0_List[1][i]) + ",")
        # TauRow.append(str(taue_List[0][i]) + "," + str(taue_List[1][i]) + ",")
        # HmodeRow.append(str(hmode_List[0][i]) + "," + str(hmode_List[1][i]) + ",")
        # NbarRow.append(str(Nbar_List[i][0]) + "," + str(Nbar_List[i][1]) + ",")
            # Ip_Max_Row.append(str(Ip_Max_List[0][i]) + "," + str(Ip_Max_List[1][i]) + ",")
            # NTtau_Max_Row.append(str(NTtau_Max_List[0][i]) + "," + str(NTtau_Max_List[1][i])+",")
            # Pnbi_Max_Row.append(str(Pnbi_Max_List[0][i]) + "," + str(Pnbi_Max_List[1][i]) +",")
            # Nbar_Max_Row.append((str(Nbar_Max_List[0][i]) + "," + str(Nbar_Max_List[1][i]) +","))
            # taue_Max_Row.append((str(taue_Max_List[0][i]) + "," + str(taue_Max_List[1][i]) +","))
            # ne0_Max_Row.append((str(ne0_Max_List[0][i]) + "," + str(ne0_Max_List[1][i]) +","))
            # te0_Max_Row.append((str(te0_Max_List[0][i]) + "," + str(te0_Max_List[1][i]) +","))
        # NTtauRow.append(str(NTtau_List[i]) + ",")
        # NTtauErrRow.append(str(NTtau_Err_List[i]))
        # print(PlasmaRow[i])
        # 
        # TestRow = (str(PnbiRow[i])+ str(NTtauRow[i]) + str(NTtauErrRow[i]) + "\n")
        # RowPNBI = str(PnbiRow[i]) + str(TempRow[i]) + str(DensRow[i]) + str(TauRow[i]) + str(HmodeRow[i]) + str(NTtauRow[i]) + str(NTtauErrRow[i])  + "\n"
        # RowIP = str(PlasmaRow[i]) + str(TempRow[i]) + str(DensRow[i]) + str(TauRow[i]) + str(HmodeRow[i]) + str(NTtauRow[i]) + str(NTtauErrRow[i])  +"\n"
        # RowB0 = str(B0Row[i]) + str(TempRow[i]) + str(DensRow[i]) + str(TauRow[i]) + str(HmodeRow[i]) + str(NTtauRow[i]) + str(NTtauErrRow[i])  +"\n"
        # RowNbar = str(NbarRow[i]) + str(TempRow[i]) + str(DensRow[i]) + str(TauRow[i]) + str(HmodeRow[i]) + str(NTtauRow[i]) + str(NTtauErrRow[i])  +"\n"
        # RowMaxIP = str(Ip_Max_Row[i]) + str(NTtau_Max_Row[i]) + "\n"
        # RowMaxPnbi = str(Pnbi_Max_Row[i]) + str(NTtau_Max_Row[i]) + "\n"
        # RowMax = str(Ip_Max_Row[i]) + str(Pnbi_Max_Row[i])+str(Nbar_Max_Row[i]) +str(taue_Max_Row[i]) +str(ne0_Max_Row[i])+str(te0_Max_Row[i])+str(B0_Max_List[i])+ "," +str(hmode_Max_List[i])+","+ str(NTtau_Max_Row[i]) + "\n"
        Row = str(PnbiRow) + str(TempRow) + str(hmode_row) + "\n"
    
        # print(RowMaxIP)
        # print(RowPNBI)
        # print(("Plasma Current" +"," +"Plasma Current Err" +","+"P(NBI)" +"," +"P(NBI) Err" +","+"NTtau" +","+"NTtau Err"+"," + "\n"))
        # print(RowMax, datapoints[i])
        
        # print(str(NTtauRow[i]))
        print(Row)
        Results.write(Row)
else:
    start, end = 0, 300
    for var in datapoints:
        Time_List = get_variable_new((mypath + var), ["temps"],start,end)
        NTtau_List = get_variable_new((mypath + var),["nTtau"],start,end)
    Results.write("nTtau,"+"Time"+"\n")
    Time_List = Time_List[0]
    NTtau_List = NTtau_List[0]
    for i in range(len(Time_List[1])):
        print(i)
        row = str(NTtau_List[1][i]) +","+ str(Time_List[1][i]) + "\n"
        print(row)
        Results.write(row)
    # print(PlasmaRow)

print("done")

