# -*- coding: utf-8 -*-

from LVQ_Network import LVQNetwork,LVQNeuron
from DataFileIO import C_StoreDataFileIO
from Config_Function import Cinitial_config
import ConstantFile as cf
import random
import os

import Config_Function

constFirstListIndex = 0

ConstCorrectOutput = True



class LVQNetworkBuilder(object):

    def __init__(self,learningNetwork_Type=cf.const_learningNetworkType_LVQ):
        # Will be Initialize on  with parameter on ConfigFile.txt

        # AddFuntion to uniformize DataFile

        # Parameter for the reading of File DataFile
        self.nbLineInDataFiles = 0  # use also for uniformize DataFile #same thing that  self.nbLineInDataFiles
        self.nbParametersToGetOnDataLines = 0
        self.nbInput = self.nbParametersToGetOnDataLines * self.nbLineInDataFiles

        self.networkType = learningNetwork_Type

        if (self.networkType == cf.const_learningNetworkType_LVQ):
            # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
            self.nbClass = 0
            self.nbNeuronsByClass= 0
            self.nbNeuron = 0
        else:

            self.neuronActivationFunction = 1
            self.listNbNeuronsOnHiddenLayer = []
            self.momentum = 0.5  # momentum optionnel

        self.learningRate = 0  # taux d'apprentissage
        self.learningRateDrop = 0 # learning rate drop rate
        self.learningRateDropCycle = 1


        # Parameter for Training and Validation Test
        self.nbCycle = 0  # we update our weight value
        self.learningRateThreshould = 0

        self.percentageResultToEndLearning = 0  # in percentage, to configure

        self.InitializeDefault_Config()

        # Variable For DataInfoFile
        self.listInfoDataFileIO = {}
        self.InitializeDataFileIO()

        self.trainResult = 0
        self.vcResult = 0
        self.testResult = 0





        # Initialization of LVQ with Default value
        if (self.networkType == cf.const_learningNetworkType_LVQ):
            listWeight = self.GetDefaultListWeight(self.nbClass,self.nbNeuronsByClass)  # Change list Neurons to Get

            self.LVQNetwork = LVQNetwork(self.nbInput, self.nbClass,self.nbNeuronsByClass, listWeight, self.learningRate,self.learningRateDrop)
        else:

            # Initialization of NEuralNetwork with Default value
            self.neuralNetwork = NeuralNetwork(self.nbInput, listNbNeuronsOnLayer, self.learningRate,
                                               self.neuronActivationFunction, self.momentum)




        # List Train InputIndex to pick random data during Learning Phase
        self.listTrainDataInputIndex = []

        infoTrain_IO = self.listInfoDataFileIO[cf.constInfoTrainFile]
        self.listTrainDataInputIndex = self.__setListInputIndexForTrainFile(infoTrain_IO.nbDataFile)


    #Get the first element input to set them like weight
    # ask if we should take the first element
    def GetDefaultListWeight1(self,nbClass,nbNeuronsOnEachClass):

        listWeight =[]
        listTrainDataFile = self.listInfoDataFileIO[cf.constInfoTrainFile].listDataFile[:]
        nbVectorWeightToGet= nbClass*nbNeuronsOnEachClass
        for i in range(0, nbVectorWeightToGet):
            classToGet = i% nbClass

            for j in range(0,len(listTrainDataFile)):
                if(classToGet==listTrainDataFile[j].fileOutput):
                    fileVectorInput = listTrainDataFile.pop(j)
                    listWeight.append(fileVectorInput.fileInput)
                    break

        # initialize list Weight

        return listWeight

    #Get the first element input to set them like weight
    # ask if we should take the first element
    def GetDefaultListWeight(self,nbClass,nbNeuronsOnEachClass):

        listWeight =[]
        listTrainDataFile = self.listInfoDataFileIO[cf.constInfoTrainFile].listDataFile[:]
        nbVectorWeightToGet= nbClass*nbNeuronsOnEachClass
        for i in range(0, nbVectorWeightToGet):
            listWeight.append(listTrainDataFile[i].fileInput)

        # initialize list Weight

        return listWeight

    def Update_LVQNetwork(self):

        # initialize list Weight

        listWeight = self.GetDefaultListWeight(self.nbClass, self.nbNeuronsByClass)  # Change list Neurons to Get
        #Initialization of NEuralNetwork with Default value
        self.LVQNetwork = LVQNetwork(self.nbInput, self.nbClass,self.nbNeuronsByClass, listWeight, self.learningRate,self.learningRateDrop)


    def InitializeDataFileIO(self):

        listDataFilesName = [cf.constInfoTrainFile, cf.constInfoVcFile, cf.constInfoTestFile]
        listOutPutCode = []

        if(self.networkType == cf.const_learningNetworkType_LVQ):
            listOutPutCode = cf.constListClassOutput


        elif (self.networkType == cf.const_learningNetworkType_NN):
            if (self.nbClass == 10):
                listOutPutCode = cf.constListOutPutcode_4bits

            else:
                listOutPutCode = cf.constListOutPutcode_10bits



        for infoDataFile in listDataFilesName:
            fileInfoDataFile = self.SetdataFileInfoPath(infoDataFile, self.nbLineInDataFiles)
            self.listInfoDataFileIO[infoDataFile] = C_StoreDataFileIO(fileInfoDataFile, self.nbParametersToGetOnDataLines,
                                                                 listOutPutCode)

    # mehtod UpdateInput
    # use to update the number of total input
    def UpdateInput(self):
        self.nbInput = self.nbParametersToGetOnDataLines * self.nbLineInDataFiles



    #Modify for LVQ
    def InitializeDefault_Config(self):
        dConfig = Cinitial_config()
        dConfig.ReadandGetFileConfig()
        # With A config File

        # Parameter for the reading of File DataFile
        self.nbLineInDataFiles = dConfig.nbLineInDataFiles  # use also for uniformize DataFile #same thing that  self.nbLineInDataFiles
        self.nbParametersToGetOnDataLines = dConfig.nbParametersToGetOnDataLines

        self.nbInput = self.nbParametersToGetOnDataLines * self.nbLineInDataFiles

        if(self.networkType==cf.const_learningNetworkType_LVQ):
        # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
            self.nbClass = dConfig.lvqNetworkNbClass
            self.nbNeuronsByClass = dConfig.nbNeuronsByClass
            self.nbNeuron =self.nbClass * self.nbNeuronsByClass

        elif(self.networkType==cf.const_learningNetworkType_NN):

            self.listNbNeuronsOnHiddenLayer = dConfig.listNbNeuronsOnHiddenLayer


        self.learningRateDrop  = dConfig.learningRateDrop

        # Parameter For Configuring the NEural Network

        self.learningRate = dConfig.learningRate  # taux d'apprentissage


        # Parameter for Training and Validation Test
        self.learningRateThreshould = dConfig.learningRateThreshould
        self.nbCycle = dConfig.nbCycle  # we update our weight value
        self.percentageResultToEndLearning = dConfig.percentageResultToEndLearning  # in percentage, to configure
        print("Initialize DefaultConfig")

    # SetdataFileInfoPath
    # We use the function to add a filte path to  a file name
    # Example filename = "info_train.txt" will become Generate_InfoPathFiles\tidigits_30.info_train_30.txt
    # So we can get the location of the infoDatafile
    def SetdataFileInfoPath(self, infoDataFile, nbLineInDataFiles):
        # Concatonate the path from the infoData File

        defaultinfoDataFilePath = cf.const_Default_InfoPathFile + infoDataFile

        infoDataFilePath = defaultinfoDataFilePath.replace(cf.const_folder_tidigits,
                                                           cf.const_folder_tidigits + "_" + "{}".format(
                                                               nbLineInDataFiles))
        infoDataFilePath = infoDataFilePath.replace(cf.const_FileExtension,
                                                    "_" + "{}".format(nbLineInDataFiles) + cf.const_FileExtension)

        return infoDataFilePath



    # iterate through all the dataFiles For updating neural Network

    # This create a list with number 0 to nb of dataFile on the info data file(Example of data file : infotrain.txt)
    # This list will be use to randomly pick our data File for training purpose
    def __setListInputIndexForTrainFile(self, nbDataFile):

        listInputIndex = []
        for i in range(constFirstListIndex, nbDataFile):
            listInputIndex.append(i)

        return listInputIndex

    # TrainNeuralNetwork()
    # First we get a list with value all index representing all our data file example 0 to 1339
    # Then we will shuffle all the index to put then on a random order
    # We will read our listInputIndex to get the index to read.
    def TrainLVQNetwork(self):

        print("Training Cycle")

        listInputIndex = self.listTrainDataInputIndex
        lvqNetwork= self.LVQNetwork
        # Shuffle to get a random order of value
        random.shuffle(listInputIndex)

        InfoTrain_IO = self.listInfoDataFileIO[cf.constInfoTrainFile]

        i = 0
        for trainDatainputIndex in listInputIndex:
            # Setting Input and Output with DataFile
            vectorInput = InfoTrain_IO.listDataFile[trainDatainputIndex].fileInput
            inputExpectedClass = InfoTrain_IO.listDataFile[trainDatainputIndex].fileOutput
            lvqNetwork.UpdateNetwork(vectorInput ,inputExpectedClass)
            i = i + 1
            #print(i)

    # We run the feedForward then we compare output of outputlayer with the desiredOutput associated to the entry data
    def ValidateData(self, infoDataFile):
        lvqNetwork = self.LVQNetwork

        listInfoData_IO = self.listInfoDataFileIO[infoDataFile]
        nbData = listInfoData_IO .nbDataFile

        nbSuccess = 0

        for i in range(0, nbData): # rechange to nbData

            # print(i)
            inputVector= listInfoData_IO .listDataFile[i].fileInput
            inputExpectedClass = listInfoData_IO.listDataFile[i].fileOutput

            isCorrectOuput = self.LVQNetwork.isCorrectOutput(inputVector , inputExpectedClass)

            if isCorrectOuput:
                nbSuccess = nbSuccess + 1

        percentageSuccess = nbSuccess / nbData * 100
        return percentageSuccess




    def TrainDataValidation(self):

        self.trainResult = round(self.ValidateData(cf.constInfoTrainFile), 2)
        print("TrainDataValidation success Rate:" + str(self.trainResult))

    def CrossedValidation(self):

        self.vcResult = round(self.ValidateData(cf.constInfoVcFile), 2)
        print("CrossedValidation success Rate:" + str(self.vcResult))

    # Same thing that CrossedValidation but with data file in  infotext_XX.txt
    def LearningTest(self):
        self.testResult = round(self.ValidateData(cf.constInfoTestFile), 2)
        print("Learning Test :" + str(self.testResult))




    def TrainAndTestLVQNetwork(self):

        nbCycle = self.nbCycle
        for cycle in range(0, nbCycle):
            self.TrainLVQNetwork()
            self.TrainDataValidation()
            #self.CrossedValidation()
            #self.LearningTest()

            self.LVQNetwork.CalculateNewLearningRate()

            if( self.vcResult > self.percentageResultToEndLearning):
                break

    # DisplayNeuralNetworkInfo
    # return all NeuralNetwork_Builder information on a string
    # we dont't return Neuron or Weight
    def DisplayNeuralNetworkInfo(self):
        displayText = ""

        displayText = self.GetNetworkInformationStr(cf.const_informationType_ToDisplay)
        return displayText


    def GetNetworkInformationStr(self,informationType):

        tempLine=""
        if(informationType== cf.const_informationType_ToSave):

            tempLine += "##" + "SaveNeuralNetworkFile" + "\n"
            tempLine  += "##" + "TrainDataValidation success Rate:" + str(self.trainResult) + "\n"
            tempLine  += "##" + "CrossedValidation success Rate:" + str(self.vcResult) + "\n"
            tempLine  += "##" + "Learning Test :" + str(self.testResult) + "\n"


        tempLine += cf.const_nbLineInDataFiles + " " + cf.const_ParameterValueSeperator + " " + str(
            self.nbLineInDataFiles) + "\n"

        tempLine += cf.const_nbParametersToGetOnDataLines + " " + cf.const_ParameterValueSeperator + " " + str(
            self.nbParametersToGetOnDataLines) + "\n"

        tempLine += cf.const_lvqNetworkNbClass + " " + cf.const_ParameterValueSeperator + " " + str(
            self.nbClass) + "\n"

        tempLine += cf.const_NbNeuronsOnEachClass + " " + cf.const_ParameterValueSeperator + " " + str(
            self.nbNeuronsByClass) + "\n"

        tempLine += cf.const_learningRate + " " + cf.const_ParameterValueSeperator + " " + str(self.learningRate) + "\n"
        tempLine += cf.const_learningRateDrop + " " + cf.const_ParameterValueSeperator + " " + str(self.learningRateDrop) + "\n"


        tempLine += cf.const_nbCycle + " " + cf.const_ParameterValueSeperator + " " + str(self.nbCycle) + "\n"
        tempLine += cf.const_learningRateThreshould  + " " + cf.const_ParameterValueSeperator + " " + str(self.learningRateThreshould) + "\n"

        tempLine += cf.const_percentageResultToEndLearning + " " + cf.const_ParameterValueSeperator + " " + str(
            self.percentageResultToEndLearning) + "\n"

        if (informationType == cf.const_informationType_ToSave):
            tempLine += cf.const_listNeurons + " " + cf.const_ParameterValueSeperator + "\n"


            i=0
            for currentNeuron in self.LVQNetwork.listNeuron:
                tempLine +="Neuron {} {}".format(i,cf.const_ClassStr) + cf.const_ParameterValueSeperator + "{}".format(currentNeuron.outputClass)+ "\n"
                tempLine += "##  Weights " + "\n"
                j=0
                for weight in currentNeuron.listWeight:

                    tempLine += "   {}.{} ".format(i,j)+ cf.const_ParameterValueSeperator + "{}".format(weight) +"\n"
                    j=j+1
                i = i + 1

                tempLine += cf.const_EndOfTheListInSavedFile + "\n"  # Represent the end of the list


        return tempLine



    def SaveCurrentNetwork(self, fileName=cf.const_SavedNeuralNetworkInfo):

        infoNetworkLine=self.GetNetworkInformationStr(cf.const_informationType_ToSave)

        if not os.path.exists(cf.const_SavedNeuralNetworkFolder):
            os.makedirs(cf.const_SavedNeuralNetworkFolder)

        try:
            with open(fileName, "w") as my_file:
                my_file.writelines(infoNetworkLine)
                my_file.close()

        except ValueError:
            print("Not an integer!")
            pass

    # LoadSavedNetworkInfo
    # get The save from a save file
    def LoadSavedNetworkInfo(self, networkInfoFile=cf.const_SavedNeuralNetworkInfo):
        try:
            readWeight = False
            readNeuron= False

            tempClass = 0
            listWeight = []
            listNeuron= []

            with open(networkInfoFile, "r") as my_file:
                for line in my_file:
                    tempLine = line.replace("\n", "")
                    tempLineArray = tempLine.split(cf.const_ParameterValueSeperator)
                    tempLineParameterName = tempLineArray[0].strip()

                    if ("##" in tempLine):
                        tempLine = ""

                    elif (cf.const_EndOfTheListInSavedFile in tempLine):
                        newNeuron=LVQNeuron(tempClass,listWeight)
                        listNeuron.append(newNeuron)
                        readWeight=False


                    elif readWeight:

                        listWeight.append( float(tempLine.split(cf.const_ParameterValueSeperator)[1]))


                    elif (cf.const_nbDataLinesToGet == tempLineParameterName):
                        self.nbDataLinesToGet = int(tempLineArray[1])

                    elif (cf.const_nbLineInDataFiles == tempLineParameterName):
                        self.nbLineInDataFiles = int(tempLineArray[1])

                    elif (cf.const_nbParametersToGetOnDataLines == tempLineParameterName):
                        self.nbParametersToGetOnDataLines = int(tempLineArray[1])

                    elif (cf.const_lvqNetworkNbClass == tempLineParameterName):
                        self.lvqNetworkNbClass = int(tempLineArray[1])

                    elif (cf.const_NbNeuronsOnEachClass == tempLineParameterName):
                        self.nbNeuronsByClass = int(tempLineArray[1])

                        # We get the string NbNeuronOnHiddenLayer then we convert it into a list
                        # each item in the list is the number of neuron for each hidden network
                    elif (cf.const_listNbNeuronsOnHiddenLayer == tempLineParameterName):
                        templistNbNeuronsOnHiddenLayer = (tempLineArray[1])
                        self.listNbNeuronsOnHiddenLayer = list(
                            map(int, templistNbNeuronsOnHiddenLayer.split(cf.const_ValueSeperator)))


                    elif (cf.const_learningRateThreshould == tempLineParameterName):
                        self.learningRateThreshould = float(tempLineArray[1])


                    elif (cf.const_learningRate == tempLineParameterName):
                        self.learningRate = float(tempLineArray[1])

                    elif (cf.const_learningRateDropCycle == tempLineParameterName):
                        self.learningRateDropCycle = float(tempLineArray[1])

                    elif (cf.const_learningRateDrop == tempLineParameterName):
                        self.learningRateDrop = float(tempLineArray[1])

                    elif (cf.const_momentum == tempLineParameterName):
                        self.momentum = float(tempLineArray[1])


                    elif (cf.const_nbCycle == tempLineParameterName):
                        self.nbCycle = int(tempLineArray[1])

                    elif (cf.const_percentageResultToEndLearning == tempLineParameterName):
                        self.percentageResultToEndLearning = float(tempLineArray[1])

                    elif (cf.const_listNeurons in tempLine):
                        readNeuron = True

                    elif (cf.const_ClassStr in tempLine and readNeuron):
                        tempClass= int(tempLine.split(cf.const_ParameterValueSeperator)[1])
                        listWeight = []
                        readWeight = True

                my_file.close()

                self.Update_LVQNetwork()
                self.LVQNetwork.listNeurons = listNeuron


        except OSError as ex:
            print("Not an integer!")
            pass


def MainPRog1():
    try:


        n = LVQNetworkBuilder()
        #n.LoadSavedNetworkInfo()
        #n.SaveCurrentNetwork()

        n.TrainAndTestLVQNetwork()
        #n.SaveCurrentNetwork()
        #n = NeuralNetworkBuilder()
        #n.LoadSavedNetworkInfo()
       # n.TrainAndTestNeuralNetwork()

        print("Ending")




    except OSError as ex:

        print(ex)
        pass


#MainPRog1()