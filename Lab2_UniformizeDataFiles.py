
# -*- coding: utf-8 -*-

# UniformizeDataFiles.py
#Autor : Boravan Ung and Wantel Simon
# program purpose : Uniformize a list of data files with different number of LinesData on them and rewrite the unifomize
#					data files on new files.

# Open the file with read only permit
# Open the file and we read each line we put each line on a table for 26 case for each parameters
# Then we return a table with all info on file
from operator import attrgetter

import os
import errno
import Config_Function
import ConstantFile as cf
#List of Constants


const_NbParameters= cf.const_NbParameters

const_PathToRemove = cf.const_PathToRemove
const_FileExtension=cf.const_FileExtension

const_Config_File = cf.const_Config_File
const_Folder_Default_File=cf.const_Folder_Default_File

const_Folder_Generate_InfoPathFiles =cf.const_Folder_Generate_InfoPathFiles

const_folder_tidigits = cf.const_folder_tidigits


#Class CfileData
# Use for stocking lineData from DataFiles
class CFileData(object):

    def __init__(self):

        self.LineParameters = ""
        self.ListParameters = []
        self.EnergyStrength = 0.00

    #Function  setListParametersWithLineParameters
    # Parameters vLineParameters : variable type string
    def setListParametersWithLineParameters(self,vLineParameters):
        # Replace \n by nothing

        self.LineParameters= vLineParameters

        "Remove line jump from string"
        vLineParameters = vLineParameters.replace(" \n", "")
        vLineParameters = vLineParameters.replace("\n", "")

        self.ListParameters = vLineParameters.split(" ")
        EnergyStrength = self.ListParameters[12]

        self.EnergyStrength = ConvertParameterStringToNumber(EnergyStrength)

    # Function  setListParametersWithListParametersDecimal
    # Parameters vListParametersDecimal : variable type float
    def setListParametersWithListParametersDecimal(self,vListParametersDecimal):

        self.ListParameters = []
        self.EnergyStrength =float(format(vListParametersDecimal[12],'.6f'))

        for parametersDecimal in vListParametersDecimal:

            # Modify the decimal value to Engineer Notation (we use this format to write in the file).
            self.ListParameters.append(ConvertDecimalToEngrNotation(parametersDecimal))

        self.LineParameters = self.__convertListParametersToLineParameters(self.ListParameters)

    # Private Function  setListParametersWithListParametersDecimal
    # Parameters vListParameters: variable type Array
    def __convertListParametersToLineParameters(self,vListParamters):

        i=0
        tempLineParameters=vListParamters[i]

        for  i  in range(1,const_NbParameters-1):
            tempLineParameters = tempLineParameters +" "+ vListParamters[i]

        tempLineParameters = tempLineParameters + " " + vListParamters[i] +"\n"

        return  tempLineParameters



#Function ConvertParameterStringToNumber
# Use for converting Parameter string on DataFile to a decimal number
def ConvertParameterStringToNumber(vParameterStr):

    Energy = vParameterStr.split("e")

    #Convert value to float to do mathematic operation
    number = float(Energy[0])
    parameterPower = float(Energy[1])
    parameterInNumber = number * (10 ** parameterPower)

    return float(parameterInNumber)


