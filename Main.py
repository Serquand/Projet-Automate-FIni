from Automate.Automate import * 

def giveAlphabet(numberLetter):
    alphabet = []
    for i in range(numberLetter): 
        alphabet.append(chr(97 + i))
    return alphabet

def giveInitialFinalState(automate): 
    sizeInitialState = int(automate[0])
    initialState = []
    temp = automate.split(' ')
    for i in range(sizeInitialState): 
        initialState.append(int(temp[i + 1]))
    return initialState

def extractAutomateFromFile(): 
    automate = open("./AFTest3.txt", "r")
    my_list = []
    for ligne in automate: 
        my_list.append(ligne)
    return my_list

def parseFirstTab(tabAutomate):
    size = len(tabAutomate)
    for i in range(size):
        if('\n' in tabAutomate[i]):
            tabAutomate[i] = tabAutomate[i].split('\n')[0]
    return tabAutomate

def createAutomate():
    automate = parseFirstTab(extractAutomateFromFile())
    alphabet = giveAlphabet(int(automate[0]))
    numberState = int(automate[1])
    initialState = giveInitialFinalState(automate[2])
    finalState = giveInitialFinalState(automate[3])
    return Automate(len(alphabet), alphabet, initialState, len(initialState), finalState, len(finalState), numberState, automate)

def main() :
    initialAutomate = createAutomate()
    initialAutomate.print()

    initialAsynchrone = initialAutomate.isAsynchronous()
    initialDeterm = initialAutomate.isADetermAF()
    initialFull = initialAutomate.isAFullAF()

    if(initialAsynchrone) :
        print("Cette automate est aynchrone. Nous ne possédons pas la fonction pour supprimer les epsilons-transitions.")
        if(initialDeterm) : print("De plus, il est déterministe.")
        else : print("De plus, il n'est pas déterministe.")
        if(initialFull) : print("Enfin, il est complet.")
        else : print("Enfin, il n'est pas complet.")
        return
    else:
        print("\nCette automate est synchrone.")
        if(initialDeterm) :
            print("Cette automate est déterministe.")
            if(initialFull) :
                print("Cette automate est complet.\n")
            else : 
                print("Cette automate n'est pas complet. Nous allons le compléter.\n")
                #Lancer la complétion
                initialAutomate.completion()
        else :
            print("Cette automate n'est pas déterministe.")
            if(initialFull) : 
                print("Cette automate est complet. \nNous allons le déterminiser et après compléter l'automate obtenu.\n")
            else :
                print("Cette automate est non complet. \nNous allons le déterminiser et le compléter.\n")
            #Lancer la déterminisation
            initialAutomate.determinisation()
            print()

            #Lancer la complétion
            initialAutomate.completion()
            
    #Afficher l'automate
    initialAutomate.print()

    #Lancer la minimisation
    #Lancer la lecture de mot
    initialAutomate.readWord()
    

main()