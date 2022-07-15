#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:30:24 2022

@author: kobero
"""

from Utils import ChronoMeter
from Utils import lettoreCuttingPlain
import gurobipy as gp
import numpy as np
import math

class cuttingStock:
    def __init__(self,instance):
        #variabili dei dati statistici
        self.namePath=""
        self.zRilassamentoLineare=0
        self.RoundupZ=0
        self.ZPLIColonneTrovate=0
        self.zopt=0
        self.xopt=[]
        self.TempoGenerazioneColonne=0
        self.TempoSoluzioneMigliore=0
        self.TempoTerminazione=0
        self.NumeroColonne=0
        self.ErroreAssolutoRoundUp=0
        self.ErroreRelativoRoundUp=0
        self.ErroreAssolutoBranch=0
        self.ErroreRelativoBranch=0
        self.crono=ChronoMeter()
        self.soluzioneOttima=0
        
        #variabili del Modello
        self.size=instance.getSize()
        self.D=[]
        self.L=[]
        self.b=instance.getb()
        self.A=[]
        for i in instance.getA():
            self.A.append(i.copy())
        for i in instance.getList():
            self.D.append(i.getDemand())
            self.L.append(i.getWeight())
        self.pattern=instance.getPattern().copy()

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

        #secondo blocco di condizioni di non negatività
        for i in range(0,len(self.A[0])):
            constr=gp.LinExpr()
            constr.add(self.x[i],1)
            self.model.addConstr(constr>=0)
        
    def creazioneModel(self):
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
            
        #secondo blocco di condizioni di non negatività
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
                self.NumeroColonne=self.NumeroColonne+1
                path=[]
                for i in range(0,len(self.A)):
                   self.A[i].append(int(alfa[i].X))
                   path.append(alfa[i].X)
                self.pattern.append(path)
                self.creazioneModel()
        #calcolo l'ottimo con la matrice A
        cuttingOPT=gp.Model()
        cuttingOPT.setParam("OutputFlag",0)
        xpli=cuttingOPT.addVars(len(self.A[0]),vtype=gp.GRB.INTEGER)
        #funzione Obiettivo
        fo=gp.quicksum(xpli) 
        cuttingOPT.setObjective(fo,gp.GRB.MINIMIZE)
        #vincoli
        for i in range (0,len(self.A)):
            condizione= gp.LinExpr()
            for j in range (0,len(self.A[i])):
                condizione.add(xpli[j],self.A[i][j])   #inverto la matrice
            cuttingOPT.addConstr(condizione>=self.D[i],str(i))
        for i in range(0,len(xpli)):    
            cuttingOPT.addConstr(xpli[i]>=0,"c"+str(i)); #vincolo di non negatività
        cuttingOPT.optimize()
        self.ZPLIColonneTrovate=cuttingOPT.objVal
        return self.model.objVal
    
    def intero(self,x):
        for i in range(0,len(x)):
            if x[i].X!=math.ceil(x[i].X):
                return False
        return True
    
    def fi(self,s):
        if(s>0):
            return s-math.trunc(s)
        else:
            x=-s
            return math.ceil(x)-x 
        
        
# funzione implementata ma ancora non implementata come miglioria del codice
    def gomoryCut1(self,model):
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
                print(lin)
                model.addConstr(lin<=math.floor(x[indexB[i]].X))
                break
        for i in range(0,len(Xb)):
            if Xb[i].X!=math.trunc(Xb[i].X):
                lin=gp.LinExpr()
                for j in range(0,len(Xnb)):
                    lin.add(Xnb[j],self.fi(NB.tolist()[i][j]))
                print(lin)
                model.addConstr(lin>=self.fi(x[indexB[i]].X))
                break
        return model


    def controllo(self,Q):
        for i in range(0,len(Q)):
            if Q[i]>=0:
                return False
        return True
    
    def branchboundNotRecursive(self,model,T):
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
        if LB[0]<self.zopt:
            x=model.getVars()
            for i in range(0,len(x)):
                if x[i].X!=math.trunc(x[i].X):
                    Q.append(0)
                    vbranch.append(i)
                    valore.append(x[i].X)
                    break
         
        while (not self.controllo(Q)) and self.crono.current_time()-self.crono.inizio<T:
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
                    x[h].setAttr("VType","I")
                    fo=gp.LinExpr()
                    fo.add(x[h],1)
                    f.addConstr(x[h]<=math.trunc(val))
                else:
                    padre.append(-t)
                    f=M[t].copy()
                    x=f.getVars()
                    x[h].setAttr("VType","I")
                    fo=gp.LinExpr()
                    fo.add(x[h],1)
                    f.addConstr(x[h]>=math.ceil(val))
                f.optimize()
                if f.getAttr("Status")<3:
                    LB.append(f.objVal)
                    if self.intero(f.getVars()) and f.objval<self.zopt:
                        self.zopt=f.objVal
                        self.xopt=[]
                        self.TempoSoluzioneMigliore=self.crono.current_time()-self.crono.inizio 
                        puntiInteriPositivi=puntiInteriPositivi+1
                        for i in range(0,len(f.getVars())):
                            self.xopt.append(f.getVars()[i].X)
                        for i in range(0,len(Q)):
                            if LB[Q[i]]>=self.zopt:
                                Q[i]=-1
                    if LB[m]<self.zopt:
                        x=f.getVars()
                        for i in range(0,len(x)):
                            if x[i].X!=math.trunc(x[i].X):
                                vbranch.append(i)
                                valore.append(x[i].X)
                                Q.append(len(vbranch)-1)
                                break
                        M.append(f)
                        
    def Algoritmo(self,path,T=300000): 
        self.namePath=path
        self.crono.start()
        self.zRilassamentoLineare=self.solve()
        self.TempoGenerazioneColonne=self.crono.current_time()-self.crono.inizio          
        self.xopt=[]
        x=self.model.getVars()
        for i in range(0,len(x)):
            self.RoundupZ=self.RoundupZ+math.ceil(x[i].X)
            self.xopt.append(math.ceil(x[i].X))
        self.zopt=self.RoundupZ
        self.branchboundNotRecursive(self.model,T)
        self.crono.stop()
        self.TempoTerminazione=self.crono.getDurate()
        if self.TempoSoluzioneMigliore==0:
            self.TempoSoluzioneMigliore=self.TempoTerminazione
        self.ErroreAssolutoRoundUp=math.fabs(self.ZPLIColonneTrovate-self.RoundupZ)
        self.ErroreRelativoRoundUp=math.fabs((self.ZPLIColonneTrovate-self.RoundupZ)/self.ZPLIColonneTrovate)
        self.ErroreAssolutoBranch=math.fabs(self.ZPLIColonneTrovate-self.zopt)
        self.ErroreRelativoBranch=math.fabs((self.ZPLIColonneTrovate-self.zopt)/self.ZPLIColonneTrovate)
    
    def statistic(self):
        print("path",self.namePath)
        print("dimensione paperRoll",self.size)
        print("numero Taglie ",len(self.D))
        print("numero Colonne",self.NumeroColonne)
        print("Errore Assoluto RoundUp",self.ErroreAssolutoRoundUp)
        print("Errore relativo RoundUp",self.ErroreRelativoRoundUp)
        print("Errore Assoluto branch",self.ErroreAssolutoBranch)
        print("Errore relativo branch",self.ErroreRelativoBranch)
        print("Tempo generazione Colonne",self.TempoGenerazioneColonne)
        print("Tempo Soluzione migliorata",self.TempoSoluzioneMigliore)
        print("Tempo Terminazione Algoritmo",self.TempoTerminazione)
        print("soluzione rilassamento",self.zRilassamentoLineare)
        print("Soluzione ZPLIColonneTrovate",self.ZPLIColonneTrovate)
        print("soluzione ottimo trovata",self.zopt)
        print("soluzione ottimo dal RoundUp",self.RoundupZ)
        return (self.namePath,self.size,len(self.D),self.NumeroColonne,
                self.ErroreAssolutoRoundUp,self.ErroreAssolutoBranch,self.ErroreRelativoRoundUp,self.ErroreRelativoBranch,
                self.TempoGenerazioneColonne,self.TempoSoluzioneMigliore,self.TempoTerminazione,
                self.zRilassamentoLineare,self.ZPLIColonneTrovate,self.zopt,self.RoundupZ
                )

