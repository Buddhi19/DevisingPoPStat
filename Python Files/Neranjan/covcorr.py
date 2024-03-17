'''''''''''''''''''''''# Statistical messuares'''''''''''''''''''''''''''
import pandas as pd
import numpy as np
from ConstructCountries import get_names_and_data
from scipy.spatial.distance import euclidean
import csv
from numpy.linalg import norm
from scipy.special import rel_entr
import math
from dictances import bhattacharyya, bhattacharyya_coefficient
from scipy.stats import wasserstein_distance
#%%
path = 'D:/COVID-NER/pop pyramid/Pyramid/POPU_data/'
data = get_names_and_data()
county, country_name_map = data[:2]
path1 = 'D:/COVID-NER/pop pyramid/Pyramid/covid_final_date.csv'
df = pd.read_csv(path1)
df2=df['location'].tolist()

#%%
def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result
S=common_elements(county,df2)
df2=np.array(df2)
where = []
for i in range (len(S)):
    name = S[i]
    #print(name+'done')
    boolean = (name == df2)
    #print(boolean)
    iden = np.where(boolean)[0]
    #print(iden)
    where.append(iden[0])
#%%    
POP_M=[]
POP_F=[]
POP_T=[]

for i in range(len(S)):
    file_name = path + S[i] + '_population.csv'
    df1 = pd.read_csv(file_name)
    '''# Male Population analysis'''
    male = np.array(df1[0:])[:,0]
    '''# Normalize the population'''
    male_n=male/sum(male,0)
    POP_M.append(male_n)
    
    '''path_header = "D:/COVID-NER/pop pyramid/Pyramid/"
    with open(path_header+'POP_M.csv', 'w') as f:
         write = csv.writer(f)
         write.writerows(POP_M)'''

    '''# Female Population analysis'''
    female = np.array(df1[0:])[:,1]
    '''# Normalize the population'''
    female_n = female / sum(female, 0)
    POP_F.append(female_n)

    '''# Total Population analysis'''
    total = np.array(df1[0:])[:,2]
    '''# Normalize the population'''
    total_n = total / sum(total, 0)
    POP_T.append(total_n)

''' # Remove Europe population '''
POP_M=np.concatenate((POP_M[0:54], POP_M[55:]), axis=0)
POP_F=np.concatenate((POP_F[0:54], POP_F[55:]), axis=0)
POP_T=np.concatenate((POP_T[0:54], POP_T[55:]), axis=0)
#pd.DataFrame(POP_M).to_csv("D:/COVID-NER/pop pyramid/Pyramid/POP_M.csv",header=False)
'''# Niger Referencing '''
POP_Mref=POP_M[116]/sum(POP_M[116],0)
POP_Fref=POP_F[116]/sum(POP_F[116],0)
POP_Tref=POP_T[116]/sum(POP_T[116],0)

''' <<<<<<<<<<<< Euclidean Distance for all datasets >>>>>>>>>>>>>'''
M_euc=[]
F_euc=[]
T_euc=[]
print(POP_F.shape)
for j in range(len(POP_F)):
    M1_euc = euclidean(POP_M[j],POP_Mref)  # For Men
    F1_euc = euclidean(POP_F[j], POP_Fref)  # For Women
    T1_euc = euclidean(POP_T[j], POP_Tref)  # For Total
    M_euc.append(M1_euc)
    F_euc.append(F1_euc)
    T_euc.append(T1_euc)
''' <<<<<<<<<<<< KL Divergence (Q || P) for all datasets >>>>>>>>>>>>>'''
M_KL=[]
F_KL=[]
T_KL=[]
for j in range(len(POP_F)):
    M1_KL=sum(rel_entr(POP_M[j],POP_Mref))
    F1_KL=sum(rel_entr(POP_F[j],POP_Fref))
    T1_KL=sum(rel_entr(POP_T[j],POP_Tref))
    M_KL.append(M1_KL)
    F_KL.append(F1_KL)
    T_KL.append(T1_KL)

''' <<<<<<<<<<<< Hellinger distance >>>>>>>>>>>>>'''
def H(p, q):
  # distance between p an d
  # p and q are np array probability distributions
  n = len(p)
  sum = 0.0
  for i in range(n):
    sum += (np.sqrt(p[i]) - np.sqrt(q[i]))**2
  result = (1.0 / np.sqrt(2.0)) * np.sqrt(sum)
  return result

