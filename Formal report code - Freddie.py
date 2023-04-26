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

# plt.rcParams["text.usetex"] = True
# plt.rcParams["text.latex.preamble"] = "\n".join(
#     [
#         r"\usepackage{siunitx}",
#     ]
# )


chosen_subsection = "zerod"
variables = ["pnbi","temps"]  #  #Always has to have more than two #no B0#.
yaxis_variables = ["nTtau","modeh"] # Y axis variables
# variables = []

calc_start = 44
calc_end = 108


graph_start = 44
graph_end = 108

time_width = 3 #Time width over which take average of nTtau


save_graph = False
Triple_product = True
FindMax = True
FindMaxFile = True
findTimeAverageForNTtau = False

plot_data = False
plot_files = not plot_data

plotxTime = True
plotxnTtau = False



if plot_files:
    plotxTime = False
    plotxnTtau = False
    plotnTtauMax = False


if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

assert not ((plot_data and plot_files) == True), "You can not plot both data and averages at the same time"


mypath = "H:\Desktop\Tokamak Modelling\Settings\\"
datapoints = [f for f in listdir(mypath) if isfile(join(mypath, f))]
datapoints.sort()

file_paths = []

for i in datapoints:
    file_paths.append(mypath + i)
nrows = len(file_paths)
ncols = len(variables)

if Triple_product:
    variables.append("nTtau")
    assert variables[-1] == "nTtau" ,"nTtau should be the last variable in the list"





if FindMax:
    data_matrix = []
    max_value_matrix = []
    nTtau_values = []
    time_lists = []
    max_nTtau = 0

    for i, files in enumerate(file_paths):
        data_matrix = (get_variable(files,variables,calc_start,calc_end))
        # print(data_matrix)
        max_value_matrix.append(find_max_value(data_matrix,variables))
    if FindMaxFile:
        for i in range(len(max_value_matrix)):
            for j in range(len(max_value_matrix[0])):
                if max_value_matrix[i][j][0] == "nTtau":
                    if max_value_matrix[i][j][1] > max_nTtau:
                        max_nTtau = max_value_matrix[i][j][1]
                        Max_file = i
                    nTtau_values.append(max_value_matrix[i][j][1])


    


    max_from_files = max_value_matrix[Max_file]
    max_nTtau_file = file_paths[Max_file]
    for i in range(len(max_value_matrix)):
        print(max_value_matrix[i],file_paths[i])
    print("MAXIMUM nTtau & File",max_from_files,max_nTtau_file)
    
if findTimeAverageForNTtau:
    if "temps" not in variables:
        variables.insert(0, "temps")
    nTtau_avg_list = []
    timeDifferenceList = []
    nTtauAndtimeList = []
    for i, files in enumerate(file_paths):
        

        data_matrix = get_variable(files,variables,calc_start,calc_end)
        maxidx = find_max_value(data_matrix,variables,returnIdx=True)
        nTtauinfo = [x for x in maxidx if x[0] == "nTtau"]
        nTtauidx = nTtauinfo[0][1]
        # print(maxidx,nTtauidx)

        timeIdxInVar = variables.index("temps")
        nTtauIdxInVar = variables.index("nTtau")

        timedata = data_matrix[timeIdxInVar]
        nTtaudata = data_matrix[nTtauIdxInVar]
    
        timeMaxPoint = timedata[1][nTtauidx]
        timeMaxPoint_min = timeMaxPoint-(time_width/2)

        timePoint_min_idx = min(range(len(timedata[1])),key = lambda i: abs(timedata[1][i]-timeMaxPoint_min))
        timePoint_max_idx = nTtauidx + (nTtauidx-timePoint_min_idx)
        if timePoint_max_idx >= len(timedata[1]):
            timePoint_max_idx = len(timedata[1]) 
        
        TimeDataList = timedata[1][timePoint_min_idx:timePoint_max_idx]
        nTtauDataList = nTtaudata[1][timePoint_min_idx:timePoint_max_idx]
        timeDifferenceList.append(TimeDataList[-1]-TimeDataList[0])
        nTtau_avg_list.append(np.mean(nTtauDataList))
        nTtauAndtimeList.append([np.mean(nTtauDataList),TimeDataList[-1]-TimeDataList[0]])
    
    nTtauAndtimeList = nTtauAndtimeList[0]
    maxAvgnTtau = max(nTtau_avg_list)
    idx = nTtau_avg_list.index(maxAvgnTtau)
    print("The highest average nTtau is",nTtauAndtimeList[0],"over a time span of",nTtauAndtimeList[1],"seconds",file_paths[idx])

    if plotxTime == False:
        variables.remove("temps")
