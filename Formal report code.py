from os import listdir
from os.path import isfile, join
from EM1PythonFunctions import *
import matplotlib.pyplot as plt
from numpy import insert


def get_variable(file_path, index, chosen_subsection="zerod"):
    full_dataset = scipy.io.loadmat(file_path)
    a = full_dataset["post"][chosen_subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a


def get_List(start, end, file_path, variables, subsection="zerod"):
    a = get_variable(file_path, variables, subsection)
    return a[start:end]


def scan_file(file_path, variables, start, end, subsection="zerod"):
    data_matrix = []
    for i in variables:
        a = get_List(start, end, file_path, i, subsection)
        data_matrix.append(a)
    return data_matrix

def Extract_Data(Data_Array,Array,index):
    for files in range(len(Array)):
        Data_Array.append(Array[files][index])
    return Data_Array



mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath, f))]
datapoints.sort()

Full_Paths = []

for i in datapoints:
    Full_Paths.append(mypath + i)

Variable_List = [
    "te0",
    "taue",
    "ne0",
    "pnbi"
]  # List the Variables you would like to analyse - DON'T INCLUDE B0 (Needs a differing subsection which breaks this loop)
data_matrix = []
for paths in Full_Paths:
    Data = scan_file(paths, Variable_List, 44, 104)
    data_matrix.append(Data)

Temp_Data = []
Taue_Data = []
ne0_Data = []
NTtau_data = [Temp_Data,Taue_Data,ne0_Data]

for array in NTtau_data:
    i=0
    Extract_Data(array,data_matrix,i)
    i+=1

NTtau_Calculated = np.zeros((len(Temp_Data),len(Temp_Data[0])))

for files in Temp_Data:
    index = Temp_Data.index(files)
    for i in range(len(files)):
        NTtau_Calculated[index][i] = Temp_Data[index][i]*Taue_Data[index][i]*ne0_Data[index][i]

