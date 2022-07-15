# progettoAMOD
progetto universitario del corso di A.M.O.D. della facoltà di Ingegneria dell'università degli studi di Roma Torvergata 

## Obiettivo

1. Risoluzione del problema di cutting stock utilizzando l’algoritmo di generazione delle colonne utilizzando la tecnica di Round-UP per passare dalla soluzione del rilassamento lineare alla soluzione Intera

2. Miglioramento della soluzione Ottenuta con il Round-UP utilizzando una tecnica di Branch-and-Bound sul problema ottenuto dall’algoritmo di generazione colonne

3. Confronto prestazionale tra i due metodi, in particolare analizzare i tempi di completamento e la distanza tra la soluzione ottima e la soluzione trovata dalle due tecniche su istanze di cui si conosce la Soluzione Ottima Intera

## Come preparare l'ambiente
i requisiti che lo script in pyhon richiede per poter essere avviato sono:
1. Richiede  di aver installato python:
   - per windows basta la versione 3.8 o superiore
   - per macOS serve una versione di python 3.10 o superiore
2. Libreria di gurobipy di python
    per installarlo di seguito metto il comando<br/>
    `python3 -m pip install gurobipy`
3. Libreria numpy di python:
    per installarlo di seguito metto il comando<br/>
    `python3 -m pip install numpy`
4. Scaricare il seguente repository e avviare il main.  

## Dati 
Le istanze di test sono state tutte le 160 istanze che si trovano dentro la direcotry Falkenauer_CPS, per aggiungere un istanza bisogna inserirle all'interno di una delle direcotry all'interno di Falkenauer_CPS e il file deve essere conforme allo schema degli altri file per tanto deve essere:
1. la prima riga deve contenere solo il numero di oggetti (m)
2. la seconda riga deve contenere solo la capacità del Foglio (c)
3. per ogni oggetto ci deve essere una riga che contiene prima il peso (wj) e poi la richiesta (dj),dj deve distare un tab da wj!!!;  
ESEMPIO:<br />
il numero di tagli é 3.  
il vettore dei tagli é: 10,20,30. 
il paper roll ha dimensione: 500.  
il vettore della richiesta è: 400,350,375. 
allora il file dovra essere scritto nel seguente modo:
```
3<br /> 
500<br />
10   400<br />
20   350<br /> 
30   375<br /> 
```
## Main
Il solutore può essere avviato in due modi il primo utilizzando il file main2.py, Una volta avviato, il programma che andrà in esecuzione risolverà tutti i 
