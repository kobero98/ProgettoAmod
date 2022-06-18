#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:11:14 2022

@author: kobero

"""
import time
import math

class lettoreCuttingPlain:
    def Lettore(path):
        file=open(path,"r")
        n=int(file.readline())
        size=int(file.readline())
        L=[]
        for i in range(0,int(n)):
            w=""
            d=""
            f=True
            while f:
                s=file.read(1)
                if s=='\t':
                    f=False
                else:
                    w=w+s
            f=True
            while f:
                s=file.read(1)
                if s=='\n':
                    f=False
                else:
                    d=d+s
            L.append(objectToStock(int(w),int(d)))                
        return cuttingStockInstance(L, size)
class cut:
    def __init__(self,Coefficienti,pattern,condizione,limite):
        self.Coefficienti=Coefficienti
        self.pattern=pattern
        self.condizione=condizione
        self.Limite=limite
    def getCoef(self):
        return self.Coefficienti
    def getPath(self):
        return self.pattern
    def getcondizione(self):
        return self.condizione
    def getLimit(self):
        return self.Limite
        
class ChronoMeter:
    start = 0
    end = 0
    press= False
    def start(self):
        if not self.press:
            self.press=True
            self.start = self.current_time()

    def stop(self):
        if self.press:
            self.end = self.current_time()
            self.press=False

    def getDurate(self):
        if self.end>=self.start:
            return self.end - self.start
        return 0
    def current_time(self):
        return round(time.time() * 1000)   
        
class objectToStock:
    def __init__(self,weight,demand):
        self.weight=weight
        self.demand=demand
    def getDemand(self):
        return self.demand
    def getWeight(self):
       return self.weight
    
class cuttingStockInstance:
    def __init__(self,listObjectToStock,size):
        self.size=size
        self.listObjectToStock=listObjectToStock
        self.A=[]
        self.Pattern=[]
        for i in range (0,len(self.listObjectToStock)):
            pattern=[0]*len(self.listObjectToStock)
            pattern[i]=math.trunc(self.size/self.listObjectToStock[i].getWeight())
            self.A.append(pattern.copy())
            self.Pattern.append(pattern.copy())
    def getSize(self):
        return self.size
    def getList(self):
        return self.listObjectToStock
    def getPattern(self):
        return self.Pattern.copy()
    def getA(self):
        return self.A.copy()
    def getb(self):
        b=[]
        return b
 #   def getA(self):
 #       A1=[]
 #       for j in range(0,len(self.A[0])):
 #           A2=[]
 #           A1.append(A2)
 #       for i in range(0,len(self.A)):
 #           for j in range(0,len(self.A[i])):
 #               A1[j].append(self.A[i][j])
 #       for i in range(0,len(A1[0])):
 #           A1.append([0]*len(A1[0]))
 #           A1[len(A1)-1][i]=1
 #       return A1
 #   def getb(self):
 #       b=[]
 #       for i in range(0,len(self.listObjectToStock)):
 #           b.append(self.listObjectToStock[i].getDemand())
 #       for i in range(0,len(self.listObjectToStock)):
 #           b.append(0)
 #       return b
