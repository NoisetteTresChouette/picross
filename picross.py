import matplotlib.pyplot as plt
from numpy import inf
from random import randint
from gogol import wait
from gogol import test_int
from time import time

doImage = True

def home(doImage):
    print('\nQue voulez-vous faire?\n')
    while True:
        task = str(input('1. Jouer\n2. Créer\n3. Image: '+(doImage)*'on' +(not(doImage))*'off'+'\n4. Quitter\n'))
        if task in ['1','2','4']:
            break
        elif task == '3':
            doImage = not(doImage)
        else:
            print('\nVeuillez Réessayer\n')
    if task =='1':
        print('\nQuel puzzle voulez-vous jouer?')
        while True:
            task = str(input('1. Au hasard\n2. Custom\n3. Annuler\n'))
            if task in ['1','2','3']:
                break
            else:
                print('\nVeuillez réessayer\n')
        if task == '1':
            play(doImage)
        elif task == '2':
            while True:
                task = input('\nAvec quoi voulez-vous chercher?\n1. Le titre\n2. Le code\n3. Annuler\n')
                if task not in ['1','2','3']:
                    print('\n Veuillez réessayer\n')
                else:
                    break
            if task == '1':
                print('not available yet')
            elif task == '2':
                key = input('\nVeuillez saisir la clef: ')
                keys =[]
                fichier = open('Picross Custom.txt','r')
                infos = fichier.read()
                fichier.close()
                if infos == ['']:
                    infos = []
                else:
                    infos = infos.split('\t')
                    while '\n\n' in infos:
                        infos.remove('\n\n')
                    infos.pop(0)
                for k in range(3,len(infos),4):
                    clef = ((''.join(infos[k])).split(': '))[1]
                    keys.append(clef)
                if key in keys:
                    puzzle = decode(key)
                    print('\nVous allez jouer à: ' + infos[4*keys.index(key)][9:])
                    play(doImage,puzzle,key)
                else:
                    while True:
                        playing = input('\nCette partie n\'existe pas, voulez vous tout de même y jour? [Y/N]\n').lower()
                        if playing not in ['y','n']:
                            print ('\nVeuillez réessayer\n')
                        else:
                            break
                    if playing == 'y':
                        puzzle = decode (key)
                        if puzzle != None:
                            play(doImage,puzzle,key)
                        else:
                            print('\nErreur de saisie, le code n\'a pas pu être lu\n')
                            home(doIamge)
                    else:
                        home(doImage)
            elif task == '3':
                home(doImage)
        elif task == '3':
            home(doImage)
    elif task == '2':
        edit(doImage)
        home(doImage)

def grid(L,C):
    return  [[[1.,1.,1.] for j in range(C) ]for i in range(L)]

def noires(M):
    cycle = True
    L = len(M)
    C = len(M[0])
    for i in range(L):
        for j in range(C):
            couleur = randint(0,1)
            if couleur == 0:
                M[i][j] = [0,0,0]
    for i in range(L):
        for j in range(C):
            if M[i][j] == [0,0,0]:
                cycle = False
                break
        if cycle == False:
            break
    if cycle == True:
        M = noires(M)
    return M

def indices(M):
    I=[[[] for i in range(len(M))],[[] for j in range(len(M[0]))]]
    for i in range(len(M)):
        k = 0
        for j in range(len(M[i])):
            if M[i][j] == [1.,1.,1.] and not(len(I[0][i]) == 0):
                I[0][i].append(' ')
                k += 1
            elif M[i][j] == [0.,0.,0.]:
                if len(I[0][i]) == 0:
                    I[0][i].append(1)
                    k += 1
                elif I[0][i][k-1] == ' ':
                    I[0][i].append(1)
                    k += 1
                elif I[0][i][k-1] != ' ':
                    I[0][i][k-1] += 1
    for j in range(len(M[0])):
        k = 0
        for i in range(len(M)):
            if M[i][j] == [1.,1.,1.] and not(len(I[1][j]) == 0):
                I[1][j].append(' ')
                k += 1
            elif M[i][j] == [0.,0.,0.]:
                if len(I[1][j]) == 0:
                    I[1][j].append(1)
                    k += 1
                elif I[1][j][k-1] == ' ':
                    I[1][j].append(1)
                    k += 1
                elif I[1][j][k-1] != ' ':
                    I[1][j][k-1] += 1
    return I

