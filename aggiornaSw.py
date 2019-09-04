#TODO
#aggiungere numero istanze trovate


helpText = """
	aggiornaSw -- uno script che permette di gestire l'aggiornamento di file all'interno di una cartella con molte sottocartelle

	USO:

	>>aggiornaSw aiuto
		stampa questa lista di spiegazioni sull'uso dello script


	>>aggiornaSw <cartella> trova <nome file>
		percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica
		
	>>aggiornaSw <cartella> trova <nome file> log <path per il log>
		percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica
		
	>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire>
		percorre <cartella> e tutte le sue subdirectories, e sostituisce ogni istanza di <nome file da sostituire> con il file trovato a <path file con cui sostituire>. Stampa una lista dei cambi effettuati.
		TI VERRÀ CHIESTO SE SALVARE UN LOG E SE CREARE UNA CARTELLA DI UPDATE

	"""

import sys, os, shutil, time

#save input to command array
command = sys.argv

def main (command):
	try:
		if len(command) == 2: #se c'è solo un comando____AIUTO
			if command[1].lower() == "aiuto":
				#>>aggiornaSw -aiuto
				#stampa questa lista di spiegazioni sull'uso dello script
				aiuto()
			else:
				nonValido()
		
		else:
			if os.path.isdir(command[1]):	#tutte le varie funzioni
				if command[2].lower() == "trova":	#funzioni TROVA
														
					if command[3] == "mod" or command[3] == "creato": 
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
					
					else: 	#TROVA semplice
						listaFile = trovaFile(command[3], command[1])
						if listaFile == []:
							print("\nNon ci sono file con questo nome, ricontrolla.\n")
							return
						listaDate = aggiungiDate(listaFile)

						if len(command) == 4:
							#>>aggiornaSw <cartella> trova <nome file>
							#percorre <cartella> e tutte le sue subdirectories e stampa una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica
							print(bellaListaConDate(listaDate, 80))

						elif len(command) == 6 and command[4].lower() == "log":
						#>>aggiornaSw <cartella> trova <nome file> log <path per il log>
						#percorre <cartella> e tutte le sue subdirectories e crea un file nella cartella <path per il log> con una lista di tutti i path in cui quel file appare, con data di creazione e di ultima modifica
							saveLog(command[5], listaDate)
						else:
							nonValido()

				elif command[2].lower() == "sostituisci":	#funzioni SOSTITUISCI
					if os.path.isfile(command[4]):
						#>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire>
						#percorre <cartella> e tutte le sue subdirectories, e sostituisce ogni istanza di <nome file da sostituire> con il file trovato a <path file con cui sostituire>. Stampa una lista dei cambi effettuati.
						listaFile = trovaFile(command[3], command[1])
						if listaFile == []:
							print("\nNon ci sono file con questo nome, ricontrolla.\n")
							return
						listaConDate = aggiungiDate(listaFile)

						#>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire>
						#percorre <cartella> e tutte le sue subdirectories, e sostituisce ogni istanza di <nome file da sostituire> con il file trovato a <path file con cui sostituire>. Stampa una lista dei cambi effettuati.
						listaSostituzioni = "\nI file che saranno sostituiti con " + command[4] + " sono i seguenti:\n" + bellaListaConDate(listaConDate, 80) + "\n"
						print(listaSostituzioni)
						if input("\nVuoi procedere? y/n ").lower() == "y":
							if input("\nVuoi salvare un log delle operazioni? y/n ").lower() == "y":
								log = True									
								logPath = input("Scrivi il path (incluso il nome del file) dove vuoi che crei il log: ")
							if input("\nVuoi anche creare una cartella con gli update? y/n ").lower() == "y":
								update = True
								updatePath = input("Scrivi il path della cartella dove vuoi che crei la cartella update: ")
								if input("\nVuoi salvare un log dell'update (sarà salvato nella cartella dell'update)? y/n ").lower() == "y":
								 updateLog = True									
								
							print("\nInizio sostituzione...")
							listaSostituzioniFatte = (sostituisci(listaFile, command[4])) #non crea solo lista SOSTITUISCE I FILE
							ListaSostFatteDate = aggiungiDate(listaSostituzioniFatte)
							print("\nOperazione effettuata. Sostituzioni effetuate:")
							print(bellaListaConDate(ListaSostFatteDate, 80)+"\n")								
							if log:
								saveLog(logPath, ListaSostFatteDate)
							if update:
								print("\nInizio a creare la cartella Update in " + updatePath)
								pathUpdate, listaUpdated = makeUpdate(listaSostituzioniFatte, command[1], updatePath)
								print("\nCartella Update creata.")
								if updateLog:
									listaUpdatedDate = aggiungiDate(listaUpdated)
									updateLogPath = os.path.join(pathUpdate, "update-log.txt")
									saveLog(updateLogPath, listaUpdatedDate)

									

						else:
							print("\nOperazione annullata.\n")
							return


					else: #se il file con cui sostituire non esiste
						nonValido()
				


				

				#>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire> update <cartellaUpdate>
				#effettua tutte le azioni di "sostituisci" ma per ogni istanza di sostituzione di <nome file da sostituire>, ricrea lo stesso path all'interno di <cartellaUpdate>, e in quel path aggiunge <path file con cui sostituire>

				#>>aggiornaSw <cartella> sostituisci <nome file da sostituire> <path file con cui sostituire> log <path per il log> update <cartellaUpdate>
				#effettua tutte le azioni di "sostituisci log", ma per ogni istanza di sostituzione di <nome file da sostituire>, ricrea lo stesso path all'interno di <cartellaUpdate>, e in quel path aggiunge <path file con cui sostituire>

			else:
				nonValido()
	except IndexError:
		nonValido()	

