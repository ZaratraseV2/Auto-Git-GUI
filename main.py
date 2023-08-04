import git
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import webbrowser
from git import Repo
import os
import shutil
import time
import tempfile

app = QApplication(sys.argv)
app.setStyle('Fusion') 


############################################ Fenetre 1 ############################################

def open_root1():
    global main, root, root2  
    main.hide()
    root.show()
    center_window(root) 

def open_root2():
    global main, root, root2 
    main.hide()
    root2.show()
    center_window(root2) 

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
        repo.create_remote("origin", url=lien)
    repo.git.branch("-M", "main")
    repo.git.push("--set-upstream", "origin", "main")
    info2.setText("Fichiers envoyés avec succès !")
    info2.adjustSize()
    QMessageBox.information(message, "Auto Git", "Dossier envoyé avec succès !")
    entry1.clear()
    entry2.clear()
    entry3.clear()  
    entry4.clear()

def center_window(window):
    screen_geometry = QDesktopWidget().screenGeometry()
    window_geometry = window.frameGeometry()
    x_position = (screen_geometry.width() - window_geometry.width()) // 2
    y_position = (screen_geometry.height() - window_geometry.height()) // 2
    window.move(x_position, y_position)

def label_click(event):
    webbrowser.open("https://github.com/new")
def open_github(event):
    webbrowser.open("https://github.com/ZaratraseV2")

###################################################################################################



############################################ Fenetre 2 ############################################

def fermer_fenetre(event):
    global main, root, root2
    if root.isVisible():
        center_window(main)
        root.hide()
        main_pos = root.pos()
    elif root2.isVisible():
        center_window(main)
        root2.hide()
        main_pos = root2.pos()
    main.setGeometry(main_pos.x(), main_pos.y(), 400, 400)
    main.show() 
    entry1.clear()
    entry2.clear()
    entry3.clear()  
    entry4.clear()


def clone_replace_send():
    global info
    lien_clone = entry3.text()
    faux_destination = tempfile.mkdtemp()
    dossier_a_clone = entry4.text()
    segments = lien_clone.split('/')
    name_seg = segments[-1]
    fin_path = name_seg.rstrip('.git')
    destination_path = "\\".join((faux_destination,fin_path))

    # Clonage de Github a PV
    info.setText("Clonage...")
    info.adjustSize()
    Repo.clone_from(lien_clone, destination_path)
    info.setText("Clonage réussit")
    info.adjustSize()

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
    info.setText("Fichiers envoyés avec succès !")
    info.adjustSize()
    QMessageBox.information(message, "Auto Git", "Fichiers envoyés avec succès !")
    entry3.clear()  
    entry4.clear()
    time.sleep(3)
    info.setText("")

###################################################################################################




# Fenetre Principale
main = QWidget()
main.setWindowTitle("Auto git")
main.setStyleSheet("""
    background-color: #0D1117;
    font-family: Arial, sans-serif;
""")
main_width = 400
main_height = 400
screen_geometry = QDesktopWidget().screenGeometry()
main_x = (screen_geometry.width() - main_width) // 2
main_y = (screen_geometry.height() - main_height) // 2
main.setGeometry(main_x, main_y, main_width, main_height)
main.setWindowIcon(QIcon("./Icon/git_logo.ico"))

text_title = QLabel("Auto Git", main)
text_title.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica;
    font-size: 30px;
""")
text_title.move(150, 30)
text_title.adjustSize()

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

layout = QVBoxLayout(main)
layout.setAlignment(Qt.AlignCenter)

github_layout = QVBoxLayout()
github_layout.addStretch(1)
github = QLabel(main)
pixmap = QPixmap("./Icon/github3.png").scaled(80, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
github.setPixmap(pixmap)
github.setAlignment(Qt.AlignCenter)
github.setCursor(Qt.PointingHandCursor)
github.mousePressEvent = open_github
github_layout.addWidget(github)
layout.addLayout(github_layout)


# FENETRE1 
root = QWidget()
root.setWindowTitle("Auto git - Crée un Repository")
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

info2 = QLabel("", root)
info2.setStyleSheet("""
    color: green;
    font-family: Halvetica;
    font-size: 11px;
""")
info2.move(135, 270)

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
button.move(145, 320)
root.hide()



# Fenetre 2
root2 = QWidget()
root2.setWindowTitle("Auto git - Remplacer un Repository")
root2.setStyleSheet("""
    background-color: #0D1117;
    font-family: Arial, sans-serif;
""")
root2.setGeometry(100, 100, 400, 400)
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
text_title.move(145, 30)
text_title.setCursor(Qt.PointingHandCursor)
text_title.mousePressEvent = label_click

text_lien = QLabel("Lien du Repository", root2)
text_lien.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")
text_lien.move(85, 110)


entry3 = QLineEdit(root2)
entry3.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;
    font-size: 12px;
""")
entry3.setGeometry(150, 250, 250, 35)
entry3.move(85, 140)

text_chemin = QLabel("Chemin du Dossier", root2)
text_chemin.setStyleSheet("""
    color: #ffffff;
    font-family: Halvetica, sans-serif;
    font-size: 18px;
""")
text_chemin.move(85, 190)

entry4 = QLineEdit(root2)
entry4.setStyleSheet("""
    color: white;
    border: 2px solid #6E2BF1;
    border-radius: 5px;  
    font-size: 13px;               
""")
entry4.setGeometry(150, 250, 250, 35)
entry4.move(85, 220)

info = QLabel("", root2)
info.setStyleSheet("""
    color: green;
    font-family: Halvetica;
    font-size: 11px;
""")
info.move(135, 270)

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
button.move(145, 320)


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

github = QLabel(root2)
pixmap = QPixmap("./Icon/github.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
github.setPixmap(pixmap)
github.setGeometry(5, 5, pixmap.width(), pixmap.height())
github.setCursor(Qt.PointingHandCursor)
github.mousePressEvent = fermer_fenetre 

main.show()

sys.exit(app.exec_())
