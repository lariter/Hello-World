

#Save that we can load

#Class Cinitial_config
# Use for stocking file configuration info
# Parameters to stock : NbDataLinesToGet => Nb of line in which each file will be uniformized

# For intialization : take accounts of parameter en NeuralNetwork_Builder_v2

import ConstantFile as cf



class Cinitial_config(object):


    def __init__(self,networkType = cf.const_learningNetworkType_LVQ):

        self.configFileName = cf.const_ConfigFilePath
        self.nbDataLinesToGet = 0 # 30,50,60 # This if for Uniformize

        self.nbLineInDataFiles = 0 # This is for Generate Function
        self.nbParametersToGetOnDataLines =0 # default 26
        self.networkType =networkType


        if(self.networkType == cf.const_learningNetworkType_LVQ):

            # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
            self.lvqNetworkNbClass= 10
            self.nbNeuronsByClass = 0  # [40, self.NbOutput]  # Modify for a table with Independant Nb Neurons for each Hidden Layer
        else:

        # Parameter For Configuring the NEural Network
            self.listNbNeuronsOnHiddenLayer = []  # [40, self.NbOutput]  # Modify for a table with Independant Nb Neurons for each Hidden Layer
            self.momentum = 0  # momentum optionnel



        self.learningRate = 0.1  # taux d'apprentissage
        self.learningRateDrop = 1 # to implement
        self.learningRateDropCycle =10
        self.learningRateThreshould = 0


        # Parameter for Training and Validation Test
        self.nbCycle = 3  # we update our weight value
        self.percentageResultToEndLearning = 50  # in percentage, to configure
		


    # if we have a diese then we don't read the line
    # We read each line to get parameter from the config File
    #
    def ReadandGetFileConfig(self):

        tempLine = ""

        try:
            with open(self. configFileName , "r") as my_file:
                for line in my_file:
                    tempLine = line.replace("\n", "")
                    tempLineArray=tempLine.split(cf.const_ParameterValueSeperator)
                    tempLineParameterName = tempLineArray[0].strip()

                    if ( "##" in line):
                        tempLine =""

                    elif( cf.const_nbDataLinesToGet ==tempLineParameterName ):
                        self.nbDataLinesToGet = int(tempLineArray[1])

                    elif( cf.const_nbLineInDataFiles ==tempLineParameterName ):
                        self.nbLineInDataFiles= int(tempLineArray[1])

                    elif( cf.const_nbParametersToGetOnDataLines ==tempLineParameterName ):
                        self.nbParametersToGetOnDataLines = int(tempLineArray[1])

                    elif( cf.const_lvqNetworkNbClass ==tempLineParameterName ):
                        self.lvqNetworkNbClass = int(tempLineArray[1])

                    elif (cf.const_NbNeuronsOnEachClass ==tempLineParameterName ):
                        self.nbNeuronsByClass= int(tempLineArray[1])


                    #We get the string NbNeuronOnHiddenLayer then we convert it into a list
                    # each item in the list is the number of neuron for each hidden network
                    elif( cf.const_listNbNeuronsOnHiddenLayer   ==tempLineParameterName ):
                        templistNbNeuronsOnHiddenLayer  = (tempLineArray[1])
                        self.listNbNeuronsOnHiddenLayer = list(map(int,templistNbNeuronsOnHiddenLayer .split(cf.const_ValueSeperator)))


                    elif (cf.const_learningRateThreshould ==tempLineParameterName ):
                        self.learningRateThreshould= float(tempLineArray[1])


                    elif( cf.const_learningRate ==tempLineParameterName ):
                        self.learningRate = float(tempLineArray[1])

                    elif( cf.const_learningRateDropCycle ==tempLineParameterName ):
                        self.learningRateDropCycle = float(tempLineArray[1])

                    elif( cf.const_learningRateDrop ==tempLineParameterName ):
                        self.learningRateDrop = float(tempLineArray[1])

                    elif( cf.const_momentum ==tempLineParameterName ):
                        self.momentum  = float(tempLineArray[1])


                    elif( cf.const_nbCycle ==tempLineParameterName ):
                        self.nbCycle = int(tempLineArray[1])

                    elif( cf.const_percentageResultToEndLearning ==tempLineParameterName ):
                        self.percentageResultToEndLearning  = float(tempLineArray[1])

                my_file.close()

        except ValueError:
            print("Not an integer!")
            pass




def test():
    c = Cinitial_config()
    c.ReadandGetFileConfig()
    print("ok")


#test()