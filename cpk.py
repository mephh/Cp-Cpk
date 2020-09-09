import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm
import math


data_file = "HAB_mosfety.txt"

def init():
    global mean, std_dev, cp, cpk, data_input, low_limit, high_limit
    low_limit = get_input("Podaj dolny limit")
    high_limit = get_input("Podaj gorny limit")
    data_input = convert_txt(data_file)
    data_input = np.array(data_input).astype(float)
    mean = calculate_mean(data_input)
    std_dev = calculate_Standard_dev(data_input)
    cp = calculate_Cp(high_limit, low_limit)
    cpk = calculate_Cpk(high_limit, low_limit)
    plot_hist(low_limit, high_limit)

def plot_hist(lowlimit, highlimit):
    # dist = pd.DataFrame(np.random.normal(loc=mean, scale=std_dev, size=(1000,2)))
    dist = pd.Series(data_input)
    dist.agg(['min', 'max', 'mean', 'std']).round(decimals=2)
    # print(dist)
    rmean = round(mean,3)
    rstd = round(std_dev,3)
    rcp = round(cp, 3)
    rcpk = round(cpk, 3)

    fig, ax = plt.subplots()
    plt.xticks(range(int(low_limit), int(high_limit), 20))
    plt.xlim(int(low_limit)*0.95, int(high_limit)*1.05)
    bin_width = 0.3
    n = math.ceil((dist.max() - dist.min())/bin_width)
    hist_title = "Mean: {} Std_dev: {} Cp: {} Cpk: {}".format(rmean,rstd,rcp,rcpk)

    title = ("Mean: %.3f" %mean, " Std_dev: %.3f" %std_dev, " Cp: %.3f" %cp, " Cpk: %.3f" %cpk)
    h_title = ""
    h_title = h_title.join(title)

    # dist.plot.kde(ax=ax, legend=False, title=("Mean: "+str(mean)+" Std_dev: "+str(std_dev)+" Cp: "+str(cp)+" Cpk: "+str(cpk)))
    dist.plot.kde(ax=ax, legend=False,
                  title=h_title)

    dist.plot.hist(density=True, ax=ax, bins=n)
    plt.grid(True)
    image_name = data_file.split('.').pop(0)
    plt.savefig(image_name+'.png')
    plt.show()

def convert_txt(input_file):
    try:
        with open(input_file, "r") as in_f:
            values = []
            for line in in_f:
                values.append(line.strip())
        return values
    except Exception as e:
        basic_error_handler("Can't access measurements file", e)
        return False

def get_input(question):
    while True:
        try:
            print(question)
            a = input()
            return float(a)
        except Exception as e:
            basic_error_handler("Can't cast to float. Did You type number?", e)
            continue
        else:
            break

def calculate_mean(measurements):
    try:
        mean = np.sum(measurements) / len(measurements)
        print("Mean:" + str(mean.round(2)))
        return mean
    except Exception as e:
        basic_error_handler("Can't calculate mean. Check input data!", e)
        return False

def calculate_Standard_dev(measurements):
    try:
        std_dev = float(np.std(measurements))
        print("Standard deviation:" + str(round(std_dev, 2)))
        return std_dev
    except Exception as e:
        basic_error_handler("Can't calculate std dev. Check input data!", e)
        return False

def calculate_Cp(usl, lsl):
    try:
        cp = (usl - lsl)/(std_dev)
        print("Cp: " + str(round(cp,2)))
        return cp
    except Exception as e:
        basic_error_handler("Can't calculate Cp. Check input data!", e)
        return False

def calculate_Cpk(usl, lsl):
    try:
        cpk = min(((mean - lsl)/(3*std_dev)), ((usl - mean)/(3*std_dev)))
        print("Cpk: " + str(round(cpk,2)))
        return cpk
    except Exception as e:
        basic_error_handler("Can't calculate Cpk. Check input data!", e)
        return False

def basic_error_handler(message, error, text = "", text1 = "", text2 = ""):
    print(message + "  | Error code: " + str(error))
    return

if __name__ == "__main__":
    init()
