# -*- coding: utf-8 -*-
#DataFileIO
# Class to get every DataFileName from InfoFile ( infotrain.txt; info_vc.txt ; info_
# Class to get input and output from Data File


from Lab2_UniformizeDataFiles import ConvertParameterStringToNumber
import ConstantFile as cf
import os




const_PathToRemove  = cf.const_PathToRemove

constListOutPutcode_10bits = cf.constListOutPutcode_10bits
constListOutPutcode_4bits = cf.constListOutPutcode_4bits

# Class to store info of a infoFile with all the file associated to them
class C_StoreDataFileIO(object):


    def __init__(self,infoDataFileName ,nbParameterToGet,ListOutPutCode =constListOutPutcode_10bits ):
        self.InfoDataFileName = infoDataFileName



        self.NbParamterToGet  =nbParameterToGet
        self.ListOutPutCode = ListOutPutCode
        if(ListOutPutCode ==cf.constListClassOutput):
            self.NbOuput =""
        else:
            self.NbOutput = len(self.ListOutPutCode["1"])

        self.listDataFile =[]
        self.SetFileIOFromInfoDataFile()
        self.nbDataFile = len(self.listDataFile)



    def SetFileIOFromInfoDataFile(self):
        listDataFileName = self.ReadFileDataPaths(self.InfoDataFileName)

        listFileIO= []
        for dataFileName in listDataFileName:

            fileInput= self.GetInputFromDataFile(dataFileName )
            fileOutput= self.GetOutputFromDataFile(dataFileName )
            newFileIO = fileIO(dataFileName,fileInput,fileOutput)
            listFileIO.append(newFileIO)

        self.listDataFile=listFileIO



    # Method to get all dataFileName from file info_XX.txt
    def ReadFileDataPaths(self,file_path):
        ListDataPath = []

        with open(file_path, "r") as my_file:
            for line in my_file:

                templine = line.replace(const_PathToRemove, "")
                templine = templine.replace("\n", "")
                if (templine != ""):
                    dataPath = templine.split(" ",1)[1]
                    ListDataPath.append(dataPath)

            my_file.close()
            return ListDataPath


    def SetdataFileIO(self,infoDataFileName,nbParameterToGet,ListOutPutCode =constListOutPutcode_10bits ):

        self.InfoDataFileName = infoDataFileName
        self.listDataFileName = self.ReadFileDataPaths(self.InfoDataFileName)
        self.NbParamterToGet = nbParameterToGet
        self.ListOutPutCode = ListOutPutCode
        self.nbDataFile = len(listDataFileName)

        # Start Of the test of class DataFileIO
        #dataFile

        # With A config File
        print("DefaultConfig")


      # We read a data file and we get the entry of the file
        #  We use the NbParameter toGet to set the number of Entry we will get from the file
    # The total entry from a data file is numberOfParameterToGEt * NumberOfDataLine on the file
    def GetInputFromDataFile(self,dataFileName):
        # Read File then Get the number of parameters equal the
        listInput = []
        i = 0

        nbParametersToGet=self.NbParamterToGet


        with open(dataFileName, "r") as my_file:
            for line in my_file:

                tempLine = line.replace("\n", "")
                if (tempLine != ""):
                    # We get a table with the first twelve parameters from each line
                     listParameters = line.split(" ")[0:nbParametersToGet]

                for parameter in listParameters[0:nbParametersToGet]:
                        #i=1+i
                        # We convert Parameters written on the file on float format
                        #listInput[str(i)] = ConvertParameterStringToNumber(parameter)
                        listInput.append(ConvertParameterStringToNumber(parameter))

            my_file.close()

            return listInput

    #Return the DesiredOutputInAString
    #We get the output of the DataFile in the File NAme
    # Example for the following data file: tidigits_30/txt_dist/test/man/nr/8b.txt
    # His output will be 8 . The output will always be in the same position for all Data Files.
    def GetOutputFromDataFile(self,dataFileName):
        # Read File then Get the number of parameters equal the
            DataFileName =  dataFileName.split("/")[-1]
            output =  DataFileName[0]
            outputCode= self.ListOutPutCode[output]

            return outputCode


    #Return the DesiredOutputInAString
    #We get the output of the DataFile in the File NAme
    # Example for the following data file: tidigits_30/txt_dist/test/man/nr/8b.txt
    # His output will be 8 . The output will always be in the same position for all Data Files.
    def GetOutputClassFromDataFile(self,indexOfFileToGet):
        # Read File then Get the number of parameters equal the
            DataFileName =  self.listDataFileName[indexOfFileToGet].split("/")[-1]
            output =  DataFileName[0]
            outputCode= self.ListOutPutCode[output]

            return outputCode


# Class to store the input and the output of a dataFile
class fileIO(object):

    def __init__(self, fileName, fileInput, fileOutput):
        self.fileName = fileName
        self.fileInput = fileInput
        self.fileOutput = fileOutput


