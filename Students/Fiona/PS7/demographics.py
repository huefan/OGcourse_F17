import time
import numpy as np
import pandas as pd
import scipy.optimize as opt
import scipy.interpolate as itp
from functools import reduce
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

#0,0,0,0,0,0,0,0,0,
age = np.array([9,10, 12, 16, 18.5, 22, 27, 32, 37, 42, 47,55, 56])
fert = np.array([0.0,0.0, 0.3, 12.3, 47.1, 80.7, 105.5, 98, 49.3, 10.4, 0.8,0.0, 0.0])/2000

def get_fert(tot_per,fert_graph, age_d = age, fert_d = fert):

    f = itp.interp1d(age_d, fert_d, kind='cubic')
    age_sm = np.linspace(1, 100, 100000)
    fert_sm = np.zeros(age_sm.shape)
    fert_sm[((age_sm >= 9) & (age_sm <= 56))] = f(age_sm[((age_sm >= 9) & (age_sm <= 56))])
    step = int(round(100/tot_per))
    numper = int (100/step)
    age_tp = np.fromfunction(lambda x: x*step, (numper,))
    np.append(age_tp,100)
    fert_tp = np.zeros (age_tp.shape)
    fert_tp[((age_tp >= 9) & (age_tp <= 56))] = f(age_tp[((age_tp >= 9) & (age_tp <= 56))])

    # for i in range (len(age_d)-1):
    #     snip = fert_sm[i:i+step]
    #     snip[0] = 1-snip[0]
    #     fert_tp[i] = 1- reduce (lambda x,y: x * (1-y), snip)
    np.append(fert_tp,[0])
    # print(age_tp)
    # print(fert_sm)
    # print (fert_tp)
    if fert_graph:
        cur_path = os.path.split(os.path.abspath(__file__))[0]
        output_fldr = "images_dem"
        output_dir = os.path.join(cur_path, output_fldr)
        if not os.access(output_dir, os.F_OK):
            os.makedirs(output_dir)


        fig, ax = plt.subplots()
        #'r-',
        ax.plot(age_sm, fert_sm, label="100 periods interpolated, fine")
        ax.scatter(age_tp, fert_tp, color='red', label=f"{tot_per} periods interpolated")
        #     plt.plot(x_vec, y_vec)
        plt.title(f'Fertility Rate', fontsize=20)
        plt.grid(b=True, which='major', color='0.65', linestyle='-')
        plt.xlabel('Age')
        plt.ylabel('%')
        plt.legend()
        # plt.show()
        output_path = os.path.join(output_dir, f'fert_rate_{tot_per}')
        plt.savefig(output_path)
        plt.close()
    # print (fert_tp.shape)
    return fert_tp

def get_mort(tot_per, mort_graph, file_name='mort_rates2011.csv'):
    df = pd.read_csv(file_name)

    df = df[['Age', 'Male Mort. Rate', 'Num. Male Lives', 'Female Mort. Rate', 'Num. Female Lives']]
    df.rename(columns={'Age':'age', 'Male Mort. Rate':'mort_m', 'Num. Male Lives': 'num_m', 'Female Mort. Rate': 'mort_f',
                       'Num. Female Lives': 'num_f'}, inplace=True)
    df['num_m']= [float(''.join(x.split(","))) for x in df['num_m']]
    df['num_f'] = [float(''.join(x.split(","))) for x in df['num_f']]
    df.astype('float64')
    df['mort_tot'] = (df.mort_m * df.num_m + df.mort_f * df.num_f) / (df.num_m+df.num_f)
    infmort_rate = df.mort_tot[0]
    df = df[0:113]
    age_d = df.age[1:]
    mort_d = df.mort_tot[1:]
    f = itp.interp1d(age_d, mort_d, kind='cubic')
    age_sm = np.linspace(1, 100, 100000)
    mort_sm = f(age_sm)
    age_100 = np.linspace(1, 100, 100)
    mort_100 = f(age_100)
    # np.savetxt("mort_100.csv", mort_100, delimiter=",")
    # print (f'mort_100: {mort_100.shape}')
    step = int(round(100 / tot_per))
    numper = int(100 / step)
    age_tp = np.fromfunction(lambda x: (x) * step, (numper-1,))

    age_tp=np.concatenate((age_tp, np.array([100])))
    # print(f'steP: {step}, numper:{numper}, agetp.shape:{age_tp}')
    mort_tp = np.zeros(age_tp.shape)
    mort_tp[0] = mort_100[0]
    for i in range (1, len(age_tp)):
        print (step * i)
        snip = mort_100[step * i:step * i + step]
        # print(snip)
        snip[0] = 1-snip[0]
        mort_tp[i] = 1- reduce (lambda x,y: x * (1-y), snip)
        print (f'mort_tp: {mort_tp[i]}', '\n')

    mort_tp[-1] = 1
    # print (mort_tp[-1])
    if mort_graph:
        cur_path = os.path.split(os.path.abspath(__file__))[0]
        output_fldr = "images_dem"
        output_dir = os.path.join(cur_path, output_fldr)
        if not os.access(output_dir, os.F_OK):
            os.makedirs(output_dir)


        fig, ax = plt.subplots()
        #'r-',
        ax.plot(age_sm, mort_sm, label="100 periods interpolated, fine")
        ax.scatter(age_tp, mort_tp, color='red', label=f"{tot_per} periods interpolated")
        #     plt.plot(x_vec, y_vec)
        plt.title(f'Mortality Rate', fontsize=20)
        plt.grid(b=True, which='major', color='0.65', linestyle='-')
        plt.xlabel('Age')
        plt.ylabel('%')
        plt.legend()
        # plt.show()
        output_path = os.path.join(output_dir, f'mort_rate_{tot_per}')
        plt.savefig(output_path)
        plt.close()
    return mort_tp, infmort_rate


def get_imm_resid (tot_per, beg_yr_demog, end_yr_demog, imm_graph):
    pass

def get_pop_objs(E,S,T,min_yr,max_yr, curr_yr):
    pass

# get_fert(80, True)
# get_fert(20, True)
mort_rates, infmort_rate =get_mort(100, True)
mort_rates, infmort_rate =get_mort(80, True)
mort_rates, infmort_rate =get_mort(20, True)

print (infmort_rate, mort_rates)
print (mort_rates.shape)