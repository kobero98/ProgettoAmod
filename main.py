#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 23:57:14 2022

@author: kobero
"""



from CuttingStock2 import *
import os

Algoritmo("./Falkenauer_CSP/Falkenauer_U/Falkenauer_u500_11.txt")

"""
List=os.listdir('./Falkenauer_CSP/Falkenauer_U')
z=[]
for path in List:
    print(path)
    z.append(Algoritmo("./Falkenauer_CSP/Falkenauer_U/"+path))
"""
"""
from Cutting_Stock import *
import os
#file=open("result1.csv","w")
List=os.listdir('./Falkenauer_CSP/Falkenauer_U')
file.write("Nome,PaperRollSize,N_Tagli,iterazioni,ErroreAssoluto,ErroreRelativo,Tempo,soluzioneTrovata,SoluzioneTrovataRilassata,SoluzioneInteraConLeColonne\n")
for path in List:
    print(path)
    #instance=lettoreCuttingPlain.Lettore("/Users/kobero/Desktop/Falkenauer_CSP/Falkenauer_U/Falkenauer_u1000_00.txt")
    instance=lettoreCuttingPlain.Lettore('./Falkenauer_CSP/Falkenauer_U/'+path)
    z=cuttingStockSolver(instance)
    model=z.solve()
    y=z.getStatistic()
   # file.write(path)
   # file.write(",")
   # for i in range(0,len(y)):
   #     file.write(str(y[i]))
   #     file.write(",")
   # file.write("\n")
file.close()

file=open("result2.csv","w")
List=os.listdir('./Falkenauer_CSP/Falkenauer_T')
file.write("Nome,PaperRollSize,N_Tagli,iterazioni,ErroreAssoluto,ErroreRelativo,Tempo,soluzioneTrovata,SoluzioneTrovataRilassata,SoluzioneInteraConLeColonne\n")
for path in List:
    break
    print(path)
    #instance=lettoreCuttingPlain.Lettore("/Users/kobero/Desktop/Falkenauer_CSP/Falkenauer_U/Falkenauer_u1000_00.txt")
    instance=lettoreCuttingPlain.Lettore('./Falkenauer_CSP/Falkenauer_T/'+path)
    z=cuttingStockSolver(instance)
    z.solve()
    y=z.getStatistic()
    file.write(path)
    file.write(",")
    for i in range(0,len(y)):
        file.write(str(y[i]))
        file.write(",")
    file.write("\n")
file.close()
"""