M_H=[]
F_H=[]
T_H=[]
for j in range(len(POP_F)):
    M1_H=H(POP_M[j],POP_Mref)
    F1_H=H(POP_F[j],POP_Fref)
    T1_H=H(POP_T[j],POP_Tref)
    M_H.append(M1_H)
    F_H.append(F1_H)
    T_H.append(T1_H)
    
''' <<<<<<<<<<<< Wasserstein distance >>>>>>>>>>>>>'''
M_WD=[]
F_WD=[]
T_WD=[]
for j in range(len(POP_F)):
    M1_WD=wasserstein_distance(POP_M[j],POP_Mref)
    F1_WD=wasserstein_distance(POP_F[j],POP_Fref)
    T1_WD=wasserstein_distance(POP_T[j],POP_Tref)
    M_WD.append(M1_WD)
    F_WD.append(F1_WD)
    T_WD.append(T1_WD)


'''<<<<<<<<<<<<   new_cases_smoothed_per_million >>>>>>>>>>>>>>>>'''
Cs=[]
Sm=df['new_cases_smoothed_per_million']
for i in range (len(S)):
    E=Sm[where[i]]
    Cs.append(E)
Cs=np.array(Cs)
Cs[np.isnan(Cs)]=0.0001
Cs[Cs == 0] = 0.0001
CS=np.concatenate((Cs[0:54], Cs[55:]), axis=0)
CS_lg=[]
for i in range(len(CS)):
    lg=math.log(CS[i])
    CS_lg.append(lg)
#%%
'''<<<<<<<<<<<<< PLOT SECTION >>>>>>>>>>>>'''
import matplotlib.pyplot as plt
for i in range(3):
    plt.figure(i)
    x1=[M_KL,F_KL,T_KL]
    colors=['red','blue','green']
    plt.scatter(x1[i],CS_lg,color=colors[i])
    plt.xlabel('KL Divergence')
    plt.ylabel('new_cases_smoothed_per_million/log')
    label=['Male_Population','Female_Population','Total_Population']
    plt.title(label[i])
    a, b = np.polyfit(np.array(x1[i]), CS_lg, 1)
    plt.plot(np.array(x1[i]), a*np.array(x1[i])+b)
    plt.show()
    
    plt.figure(i+3)
    x2=[M_H,F_H,T_H]
    plt.scatter(x2[i],CS_lg,color=colors[i])
    plt.xlabel('Hellinger distance')
    plt.ylabel('new_cases_smoothed_per_million/log')
    plt.title(label[i])
    a, b = np.polyfit(np.array(x2[i]), CS_lg, 1)
    plt.plot(np.array(x2[i]), a*np.array(x2[i])+b)
    plt.show()
    
    plt.figure(i+6)
    x3=[M_WD,F_WD,T_WD]
    plt.scatter(x3[i],CS_lg,color=colors[i])
    plt.xlabel('Wasserstein distance')
    plt.ylabel('new_cases_smoothed_per_million/log')
    plt.title(label[i])
    a, b = np.polyfit(np.array(x3[i]), CS_lg, 1)
    plt.plot(np.array(x3[i]), a*np.array(x3[i])+b)
    plt.show()
  
    
    plt.figure(i+9)
    x4=[M_euc,F_euc,T_euc]
    plt.scatter(x4[i],CS_lg,color=colors[i])
    plt.xlabel('Euclidean distance')
    plt.ylabel('new_cases_smoothed_per_million/log')
    plt.title(label[i])
    a, b = np.polyfit(np.array(x4[i]), CS_lg, 1)
    plt.plot(np.array(x4[i]), a*np.array(x4[i])+b)
    plt.show()
#%%
''' <<<<<<<<<<< Correlation Calculation >>>>>>>>>>>>>> '''
Cr1=np.corrcoef(x1[0],CS_lg)
Cr2=np.corrcoef(x1[1],CS_lg)
Cr3=np.corrcoef(x1[2],CS_lg)

country_count = len(S)
corr_mat, pop_dist_mat = np.zeros((country_count, country_count)), np.zeros((country_count, country_count))
C_M=[]
for j in range (len(POP_T)):
    corr_mat = np.corrcoef(POP_T[j].T, POP_Tref)
    C_M.append(corr_mat)
Co_M=np.array(C_M)
gg=Co_M[:,1,:]
cx=gg[:,0];
Rel=cx[ np.where( cx > 0.7 ) ].shape