# function ConvertDecimalToEngrNotation(vNbDecimal)
# Convert Decimal to Enginner notation
# We verify if the number is positive and negative then
# if the number in absolute is higher then we find the power by reducing the number 10 just when the numbeer is below 10
# if the number in aboslute is less than  1 then we find the by multiply by 10 just when the number is higher than 0
# with the following notation : 1.168258e+01
def ConvertDecimalToEngrNotation(vNbDecimal):
    if (vNbDecimal < 0):
        isNbNegative = True
    else:
        isNbNegative = False

    strPower=""
    tempNbDecimal = abs(vNbDecimal)


    if tempNbDecimal > 1:
        power = 0
        while tempNbDecimal > 10:
            tempNbDecimal = tempNbDecimal / 10
            power = power + 1

        if (power < 10):
            strPower = "0" + str(power)
        else:
            strPower = str(power)

        strPower = "+" + strPower

    elif (tempNbDecimal ==0 or tempNbDecimal ==1):
        strPower="+" +"00"

    elif tempNbDecimal < 1:
        power = 0
        while tempNbDecimal < 1:
            tempNbDecimal = tempNbDecimal * 10
            power = power + 1

            if (power < 10):
                strPower = "0" + str(power)
            else:
                strPower = str(power)

            strPower = "-" + strPower


    if isNbNegative:
            nbSign = "-"
    else:
            nbSign = ""

    #Writing the decimal number in string format for Data Files

    tempNbDecimal = format(tempNbDecimal,'.6f')
    NbEngrNotation = nbSign + tempNbDecimal + "e" + strPower
    return NbEngrNotation


# function ReadDataFile(file_path)
# Read a data File in get every Data Lines
# REturn an array

def ReadDataFile(file_path):
    LinesData = []

    with open(file_path, "r") as my_file:
        for line in my_file:

            tempLine = line.replace("\n","")
            if (tempLine != ""):
                newLineData= CFileData()

                newLineData.setListParametersWithLineParameters(line)
                LinesData.append(newLineData)

        my_file.close()

    return LinesData


########  RewriteEntryFileToAFixedLineNumber ##################
#Read File then create a file with a fix number of Lines of Data.

def RewriteEntryFileToAFixedLineNumber(filePath,NewNbLineData):

    try:

        ListLineData = ReadDataFile(filePath)
        NbLineData = len(ListLineData)

        # IF the number of line data to have after formating is higher than the number of line of current file
        # We will take the parameters of first line and the parameters for second line then do an average of each parameters to create a new line
        # Then we will do second and third, third and fourth. and we will stop when we will have our number of line we want for reformating fiel
        if (NbLineData < NewNbLineData):

            NbLineToAdd = NewNbLineData - NbLineData

            for i in range(0,NbLineToAdd) :

                index = i
                NewLineListParameters=[]

                for j in range (0,const_NbParameters):
                    NewParameters = (float(ListLineData[index].ListParameters[j])+float(ListLineData[index+1].ListParameters[j]))/2
                    NewParameters = float(format(round(NewParameters,6),'.6f'))
                    NewLineListParameters.append(NewParameters)

                newDataLine = CFileData()
                newDataLine.setListParametersWithListParametersDecimal(NewLineListParameters)

                ListLineData.append(newDataLine)

            SortedListLineData = ListLineData[0:NewNbLineData]  # return the newFileData

        else:
            # If we have more line that we wanted we need, we will do  a sorting with highest Energy's Strenghts and get the number of line for the reformating of the Data File

            ListLineData.sort(key=attrgetter("EnergyStrength"), reverse=True)
            SortedListLineData = ListLineData[0:NewNbLineData]

        newFilePath =filePath.replace(const_folder_tidigits ,const_Folder_Generate_InfoPathFiles +const_folder_tidigits +"_"+ str(NewNbLineData)) # Modify the path for : txt.distr_30/man/...

        # Get the path of the file "NewFilePath"
        newFileDirectory =os.path.dirname(newFilePath)

        # Function to verify if a path exists and if it don't create the path
        if not os.path.exists(newFileDirectory):
            os.makedirs(newFileDirectory)


        # Write LineDatas in the File in the new DataPath
        with open( newFilePath, "w") as text_file:

            for lineData in SortedListLineData:
                text_file.write(lineData.LineParameters)

            text_file.close()

    # If a error happens show it
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise
        print(ex)

# function ReadFileDataPaths(file_path)
# Read a file with the Path of DataFiles
# get a variable with number of line in the file and with the dataPath of the file
# Return an array with every datapath with the number of line in the file

def ReadFileDataPaths(file_path):
    ListDataPath = []

    with open(file_path, "r") as my_file:
        for line in my_file:

            templine=line.replace(const_PathToRemove,"")
            templine = templine.replace("\n","")
            if( templine != ""):
                dataPath= templine.split()
                ListDataPath.append(dataPath)

        my_file.close()
        return ListDataPath



