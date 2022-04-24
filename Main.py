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
    automate = open("./AFTest.txt", "r")
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
    AutomateFinal = createAutomate()
    if(AutomateFinal.isAFullAF()) : print("Cette automate est complet")
    else : print("Cette automate n'est pas complet")
    if(AutomateFinal.isADetermAF()) : print("Cette automate est déterministe")
    else : print("Cette automate n'est pas déterministe")
    if(AutomateFinal.isAsynchronous()) : print("L'automate est asynchrone")
    else : print("L'automate est synchrone")
    AutomateFinal.print()

main()