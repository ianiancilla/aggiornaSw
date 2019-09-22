import PySimpleGUI as sg
import sys, os, shutil, time

###___GUI SECTION___###

# DEFINE LAYOUT
col_1 = [
            [sg.Text('Scegli la cartella dove vuoi effettuare la ricerca:')],
            [sg.InputText(), sg.FolderBrowse("Sfoglia", key="folder-to-search")],
            [sg.Text("\nScrivi il nome del file da cercare, inclusa l'estensione:")],
            [sg.InputText(key= "file-old")],
            [sg.Text("\nDecidi cosa vuoi fare:")],
            [sg.InputCombo(("Trova e basta", "Trova e sostituisci", "Trova, Sostituisci, e crea folder Update"), key= "action")],
            [sg.Text("\nQUI SOTTO, RIEMPI SOLO I CAMPI NECESSARI:")],
            [sg.Text("\nSe vuoi che crei un log, seleziona la cartella dove lo devo creare:")],
            [sg.InputText(), sg.FolderBrowse("Sfoglia", key="folder-log")],
            [sg.Text("\nSe hai scelto Sostituisci o Sostituisci/Update")],
            [sg.Text("Seleziona il file con cui sostuire il file che hai specificato:")],
            [sg.InputText(), sg.FileBrowse("Sfoglia", key="file-new")],
            [sg.Text("\nSe hai scelto Sostituisci e crea cartella Update")],
            [sg.Text("Seleziona la cartella dove creare l'update:")],
            [sg.InputText(), sg.FolderBrowse("Sfoglia", key="folder-update")],
            [sg.Text("\n")],

            [sg.Button("ANTEPRIMA"), sg.Button("ESEGUI"), sg.Exit("ESCI")] 
]

col_2 = [
            [sg.Text('Script output....')],
            [sg.Output(size=(80, 30))],
        ]

layout = [
            [sg.Column(col_1), sg.Column(col_2)]
]

# CREATE WINDOW
window = sg.Window('Aggiorna Software GUI', layout)

# READ WINDOW
event, values = window.Read()  


