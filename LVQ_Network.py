


from math import sqrt,floor
import ConstantFile as cf
from heapq import nsmallest

constFirstListIndex =0
class LVQNetwork(object):

    def __init__(self,nbVectorParameter ,nbClass,nbNeuronsByClass,listVectorForInitializeWeight,learningRate,learningRateDrop):




        self.listNeuron=[] # each neurons reprensents a class
        self.nbVectorParameter = nbVectorParameter
        self.nbClass = nbClass
        self.nbNeuronsOnCompetitiveLayer = nbClass* nbNeuronsByClass

        self.learningRate = learningRate # a
        self.learningRateDrop = learningRateDrop

        self.InitializeNeurons(listVectorForInitializeWeight)

        #self.inputVector = []

        #self.expectedOutput = []  # output is an array
        #self.InitWeight(self.nbInput)

        self.tempListInput_NeuronDistance=[]
        self.inittempListInput_NeuronDistance()

    def InitializeNeurons(self,vectorWeight):
        listNeuron=[]

        for i in range(0,self.nbNeuronsOnCompetitiveLayer):
            outputClass= i% self.nbClass
            newNeuron = LVQNeuron(outputClass,vectorWeight[i])
            listNeuron.append(newNeuron)


        self.listNeuron=listNeuron
            # to be continue

    def InitializeWeight(self,nbVectorParameter):
        weight=[]
        for i in range(0,nbVectorParameter):
            weightValue = random.uniform(-0.1, 0.1)
            weight.append(weightValue)


    def setLearningRate(self,newLearningRate):
        self.learningRate= newLearningRate


    def inittempListInput_NeuronDistance(self):
        tempList=[]
        for i in range(constFirstListIndex, self.nbNeuronsOnCompetitiveLayer):
            tempList.append(0)

        self.tempListInput_NeuronDistance=tempList




    def GetClosestNeuronsFromInput(self,inputVector,nbVectorParameter,nbNeuronToGet=1):

        currentNeuron = 0

        # We verify every class
        for currentNeuron in range(0, self.nbNeuronsOnCompetitiveLayer):
                self.tempListInput_NeuronDistance[currentNeuron] = self.CalculateEuclideanDistance(inputVector, self.listNeuron[currentNeuron].listWeight, nbVectorParameter)

        closestNeuronsFromInput=nsmallest(nbNeuronToGet, range(len(self.tempListInput_NeuronDistance)), key=self.tempListInput_NeuronDistance.__getitem__)[0]

        return closestNeuronsFromInput

    def CalculateEuclideanDistance(self, v1, v2,nbParameterOfVector):
        distance = 0
        for i in range(0, nbParameterOfVector):
            distance = distance + (v1[i] - v2[i]) ** 2

        distance = sqrt(distance)
        return distance


    def UpdateNetwork(self,inputVector,inputClass):

        # 1- Find the closest class to the entry
        closestNeuron = self.GetClosestNeuronsFromInput(inputVector,self.nbVectorParameter)

        # 2 - Update weight
        self.UpdateWeight(inputVector,inputClass,closestNeuron)


        # 3 - atteint la valeur minimal oule taux d'apprentissage minimum ( implement in LVQ_Builder)

    def isCorrectOutput(self, inputVector,inputExpectedClass):

        closestNeuron = self.GetClosestNeuronsFromInput(inputVector,self.nbVectorParameter)

        neuron  = self.listNeuron[closestNeuron]
        if neuron.outputClass == inputExpectedClass :
            return cf.ConstCorrectOutput
        else:
            return cf.ConstWrongOutput

    def CalculateLearningRateWithStepDecay(self,learningRateDrop,currentCycle,nbCycle):
        self.learningRate = self.learningRate*learningRateDrop**floor(currentCycle/nbCycle)


    def CalculateLearningRateWithTimeDecay(self,learningRateDrop,currentCycle):
        self.learningRate *= 1/(1+learningRateDrop*currentCycle)

    def CalculateNewLearningRate(self):
        self.learningRate *=self.learningRateDrop


    # Function to determine the new  Representative
    # See Chapter 4 to better explanation
    def UpdateWeight(self,inputVector, expectedInputClass,closestNeuron):

        tempLR =self.learningRate
        oldWeight =0
        # We verify every class

        neuron = self.listNeuron[closestNeuron]

        if (expectedInputClass!= neuron.outputClass):
            tempLR = -1 * tempLR


        for i in range(0,self.nbVectorParameter):

            oldWeight = neuron.listWeight[i]
            self.listNeuron[closestNeuron].listWeight[i] = oldWeight + tempLR * (inputVector[i]-oldWeight)


    # OPTIONNAL
    # if we have enough time
    def UpdateWeightWithAdapatationRule(self,inputLVQ,nbInput, inputClass):

        tempLR =self.learningRate
        oldWeight =0
        # We verify every class
        for currentClass in range(0, self.nbClass):

            if (inputClass != currentClass):
                tempLR = -1 * tempLR

            for i in range(0, nbInput):
                oldWeight = self.listNeuron[weightClass][i]
                self.listNeuron[currentClass][i] = oldWeight + tempLR * (inputLVQ[i]-oldWeight)

        # if the value is the same weight then
        print("ok")






    # Process where we find le critère



# Class Neuron
# We don't use the attibute self.threshould (but could use on future application)
class LVQNeuron(object):

    def __init__(self,outputClass,VectorWeight):
        self.outputClass= outputClass
        self.listWeight=VectorWeight




def test():

     listNeuron = [
         [1,1,0,0],
         [0, 0, 0, 1],
         #[0, 0, 1, 1],
         #[0, 1, 1, 0]

     ]


     nbInput = 4
     learningRate = 0.1
     nbOutput = 2
     nbNeuron=1
     lvq = LVQNetwork(nbInput,nbOutput,nbNeuron,listNeuron,learningRate)
     inputq = [0,0,1,1]
     lvq.UpdateNetwork(inputq,1)

     inputq = [1,0,0,0]
     lvq.UpdateNetwork(inputq,0)

     inputq = [0, 1, 1, 0]
     lvq.UpdateNetwork(inputq, 1)


     x=0
     inputq = listNeuron[0]
     result= lvq.isCorrectOutput(inputq,1)
     if(result== True):
         x= x+1

     inputq = listNeuron[1]
     result = lvq.isCorrectOutput(inputq, 1)
     if (result == True):
         x = x + 1

     inputq = listNeuron[1]
     result= lvq.isCorrectOutput(inputq,1)
     if(result== True):
         x= x+1

     inputq = listNeuron[0]
     result= lvq.isCorrectOutput(inputq,1)
     if(result== True):
         x= x+1
     print(x)

     print("ok")



#test()

