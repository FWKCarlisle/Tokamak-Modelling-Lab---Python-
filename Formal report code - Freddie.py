import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from EM1PythonFunctions import (
    get_average,
    get_triple_product,
    get_variable,
    find_max_value,
    plot_variable,
    add_headers,
    get_new_triple_product,
)
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
)


chosen_subsection = "zerod"
variables = ["pnbi","ip"] #Always has to have more than two
# variables = ["taue", "q0", "q95", "qeff"]

start = 44
end = 104
save_graph = False
Triple_product = True
FindMax = True
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath, f))]
datapoints.sort()

files_paths = []

for i in datapoints:
    files_paths.append(mypath + i)
nrows = len(files_paths)
ncols = len(variables)

if Triple_product:
    variables.append("nTtau")
    ncols = len(variables) - 1


data_matrix = []
nTtau_Matrix = []

max_value_matrix = []

if FindMax:
    for i, files in enumerate(files_paths):
        data_matrix = (get_variable(files,variables))
        data_matrix.append(get_triple_product(files,44,104))
        print(variables)
        max_value_matrix.append(find_max_value(data_matrix,variables))

print(max_value_matrix)

fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)
for i, file_path in enumerate(files_paths):
    ydata = get_triple_product(file_path,44,104)
    xdata = get_variable(file_path,variables)
    
    for j, variable in enumerate(variables):
        if variable == "nTtau":
            continue
        ax = axs[i,j]
        ax.set_xlabel(f'{variable_symbols[variable]} ({variable_units[variable]})')
        ax.set_ylabel(f'{variable_symbols["nTtau"]}')
        ax.plot(xdata[j][1], ydata[1], ".", color="black")
# plt.show()
