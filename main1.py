#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:48:36 2022

@author: kobero
"""
from CuttingStock import cuttingStock   
from Utils import lettoreCuttingPlain

def main():
    dir1='./Falkenauer_CSP/Falkenauer_U'
    instance=lettoreCuttingPlain.Lettore(dir1+"/"+"Falkenauer_u500_19.txt")
    z=cuttingStock(instance)
    z.Algoritmo("Falkenauer_u500_19.txt")
    y=z.statistic()
    print(y)
main()