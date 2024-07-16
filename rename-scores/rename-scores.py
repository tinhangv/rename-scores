import os
import sys

def main():
    #read file path as argument
    #folder_path = sys.argv[1]

    folder_path = input("Enter folder name: ")
    while not os.path.isdir(folder_path):
        print("Invalid path")
        folder_path = input("Enter file name: ")
    fnames = os.listdir(folder_path)
    print("Folder path: " + folder_path)
    #print("file 1: " + fnames[0])
    
    #identify name format: Dorico, Finale, Sibelius, completed, other
    # #Completed
    # "##_title_v1_vln"
    # #Dorico
    # "01 - Flute 1 - Converge.pdf"
    # #Finale
    # "rootsbeneath_v6 - Basson1 1.pdf"
    # #Sibelius
    # "01 madrigal_v9 English Horn.pdf"

    #check using the first file
    file1 = fnames[0]
    program = ''
    title = ''
    ins = []
    version = 0
    if not file1[:2].isnumeric():
        program = 'Finale'
        title = file1.split(' - ')[0]
        for file in fnames:
            ins.append(file.split(' - ')[1][:-4])
    else:
        if file1[2] == '_':
            program = 'Completed'
            print("Files have already been renamed")
            exit()
        elif file1[3] == '-':
            program = 'Dorico'
            title = file1.split(' - ')[2][:-4]
            for file in fnames:
                ins.append(file.split(' - ')[1])
            version = int(input("Enter version number: "))
        else: 
            program = 'Sibelius'
            title = file1.split(' ')[1]
            for file in fnames:
                ins.append(' '.join(file.split(' ')[2:])[:-4])

    print("Program: " + program)
    print("Title: " + title)
    # print("Instrusments: ")
    # print(ins)

    #put pdfs in order
    instruments,abbrev = getConcertOrder()
    
    old_files_ind = []
    abrs = []
    for i in range(len(instruments)): 
        x=instruments[i]
        if x in ins:
            #print(str(ins.index(x)) + ' :' + x)
            old_files_ind.append(ins.index(x))
            abrs.append(abbrev[i])

    #get old file names and generate new file names
    old_files = []
    new_files = []
    for i in range(len(old_files_ind)):
        old_files.append(fnames[old_files_ind[i]])
        if (program == "Dorico"):
            new_files.append(str(i).zfill(2) + '_' + title + '_v' + str(version) + '_' + abrs[i]+".pdf")
        else:
            new_files.append(str(i).zfill(2) + '_' + title + '_' + abrs[i]+".pdf")

    # print("Old files:")
    # print(old_files)
    # print("New files:")
    # print(new_files)
    
    # #confirm change with user
    print("\nThe following changes will be made:")
    print(str(len(new_files)) + "/" + str(len(fnames)) + " files will be renamed")
    longest = max(len(s) for s in old_files)
    for i in range(len(old_files)):
        spaces = longest-len(old_files[i])
        print(old_files[i] + spaces*' ' + " ->  "+ new_files[i])
    print(str(len(fnames)-len(new_files)) + "/" + str(len(fnames)) + " files will NOT be renamed")
    for x in fnames:
        if x not in old_files:
            print(x)
    
    
    confirm = input("Rename files? [y/n] ")

    if(confirm.lower() == 'y'):
        #rename files
        for i in range(len(old_files)):
            old_file = os.path.join(folder_path, old_files[i])
            new_file = os.path.join(folder_path, new_files[i])
            os.rename(old_file,new_file)
        print("Done")
    elif(confirm.lower() == 'n'):
        print("Aborted")

def getConcertOrder():
    f = readFile("concert-order.csv").strip()
    instruments = []
    abbrev = []
    for s in f.split('\n'):
        instruments.append(s.split(',')[0])
        abbrev.append(s.split(',')[1])

    return(instruments,abbrev)
    
def readFile(filename):
    with open(filename,'r') as infile:
        return(infile.read())
    
main()