#___HELPER FUNCTIONS___ 

def aiuto():
	print(helpText)

def trovaFile (myfile, mydir):	#string, string >> list 
	"""
	trova le istanze di MYFILE in MYDIR, returns lista
	myfile: nome di file, non percorso
	mydir: absolute path di directory
	"""
	fileList = []
	for root, dirs, files in os.walk(mydir):
		for fileName in files:
			if fileName.lower() == myfile.lower():
				fileList.append(os.path.join(root, fileName))
	return fileList

def aggiungiDate (fileList):	#list >> list of tuples (filePath, data creazione, data modifica)
	"""
	prende una lista di percorsi di file (come generata da trovaFile), e ritorna una lista di tuples con (path del file, data di creazione, data di modifica)
	fileList: una lista di percorsi di file
	https://docs.python.org/3/library/os.path.html#os.path.getctime
	https://docs.python.org/3/library/os.path.html#os.path.getmtime
	"""
	listaDate = []
	for fileName in fileList:
		dataCreazione = os.path.getctime(fileName)
		#https://docs.python.org/3/library/os.path.html#os.path.getctime
		dataModifica = os.path.getmtime(fileName)
		#https://docs.python.org/3/library/os.path.html#os.path.getmtime
		listaDate.append((fileName, dataCreazione, dataModifica))
	
	return listaDate

def sostituisci (listaFile, fileNuovo):	#list, string >> list
	"""
	prende una lista di percorsi di file (come generata da trovaFile), e il percorso di un file. Sostituisce tutti i file nella lista con il nuovo file.
	Ritorna una lista dei percorsi dei nuovi file.
	listaFile: lista di percorsi assoluti di file che vanno rimpiazzati
	fileNuovo: percorso assoluto del file che deve rimpiazzare tutti quelli nella lista
	"""
	listaCambiamenti = []
	for fileName in listaFile:
		shutil.copy(fileNuovo, fileName)
		listaCambiamenti.append(fileName)
	
	return listaCambiamenti
	
def nonValido (): # >> string
	"""
	avvisa l'utente che l'input dato non è valido
	"""
	print("Stai cercando di usare lo script in maniera non corretta. Per vedere istruzioni dettagliate, digita \"aggiornaSW aiuto\"")

def parseTime(dataEpoch):	#data in formato seconds from epoch >> string
	"""
	prende una data come espressa da getctime, come nelle tuple di aggiungiDate, e la ritorna in string con formato "YYYY/MM/GG"
	"""
	return time.strftime("%Y/%m/%d", time.localtime(dataEpoch))

def bellaListaConDate (listaConDate, caratteri):	#list of tuple >> string
	"""
	prende una lista di tuples come ritornata da aggiungiDate, e ritorna una stringa formattata in maniera leggibile, con righe di lunghezza <caratteri>
	"""
	prettyString = ""
	firstLine = "\n=== CREATO =="+"= MODIFICATO ="+"== NOME FILE "
	firstLine = firstLine.ljust(caratteri,"=")

	prettyString += firstLine

	for tup in listaConDate:
		prettyLine = ""
		dataCreato = parseTime(tup[1])
		dataModificato = parseTime(tup[2])
		fileName = tup[0]
		prettyLine += "\n "+ dataCreato + "."*4 + dataModificato + "."*5 + fileName
		prettyString+= prettyLine
	prettyString+= "\n"
	occurrenceNumber = len(listaConDate)
	prettyString += "Numero di file: " + str(occurrenceNumber) + "\n"
	return prettyString

def saveLog (logFile, listaConDate):
	if os.path.isfile(logFile):
		confermaSovrascrivi = "Il file che hai scelto per il log " + logFile + " esiste già. Vuoi sovrascriverlo? y/n "
		if input(confermaSovrascrivi).lower() == "y":
			log = open(logFile, "w")
			log.write(bellaListaConDate(listaConDate, 120))
			log.close()
			print(bellaListaConDate(listaConDate, 80))
			print("\nPuoi trovare il log qui:", logFile)
		else:
			print("Operazione annullata.")
	else:
		log = open(logFile, "w")
		log.write(bellaListaConDate(listaConDate, 120))
		log.close()
		print(bellaListaConDate(listaConDate, 80))
		print("\nPuoi trovare il log qui:", logFile)

def makeUpdate (listaFile, myDir, newDir):	#list, str, str > (str, list)
	""" return: tuple of: directory with the update ,lista dei file copiati (con percorso)
	prende una lista di file con origine del proprio tree in myDir, e li copia con la stessa struttura in newDir
	listaFile: lista di percorsi di file, come ritornata da TROVA
	myDir: directory da cui effettuare la copia
	newDir: directory in cui effettuare la copia
	"""
	listaCopiati = []
	for filePath in listaFile:
		dirName = os.path.dirname(filePath)
		relPath = os.path.relpath(dirName, myDir)
		newPath = os.path.join(newDir,"update",relPath)
		os.makedirs(newPath, exist_ok=True)
		listaCopiati.append(shutil.copy(filePath, newPath))
	return (newPath, listaCopiati)


#__TESTING AREA__#

main(command)

