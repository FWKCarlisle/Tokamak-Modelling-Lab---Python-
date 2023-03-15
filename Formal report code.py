from os import listdir
from os.path import isfile, join
from EM1PythonFunctions import *
import matplotlib as mpl


def get_variable(file_path, index, chosen_subsection="zerod"):
    full_dataset = scipy.io.loadmat(file_path)
    a = full_dataset["post"][chosen_subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a

def get_List(start,end, file_path, variables, subsection='zerod'):
    a = get_variable(file_path,variables, subsection)
    return (a[start:end])

def scan_file(file_path,variables, start, end, subsection ='zerod'):
    data_matrix = []
    for i in variables:
        a = get_List(start,end, file_path,i,subsection)
        a.insert(0,i + " " + file_path)
        data_matrix.append(a)
    return data_matrix


    
mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath,f))]
datapoints.sort()



variables_list = ["te0","ne0","taue","modeh","ip","nbar"]
for i in datapoints:
    Full_Path = mypath + i
    data_matrix = (scan_file(Full_Path,variables_list,44,104))
        

