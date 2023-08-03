import git
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import webbrowser
from git import Repo 
import os
import shutil


app = QApplication(sys.argv)
app.setStyle('Fusion') 



############################################ Fenetre 1 ############################################

def open_root1():
    global main, root, root2
    main_pos = main.pos()
    main.hide()
    root.setGeometry(main_pos.x(), main_pos.y(), 400, 400)
    root.show()

def open_root2():
    global main, root, root2
    main_pos = main.pos()
    main.hide()
    root2.setGeometry(main_pos.x(), main_pos.y(), 400, main.height() + 70)  
    root2.show()


def algo():
    lien = entry1.text()
    chemin_dossier = entry2.text()
    repo = git.Repo.init(chemin_dossier)
    repo.git.add(all=True)
    repo.git.commit(m="first commit", allow_empty=True)
    remote_exists = False
    for remote in repo.remotes:
        if remote.name == "origin":
            remote_exists = True
            break
    if not remote_exists:
        chargement.setText(f"Ajout du dépôt distant 'origin' avec l'URL: {lien}...")
        repo.create_remote("origin", url=lien)
    repo.git.branch("-M", "main")
    repo.git.push("--set-upstream", "origin", "main")
    QMessageBox.information(message, "Auto Git", "Dossier envoyé avec succès !")
    entry1.clear()
    entry2.clear()
    entry3.clear()  
    entry4.clear()
    entry5.clear()


def label_click(event):
    webbrowser.open("https://github.com/new")

###################################################################################################


############################################ Fenetre 2 ############################################

def fermer_fenetre(event):
    global main, root, root2
    if root.isVisible():
        root.hide()
        main_pos = root.pos()
    elif root2.isVisible():
        root2.hide()
        main_pos = root2.pos()
    main.setGeometry(main_pos.x(), main_pos.y(), 400, 400)
    main.show() 
    entry1.clear()
    entry2.clear()
    entry3.clear()  
    entry4.clear()
    entry5.clear()



def clone_replace_send():
    lien_clone = entry3.text()
    faux_destination = entry4.text()
    dossier_a_clone = entry5.text()
    segments = lien_clone.split('/')
    name_seg = segments[-1]
    fin_path = name_seg.rstrip('.git')
    destination_path = "\\".join((faux_destination,fin_path))

    # Clonage de Github a PV
    print("-Clonage...")
    Repo.clone_from(lien_clone, destination_path)
    print("-Clonage réussit")

    # Déplacement les fichiers au fichier destination
    for fichier in os.listdir(dossier_a_clone):
        chemin_fichier_source = os.path.join(dossier_a_clone, fichier)
        if os.path.isfile(chemin_fichier_source):
            chemin_fichier_destination = os.path.join(destination_path, fichier)
            shutil.move(chemin_fichier_source, chemin_fichier_destination, copy_function=shutil.copy2)
            print(f"-Fichier '{fichier}' déplacé avec succès.")
        else:
            print("Erreur")

    # Envoir PC a Github
    repo = git.Repo.init(destination_path)
    repo.git.add(all=True)
    repo.git.commit(m="Modification des fichiers", allow_empty=True)
    repo.git.push("--set-upstream", "origin", "main")
    QMessageBox.information(message, "Auto Git", "Fichiers envoyés avec succès !")
    entry3.clear()  
    entry4.clear()
    entry5.clear()

###################################################################################################



# Fenetre Principale
main = QWidget()
main.setWindowTitle("Auto git")
main.setStyleSheet("""
    background-color: #0D1117;
    font-family: Arial, sans-serif;
""")
main.setGeometry(100, 100, 400, 400)
main.setWindowIcon(QIcon("./Icon/git_logo.ico"))

text_title = QLabel("Auto Git", main)
text_title.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica;
    font-size: 30px;
""")
text_title.move(150, 30)

push = QPushButton("Crée un Repository", main)
push.setGeometry(300, 500, 300, 45)
push.setStyleSheet("""
    QPushButton {
        background-color: #6E2BF1;
        color: #ffffff;
        font-family: Halvetica;
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
                          
    }
    QPushButton:hover {
        background-color: #0D1117;
        border: 2px solid blue;
    }
""")
push.move(50,140)
push.clicked.connect(open_root1)


clone = QPushButton("Remplacer un Repository", main)
clone.setGeometry(300, 500, 300, 45)
clone.setStyleSheet("""
    QPushButton {
        background-color: #6E2BF1;
        color: #ffffff;
        font-family: Halvetica;
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
                          
    }
    QPushButton:hover {
        background-color: #0D1117;
        border: 2px solid blue;
    }