# MAIN FUNCTION
def main(event, values):
    """
    the main loop of the program, calling all other functions
    event, values as given by PySimpleGUI
    """
    print_width = 70

    # if user only wants a preview
    if event == "ANTEPRIMA":
        try:
            # if user only wants to find files
            if values["action"] == "Trova e basta":
                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                dated_list = add_dates(file_path_list)
                description = "Ho trovato le seguenti istanze del file\n" + values["file-old"] + "\nnella cartella\n" +  values["folder-to-search"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))
                
                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-trova.txt")
                    save_log(log_file_path, dated_list, description)

            # if user asked a preview of a file replacement    
            elif values["action"] == "Trova e sostituisci":
                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                dated_list = add_dates(file_path_list)
                description = "\n\nANTERPIMA\n\n\nLe seguenti istanze del file\n" + values["file-old"] + "\nnella cartella\n" +  values["folder-to-search"] + "\nverrebbero sostituite con il file\n" + values["file-new"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))

                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-sostituisci-anteprima.txt")
                    save_log(log_file_path, dated_list, description)

            #if user asked a preview of file replacement and update folder creation:
            elif values["action"] == "Trova, Sostituisci, e crea folder Update":

                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                dated_list = add_dates(file_path_list)
                description = "\n\nANTERPIMA\n\n\nLe seguenti istanze del file\n" + values["file-old"] + "\nnella cartella\n" +  values["folder-to-search"] + "\nverrebbero sostituite con il file\n" + values["file-new"] + "\ne il folder per l'update verrebbe creato al path\n" + values["folder-update"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))

                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-sostituisci-update-anteprima.txt")
                    save_log(log_file_path, dated_list, description)

            #what to do if required data was not given
        except NameError as error:
            nonValid(error)

    elif event == "ESEGUI":
        try:
            # if user only wants to find files
            if values["action"] == "Trova e basta":
                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                dated_list = add_dates(file_path_list)
                description = "Ho trovato le seguenti istanze del file " + values["file-old"] + " nella cartella " +  values["folder-to-search"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))
                
                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-trova.txt")
                    save_log(log_file_path, dated_list, description)

            # if user asked for file replacement
            elif values["action"] == "Trova e sostituisci":
                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                
                # user confirmation before modifying files
                if user_confirm() == "No":
                    return

                replaced_list = replace_file(file_path_list, values["file-new"])
                dated_list = add_dates(replaced_list)
                description = "\n\nESEGUITO\n\n\nLe seguenti istanze del file\n" + values["file-old"] + "\nnella cartella\n" +  values["folder-to-search"] + "\nsono state sostituite con il file\n" + values["file-new"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))

                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-sostituzioni.txt")
                    save_log(log_file_path, dated_list, description)

            # if user asked for file replacement and creation of update folder:
            elif values["action"] == "Trova, Sostituisci, e crea folder Update":
                file_path_list = find_file(values["file-old"], values["folder-to-search"])
                
                # user confirmation before modifying files
                if user_confirm() == "No":
                    return

                replaced_list = replace_file(file_path_list, values["file-new"])
                dated_list = add_dates(replaced_list)
                description = "\n\nESEGUITO\n\n\nLe seguenti istanze del file\n" + values["file-old"] + "\nnella cartella\n" +  values["folder-to-search"] + "\nsono state sostituite con il file\n" + values["file-new"] + "\ne il folder per l'update verrà creato al path\n" + values["folder-update"] + ":\n"
                print(format_dated_list(dated_list, print_width, description))

                # in case a log is requested > logs the replacement
                if values["folder-log"]:
                    log_file_path = os.path.join( values["folder-log"], "log-sostituzioni-update.txt")
                    save_log(log_file_path, dated_list, description)

                update_result = makeUpdate(replaced_list, values["folder-to-search"], values["folder-update"])
                dated_update_list = add_dates(update_result[1])
                description_update = "\n\nESEGUITO\n\n\nSono stati generati i seguenti file e cartelle:\n"
                print(format_dated_list(dated_update_list, print_width, description_update))

                # in case a log is requested
                if values["folder-log"]:
                    log_file_path = os.path.join( update_result[0], "log-update.txt")
                    save_log(log_file_path, dated_update_list, description_update)
                
            
            #what to do if required data was not given
        except NameError as error:
            nonValid(error)



# HELPER FUNCTIONS

def find_file(my_file_name, dir_path):	#string, string >> list 
    """"
    finds instances of my_file_name in dir_path
    returns: list of file paths (str)

    my_file_name: str, file name (not path)
    dir_path: str, absolute directory path
    """
    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if file_name.lower() == my_file_name.lower():
                file_path_list.append(os.path.join(root, file_name))
    return file_path_list

def add_dates(file_path_list):	#list >> list of tuples (file path (str), creation date (number, sec since epoch), last mod date (number, sec since epoch))
    """
    file_path_list: a list of file path strings (as generated by find-file)
    returns: a list of tuples, each like: (file path (str), creation date (number, sec since epoch), last mod date (number, sec since epoch))

    https://docs.python.org/3/library/os.path.html#os.path.getctime
    https://docs.python.org/3/library/os.path.html#os.path.getmtime
    """
    dated_list = []
    for file_name in file_path_list:
        creation_date = os.path.getctime(file_name)
        #https://docs.python.org/3/library/os.path.html#os.path.getctime
        mod_date = os.path.getmtime(file_name)
        #https://docs.python.org/3/library/os.path.html#os.path.getmtime
        dated_list.append((file_name, creation_date, mod_date))

    return dated_list

def replace_file(file_path_list, new_file_path):	#list of strings (file paths), string (file path) >> list
    """
    returns: list of str (paths of new files, all that were replaced)
    action: replaces all files at the paths in file_path_list with the file at the new_file_path

    takes a list of file paths (as generated by find_file) and a string with abs path of a file. Replaces all files in the list with the specified file.

    file_path_list: list of strings. Paths of files to replace. As output by find-file()
    new_file_path: abs path (str) of file which needs to replace all files in the list
    """
    replacement_list = []
    for file_path in file_path_list:
        shutil.copy(new_file_path, file_path)
        replacement_list.append(file_path)

    return replacement_list

