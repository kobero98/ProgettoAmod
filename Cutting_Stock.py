#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 17:42:58 2022

@author: kobero
"""
from Utils import *
import gurobipy as gp
import math as math

class cuttingStockSolver:
    
    def __init__(self,instance):
        self.pattern=[]
        self.size=instance.getSize()
        self.L=[]
        self.b=[]
        for s in instance.getList():
            self.L.append(s.getWeight())
            self.b.append(s.getDemand())
        self.Iterazioni=0
        self.Tempo=0
        self.ErroreAssoluto=0
        self.ErroreRelativo=0
        self.soluzione=0
        self.soluzioneRilassamento=0
        self.soluzioneOttimaIntera=0
    def roundingUP(self,x):
        y=0
        for z in range(0,len(x)):
            y=math.ceil(x[z].X)+y
        return y
    
    def getStatistic(self):
        return (self.size,len(self.L),self.Iterazioni,self.ErroreAssoluto,
                self.ErroreRelativo,self.Tempo,self.soluzione,self.soluzioneRilassamento,
                self.soluzioneOttimaIntera
                )

        
    def solve(self,vincoliIniziali=[]):
        #size=5600
        #L=[1300,1520,1560,1710,1820,1880,1930,2000,2050,2100,2140,2150,2200]
        #b=[22,25,12,14,18,18,20,10,12,14,16,18,20]
        size=self.size
        L=self.L
        b=self.b
        M=len(L)
        
            
        cronometro=ChronoMeter()
        #prima soluzione di base
        #algoritmo greedy per trovare M pattern ammissibili
        cronometro.start()
        A=[]
        for i in range (0,M):
            pattern=[0]*M
            pattern[i]=math.trunc(size/L[i])
            A.append(pattern)
        z=2
        count=0
        while z>1:# and sol1 != sol:
            count=count+1
            self.cutting=gp.Model("cutting-stock")
            pricing=gp.Model("pricing")
            self.cutting.setParam("OutputFlag",0)
            pricing.setParam("OutputFlag",0)
            #trovati i pattern iniziali posso cercare la soluzione con questi pattern
            #costruisco il problema di cutting stock
            x=self.cutting.addVars(len(A))
            
            #funzione obbiettivo
            fo= gp.LinExpr()
            for j in range (0,len(A)):
                fo.add(x[j],1)   #inverto la matrice
            self.cutting.setObjective(fo,gp.GRB.MINIMIZE)
            #vincoli
            for i in vincoliIniziali:
                self.cutting.addConstr(i,"")
            for i in range (0,M):
                condizione= gp.LinExpr()
                for j in range (0,len(A)):
                    condizione.add(x[j],A[j][i])   #inverto la matrice
                self.cutting.addConstr(condizione>=b[i],str(i))
            #for i in range(0,len(A)):    
            #    cutting.addConstr(x[i]>=0,"c"+str(i)); #vincolo di non negatività
            self.cutting.optimize()
            
            #ora si passa a trovare i gamma
            y=self.cutting.getAttr("Pi", self.cutting.getConstrs())
            
            
            
            #vediamo se esistono ulteriori tagli ammissibili migliori
            alfa=pricing.addVars(M,vtype=gp.GRB.INTEGER)
            
            fpricing= gp.LinExpr()
            for j in range (0,M):
                fpricing.add(alfa[j],y[j])   #inverto la matrice
            pricing.setObjective(fpricing,gp.GRB.MAXIMIZE)
            #creo il vincolo del knapsack
            vincolo=gp.LinExpr()
            for j in range(0,M):
                vincolo.add(alfa[j],L[j])
            pricing.addConstr(vincolo<=size)
            for i in range(0,M):    
                pricing.addConstr(alfa[i]>=0,"c"+str(i)); #vincolo di non negatività
            pricing.optimize()
            app=[]
            for i in range(0,M):
                app.append(alfa[i].X)
            if app in A:
                break
            A.append(app)
            z=pricing.objVal
           # z=z-0.000000000000009 #evita il loop di soluzioni che migliorano solo di 10^-9 e che fanno ciclare il while all'infinito
           # z=z-0.000000000009
        #faccio il roundin down della soluzione e ne calcolo la soluzione
        y=self.roundingUP(x)
        cronometro.stop()
        c=[]
        for i in range(0,len(x)):
            c.append(x[i].X)
        #calcolo l'ottimo con la matrice A
        cuttingOPT=gp.Model()
        cuttingOPT.setParam("OutputFlag",0)
        x=cuttingOPT.addVars(len(A),vtype=gp.GRB.INTEGER)
        fo= gp.LinExpr()
        for j in range (0,len(A)):
            fo.add(x[j],1)   #inverto la matrice
        cuttingOPT.setObjective(fo,gp.GRB.MINIMIZE)
         #vincoli
        for i in range (0,M):
            condizione= gp.LinExpr()
            for j in range (0,len(A)):
                condizione.add(x[j],A[j][i])   #inverto la matrice
            cuttingOPT.addConstr(condizione>=b[i],str(i))
        for i in range(0,len(A)):    
            cuttingOPT.addConstr(x[i]>=0,"c"+str(i)); #vincolo di non negatività
        cuttingOPT.optimize()
        self.ErroreRelativo=(cuttingOPT.objVal-y)/cuttingOPT.objVal
        self.ErroreAssoluto=cuttingOPT.objVal-y
        self.Tempo=cronometro.getDurate()
        self.Iterazioni=count
        self.soluzione=y
        self.soluzioneRilassamento=self.cutting.objVal
        self.soluzioneOttimaIntera=cuttingOPT.objVal
        self.A=cuttingOPT.objVal
        return self.cutting




