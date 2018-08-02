#List of Constants

const_NbParameters= 26


const_learningNetworkType_LVQ="2"
const_learningNetworkType_NN = "1"

# For LAb2_UniformizeDataFiles
constInfoTrainFile="info_train.txt"
constInfoVcFile="info_vc.txt"
constInfoTestFile="info_test.txt"


const_PathToRemove = "/home/pub/ele-778/labo/labo2/BaseDonnees/"
const_FileExtension= ".txt"

const_Config_File = "Config_File.txt"
const_SavedNeuralNetworkFolder = "SavedFile\\"
const_SavedNeuralNetworkInfo = const_SavedNeuralNetworkFolder +"SavedNeuralNetworkInfo.txt"
const_Folder_Default_File="Default_Files\\"

const_Folder_Generate_InfoPathFiles ="Generate_InfoPathFiles\\"

const_folder_tidigits = "tidigits"
const_Default_InfoPathFile = const_Folder_Generate_InfoPathFiles + const_folder_tidigits +"\\"

const_ConfigFilePath = const_Folder_Default_File + const_Config_File



# Neuron Activation Function
constant_Activation_function_sigmoid =1
constant_Activation_function_tanh =2
constant_Sigmoid = "Sigmoid"
constant_Tanh = "Tanh"

#Output Code
constListOutPutcode_10bits = {
            '1':  [1,0,0,0,0,0,0,0,0,0],
            '2':  [0,1,0,0,0,0,0,0,0,0],
            '3':  [0,0,1,0,0,0,0,0,0,0],
            '4':  [0,0,0,1,0,0,0,0,0,0],
            '5':  [0,0,0,0,1,0,0,0,0,0],
            '6':  [0,0,0,0,0,1,0,0,0,0],
            '7':  [0,0,0,0,0,0,1,0,0,0],
            '8':  [0,0,0,0,0,0,0,1,0,0],
            '9':  [0,0,0,0,0,0,0,0,1,0],
            "o":  [0,0,0,0,0,0,0,0,0,1],
        }

constListOutPutcode_4bits = {
            '1':  [0,0,0,1],
            '2':  [0,0,1,0],
            '3':  [0,0,1,1],
            '4':  [0,1,0,0],
            '5':  [0,1,0,1],
            '6':  [0,1,1,0],
            '7':  [0,1,1,1],
            '8':  [1,0,0,0],
            '9':  [1,0,0,1],
            "o":  [1,1,0,0],
        }

constListClassOutput= {
            "o":  0,
            '1':  1,
            '2':  2,
            '3':  3,
            '4':  4,
            '5':  5,
            '6':  6,
            '7':  7,
            '8':  8,
            '9':  9,

        }




const_nbDataLinesToGet="nbDataLinesToGet"
const_nbLineInDataFiles="nbLineInDataFiles"
const_nbParametersToGetOnDataLines="nbParametersToGetOnDataLines"
const_neuralNetworkNbOutput="neuralNetworkNbOutput"
const_neuronActivationFunction="neuronActivationFunction"
const_listNbNeuronsOnHiddenLayer ="listNbNeuronsOnHiddenLayer"
const_learningRate="learningRate"
const_learningRateDrop ="learningRateDrop"
const_learningRateDropCycle ="learningRateDropCycle "
const_learningRateThreshould = "learningRateThreshould"
const_NbNeuronsOnEachClass="nbNeuronsOnEachClass"



const_momentum="momentum"
const_nbCycle="nbCycle"
const_learningRateThreshould ="learningRateThreshould"
const_percentageResultToEndLearning="percentageResultToEndLearning"

const_lvqNetworkNbClass ="lvqNetworkNbClass"
const_listClassWeight="listClassWeight"

const_listWeight="listWeight"
const_listNeurons="listNeurons"

const_ClassStr="Class"
const_singleSpace =" "

const_ParameterValueSeperator ="="
const_DictionnarySeperator =":"
const_ValueSeperator =","
const_EndOfTheListInSavedFile ="-------------------"
const_Yes="y"
const_No ="n"

ConstCorrectOutput = True
ConstWrongOutput =False


const_CalculDecimalPrecision=5

const_informationType_ToDisplay=1
const_informationType_ToSave=2