class State: 
    def __init__(self, initialState, finalState, automate, number, alphabet):
        self.number = number #Le numéro de l'état
        self.alphabet = alphabet
        self.asynchronous = self.isAsynchronous()
        self.numberTransition = self.findNumberTransition(number, automate)
        self.particularity = self.setParticularity(finalState, initialState, self.number) 
        self.transitionMatrix = self.giveTransitionMatrix(automate)
        self.arrayForEachTransition = self.returnArrayForEachTransition(alphabet, automate, number)
        self.isAFullState = self.isFull()
        self.isADetermState = self.isDeterm()
        self.color = 0

    # Will return the particularity (if the state is an output or an input)
    def setParticularity(self, finalState, initialState, number):
        string = ''
        if(number in finalState) :
            string += 'S'
        if(number in initialState) :
            string += 'E'
        return string

    #Will return the number of the transition for this state
    def findNumberTransition(self, number, automate):
        numberTransition = 0
        for i in range(len(automate) - 5) : 
            if(automate[5 + i].startswith(str(number))) : numberTransition += 1 
        return numberTransition
    
    #Will return an array where each index is for the transition
    def returnArrayForEachTransition(self, alphabet, automate, number):
        arrayFor = []
        addAsy = 1 if '*' in alphabet else 0
        for i in range(len(alphabet)):
            arrayFor.append(0)
        for i in range(len(automate) - 5):
            if(automate[5 + i].startswith(str(number))):
                if(automate[5 + i][1] == '*') : arrayFor[0] += 1
                else :
                    arrayFor[addAsy + ord(automate[5 + i][1]) - 97] += 1
        return arrayFor

    #Will check if the state is asynchronous or not. If it's, also the AF is asynchronous.
    def isAsynchronous(self) :
        return True if '*' in self.alphabet else False

    #Will check if the state is full, we'll just loop on all the AF to see if it's full
    def isFull(self) -> bool: 
        for i in range(len(self.alphabet)):
            if(self.arrayForEachTransition[i] == 0) : return False
        return True

    #Will check if the state is deterministic
    def isDeterm(self) -> bool:
        for i in range(len(self.alphabet)):
            if(self.arrayForEachTransition[i] > 1) : return False
        return True

    def giveTransitionMatrix(self, automate) :
        transitionMatrix = []
        for i in self.alphabet :
            transitionMatrix.append([])
        for i in range(len(automate) - 5) :
            if(automate[5 + i][0] == str(self.number)): 
                index = ord(automate[5 + i][1]) - 97
                transitionMatrix[index].append(automate[5 + i][2])
        return transitionMatrix

    def computeTransition(self) :
        compteur = 0
        for i in range(len(self.alphabet)):
            compteur += len(self.transitionMatrix[i])
        return compteur

    #To print the state
    def __str__(self) -> str:
        return "L'état " + str(self.number) + " est un " + str(self.particularity) + " état. De plus, il contient " + str(self.computeTransition()) + " transitions étant " + str(self.transitionMatrix)