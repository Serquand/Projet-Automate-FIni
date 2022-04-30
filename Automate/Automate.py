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
        if(int(self.automate[2][0]) != 1) : return False
        for state in self.listState:
            if(state.isADetermState == False): return False
        return True

    def print(self):
        for state in self.listState:
            print(state)

    def completion(self) : 
        self.listState.append(State(self.initialState, self.finalState, self.automate, "P", self.alphabet))
        for state in self.listState: 
            for i in range(len(self.alphabet)):
                if(state.transitionMatrix[i] == []) : state.transitionMatrix[i].append('P')

    def searchInitialState(self):
        for state in self.listState:
            if('E' in state.particularity): 
                return state

    def searchState(self, stateToSearch): 
        for state in self.listState:
            if(str(state.number) == str(stateToSearch)) :
                return state

    def isAcceptedWord(self, word):
        print("Nous allons lancer une reconnaissance sur " + word)
        currentState = self.searchInitialState()
        for letter in word: 
            currentState = self.searchState(currentState.transitionMatrix[ord(letter) - 97][0])
        if('S' in currentState.particularity) : print("Le mot est reconnu")
        else : print("Le mot n'est pas reconnu")
            

    def readWord(self): 
        print("\nNous lançons la fonction de lecture de mot.")
        while(True):
            self.isAcceptedWord(input("Entrez un mot. L'alphabet est : " + str(self.alphabet) + " et nous vous dirons si il accepté.\n"))
            