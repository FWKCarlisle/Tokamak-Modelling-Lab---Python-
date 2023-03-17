from os import listdir
from os.path import isfile, join
from EM1PythonFunctions import *
import matplotlib as mpl


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
        a.insert(0, i + " " + file_path)
        data_matrix.append(a)
    return data_matrix


def find_variable(Matrix, value):
    for file in Matrix:
        for i in file:
            if Matrix[file, i] == value:
                return i


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
    "hmode",
]  # List the Variables you would like to analyse - DON'T INCLUDE B0 (Needs a differing subsection which breaks this loop)
data_matrix = []
for paths in Full_Paths:
    for variable in Variable_List:

        Data = scan_file(paths, variable, 44, 104)

        data_matrix.append(Data)

variable_indexs = []

for variables in Variable_List:
    variable_indexs.append(find_variable(data_matrix, variables))

print(variable_indexs)

for i in variable_indexs:
    assert variable_indexs[i] == Variable_List[i]