""")
clone.move(50,220)
clone.clicked.connect(open_root2)




# FENETRE1 
root = QWidget()
root.setWindowTitle("Auto git")
root.setStyleSheet("""
    background-color: #0D1117;
    font-family: Arial, sans-serif;
""")
root.setGeometry(100, 100, 400, 400)
root.setWindowIcon(QIcon("./Icon/git_logo.ico"))

fleche = QLabel(root)
pixmap = QPixmap("./Icon/fleche.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
fleche.setPixmap(pixmap)
fleche.setGeometry(5, 5, pixmap.width(), pixmap.height())
fleche.setCursor(Qt.PointingHandCursor)
fleche.mousePressEvent = fermer_fenetre


text_title = QLabel("Auto Git", root)
text_title.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica;
    font-size: 30px;
""")
text_title.move(150, 30)
text_title.setCursor(Qt.PointingHandCursor)
text_title.mousePressEvent = label_click

text_lien = QLabel("Lien du Repository", root)
text_lien.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")

text_lien.move(80, 110)

entry1 = QLineEdit(root)
entry1.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;
    font-size: 12px;
""")
entry1.setGeometry(150, 250, 250, 35)
entry1.move(80, 140)

text_chemin = QLabel("Chemin du Dossier", root)
text_chemin.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")
text_chemin.move(80, 190)

entry2 = QLineEdit(root)
entry2.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;  
    font-size: 13px;               
""")
entry2.setGeometry(150, 250, 250, 35)
entry2.move(80, 220)

chargement = QLabel("", root)
chargement.setStyleSheet("""
    color: #ff8c00;
    font-family: Halvetica, sans-serif;
    font-size: 12px;
""")
chargement.move(130, 260)

button = QPushButton("Valider", root)

button.setGeometry(150, 320, 120, 40)
button.setStyleSheet("""
    QPushButton {
        background-color: #161B22;
        color: #ffffff;
        font-family: Halvetica;
        font-size: 15px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
                          
    }
    QPushButton:hover {
        background-color: green;
        color: white;
    }
""")
button.clicked.connect(algo)
root.hide()





# Fenetre 2
root2 = QWidget()
root2.setWindowTitle("Auto git")
root2.setStyleSheet("""
    background-color: #0D1117;
    font-family: Arial, sans-serif;
""")
root2.setGeometry(200, 200, 600, 600)
root2.setWindowIcon(QIcon("./Icon/git_logo.ico"))

fleche = QLabel(root2)
pixmap = QPixmap("./Icon/fleche.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
fleche.setPixmap(pixmap)
fleche.setGeometry(5, 5, pixmap.width(), pixmap.height())
fleche.setCursor(Qt.PointingHandCursor)
fleche.mousePressEvent = fermer_fenetre


text_title = QLabel("Auto Git", root2)
text_title.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica;
    font-size: 30px;
""")
text_title.move(150, 30)
text_title.setCursor(Qt.PointingHandCursor)
text_title.mousePressEvent = label_click

text_lien = QLabel("Lien du Repository", root2)
text_lien.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")

text_lien.move(80, 110)

entry3 = QLineEdit(root2)
entry3.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;
    font-size: 12px;
""")
entry3.setGeometry(150, 250, 250, 35)
entry3.move(80, 140)
dossier_destination = QLabel("Dossier Destination", root2)
dossier_destination.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")
dossier_destination.move(80, 200)


entry4 = QLineEdit(root2)
entry4.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;  
    font-size: 13px;               
""")
entry4.setGeometry(150, 250, 250, 35)
entry4.move(80, 230)


dossier_référence = QLabel("Nouveau Dossier", root2)
dossier_référence.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")
dossier_référence.move(80, 290)

entry5 = QLineEdit(root2)
entry5.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;  
    font-size: 13px;               
""")
entry5.setGeometry(150, 250, 250, 35)
entry5.move(80, 320)


button = QPushButton("Valider", root2)
button.setGeometry(150, 320, 120, 40)
button.setStyleSheet("""
    QPushButton {
        background-color: #161B22;
        color: #ffffff;
        font-family: Halvetica;
        font-size: 15px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
                          
    }
    QPushButton:hover {
        background-color: green;
        color: white;
    }
""")

button.clicked.connect(clone_replace_send)
button.move(140, 400)

message = QWidget()
message.setWindowTitle("Information")
message.setStyleSheet("""
    background-color: white;
    font-family: Halvatica;
    color: black;                 
""")
message.setGeometry(200, 200, 600, 600)
message.setWindowIcon(QIcon("./Icon/git_logo.ico"))
message.hide()

main.show()
sys.exit(app.exec_())
