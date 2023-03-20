#!/usr/bin/env python3

import scipy.io
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join

mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath,f))]
datapoints.sort()


def list_subsections():
    print("subsections (I'm using zerod by default):")
    print(full_dataset['post'].dtype)


def list_indexes(subsection='zerod'):
    print("indexes in subsection " + subsection + ":")
    print(full_dataset['post']['zerod'][0][0].dtype)


def get_variable(index, subsection='zerod'):
    a = full_dataset['post'][subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a

def get_average(start, end, index, subsection='zerod'):
    List = []
    a = get_variable(index, subsection=subsection)
    List.append(np.mean(a[start:end]))
    List.append(np.std(a[start:end]))
    return List

te0_List = []
pnbi_List = []
ne0_List = []
taue_List = []
NTtau_List = []
betap_List = []
hmode_List = []


for i in range(len(datapoints)):
    full_dataset = scipy.io.loadmat(mypath + datapoints[i])
    te0_List.append(get_average(44, 49, 'te0'))
    pnbi_List.append(get_average(44, 49, 'pnbi'))
    ne0_List.append(get_average(44, 49, 'ne0'))
    taue_List.append(get_average(44, 49, 'taue'))
    betap_List.append(get_average(44, 49, 'betap'))
    hm_List.append(get_average(44, 49, 'taue'))

# list_subsections()
# list_indexes()
# print(get_average(44, 49, 'te0'))
# plt.plot(get_variable('te0'))
# plt.show()

for i in range(len(ne0_List)):
    NTtau_List.append(te0_List[i][0] * ne0_List[i][0] * taue_List[i][0])

for i in range(len(te0_List)):
    # print("Density -" + (str(ne0_List[i])) + "- NTtau -" + str(NTtau_List[i]))
    # print("Power of NBI - " + str(pnbi_List[i]))
    # print("Temp - " + str(te0_List[i]))
    print("Tau e - " + str(taue_List[i]))
#     # print(betap_List[i])
# # print(te0_List[1][0])



    