def clean(I):
    for k in range(2):
        for l in range(len(I[k])):
            for m in range(len(I[k][l])):
                I[k][l][m] = str(I[k][l][m])
            if I[k][l] == []:
                I[k][l] = ['0']
            else:
                while ' ' in I[k][l]:
                    I[k][l].remove(' ')
    return I

def edit(doImage):
    puzzle = grid(5,5)
    clef = None
    index_lignes = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    index_lignes = index_lignes[:len(puzzle)]
    edition = True
    black =False
    print('\nBienvenue dans l\'éditeur de niveau')
    print('Vous pouvez taper "/help" pour obtenir les commandes de l\'éditeur')
    while edition == True:
        while True:
            dim = False
            prop = input('\nVeuillez saisir les coordonnées à colorier: ')
            if prop in ['/help','/black','/dim','/save','/quit','/import']:
                break
            else:
                saisie = True
                dim = True
                prop = prop.split(',')
                while '' in prop:
                    prop.remove('')
                for k in prop:
                    if len(k) < 2 or k[0] not in ['a','b','c','d','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                        saisie = False
                        break
                    elif test_int(k[1:]) == False:
                        saisie = False
                        break
                if saisie == False:
                    print('\nMauvaise saisie, Veuillez réessayer\n')
                else:
                    for k in prop:
                        if k[0] not in index_lignes or int(k[1:]) > len(puzzle[0]) or int(k[1:]) <=0:
                            dim = False
                            print('\nCoordonnées innexistantes, Veuillez réessayer\n')
                            break
                if saisie == True and dim == True:
                    break
        if prop == '/black':
            black = not black
            for i in range(len(puzzle)):
                for j in range(len(puzzle[0])):
                    for k in range(3):
                        puzzle[i][j][k] = 1. - puzzle[i][j][k]
        elif prop == '/dim':
            while True:
                dim = input('\nQuelles dimension désirez-vous?')
                dim = dim.split('x')
                if len(dim) != 2 :
                    print('\nMauvaise saisie, Veuillez réessayer\n')
                elif not test_int(dim[0]) or not test_int(dim[1]):
                    print('\nMauvaise saisie, Veuillez réessayer\n')
                elif (int(dim[0]) >= 10) or (int(dim[0]) >= 9):
                    print('\nTrop grande dimension 9x9, Veuillez réessayer\n')
                elif (int(dim[0]) <= 0) or (int(dim[1]) <= 0):
                    print('\nDimension 0 impossible, Veuillez réessayer\n')
                else:
                    break
            L = int(dim[0])
            C = int(dim[1])
            if L < len(puzzle):
                for _ in range(len(puzzle) - L):
                    puzzle.pop()
            else:
                for _ in range(L - len(puzzle)):
                    if black == False:
                        puzzle.append([[1.,1.,1.] for k in range(len(puzzle[0]))])
                    else:
                        puzzle.append([[0.,0.,0.] for k in range(len(puzzle[0]))])
            old_C = len(puzzle[0])
            if C < old_C:
                for i in range(len(puzzle)):
                    for _ in range(old_C - C):
                        puzzle[i].pop()
            else:
                for i in range(len(puzzle)):
                    for _ in range(C - old_C):
                        if black == False:
                            puzzle[i].append([1.,1.,1.])
                        else:
                            puzzle[i].append([0.,0.,0.])
            index_lignes = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            index_lignes = index_lignes[:len(puzzle)]
        elif prop == '/quit':
            print('\nToute progression non sauvegardée sera perdue')
            while True:
                stop = input('Voulez vous quitter l\'éditeur? [Y/N]\n').lower()
                if stop not in ['y','n']:
                    print('\nVeuillez réessayer\n')
                else:
                    break
            if stop == 'y':
                edition = False
        elif prop == '/save':
            fichier = open('Picross Custom.txt','r')
            infos = fichier.read()
            fichier.close()
            infos = infos.split('\t')
            while '\n\n' in infos:
                infos.remove('\n\n')
            if infos != ['']:
                infos.pop(0)
            else:
                infos = []
            if clef != None:
                old_keys = []
                for k in range(3,len(infos),4):
                    old_keys.append(infos[k][6:])
                num_puzzle = old_keys.index(clef)
            save = input('\nVoulez-vous enregistrer ce puzzle? [Y/N]\n').lower()
            while True:
                if save not in ['y','n']:
                    print('\nVeuillez réessayer\n')
                else:
                    break
            if save == 'y':
                add = True
                if clef != None:
                    delete = input('Voulez-vous supprimer l\'ancienne sauvegarde? [Y/N]\n').lower()
                    while True:
                        if delete not in ['y','n']:
                            print('Veuillez réessayer')
                        else:
                            break
                    titre = infos[0 + 4*int(num_puzzle)][7:]
                    clef = encodage(puzzle,None,None)
                    if delete == 'y':
                        add = False
                        infos[1 + 4*int(num_puzzle)] = 'Temps: ' + temps
                        infos[2 + 4*int(num_puzzle)] = 'x: ' + str(x)
                        infos[3 + 4*int(num_puzzle)] = 'Clef: ' + clef
                else:
                    titre = input('\nQuel titre voulez vous donner à ce puzzle?\n')
                    clef = encodage(puzzle,None,None)
                if add == True:
                    infos.append('\n\nTitre: '+titre)
                    infos.append('Temps: '+'None')
                    infos.append('x: '+'None')
                    infos.append('Clef: '+clef)
                infos.append('\n\n')
                infos = tri(infos)
                fichier = open('Picross Custom.txt','w')
                fichier.write('Picross Custom\t'+'\t'.join(infos))
                fichier.close()
                wait(0,'Partie Sauvegardée')
            while True:
                stop = input('\nVoulez vous continuer à travailler sur ce puzzle? [Y/N]\n').lower()
                if stop not in ['y','n']:
                    print('\nVeuillez réessayer\n')
                else:
                    break
            if stop == 'n':
                edition = False
        elif prop == '/import':
            while True:
                task = input('\nAvec quoi voulez-vous chercher?\n1. Le titre\n2. Le code\n3. Annuler\n')
                if task not in ['1','2','3']:
                    print('\n Veuillez réessayer\n')
                else:
                    break
            if task == '1':
                print('not available yet')
            elif task == '2':
                key = input('\nVeuillez saisir la clef: ')
                keys =[]
                fichier = open('Picross Custom.txt','r')
                infos = fichier.read()
                fichier.close()
                if infos == ['']:
                    infos = []
                else:
                    infos = infos.split('\t')
                    while '\n\n' in infos:
                        infos.remove('\n\n')
                    infos.pop(0)
                for k in range(3,len(infos),4):
                    clef = ((''.join(infos[k])).split(': '))[1]
                    keys.append(clef)
                if key in keys:
                    puzzle = decode(key)
                    print('\nVoici: ' + infos[4*keys.index(key)][9:])
                else:
                    print('\nCe puzzle n\'existe pas\n')
        elif prop == '/help':
            need_help = True
            First = True
            print('\nDans cette éditeur, vous pouvez créer vos propres puzzle.\nPour ce faire, saisissez les coordonnées des cases dont vous voulez changer la couleur, le puzzle faisant innitialement du 5x5.')
            while need_help == True:
                while True:
                    if First == True:
                        task = input('Vous pouvez également saisir différentes commandes, voulez-vous que je les explique:\n1. Non merci\n2. "/black"\n3. "/dim"\n4. "/import"\n5. "/quit"\n6. "/save"\n')
                    else:
                        task = input('Voulez vous d\'autres explications:\n1. Non merci\n2. "/black"\n3. "/dim"\n4. "/import"\n5. "/quit"\n6. "/save"\n')
                    if task not in ['1','2','3','4','5','6']:
                        print('\nVeuillez réessayer\n')
                    else:
                        break
                if task == '1':
                    need_help = False
                    break
                elif task == '2':
                    print('\nLa commande "/black" permet d\'inverser la couleur des cases existantes\n')
                elif task == '3':
                    print('\nLa commande "/dim" permet de modifier la dimension du puzzle, celle-ci étant innitialement 5x5\n')
                elif task == '4':
                    print('\nLa commande "/import" permet d\'importer des puzzles déjà existant afin de les modifier\n')
                elif task == '5':
                    print('\nLa commande "/quit" permet tout simplement de quitter l\'éditeur\n')
                elif task == '6':
                    print('\nLa commande "/save" permet de sauvegarder le puzzle sur lequel vous travaillez\n')
                First = False
        else:
            for k in prop:
                for c in range(3):
                    puzzle[index_lignes.index(k[0])][int(k[1:]) - 1][c] = 1. - puzzle[index_lignes.index(k[0])][int(k[1:])-1][c]
        if edition == True:
            display(doImage,puzzle,puzzle)

def display(doImage,puzzle,tableau):
    index_lignes = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    index_colonnes = ''
    for k in range(len(puzzle[0])):
        index_colonnes += str((k+1)%10)
    print('\n')
    I = indices(puzzle)
    I = clean(I)
    L = len(I[0][0])
    for k in I[0]:
        if len(k) > L:
            L = len(k)
    C = len(I[1][0])
    for k in I[1]:
        if len(k) > C:
            C = len(k)
    for c in range(C-1,-1,-1):
        indice = ''
        for k in I[1]:
            if len(k) > c:
                indice += k[len(k)-c-1]
            else:
                indice += ' '
        print(' '*L + indice)
    for j in range(len(puzzle)):
        indice = ''
        for l in range(L-1,-1,-1):
            if len(I[0][j]) > l:
                indice += I[0][j][len(I[0][j])-l-1]
            else:
                indice +=' '
        grille = ''
        for k in range(len(tableau[0])):
            if tableau[j][k] == [0.,0.,0.]:
                grille += 'N'
            elif tableau[j][k] == [1.,0.,0.]:
                grille += 'x'
            elif tableau[j][k] == [1.,1.,1.]:
                grille += '.'
        print(indice + grille+index_lignes[j])
    print(' '*L + index_colonnes)
    if doImage == True:
        x = [ k for k in range(len(puzzle[0]))]
        xlabels = [''.join(I[1][k]) for k in range(len(puzzle[0]))]
        y = [k for k in range(len(puzzle))]
        ylabels = [''.join(I[0][k]) for k in range(len(puzzle))]
        plt.yticks(y,ylabels)
        plt.xticks(x,xlabels)
        plt.imshow(tableau)
        plt.show()

def play(doImage,puzzle=None,clef = None):
    First = True
    Win = False
    if puzzle==None:
        while True:
            dim = input('\nQuelles dimension désirez-vous? (sous la forme: LIGNESxCOLONNES)\n')
            dim = dim.split('x')
            if len(dim) != 2 :
                print('\nMauvaise saisie, Veuillez réessayer\n')
            elif not test_int(dim[0]) or not test_int(dim[1]):
                print('\nMauvaise saisie, Veuillez réessayer\n')
            elif (int(dim[0]) >= 10) or (int(dim[1]) >= 10):
                print('\nDimension trop grande (au plus 9x9), Veuillez réessayer\n')
            elif (int(dim[0]) <= 0) or (int(dim[1]) <= 0):
                print('\nDimension 0 impossible, Veuillez réessayer\n')
            else:
                break
        L = int(dim[0])
        C = int(dim[1])
        puzzle = noires(grid(L,C))
    tableau = grid(len(puzzle),len(puzzle[0]))
    index_lignes = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    index_lignes = index_lignes[:len(puzzle)]
    x = 0
    print('\nBonne partie!')
    start =time()
    while Win==False:
        display(doImage,puzzle,tableau)
        prop= input('\nQuelles sont vos propositions?\n'+ First * '(Sous la forme: A1,A2,C4,..., avec A la ligne et 1 la colonne.)\n').lower()
        First = False
        type = False
        dim = False
        while type == False or dim == False:
            type = True
            dim = True
            prop = prop.split(',')
            while '' in prop:
                prop.remove('')
            for k in prop:
                if len(k) < 2 or k[0] not in ['a','b','c','d','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                    type = False
                    break
                elif test_int(k[1:]) == False:
                    type = False
                    break
            if type == False:
                print('\nMauvaise saisie, Veuillez réessayer\n')
                prop= input('\nQuelles sont vos propositions?\n(Sous la forme: A1,A2,C4,..., avec A la ligne et 1 la colonne\n').lower()
            else:
                for k in prop:
                    if k[0] not in index_lignes or int(k[1:]) > len(puzzle[0]) or int(k[1:]) <=0:
                        dim = False
                        print('\nCoordonnées innexistantes, Veuillez réessayer\n')
                        prop = input('\nQuelles sont vos propositions?\n').lower()
                        break
        for k in prop:
            if puzzle[index_lignes.index(k[0])][int(k[1:])-1] == [0.,0.,0.]:
                tableau[index_lignes.index(k[0])][int(k[1:])-1] = [0.,0.,0.]
            else:
                tableau[index_lignes.index(k[0])][int(k[1:])-1] = [1.,0.,0.]
                x += 1
        Win = test_win(puzzle,tableau)
    end = time()
    temps = str(int((end-start)//60)) +'min ' +str(int((end-start)%60))+'s'
    print('\n\nC\'Est Gagné!\n(En '+temps+' et '+str(x)+'x)'+'\n\n')
    for i in range(len(tableau)):
        for j in range(len(tableau[0])):
            if tableau[i][j] != [0.,0.,0.]:
                tableau[i][j] = [0.,1.,0.]
    if doImage == True:
        plt.imshow(tableau)
        plt.show()
    sauvegarde(puzzle,clef,start,end,temps,x)
    home(doImage)

def test_win(puzzle,tableau):
    test = True
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j]==[0.,0.,0.] and tableau[i][j] != [0.,0.,0.]:
                test = False
    return test

def sauvegarde(puzzle,clef,start=None,end=None,temps=None,x=None):
    fichier = open('Picross Custom.txt','r')
    infos = fichier.read()
    fichier.close()
    infos = infos.split('\t')
    while '\n\n' in infos:
        infos.remove('\n\n')
    if infos != ['']:
        infos.pop(0)
    else:
        infos = []
    if clef != None:
        new_record = False
        old_keys = []
        for k in range(3,len(infos),4):
            old_keys.append(infos[k][6:])
        num_puzzle = old_keys.index(clef)
        old_x = infos[2+4*int(num_puzzle)]
        old_temps= infos[1+4*int(num_puzzle)]
        old_temps = old_temps.split(': ')[1]
        if old_temps != 'None':
            old_temps = old_temps.split('min ')
            old_temps = 60 * int(old_temps[0]) + int(old_temps[1][:-1])
        else:
            old_temps = inf
        old_x = old_x.split(': ')[1]
        if old_x != 'None':
            old_x = int(old_x)
        else:
            old_x = inf
        print((old_temps > end-start)*('Nouveau record de temps!\n')+(old_x > x)*('Nouveau record de x!\n'))
        if old_temps > end-start or old_x > x:
            new_record = True
    if doImage == False:
        wait(3)
    if clef == None or new_record == True:
        save = input('\nVoulez-vous enregistrer cette partie? [Y/N]\n').lower()
        while True:
            if save not in ['y','n']:
                print('\nVeuillez réessayer\n')
            else:
                break
        if save == 'y':
            add = True
            if clef != None:
                while True:
                    delete = input('Voulez-vous supprimer l\'ancienne? [Y/N]\n').lower()
                    if delete not in ['y','n']:
                        print('\nVeuillez réessayer\n')
                    else:
                        break
                titre = infos[0 + 4*int(num_puzzle)][7:]
                clef = encodage(puzzle,temps,x)
                if delete == 'y':
                    add = False
                    infos[1 + 4*int(num_puzzle)] = 'Temps: ' + temps
                    infos[2 + 4*int(num_puzzle)] = 'x: ' + str(x)
                    infos[3 + 4*int(num_puzzle)] = 'Clef: ' + clef
            else:
                titre = input('\nQuel titre voulez vous donner à cette partie?\n')
                clef = encodage(puzzle,temps,x)
            if add == True:
                infos.append('\n\nTitre: '+titre)
                infos.append('Temps: '+temps)
                infos.append('x: '+str(x))
                infos.append('Clef: '+clef)
            infos.append('\n\n')
            infos = tri(infos)
            fichier = open('Picross Custom.txt','w')
            fichier.write('Picross Custom\t'+'\t'.join(infos))
            fichier.close()
            wait(0,'Partie Sauvegardée')

def tri(infos):
    return infos

def encodage(puzzle,temps,x):
    ligne = 'L'+str(len(puzzle))
    colonne = 'C'+str(len(puzzle[0]))
    code = ligne + colonne
    key = 'K'
    grille = 'G'
    for k in range(3):
        key += str(randint(0,9))
    paire_black = True
    grand_change = True
    milieu_change = True
    if int(key[1]) % 2 != 0:
        paire_black = False
    if int(key[2]) < 5 :
        grand_change = False
    if int(key[3]) not in [3,4,5,6,7]:
        milieu_change = False
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == [0.,0.,0.]:
                grille += str(2*randint(0,4) + (not paire_black))
            else:
                grille += str(2*randint(0,4) + paire_black)
            if int(grille[-1]) >= 5 and grand_change:
                paire_black = not paire_black
            if int(grille[-1]) < 5 and not grand_change:
                paire_black = not paire_black
            if int(grille[-1]) in [3,4,5,6,7] and milieu_change:
                grand_change = not grand_change
            if int(grille[-1]) not in [3,4,5,6,7] and not milieu_change:
                grand_change = not grand_change
    code += key + grille
    if temps == None:
        code += 'T' + str(temps)
    else:
        code += 'T' + ''.join(temps.split(' '))
    code += 'X' + str(x)
    return code

def decode(key):
    for k in ['C','K','G','T']:
        if key.count(k) != 1:
            return None
    if key[0] != 'L' :
        return None
    L = ''
    i = 1
    rajout = True
    while rajout == True:
        if key[i] != 'C':
            L += key[i]
        else:
            rajout = False
        i += 1
    if not test_int(L):
        return None
    L = int(L)
    C = ''
    rajout = True
    while rajout == True:
        if key[i] != 'K':
            C += key[i]
        else:
            rajout = False
        i += 1
    if not test_int(C):
        return None
    C = int(C)
    i -= 1
    if key[i] != 'K' :
        return None
    i += 1
    code = ''
    j = key.index('G')
    for k in range(i,j):
        code += key[k]
    i = j +1
    if len(code) != 3 or not test_int(code):
        return None
    j = key.index('T')
    grille = key[i:j]
    if not test_int(grille) or len(grille) != int(L*C):
        return None
    puzzle = grid(L,C)
    paire_black = (int(code[0])%2 == 0)
    grand_change = (int(code[1]) >= 5)
    milieu_change = (int(code[2]) in [3,4,5,6,7])
    i = 0
    j = 0
    for k in grille:
        if paire_black == True and int(k) % 2 == 0:
            puzzle[i][j] = [0.,0.,0.]
        if paire_black != True and int(k) % 2 != 0:
            puzzle[i][j] = [0.,0.,0.]
        if int(k) >= 5 and grand_change:
            paire_black = not paire_black
        if int(k) < 5 and not grand_change:
            paire_black = not paire_black
        if int(k) in [3,4,5,6,7] and milieu_change:
            grand_change = not grand_change
        if int(k) not in [3,4,5,6,7] and not milieu_change:
            grand_change = not grand_change
        if j < C-1:
            j += 1
        else:
            j = 0
            i += 1
    return puzzle






""" \tClef:L...C...K...G...\t\n\n"""
""" infos : titre  temps   x    clef"""


print('\nBonjour')
wait(2)
home(doImage)
print('bye')

