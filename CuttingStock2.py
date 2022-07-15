#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 14:39:06 2022

@author: kobero
"""
from Cutting_Stock import *
import gurobipy as gp
import numpy as np
import math

class cuttingStock:
    def controllo(pattern,listaPattern):
        for i in range(0,listaPattern):
            flag2=True
            for j in range(0,listaPattern[i]):
                if pattern[j]!=listaPattern[i][j]:
                    flag2=False
                    break
            if flag2 == True:
                return True
        return False
                
    def __init__(self,instance,tagli=[]):
        self.size=instance.getSize()
        self.D=[]
        self.L=[]
        self.b=instance.getb()
        self.A=[]
        for i in instance.getA():
            self.A.append(i.copy())
        print("dimensi",len(self.A))
        for i in instance.getList():
            self.D.append(i.getDemand())
            self.L.append(i.getWeight())
        self.pattern=instance.getPattern().copy()
        self.cut=tagli.copy()
        """
        condizioni_ulteriori=[] #sottomatriceA
        vincoli_ulteriori=[]    #sottovettoreB
        disuguaglianza=[]       #condizione < = >
        for k in range (0,len(self.cut)):
            c=self.cut[k]
            for j in range (0,len(c.getPath())):
                condizione=[]
                if c.getPath()[j] not in self.pattern:
                    
                    self.pattern.append(c.getPath()[j])
                   
                    
                    for i in range(0,len(c.getPath()[j])):
                        self.A[i].append(c.getPath()[j][i])
                    condizione.append((len(self.pattern)-1,c.getCoef()[j]))
                else:
                     index=self.pattern.index(c.getPath()[j])
                     condizione.append((index,c.getCoef()[j]))
            condizioni_ulteriori.append(condizione)
            vincoli_ulteriori.append(c.getLimit())
            disuguaglianza.append(c.getcondizione())
        """
        
        self.model=gp.Model("cutting stock")
        self.model.setParam("OutputFlag",0)
        self.x=self.model.addVars(len(self.A[0]))
        fo=gp.LinExpr()
        for i in range(0,len(self.x)):
            fo.add(self.x[i],1)
        self.model.setObjective(fo,gp.GRB.MINIMIZE)
        
        #primo blocco di condizioni
        for i in range(0,len(self.A)):
            constr=gp.LinExpr()
            for j in range(0,len(self.A[i])):
                constr.add(self.x[j],self.A[i][j])
            self.model.addConstr(constr>=self.D[i])
        """   
        #secondo blocco di condizioni
        for i in range(0,len(condizioni_ulteriori)):
            constr=gp.LinExpr()
            for j in range(0,len(condizioni_ulteriori[i])):
                index=condizioni_ulteriori[i][j][0]
                coef=condizioni_ulteriori[i][j][1]
                constr.add(self.x[index],coef)
           
            if disuguaglianza[i]==">=":
                self.model.addConstr(constr>=vincoli_ulteriori[i])
            else:
                self.model.addConstr(constr<=vincoli_ulteriori[i])
        """
        #terzo blocco di condizioni di non negatività
        for i in range(0,len(self.A[0])):
            constr=gp.LinExpr()
            constr.add(self.x[i],1)
            self.model.addConstr(constr>=0)
        
    def creazioneModel(self):
        """
        condizioni_ulteriori=[] #sottomatriceA
        vincoli_ulteriori=[]    #sottovettoreB
        disuguaglianza=[]       #condizione < = >
        for k in range (0,len(self.cut)):
            c=self.cut[k]
            for j in range (0,len(c.getPath())):
                condizione=[]
                if c.getPath()[j] not in self.pattern:
                    self.pattern.append(c.getPath()[j])
                    for i in range(0,len(c.getPath()[j])):
            
                        self.A[i].append(c.getPath()[j][i])
                    condizione.append((len(self.pattern)-1,c.getCoef()[j]))
                else:
                     index=self.pattern.index(c.getPath()[j])
                     condizione.append((index,c.getCoef()[j]))
            condizioni_ulteriori.append(condizione)
            vincoli_ulteriori.append(c.getLimit())
            disuguaglianza.append(c.getcondizione())
        """
        self.model=gp.Model("cutting stock")
        self.model.setParam("OutputFlag",0)
        self.x=self.model.addVars(len(self.A[0]))
        
        fo=gp.quicksum(self.x)
        self.model.setObjective(fo,gp.GRB.MINIMIZE)
        
        #primo blocco di condizioni
        for i in range(0,len(self.A)):
            constr=gp.LinExpr()
            for j in range(0,len(self.A[i])):
                constr.add(self.x[j],self.A[i][j])
            self.model.addConstr(constr>=self.D[i])
        """    
        #secondo blocco di condizioni
        for i in range(0,len(condizioni_ulteriori)):
            constr=gp.LinExpr()
            for j in range(0,len(condizioni_ulteriori[i])):
                index=condizioni_ulteriori[i][j][0]
                coef=condizioni_ulteriori[i][j][1]
                constr.add(self.x[index],coef)
            if disuguaglianza[i]==">=":
                self.model.addConstr(constr>=vincoli_ulteriori[i])
            else:
                self.model.addConstr(constr<=vincoli_ulteriori[i])
        """
        #terzo blocco di condizioni di non negatività
        for i in range(0,len(self.A[0])):
            constr=gp.LinExpr()
            constr.add(self.x[i],1)
            self.model.addConstr(constr>=0)
        
    def solve(self):
        z=2
        while z>1:
            self.model.optimize()
            
            if self.model.getAttr("status")>=3:
                return -1
            y=self.model.getAttr("Pi", self.model.getConstrs()[0:len(self.L)])
           
            #vediamo se esistono ulteriori tagli ammissibili migliori
            pricing=gp.Model("pricing")
            pricing.setParam("OutputFlag",0)
            alfa=pricing.addVars(len(self.L),vtype=gp.GRB.INTEGER)
        
            fpricing= gp.LinExpr()
            for j in range (0,len(self.L)):
                fpricing.add(alfa[j],y[j])   #inverto la matrice
            pricing.setObjective(fpricing,gp.GRB.MAXIMIZE)
            #creo il vincolo del knapsack
            vincolo=gp.LinExpr()
            for j in range(0,len(self.L)):
                vincolo.add(alfa[j],self.L[j])
            pricing.addConstr(vincolo<=self.size)
            for i in range(0,len(self.L)):    
                pricing.addConstr(alfa[i]>=0,"c"+str(i)); #vincolo di non negatività
            pricing.optimize()
            z=pricing.objVal
            z=z-0.000000009
            if z>1:
                path=[]
                for i in range(0,len(self.A)):
                   self.A[i].append(int(alfa[i].X))
                   path.append(alfa[i].X)
                self.pattern.append(path)
                self.creazioneModel()
        return self.model.objVal    
def intero(x):
    for i in range(0,len(x)):
        if x[i].X!=math.ceil(x[i].X):
            return False
    return True
""" 
#primo tentativo di Branch&Bound 
def branchboubd(model,foAd=[],T=600000): 
    global xopt
    global zopt
    global crono
    if T<crono.current_time()-crono.start:
        return
    if foAd != []:
        fo=gp.LinExpr()
        fo.add(model.getVars()[foAd[1]],1)
        if foAd[0]==">=":
            model.addConstr(fo>=foAd[2])
        else:
            model.addConstr(fo<=foAd[2])
    model.optimize()
    z=model.objVal
    if z<0: #caso infeaseble
        return
    if intero(model.getVars()):
        if model.objVal<zopt:
            zopt=model.objVal
            xopt=[]
            for i in range(0,len(model.getVars())):
                xopt.append(model.getVars()[i])
        return
    if z>zopt:
        return
    x=model.getVars()
    for i in range(0,len(x)):
        if x[i].X!=math.ceil(x[i].X):
            fo1=i
            branchboubd(model.copy(),["<=",fo1,math.trunc(x[i].X)])
            branchboubd(model.copy(),[">=",fo1,math.ceil(x[i].X)])