def nonValid(error): # >> string
    """
    warns the user that data that has been input is somehow invalid
    """
    warning= """
    **************
    Stai cercando di usare il programma in maniera non corretta.
    Ricontrolla bene di aver inserito tutti i dati necessari, e in maniera corretta.
    **************\n
    """
    print(warning)
    print(error)

def parse_time(date_epoch):	#number (date in seconds from epoch) >> string (date in local time)
    """
    returns: string form of a date in format "YYYY/MM/DD"
    takes: a date as returned by getctime (as output in add_dates)
    """
    return time.strftime("%Y/%m/%d", time.localtime(date_epoch))

def format_dated_list(dated_list, char_number, description):	#list of tuple, int, string >> string
    """
    returns: a string version of the list of tuples, formatted in a legible way, with lines of length "char_number
    takes: a list of tuples (as output by add_dates), a number of characters for width size, a string with the description of the list contents
    """
    formatted_string = description
    head_line = "\n=== CREATO =="+"= MODIFICATO ="+"== NOME FILE "
    head_line = head_line.ljust(char_number,"=")

    formatted_string += head_line + "\n"

    for tup in dated_list:
        formatted_line = ""
        creation_date = parse_time(tup[1])
        mod_date = parse_time(tup[2])
        file_path = tup[0]
        formatted_line += "\n "+ creation_date + "."*4 + mod_date + "."*5 + file_path
        formatted_string+= formatted_line
    formatted_string+= "\n"
    occurrence_num = len(dated_list)
    formatted_string += "\nNumero di file: " + str(occurrence_num) + "\n"
    return formatted_string

def save_log(log_file_path, dated_list, description):
    #loop to check whether log file is present, and if it is overwrite or change target file
    while os.path.isfile(log_file_path):
        overwrite_confirm = "Il file che hai scelto per il log:\n\n" + log_file_path + "\n\nesiste già. Vuoi sovrascriverlo?"
        overwrite_answer = sg.popup_yes_no(overwrite_confirm)
        # break out of loop and create log if use chooses to overwrite
        if overwrite_answer == "Yes":
            break
        else:
            get_file_message = "Seleziona il file dove vuoi salvare il log."
            log_file_path = sg.popup_get_file(get_file_message, default_path=os.path.dirname(log_file_path), default_extension="txt",)

    log = open(log_file_path, "w")
    log.write(format_dated_list(dated_list, 120, description))
    log.close()
    print("\nPuoi trovare il log qui:", log_file_path)

def makeUpdate (file_path_list, origin_dir_path, new_dir_path):	#list of str, str, str > (str, list of str)
    """
    return: tuple of (str (path of directory where update folder was created) , [list of str (paths of updated files)]
    takes a list of files with paths originating in origin_dir_path, and created same tree in new_dir_path \\Update

    file_path_list: list of file paths, as returned by find_file
    origin_dir_path: directory da cui effettuare la copia
    new_dir_path: directory in cui effettuare la copia
    """
    #creats empty list to store new paths
    copied_path_list = []
    #walks the list of files to recreate
    for file_path in file_path_list:
        rel_file_path = os.path.relpath(file_path, origin_dir_path) #returns the relative path of file, only from the start directory
        new_file_path = os.path.join(new_dir_path,"update", rel_file_path) #generates new absolute path, with new update directory
        new_file_split = os.path.split(new_file_path) #gets only directory of new file path
        os.makedirs(new_file_split[0], exist_ok=True) #creates directory if it does not exist already
        copied_path_list.append(shutil.copy(file_path, new_file_path)) #copies file and adds it to list
    return (new_dir_path, copied_path_list)

def user_confirm():
    """
    asks user for confirmation to proceed.
    returns str "Yes" or "No"s
    """
    confirm_message = "\nLa seguente azione modifcherà file in maniera definitiva.\nSei sicura di voler continuare?\n\n"
    return sg.popup_yes_no(confirm_message)

# ---===--- Loop taking in user input and using it to call scripts --- #      
while True:      
    event, values = window.Read()      
    if event is None or event == 'ESCI':      
        break      
    main(event, values)    

window.Close()