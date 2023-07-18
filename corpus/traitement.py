import os
import shutil

# Transform .xml.tsv into .tsv
def delete_dot_xml(file_path):
    new_file_path = file_path

    if file_path.endswith(".xml.tsv") or file_path.endswith(".XML.tsv"):
        base_name = file_path[:-8]
        new_file_path = base_name + ".tsv"
        os.rename(file_path, new_file_path)

    return new_file_path

folder_path = "corpus_tei"

# Deplace les tsv de corpus_tei obtenus par transformation xslt dans corpus_tsv, en modifiant leurs extensions
try:
    os.mkdir("corpus_tsv")
except FileExistsError:
    print("The 'corpus_tsv' directory already exists.")

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if filename.endswith(".xml.tsv") or filename.endswith(".XML.tsv"):
        new_file_path = delete_dot_xml(file_path)
        shutil.move(new_file_path, os.path.join("corpus_tsv", os.path.basename(new_file_path)))


def replace_spaces_by_tab(file_path):
    # lis le fichier
    with open(file_path, 'r') as file:
        content = file.read()
    
    # remplace les espaces par des tab
    modified_content = content.replace("    ", "\t")
    

    with open(file_path, 'w') as file:
        file.write(modified_content)

def count_word_and_line(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        lines = str(len(content) -1) # ne compte pas la dernière ligne vide

    with open(file_path, 'r') as file:
        content = file.read()
        #content.replace("'", " ") #on pourrait rajouter ce genre de chose pour compter 2 mots pour "l'amour", ou deux mots pour "après-midi" selon
        content.split(" ") #actuellement ne sépare que par espace

    return str(len(content)) + "\t" + lines

#coupe la première ligne des fichirs tsv pour la mettre dans la tableOfContent
def cut_first_line(file1_path, file2_path, wclc):# append c'est ce qui va être ajouté à la première ligne coupée (notamment le compte des lignes et mots)
    
    # Open file 1 in read mode
    with open(file1_path, 'r') as file1:

        first_line = file1.readline()
        lines = file1.readlines()
        
        # Open file 2 in append mode
    with open(file2_path, 'a') as file2:
        #rajouter toute les infos pour la tableOfContent 
        first_line = first_line.replace("WCLC",wclc)
        
        first_line = first_line.replace("ParatexteBellesLettresSubcorpusLinkFile","paratext\tBelles-lettres\t" + "1-standard" + "\tlink\t" + file1_path.split("/")[1])

        file2.write(first_line)

        #la var append contient tab + count line + tab + count words
        

    with open(file1_path, 'w') as file1:

        file1.writelines(lines)


folder_path = "corpus_tsv"
tableOfContent = "tableOfContent.tsv"

#on traite tout les fichiers du dossier corpus_tsv
#normalement ils sont prêt pour être donnés à l'entrainement (sauf sub-corpus qui doit encore être séléctionné)
for filename in os.listdir(folder_path):
    filename = folder_path + "/" + filename
    replace_spaces_by_tab(filename)
    cut_first_line(filename, tableOfContent, count_word_and_line(filename))

shutil.move("corpus_tsv", os.path.join("..", "corpus_tsv"))
shutil.move("tableOfContent.tsv", os.path.join("..", "tableOfContent.tsv"))

