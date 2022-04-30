from gettext import translation
from State.State import *

class Automate: 
    # longueur correspond à la taille du mot 
    # alphabet correspond à l'alphabet utilisé par l'Automate
    # initialState, nbInitialState, finalState, nbFinalState correspond aux nombres/états finaux/initiaux
    # nbState correspond dans le nombre d'état
    # automate est l'ensemble du fichier de manière à pouvoir créer les différents états
    def __init__(self, longueur, alphabet, initialState, nbInitialState, finalState, nbFinalState, nbState, automate):
        self.alphabet = alphabet #char array
        self.initialState = initialState #char array
        self.finalState = finalState #char array
        self.listState = self.setListState(automate) #State array
        self.automate = automate

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

    def searchAllInitialStateNumber(self) :
        allInitialStateNumber = ''
        for state in self.listState:
            if('E' in state.particularity) :
                allInitialStateNumber += str(state.number)
        return allInitialStateNumber

    def searchAllTransition(self, letterState, letterAlphabet): 
        longueur = len(self.searchState(letterState).transitionMatrix[letterAlphabet])
        if(longueur == 0) : return ''
        elif (longueur == 1) : return self.searchState(letterState).transitionMatrix[letterAlphabet][0] 
        else : 
            transition = ''
            for i in range(longueur) :
                transition += self.searchState(letterState).transitionMatrix[letterAlphabet][i]
            return transition
                    
    def epureTransition(self, transition) : 
        allTransition = []
        allTransition.append(transition[0])
        compteur = 0
        for i in transition:
            if(i not in allTransition) : 
                allTransition.append(i)
                compteur += 1
        transition = ''
        for i in range(len(allTransition)) :
            transition += allTransition[i]
        return transition

    def searchDontDo(self, listStateDAF) :
        for state in listStateDAF:
            for i in range(len(self.alphabet)):
                if(len(state.transitionMatrix[i]) == 1): 
                    askState = state.transitionMatrix[i][0]
                    alreadyStudy = False
                    for state2 in listStateDAF:
                        if(state2.number == askState) : 
                            alreadyStudy = True 
                    if(alreadyStudy == False) : return askState

        return 'Any'
        
    def particularityStateDeterm(self, state):
        for i in self.finalState:
            if(str(i) in str(state.number)) :
                return "S"
        return ""

    def finishDeterminization(self, statesToStudy): 
        print("We will finish determinization")
        statesToStudy[0].particularity = "E"
        for state in statesToStudy:
            state.particularity += self.particularityStateDeterm(state)
        self.listState = statesToStudy
        for state in statesToStudy:
            print(state)
        

    def determinisation(self) :
        listStateDAF = [] 
        initialStateNumber = self.searchAllInitialStateNumber()
        listStateDAF.append(State(self.initialState, self.finalState, self.automate, initialStateNumber, self.alphabet))
        for letterAlphabet in self.alphabet:
            letterAlphabet = ord(letterAlphabet) - 97
            transition = ''
            for letterState in initialStateNumber:
                transition += self.searchAllTransition(letterState, letterAlphabet)
            if(len(transition) > 1) :
                transition = self.epureTransition(transition)
            if(len(transition) != 0) :
                listStateDAF[0].transitionMatrix[letterAlphabet].append(transition)

        while(True) :
            stateToStudy = self.searchDontDo(listStateDAF)
            if(stateToStudy == 'Any') :
                self.finishDeterminization(listStateDAF)
                return 
            listStateDAF.append(State(self.initialState, self.finalState, self.automate, stateToStudy, self.alphabet))
            for letterAlphabet in self.alphabet:
                letterAlphabet = ord(letterAlphabet) - 97
                transition = ''
                for letterState in stateToStudy:
                    transition += self.searchAllTransition(letterState, letterAlphabet)
                if(len(transition) > 1) :
                    transition = self.epureTransition(transition)
                if(len(transition) != 0) :
                    longueur = len(listStateDAF)
                    listStateDAF[longueur - 1].transitionMatrix[letterAlphabet] = []
                    listStateDAF[longueur - 1].transitionMatrix[letterAlphabet].append(transition)