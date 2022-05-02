from State.State import *

class Automate: 
    def __init__(self, longueur, alphabet, initialState, nbInitialState, finalState, nbFinalState, nbState, automate):
        self.alphabet = alphabet #char array
        self.initialState = initialState #char array
        self.finalState = finalState #char array
        self.listState = self.setListState(automate) #State array
        self.automate = automate
        self.numberColor = 2 #For minimization

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
        currentState = self.searchInitialState()
        for letter in word:
            currentState = self.searchState(currentState.transitionMatrix[ord(letter) - 97])

        #On a fait le complémentaire avant donc on inverse la logique
        if('S' not in currentState.particularity) : 
            print("Le mot est reconnu par l'automate initial et donc pas par son complémentaire")
        else : 
            print("Le mot n'est pas reconnu par l'automate initial et est donc reconnu par son complémentaire")
            

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


    def bubbleSort(self, arr):
        n = len(arr)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if arr[j] > arr[j + 1] :
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


    # Génére un tableau d'entier contenant les différentes entiers de la transition
    # Bubble sort sur ce tableau d'entier
    # Reforme la transition
    # Print la transition pour voir si elle est correcte
    # Retourne la transition            
    def bubbleSortMain(self, transition) :
        entierTransition = []
        for letter in transition:
            entierTransition.append(int(letter))
        entierTransition = self.bubbleSort(entierTransition)
        transition = ""
        for letter in entierTransition :
            transition += str(letter)
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
        transition = self.bubbleSortMain(transition) 
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
        statesToStudy[0].particularity = "E"
        for state in statesToStudy:
            state.particularity += self.particularityStateDeterm(state)
        self.listState = statesToStudy

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


    def tabIsDifferent(self, oldColor) :
        i = 0
        for state in self.listState:
            if(state.color != oldColor[i]) : return True
            i += 1
        return False

    def searchNumberArray(self, transitionMatrix):
        numberArray = []
        for transition in transitionMatrix:
            numberArray.append(self.searchState(transition[0]).color)
        return numberArray


    # Nous allons ajouter la condition de savoir si un autre état ayant les mêmes transitions mais pas la même couleur de base :    
    def isInMatrix(self, color, matrixDone) :
        for i in range (len(matrixDone)):
            if(color == matrixDone[i]):
                return i 

        self.numberColor += 1
        matrixDone.append(color)
        return self.numberColor - 1

    def computeColor(self, colorMatrix):
        self.numberColor = 0
        matrixToAssign = []
        matrixDone = []
        for i in range(len(colorMatrix)) : 
            matrixToAssign.append(self.isInMatrix(colorMatrix[i], matrixDone))
        return matrixToAssign

    def minimisation(self) :
        oldColor = []
        for state in self.listState: 
            oldColor.append(state.color)
        for state in self.listState:
            if('S' in state.particularity) :
                state.color = 2
        while(self.tabIsDifferent(oldColor)) :
            # Nous allons commencer en assigner à oldColor les couleurs de self.listState.color
            i = 0
            for state in self.listState :
                oldColor[i] = state.color
                i -= -1

            # Nous allons ensuite créer la matrice des couleurs
            colorMatrix = []
            i = 0
            for state in self.listState:
                colorMatrix.append(self.searchNumberArray(state.transitionMatrix))
                colorMatrix[i].append(state.color)
                i += 1

            # On regarde si il y a des états différents --- BuG PROBABLE ---
            i = 0
            matrixToAssign = self.computeColor(colorMatrix)
            for state in self.listState:
                state.color = matrixToAssign[i]
                i += 1

        # On va combiner les différents états
        numberStateFin = 0
        for state in self.listState:
            if(state.color > numberStateFin) :
                numberStateFin = state.color
        numberStateFin += 1

        newListStateName = []
        for i in range(numberStateFin) :
            currentStateName = ''
            for state in self.listState:
                if(state.color == i) :
                    currentStateName += str(state.number) + '-'
            newListStateName.append(currentStateName[:-1])

        # On va créer maintenant les états et les ajouter dans un tableau
        newListState = []
        for stateName in newListStateName:
            newListState.append(State(self.initialState, self.finalState, self.automate, stateName, self.alphabet))

        # On va réassigner les transitions et les particularités
        for i in range(len(newListState)):
            stateToSearch = newListState[i].number.split("-")[0]
            oldState = self.searchState(stateToSearch)
            newListState[i].transitionMatrix = oldState.transitionMatrix
            for j in range(len(self.alphabet)):
                for listeState in newListStateName :
                    if(newListState[i].transitionMatrix[j][0] in listeState) :
                        newListState[i].transitionMatrix[j] = listeState
            newListState[i].particularity = oldState.particularity

        # On va remplacer l'ancien automate par celui venant d'être crée
        self.listState = newListState


    def complementaire(self): 
        i = 0
        particularity = []
        for state in self.listState :
            particularity.append('')
            if('ES' == state.particularity) : particularity[i] = 'E'
            elif('S' == state.particularity) : particularity[i] = ''
            elif('E' == state.particularity) : particularity[i] = 'ES'
            else : particularity[i] = 'S'
            i += 1
        for j in range(i) : 
            self.listState[j].particularity = particularity[j]
