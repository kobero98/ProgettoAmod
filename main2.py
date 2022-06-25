#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:08:24 2022

@author: kobero
"""

from CuttingStock import cuttingStock   
from Utils import lettoreCuttingPlain
import os

def main():
    file=open("result2.csv","w")
    dir1='./Falkenauer_CSP/Falkenauer_T'
    List=os.listdir(dir1)
    file.write("Nome,PaperRollSize,N_Tagli,numero Colonne,Errore Assoluto RoundUp,Errore Relativo RoundUp,Errore Assoluto branch,Errore Relativo branch,Tempo generazione Colonne,Tempo Soluzione migliorata,Tempo Terminazione Algoritmo,soluzione rilassamento,soluzione Ottima,soluzioneTrovata,soluzione ottimo dal RoundUp\n")
    indice=0
    for path in List:
        print(str(indice)+")"+path)
        instance=lettoreCuttingPlain.Lettore(dir1+"/"+path)
        z=cuttingStock(instance)
        z.Algoritmo(path)
        y=z.statistic()
        for i in range(0,len(y)):
            file.write(str(y[i]))
            file.write(",")
        file.write("\n")
        file.flush()
        indice=indice+1
    file.close()
        
main()