if plotxnTtau == False:
    variables.remove("nTtau")




print(nrows, ncols)
if plot_data:
    ncols = (len(variables) * len(yaxis_variables))
    for i, var in enumerate(variables):
        for j, gvar in enumerate(yaxis_variables):
            if var == gvar:
                ncols -= 1

    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 4 * nrows), constrained_layout=True,sharex=False,sharey=False)
    row = 0
    print(variables,yaxis_variables)
    for i, file_path in enumerate(file_paths):
        xdata = get_variable(file_path,variables,graph_start,graph_end)
        ydata = get_variable(file_path,yaxis_variables,graph_start,graph_end)
        colomn = 0    
        for j, variable in enumerate(variables):
            for y, var in enumerate(yaxis_variables): 
                if var == variable:
                    continue
                ax = axs[row,colomn]
                if len(yaxis_variables)<2 or y == 1:
                    ax.set_title(datapoints[i])
                ax.set_xlabel(f'{variable_symbols[variable]}')
                ax.set_ylabel(f'{variable_symbols[yaxis_variables[y]]}')
                ax.plot(xdata[j][1], ydata[y][1], ".", color="black")
                colomn += 1
        row += 1       

if plot_files:
    xdata_matrix = []
    ydata_matrix = []
    xdata = []
    ydata = []
    if plotnTtauMax:
        yaxis_variables =["nTtau"]
        for i, file_path in enumerate(file_paths):
            xdata_matrix.append([x for x in max_value_matrix[i] if x[0] in variables])
            ydata_matrix.append([x for x in max_value_matrix[i] if x[0] == "nTtau"])
        # print(xdata_matrix)
        # print(ydata_matrix) 

        print(variables)
        print(yaxis_variables)
        for k in range(len(xdata_matrix[0])):
            append = []
            for i in range(len(file_paths)):
                
                append.append(xdata_matrix[i][k][1])
            xdata.append(append)
        append = []
        for i in range(len(file_paths)):
            append.append(ydata_matrix[i][0][1])
            ydata.append(append)
    else:
        for i, file_path in enumerate(file_paths):
            xdata_matrix.append(get_average(file_path,graph_start,graph_end,variables))
            ydata_matrix.append(get_average(file_path,graph_start,graph_end,yaxis_variables))

        for y in range(len(variables)):
            append = []
            for i in range(len(file_paths)):
                append.append(xdata_matrix[i][y][1])
            xdata.append(append)
        for y in range(len(yaxis_variables)):
            append = []
            for i in range(len(file_paths)):
                append.append(ydata_matrix[i][y][1])
            ydata.append(append)

    ncols = len(yaxis_variables)
    nrows = len(variables)
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 4 * nrows), constrained_layout=True,sharex=False,sharey=False)


    for j, var in enumerate(variables):
        colomn = 0
        for y, yvar in enumerate(yaxis_variables):
            if var == yvar:
                continue
            if ncols and nrows == 1:
                ax = axs
            elif ncols == 1:
                ax = axs[j]
            else:
                ax = axs[j,colomn]
            if len(yaxis_variables)<2 or y == 1:
                ax.set_title(var)
            if plotnTtauMax:
                ax.set_ylabel("nTtau Max")
            else:
                ax.set_ylabel(f'{variable_symbols[yvar]}')
            ax.set_xlabel(f'{variable_symbols[var]}')

            ax.plot(xdata[j],ydata[y], ".", color="black")
            # colomn +=1


plt.show()
