from State.State import *

class Automate: 
    # longueur correspond à la taille du mot 
    # alphabet correspond à l'alphabet utilisé par l'Automate
    # initialState, nbInitialState, finalState, nbFinalState correspond aux nombres/états finaux/initiaux
    # nbState correspond dans le nombre d'état
    # automate est l'ensemble du fichier de manière à pouvoir créer les différents états
    def __init__(self, longueur, alphabet, initialState, nbInitialState, finalState, nbFinalState, nbState, automate):
        self.longueur = longueur #int
        self.alphabet = alphabet #char array
        self.initialState = initialState #char array
        self.nbInitialState = nbInitialState #int
        self.nbFinalState = nbFinalState #int
        self.finalState = finalState #char array
        self.listState = self.setListState(automate) #State array
        self.nbState = nbState #int
        self.automate = automate
        self.isAsynchronous()

    def findTheMaxState(self) -> int:
        max = self.listState[0].number
        print(max)
        compteur = 1
        for i in range (self.nbState - 1): 
            if self.listState[compteur].number > max:
                max = self.listState[compteur].number
            compteur += 1
        return len(str(max))

    def printHr(self, longueur, asciiTable, maxState) :
        line = asciiTable[8]
        for i in range (longueur):
            if((i == 16) or (i == 19 + max(5, maxState)) or (i == 23 + max(5, maxState))) : 
                line += asciiTable[9]
            else : line += asciiTable[1]
        line += asciiTable[7]
        print(line)

    def printState(self, asciiTable, longueur, number) : 
        line = asciiTable[3] + "       " + self.listState[number].particularity + "       " + asciiTable[3] + "   " + str(number) + "   " + asciiTable[3] + " " 
        print(line)

    def print(self):
        symboleAscii = ['╔', '═', '╗', '║', '╦', '╝', '╚', '╣', '╠', '╬']
        maxState = self.findTheMaxState()
        longueur = 19 + (maxState + 3) * len(self.alphabet) + max(5, maxState) 
        line = symboleAscii[0]
        for i in range(longueur) : 
            if((i == 16) or (i == 19 + max(5, maxState)) or (i == 23 + max(5, maxState))) : 
                line += symboleAscii[4] 
            else : line += symboleAscii[1]
        line += symboleAscii[2]
        print(line)
        print(symboleAscii[3] + " Particularités " + symboleAscii[3] + " Etats " + symboleAscii[3] + " A " + symboleAscii[3] + " B " + symboleAscii[3])
        self.printHr(longueur, symboleAscii, maxState)
        self.printState(symboleAscii, longueur, 0)
        

    def isAsynchronous(self) -> bool:
        for i in range (len(self.automate) - 5):
            if(self.automate[5 + i][1] == '*'): 
                self.alphabet.append('*')
                return True
        return False

    def setListState(self, automate): 
        listStateReturn = []
        compteur = 0
        numberState = int(automate[1])
        for state in range (numberState):
            listStateReturn.append(State(self.initialState, self.finalState, automate, compteur, self.alphabet))
            compteur += 1
        return listStateReturn

    def isAFullAF(self) -> bool :
        for state in self.listState:
            if(state.isAFullState == False): return False
        return True

    def isADetermAF(self) -> bool:
        for state in self.listState:
            if(state.isADetermState == False): return False
        return True