"""
def fi(s):
    if(s>0):
        return s-math.trunc(s)
    else:
        x=-s
        return math.ceil(x)-x 
    
def gomoryCut(x,A,b,model):
    indexB=[]    #vettore degli indici in base
    indexN=[]    #vettore degli indici fuori base
    Xnb=[]
    Xb=[]
    for i in range(0,len(x)):
        if x[i].X>0:
            indexB.append(i)
            Xb.append(x[i])
        else:
            indexN.append(i)
            Xnb.append(x[i])
    B=[] #matrice della base
    for i in indexB:
        app=[]
        for j in range(0,len(A)):
            app.append(A[j][i])
        B.append(app)
    B=np.matrix(B)
    B=B.getT()
    BI=B.getI()
    N=[]#matrice delle variabili fuori base
    for i in indexN:
        app=[]
        for j in range(0,len(A)):
            app.append(A[j][i])
        N.append(app)
    N=np.matrix(N)
    N=N.getT()
    #check
    np.dot(BI,b)
    NB=np.dot(BI,N)

    for i in range(0,len(Xb)):
        if Xb[i].X!=math.trunc(Xb[i].X):
            lin=gp.LinExpr()
            for j in range(0,len(Xnb)):
                lin.add(Xnb[j],math.floor(NB.tolist()[i][j]))
            lin.add(Xb[i],1)
            model.addConstr(lin<=math.floor(x[indexB[i]].X))
            break
 
    for i in range(0,len(Xb)):
        if Xb[i].X!=math.trunc(Xb[i].X):
            lin=gp.LinExpr()
            for j in range(0,len(Xnb)):
                lin.add(Xnb[j],fi(NB.tolist()[i][j]))
            model.addConstr(lin>=fi(x[indexB[i]].X))
            break
    #model.optimize()
    return model

def gomoryCut1(model):
    indexB=[]    #vettore degli indici in base
    indexN=[]    #vettore degli indici fuori base
    Xnb=[]
    Xb=[]
    x=model.getVars()
    for i in range(0,len(x)):
        if x[i].X>0:
            indexB.append(i)
            Xb.append(x[i])
        else:
            indexN.append(i)
            Xnb.append(x[i])
    B=[] #matrice della base
    A=model.getA().toarray()
    b=[]
    for i in range(0,len(model.getConstrs())):
        b.append(model.getConstrs()[i].getAttr("RHS"))
    for i in indexB:
        app=[]
        for j in range(0,len(A)):
            app.append(A[j][i])
        B.append(app)
    B=np.matrix(B)
    B=B.getT()
    BI=B.getI()
    N=[]#matrice delle variabili fuori base
    for i in indexN:
        app=[]
        for j in range(0,len(A)):
            app.append(A[j][i])
        N.append(app)
    N=np.matrix(N)
    N=N.getT()
    #check
    np.dot(BI,b)
    NB=np.dot(BI,N)
    for i in range(0,len(Xb)):
        if Xb[i].X!=math.trunc(Xb[i].X):
            lin=gp.LinExpr()
            for j in range(0,len(Xnb)):
                lin.add(Xnb[j],math.floor(NB.tolist()[i][j]))
            lin.add(Xb[i],1)
            model.addConstr(lin<=math.floor(x[indexB[i]].X))
            break
    for i in range(0,len(Xb)):
        if Xb[i].X!=math.trunc(Xb[i].X):
            lin=gp.LinExpr()
            for j in range(0,len(Xnb)):
                lin.add(Xnb[j],fi(NB.tolist()[i][j]))
            model.addConstr(lin>=fi(x[indexB[i]].X))
            break
    return model

xopt=[]
zopt=0
crono=ChronoMeter()
def controllo(Q):
    for i in range(0,len(Q)):
        if Q[i]>=0:
            return False
    return True

def branchboundNotRecursive(model,T):
    global zopt
    global xopt
    global crono
    Q=[]
    puntiInteriPositivi=0
    m=0
    padre=[]
    LB=[]
    vbranch=[]
    valore=[]
    padre.append(0)
    LB.append(model.objVal)
    M=[]
    M.append(model)
    if LB[0]<zopt:
        x=model.getVars()
        for i in range(0,len(x)):
            if x[i].X!=math.trunc(x[i].X):
                Q.append(0)
                vbranch.append(i)
                valore.append(x[i].X)
                break
    while not controllo(Q) and crono.current_time()-crono.start<T:
        for i in range(0,len(Q)):
            if Q[i]>=0:
                t=Q[i]
                Q[i]=-1
                break
        h=vbranch[t]
        val=valore[t]
        for figlio in range(0,2):
            if figlio==0:
                padre.append(t)
                f=M[t].copy()
                x=f.getVars()
                fo=gp.LinExpr()
                fo.add(x[h],1)
                f.addConstr(x[h]<=math.trunc(val))
            else:
                padre.append(-t)
                f=M[t].copy()
                x=f.getVars()
                fo=gp.LinExpr()
                fo.add(x[h],1)
                f.addConstr(x[h]>=math.ceil(val))
            f.optimize()
            #f=gomoryCut1(f)
            #f.optimize()
            if f.getAttr("Status")<3:
                #print(f.objVal)
                m=m+1
                LB.append(f.objVal)
                if intero(f.getVars()) and f.objval<zopt:
                    zopt=f.objVal
                    xopt=[]
                    puntiInteriPositivi=puntiInteriPositivi+1
                    for i in range(0,len(f.getVars())):
                        xopt.append(f.getVars()[i])
                    print(crono.current_time()-crono.start)
                    for i in range(0,len(Q)):
                        if LB[Q[i]]>=zopt:
                            Q[i]=-1
                if LB[m]<zopt:
                    x=f.getVars()
                    for i in range(0,len(x)):
                        if x[i].X!=math.trunc(x[i].X):
                            Q.append(m)
                            vbranch.append(i)
                            valore.append(x[i].X)
                            break
                    M.append(f)
                    
def Algoritmo(path,T=120000):  
    global xopt
    global zopt
    global crono
    instance=lettoreCuttingPlain.Lettore(path)
    z=cuttingStock(instance)
    f=z.solve()           
    xopt=[]
    zopt=0
    for i in range(0,len(z.x)):
        zopt=zopt+math.ceil(z.x[i].X)
        xopt.append(math.ceil(z.x[i].X))
    print("Prima dei tagli di gomory",zopt)
    crono=ChronoMeter()
    crono.start()
    branchboundNotRecursive(z.model,T)
    return (zopt,xopt)


print(Algoritmo("./Falkenauer_CSP/Falkenauer_U/Falkenauer_u120_01.txt")[0])

"""
import os
List=os.listdir('./Falkenauer_CSP/Falkenauer_U')
z=[]
i=0
for path in List:
    print(i)
    print(path)
    z.append(Algoritmo("./Falkenauer_CSP/Falkenauer_U/"+path))
    print(z[i][0])
    i=i+1
"""    
    
"""
l=ChronoMeter()
l.start()
instance=lettoreCuttingPlain.Lettore('./Falkenauer_CSP/Falkenauer_U/Falkenauer_u120_00.txt')
z=cuttingStock(instance)
f=z.solve()
s=0
xopt=[]
for i in range(0,len(z.x)):
    s=s+math.ceil(z.x[i].X)
    xopt.append(math.ceil(z.x[i].X))
print("Prima dei tagli di gomory",s)
zopt=s

m=gomoryCut(z.x, z.A, z.D,z.model)
s=0
for i in range(0,len(z.x)):
    s=s+math.ceil(z.x[i].X)
print("dopo primo taglio di gomory",s)
for i in range(0,4000):
    b=[]
    for i in range(0,len(m.getConstrs())):
        b.append(m.getConstrs()[i].getAttr("RHS"))
    m=gomoryCut(m.getVars(),m.getA().toarray(),b, m)
print(m.objVal)
print(f)
s=0
varss=m.getVars()
y=[]

for i in range(0,len(varss)):
    n=math.ceil(varss[i].X)
    s=s+n
l.stop()
print("dopo dei tagli di gomory",s)
y=cuttingStockSolver(instance)
y.solve()
print(l.getDurate())
"""