helpText = """
aggiornaSw -- uno script che permette di gestire l'aggiornamento di file all'interno di una cartella con molte sottocartelle

USO:

>>aggiornaSw -aiuto
	stampa questa lista di spiegazioni sull'uso dello script


>>aggiornaSw <cartella> trova <nome file>
	percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica
	
>>aggiornaSw <cartella> trova <nome file> log <path per il log>
	percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica


>>aggiornaSw <cartella> trova mod|creato il <data>
	percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutti i path di file modificati|creati nella data specificata

>>aggiornaSw <cartella> trova mod|creato il <data> log <path per il log>
	percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutti i path di file modificati|creati nella data specificata


>>aggiornaSw <cartella> trova mod|creato prima|dopo <data>
	percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutti i path di file modificati|creati prima|dopo la data specificata (inclusa)

>>aggiornaSw <cartella> trova mod|creato prima|dopo <data> log <path per il log>
	percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutti i path di file modificati|creati prima|dopo la data specificata (inclusa)

    
>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire>
	percorre <cartella> e tutte le sue subdirectories, e sostituisce ogni istanza di <nome file da sostituire> con il file trovato a <path file con cui sostituire>. Stampa una lista dei cambi effettuati.

>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire> log <path per il log>
	percorre <cartella> e tutte le sue subdirectories, e sostituisce ogni istanza di <nome file da sostituire> con il file nella cartella <path per il log> trovato a <path file con cui sostituire>. Genera un file con una lista dei cambi effettuati.


>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire> update <cartellaUpdate>
>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire> log <path per il log> update <cartellaUpdate>
	effettua tutte le azioni di "sostituisci" o "sostituisci log", ma per ogni istanza di sostituzione di <nome file da sostituire>, ricrea lo stesso path all'interno di <cartellaUpdate>, e in quel path aggiunge <path file con cui sostituire>


>>aggiornaSw <cartella> trovaVuote
	percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutte le directories vuote
	
>>aggiornaSw <cartella> trovaVuote log <path per il log>
	percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutte le directories vuote

"""

import sys, os, shutil


#save input to command array
command = sys.argv

def main (command):
	if len(command) == 2: #se c'è solo un comando
		if command[1].lower() == "help":
			print(helpText)
		else:
			nonValido()
	
	else:
		if os.path.isdir(command[1]):	#tutte le varie funzioni
			if command[2].lower() == "trova":	#funzioni TROVA
				if os.path.isfile(command[3]): #TROVA semplice
					#TODO
					pass
					
				elif command[3] == "mod" or command[3] == "creato": 
					if command[4] == "il":
						#TODO
						pass
					elif command[4] == "prima":
						#TODO
						pass
					elif command[4] == "dopo":
						#TODO
						pass
					else:
						nonValido()
				
				else:
					nonValido()
			
			
			elif command[2].lower() == "sostituisci":	#funzioni SOSTITUISCI
				#TODO
				pass
		else:
			nonValido()
	



#___HELPER FUNCTIONS___ 
def trovaFile (myfile, mydir):	#string, string >> list 
	"""
	trova le istanze di MYFILE in MYDIR, returns lista
	myfile: nome di file, non percorso
	mydir: absolute path di directory
	"""
	fileList = []
	for root, dirs, files in os.walk(mydir):
		for file in files:
			if file = myfile:
				fileList.append(os.path.join(root, file))
	return fileList

def aggiungiDate (fileList):	#list >> list of tuples (filePath, data creazione, data modifica)
	"""
	prende una lista di percorsi di file (come generata da trovaFile), e ritorna una lista di tuples con (path del file, data di creazione, data di modifica)
	fileList: una lista di percorsi di file
	"""
	listaDate = []
	for file in fileList:
		dataCreazione = os.path.getctime(file)
		#https://docs.python.org/3/library/os.path.html#os.path.getctime
		dataModifica = os.path.getmtime(file)
		#https://docs.python.org/3/library/os.path.html#os.path.getmtime
		listaDate.append((file, dataCreazione, dataModifica))
	
	return listaDate
	
def sostituisci (listaFile, fileNuovo):	#list, string >> list
	"""
	prende una lista di percorsi di file (come generata da trovaFile), e il percorso di un file. Sostituisce tutti i file nella lista con il nuovo file.
	Ritorna una lista dei percorsi dei nuovi file.
	listaFile: lista di percorsi assoluti di file che vanno rimpiazzati
	fileNuovo: percorso assoluto del file che deve rimpiazzare tutti quelli nella lista
	"""
	listaCambiamenti = []
	for file in listaFile:
		shutil.copy(fileNuovo, file)
		listaCambiamenti.append(file)
	
	return listaCambiamenti

"""	
def trovaSubdirVuote (mydir):	#string >> list 
	"""
	trova le subdirectory vuote, returns lista
	mydir: absolute path di directory
	"""
	dirList = []
	for root, dirs, files in os.walk(mydir):
		for dir in dirs:
			if :
				dirList.append(os.path.join(root, dir))
	return dirList
"""
	
def nonValido (): # >> string
	"""
	avvisa l'utente che l'input dato non è valido
	"""
	print("Stai cercando di usare lo script in maniera non corretta. Per vedere istruzioni dettagliate, digita \"aggiornaSW -aiuto\"")
	
	
	