import glob
import cv2
import numpy as np
import pandas as pd
cv_img=[]
for img in glob.glob("C:/Users/AI4COVID_PROJ/Downloads/HSI_Images-20230202T180806Z-001/HSI_Images/HSV/H_A/*.JPG"):
    n=cv2.imread(img)
    cv_img.append(n)
S=[]
for i in range(len(cv_img)):
    s=np.reshape(cv_img[i],[22500,3])
    S.extend(s) 
    

k=np.array(S)
K=k[1:k.shape[0]:15,:]
pd.DataFrame(K).to_csv("D:/Fish/H_A.csv")