# Method to Uniformize Data Files
def UniformizeDataFiles():
    try:

        # Define the working directory
        # Set the directory working environment
        workingDirectoryPath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(workingDirectoryPath)


        #input("Press Enter to continue...")
        print("initializing Reformating program")
        #const_configFilePath = const_Folder_Default_File + const_Config_File

        #Generated Folder Generating file if it don't exist
        if not os.path.exists(const_Folder_Generate_InfoPathFiles):
            os.makedirs(const_Folder_Generate_InfoPathFiles)
        #input("Press Enter to continue...")
        programConfig =Config_Function.Cinitial_config()
        programConfig.ReadandGetFileConfig()

        listDataFilesName = [cf.constInfoTrainFile, cf.constInfoVcFile, cf.constInfoTestFile]

        # We will go through every file define in the variable listDataFilesName  to get the Path of each Data Files
        # Then for Each Data Files, we will read the Data Lines to write the number of line set in the config File.
        # Then we will write new file with the new  Data PAth of formated Files on the repository define by the constant" const_Folder_Generate_InfoPathFiles "
        if (programConfig.nbDataLinesToGet >0) :

            NewNbLineData = programConfig.nbDataLinesToGet

            #the variable represents the directory for file that has been reformated
            generate_InfoPathFilesDirectoryFullPath = workingDirectoryPath+ "\\"+ const_Folder_Generate_InfoPathFiles +const_folder_tidigits +"_"+ str(NewNbLineData)

            for infoDataFileName in listDataFilesName:

                infoPathDataFile = const_Folder_Default_File +infoDataFileName
                if os.path.isfile(infoPathDataFile):

                    print("Reformating " + infoPathDataFile + "'s file in process")

                    ListFileDataPaths=ReadFileDataPaths(infoPathDataFile)
                    NbDataFiles = len(ListFileDataPaths)

                    for i in range(0,NbDataFiles):

                        fileDataPath = ListFileDataPaths[i][1]
                        if os.path.isfile(fileDataPath):

                            RewriteEntryFileToAFixedLineNumber(fileDataPath,NewNbLineData)
                            ListFileDataPaths[i][0]= NewNbLineData

                            InfoPathDataFileWithoutExtension = infoPathDataFile.replace(const_FileExtension,"")

                            # Replace the folder of the Info_Xx.txt File for a new folder in the "const_Folder_Generate_InfoPathFiles" directory
                            InfoPathDataFileWithoutExtension = InfoPathDataFileWithoutExtension.replace(const_Folder_Default_File,generate_InfoPathFilesDirectoryFullPath +"\\" )
                            newInfoPathDataFile = InfoPathDataFileWithoutExtension +"_" +str(NewNbLineData) + const_FileExtension

                            # Write the new DAta Path of Data Files in the Info_XX.txt Files
                            with open(newInfoPathDataFile, "w") as my_file:

                                for fileDataPath in ListFileDataPaths:

                                    # Modify the path to write the fullPath to access the file from the current workplace (example of Workplace :school,own laptop,etc.)

                                    fileDataFullPath = fileDataPath[1].replace(const_folder_tidigits,"")
                                    fileDataFullPath = generate_InfoPathFilesDirectoryFullPath +fileDataFullPath
                                    fileDataFullPath= fileDataFullPath.replace("\\","/")

                                    my_file.write(str(fileDataPath[0]) +" " +fileDataFullPath   +"\n")

                                my_file.close()

                        else:
                            print("Didn't found the file :"+ fileDataPath )
                    print("Reformating " + InfoPathDataFileWithoutExtension + " Finished")
                else :
                    print("Didn't find "+  infoPathDataFile )
            print("Reformating completed")

            input("Press key and enter to exit")
        else:
            print("Value for NbLineData on Config File need to be higher than 0")

    except OSError as ex:

        print(ex)
        pass



