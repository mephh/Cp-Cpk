import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm
import math

data_file = "inceon.txt"

def init():
    global mean, std_dev, cp, cpk, data_input, low_limit, high_limit #do przerobienia, na globalach aby bylo, lepiej przekazywac zmienne do funkcji
    low_limit = get_input("Podaj dolny limit")
    high_limit = get_input("Podaj gorny limit")
    data_input = convert_txt(data_file) #przepisanie pliku z pomiarami do listy
    data_input = np.array(data_input).astype(float) #przepisanie do ciagu numpy jako float, inaczej wyskoczy blad przy tworzeniu serii ponizej
    mean = calculate_mean(data_input)
    std_dev = calculate_Standard_dev(data_input)
    cp = calculate_Cp(high_limit, low_limit)
    cpk = calculate_Cpk(high_limit, low_limit)  # chyba lepiej przerobic to na 1 funkcje, TODO!
    plot_hist(low_limit, high_limit)

def plot_hist(lowlimit, highlimit):
    dist = pd.Series(data_input)                #swtorzenie serii bo dane 1 wymiarowe

    fig, ax = plt.subplots()                    #stworzenie pustego wykresu
    plt.xticks([lowlimit, highlimit])           #punkty na osi x
    plt.xlim(int(low_limit)*0.7, int(high_limit)*1.3)   #min i max na osi x
    bin_width = (max(dist)-min(dist))/divide_by(mean)   #proba automatycznego dobrania szerokosci binu - nie dziala jeszcze w tej postaci
    print(bin_width)
    # n = math.ceil(dist.max() - dist.min()/bin_width)
    n = np.arange(min(dist), max(dist) + bin_width, bin_width)  #wyliczenie ilosci binow
    title = ("Mean: %.3f" %mean, " Std_dev: %.3f" %std_dev, " Cp: %.3f" %cp, " Cpk: %.3f" %cpk)
    h_title = ""
    h_title = h_title.join(title)               #join bo title powyzej jest lista
    dist.plot.kde(ax=ax, legend=False, title=h_title) #kernel density estimate - krzywa na wykresie
    dist.plot.hist(density=True, ax=ax, bins=n, rwidth=0.95)    #rysuj na ax, szerokosc binu 95%

    plt.grid(True)
    plt.axvline(lowlimit)                       #linie proste na wykresie oznaczajace limity
    plt.axvline(highlimit)

    image_name = data_file.split('.').pop(0)
    plt.savefig(image_name+'.png')
    plt.show()

def convert_txt(input_file):
    try:    #przepisanie pliku do listy
        with open(input_file, "r") as in_f:
            values = []
            for line in in_f:
                values.append(line.strip())
        return values
    except Exception as e:
        basic_error_handler("Can't access measurements file", e)
        return False

def get_input(question):
    while True:         #stackoverflow :) sprawdzanie czy wprowadzono liczbe, brak innych zabezpieczen
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

def divide_by(string_to_parse): #do wyznaczenia liczby binow
    value = ""
    string_to_parse = check_if_text(string_to_parse)
    try:
        value = len(string_to_parse.split('.').pop(0))
        print("value:" +str(value))
    except:
        value = len(string_to_parse)
    return value

def check_if_text(string_to_parse):     #convert na stringa
    try:
        if(type(string_to_parse) != "str"):
            string_to_parse = str(string_to_parse)
        return string_to_parse
    except Exception:
        print("cant parse variable to string: "+ str(Exception))
        return None

def basic_error_handler(message, error, text = "", text1 = "", text2 = ""):
    print(message + "  | Error code: " + str(error))
    return

if __name__ == "__main__":
    init()
