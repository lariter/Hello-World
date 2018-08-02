# -*- coding: utf-8 -*-
#GraphicalInterface


from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
from LVQ_NetworkBuilder import LVQNetworkBuilder
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showinfo

import ConstantFile as cf

import os

const_networkInfoFile ="Neural Network Info File ="

class GUI_LearningNetwork_Builder():
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self):

        # Load NEural Network Builder
        self.learningNetwork = LVQNetworkBuilder()

        self.networkInfoFile= "new"
        # Configure the GUI
        self.window = Tk()
        self.window.geometry("660x480")

        style = ttk.Style(self.window)
        style.configure('Treeview', rowheight=20)
        self.InitInterface()

        self.UpdateGUIDefaultSetting()

        self.listResults=[]
        self.LoadData(self.listResults)


    # Inialize Gui button, label and treeview
    def InitInterface(self):
        self.InitFrameButtonMenu(self.window)

        self.label_networkInfoFile = Label(self.window,
                                                 text="Network Info File =" + self.networkInfoFile)  # (3 choice) (30,50,60)
        self.label_networkInfoFile.pack(side=TOP)

        self.leftWindow = Frame(self.window, borderwidth=2, width=100, height=100, relief=GROOVE)
        self.leftWindow.pack(side=LEFT, fill=Y)

        self.rightWindow = Frame(self.window, borderwidth=2, width=100, height=100, relief=GROOVE)
        self.rightWindow.pack(side=RIGHT, fill=Y)

        self.InitLabelFrameSettingDataFiles(self.leftWindow)
        self.InitFrameNeuralNetwork(self.leftWindow)

        self.InitFrameLearningDataProcess(self.leftWindow)

        self.button_UpdateSetting = Button(self.leftWindow, text="Update Setting", command=self.UpdateSetting)
        self.button_UpdateSetting.pack()

        self.label_trainingDataResult = Label(self.rightWindow,
                                              text="Training Data result")  # in percentage, to configure (valuminim minimum 1%)
        self.label_trainingDataResult.pack()

        self.TreeviewResult(self.rightWindow)

        self.label_CurrentSettingTitle = LabelFrame(self.rightWindow, text="Current Setting")
        self.label_CurrentSettingTitle.pack()

        self.label_CurrentSetting = Label(self.label_CurrentSettingTitle, text=self.learningNetwork.DisplayNeuralNetworkInfo())
        self.label_CurrentSetting.pack()


    #do the performance test
    def TestNeuralNetwork(self):
        self.learningNetwork.TrainDataValidation()
        self.learningNetwork.CrossedValidation()
        self.learningNetwork.LearningTest()

        self.window.update_idletasks()
        self.listResults.append(["-", self.learningNetwork.trainResult, self.learningNetwork.vcResult, self.learningNetwork.testResult])

        self.tree.delete(*self.tree.get_children())
        self.LoadData(self.listResults)
        self.window.update_idletasks()


    #Train our neural network and test performance for each data set : training, vc and test
    def TrainAndTestNeuralNetwork(self):
        self.listResults=[]
        self.window.update_idletasks()
        self.tree.delete(*self.tree.get_children())

        nbCycle = self.nbCycle.get()

        for cycle in range(0, nbCycle):

            self.learningNetwork.TrainLVQNetwork()

            self.learningNetwork.TrainDataValidation()
            self.learningNetwork.CrossedValidation()
            self.learningNetwork.LearningTest()

            self.window.update_idletasks()
            self.listResults.append([cycle+1, self.learningNetwork.trainResult, self.learningNetwork.vcResult, self.learningNetwork.testResult])

            if(self.learningNetwork.LVQNetwork.learningRate > self.learningNetwork.learningRateThreshould):
                self.learningNetwork.LVQNetwork.CalculateNewLearningRate()

            if(self.learningNetwork.testResult > self.learningNetwork.percentageResultToEndLearning):
                break

            self.learningNetwork.LVQNetwork.learningRate = self.learningNetwork.learningRate

            self.tree.delete(*self.tree.get_children())
            self.LoadData(self.listResults)
            self.window.update_idletasks()


        self.tree.delete(*self.tree.get_children())
        self.LoadData(self.listResults)
        self.window.update_idletasks()



    # Update MEthod
    def UpdateSetting(self):

        messageError= self.validateCorrectValue()
        if( messageError==""):

            # Validate that data are good

            self.networkInfoFile = "new"
            self.UpdateNeuralNetworkBuilder()
            self.label_CurrentSetting.config(text=self.learningNetwork.DisplayNeuralNetworkInfo())


            self.label_networkInfoFile.config(text=const_networkInfoFile + self.networkInfoFile)
        else:
            showinfo("Error Update Setting",  messageError)

    def validateCorrectValue(self):

        CorrectValue = True
        # Parameter for the reading of File DataFile

        messageText=""


        if (not (self.learningRate.get()  > 0)):
            CorrectValue = False
            messageText = messageText +" Learning Rate must be higher than 0"

        if (not (self.nbNeuronsByClass.get()  > 0)):
            CorrectValue = False
            messageText = messageText +" Number of Neurons By Class must be higher than 0"

        if(self.learningRateDrop.get()  < 0):
            CorrectValue = False
            messageText = messageText +"\n" + "learningRateDrop must be minimum 0"

        if(self.learningRateThreshould.get()  <= 0):
            CorrectValue = False
            messageText = messageText +"\n" + "learning Rate Threshould must be higher than 0"

        if(self.nbCycle.get()   < 1):
            CorrectValue = False
            messageText = messageText + "\n" + "number of cycle must be minimum 1"

        if (self.percentageResultToEndLearning.get()  <= 0) or (self.percentageResultToEndLearning.get()  > 100):
            CorrectValue = False
            messageText = messageText + "\n" + "number of cycle must be between 0 and 100"


        return messageText

    # Function to update current Setting Display with the setting Data
    def UpdateGUIDefaultSetting(self):
        # Parameter for the reading of File DataFile
        self.nbLineInDataFiles.set(self.learningNetwork.nbLineInDataFiles )
        self.nbParametersToGetOnDataLines.set(self.learningNetwork.nbParametersToGetOnDataLines)

        # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
        #self.neuralNetworkNbOutput.set(self.learningNetwork.nbOutput) we don't set up output it will be only 10 class available

        #self.neuronActivationFunctionSTR.set(self.learningNetwork.GetNeuronActivationStrFromInt(self.learningNetwork.neuronActivationFunction ))
        # We don't need Activation Function

        self.nbNeuronsByClass.set(self.learningNetwork.nbNeuronsByClass)

        self.learningRate.set(self.learningNetwork.learningRate ) # taux d'apprentissage
        self.learningRateDrop.set(self.learningNetwork.learningRateDrop)

        self.learningRateThreshould.set(self.learningNetwork.learningRateThreshould)

        #self.learningRateDrop.set(self.learningNetwork.learningRateDrop)  # remove learningRateDrop

        # Parameter for Training and Validation Test
        self.nbCycle.set(self.learningNetwork.nbCycle)  # we update our weight value
        self.percentageResultToEndLearning.set(self.learningNetwork.percentageResultToEndLearning )  # in percentage, to configure

    # Function to update current Setting Display with the setting Data


    def UpdateNeuralNetworkBuilder(self):
        # Parameter for the reading of File DataFile
        self.learningNetwork.nbLineInDataFiles = self.nbLineInDataFiles.get()
        self.learningNetwork.nbParametersToGetOnDataLines = self.nbParametersToGetOnDataLines.get()

        # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
        #self.learningNetwork.nbOutput = self.neuralNetworkNbOutput.get()

        self.learningNetwork.UpdateInput()
        self.learningNetwork.InitializeDataFileIO()

        # Parameter For Configuring the NEural Network

        #self.learningNetwork.SetNeuronActivationFromStr(self.neuronActivationFunctionSTR.get())
        self.learningNetwork.nbNeuronsByClass = self.nbNeuronsByClass.get()

        self.learningNetwork.learningRate = self.learningRate.get() # taux d'apprentissage

        self.learningNetwork.learningRateDrop = self.learningRateDrop.get()  # learningRateDrop

        self.learningNetwork.Update_LVQNetwork()

        # Parameter for Training and Validation Test
        self.learningNetwork.nbCycle = self.nbCycle.get()  # we update our weight value
        self.learningNetwork.percentageResultToEndLearning = self.percentageResultToEndLearning.get()  # in percentage, to configure



    # Method To Put the default setting of the NEural Network
    def NewNeuralNetwork(self):
        # Ask the user if he wants to save the current Neural Network

        self.learningNetwork = LVQNetworkBuilder()
        self.networkInfoFile = "new"
        self.label_CurrentSetting.config(text=self.learningNetwork.DisplayNeuralNetworkInfo())
        self.label_networkInfoFile.config(text=const_networkInfoFile + self.networkInfoFile)
        self.listResults=[]
        self.LoadData("")

        self.window.update_idletasks()




    def LoadSavedNeuralNetowrk(self):
        self.networkInfoFile=self.BrowseFile()
        if(self.networkInfoFile != None):
            self.learningNetwork.LoadSavedNetworkInfo(self.networkInfoFile)
            self.label_networkInfoFile.config(text=self.networkInfoFile)
            base = os.path.basename(self.networkInfoFile)
            self.label_networkInfoFile.config(text=const_networkInfoFile + self.networkInfoFile)
            self.label_CurrentSetting.config(text=self.learningNetwork.DisplayNeuralNetworkInfo())
            self.UpdateGUIDefaultSetting()

            self.listResults = []
            self.tree.delete(*self.tree.get_children())
            self.window.update_idletasks()
            self.LoadData(self.listResults)

    # Intialization method

    def InitFrameButtonMenu(self,container):
        self.frameButtonMenu = Frame(container,borderwidth =2,width=100,height=100,relief = GROOVE)
        self.frameButtonMenu.pack(side =TOP, fill=Y)

        self.button_NewNeuralNetwork = Button(self.frameButtonMenu, text="New Neural Network", command=self.NewNeuralNetwork)
        self.button_NewNeuralNetwork.pack(side=LEFT)

        self.button_LoadNeuralNetwork = Button(self.frameButtonMenu, text="Load Neural Nework", command=self.LoadSavedNeuralNetowrk)
        self.button_LoadNeuralNetwork.pack(side=LEFT)
        self.button_SaveNeuralNetwork = Button(self.frameButtonMenu, text="Save Neural Network", command=self.SavenetworkInfoFile)
        self.button_SaveNeuralNetwork.pack(side=LEFT)

        self.button_TrainNeuralNetwork = Button(self.frameButtonMenu, text="Train Neural Network", command=self.TrainAndTestNeuralNetwork)
        self.button_TrainNeuralNetwork.pack(side=LEFT)

        self.button_TestNeuralNetwork = Button(self.frameButtonMenu, text="Test Neural Network",command=self.TestNeuralNetwork)
        self.button_TestNeuralNetwork.pack(side=LEFT)

        bouton_quitter = Button(self.frameButtonMenu,text="Quitter", command=self.window.quit)
        bouton_quitter.pack(side=LEFT)

    def InitLabelFrameSettingDataFiles(self,container):
        self.LabelFrameSettingDataFiles=LabelFrame(container,text="Setting Data Files",padx=20,pady=20,borderwidth =2)
        self.LabelFrameSettingDataFiles.pack(side=TOP,anchor="w")


        Frame1 = Frame(self.LabelFrameSettingDataFiles,width=10,height=100)
        Frame1.pack(side=TOP)

        self.label_nbLineInDataFiles = Label(Frame1, text="Number of line on data lines =") # (3 choice) (30,50,60)
        self.label_nbLineInDataFiles.pack(side = LEFT)

        #Variable
        self.nbLineInDataFiles = IntVar(Frame1)
        self.nbLineInDataFiles.set(30)  # initial value

        self.menu_nbLineInDataFiles = OptionMenu(Frame1, self.nbLineInDataFiles, 30, 50,60)
        self.menu_nbLineInDataFiles.pack(side =LEFT)

        Frame2 = Frame(self.LabelFrameSettingDataFiles, width=10, height=100)
        Frame2.pack(side=TOP)


        self.label_nbParametersToGetOnDataLines = Label(Frame2, text="Number Parameters  on lines to get =") # (2 choice) (12 or 26)
        self.label_nbParametersToGetOnDataLines.pack(side=LEFT,anchor ="s")

        # Variable
        self.nbParametersToGetOnDataLines = IntVar()
        self.nbParametersToGetOnDataLines.set(26)
        self.menu_nbParametersToGetOnDataLines = OptionMenu(Frame2, self.nbParametersToGetOnDataLines , 12, 26)
        self.menu_nbParametersToGetOnDataLines.pack(side=LEFT,anchor ="s")

    def InitFrameLearningDataProcess(self,container):
        self.LabelFrameLearningDataProcess=LabelFrame(container,text="Setting Data Files",padx=20,pady=20,borderwidth =2)
        self.LabelFrameLearningDataProcess.pack(side=TOP,anchor="w")

        Frame1 = Frame(self.LabelFrameLearningDataProcess, width=10, height=100)
        Frame1.pack(side=TOP)

        # Parameter for Training and Validation Test
        self.label_nbCycle = Label(Frame1,
                                   text="Number of Learning Cycle")  # we update our weight value(need to be a value of minimum 1)
        self.label_nbCycle.pack(side=LEFT)

        # Variable
        self.nbCycle = IntVar()
        self.nbCycle.set(3)
        self.entry_nbCycle = Entry(Frame1, textvariable=self.nbCycle, width=4)
        self.entry_nbCycle.pack(side=LEFT)


        Frame2 = Frame(self.LabelFrameLearningDataProcess, width=10, height=100)
        Frame2.pack(side=TOP)

        self.label_learningRateThreshould  = Label(Frame2,
                                                         text="Learning Rate Threshould  ")  # in percentage, to configure (valuminim minimum 1%)
        self.label_learningRateThreshould .pack(side=LEFT)

        # Variable
        self.learningRateThreshould = DoubleVar()
        self.learningRateThreshould .set(75)
        self.entry_learningRateThreshould = Entry(Frame2, textvariable=self.learningRateThreshould ,
                                                         width=4)
        self.entry_learningRateThreshould .pack(side=LEFT)



        Frame3 = Frame(self.LabelFrameLearningDataProcess, width=10, height=100)
        Frame3.pack(side=TOP)

        self.label_percentageResultToEndLearning = Label(Frame3,
                                                         text="Percentage Result to end Training ")  # in percentage, to configure (valuminim minimum 1%)
        self.label_percentageResultToEndLearning.pack(side=LEFT)

        # Variable
        self.percentageResultToEndLearning = DoubleVar()
        self.percentageResultToEndLearning.set(75)
        self.entry_percentageResultToEndLearning = Entry(Frame3, textvariable=self.percentageResultToEndLearning,
                                                         width=4)
        self.entry_percentageResultToEndLearning.pack(side=LEFT)


    def InitFrameNeuralNetwork(self,container):
        self.frameNeuralNetwork = LabelFrame(container,text="Setting Data Files",borderwidth =2,width=100,height=100)
        self.frameNeuralNetwork.pack(side =TOP, fill=Y,anchor="w")

        #Frame1 = Frame(self.frameNeuralNetwork, width=400, height=100)
       # Frame1.pack(side=TOP,fill=Y)

        #self.label_neuronActivationFunction = Label(Frame1,text="Activation Function ")  # (2 choice) (sigmoid or tanh)
        #self.label_neuronActivationFunction.pack(side=LEFT)

        #self.neuronActivationFunctionSTR = StringVar()
        #self.neuronActivationFunctionSTR.set("Sigmoid")
        #self.menu_neuronActivationFunction = OptionMenu(Frame1, self.neuronActivationFunctionSTR, cf.constant_Sigmoid, cf.constant_Tanh)
        #self.menu_neuronActivationFunction.pack(side=LEFT)

        Frame2 = Frame(self.frameNeuralNetwork, width=400, height=100)
        Frame2.pack(side=TOP,fill=Y)

        # Parameter to choose which Output_code we should use when we reading our DataFile ( output with 10bits or 4 bits)
        self.label_NetworkNbOutput = Label(Frame2, text="Number of Class =")  # (2 choice) (4 or 10)
        self.label_NetworkNbOutput.pack(side=LEFT)

        self.label_NbOutputNumber = Label(Frame2, text=str(self.learningNetwork.nbClass) )  # (2 choice) (4 or 10)
        self.label_NbOutputNumber.pack(side=LEFT)

        #self.neuralNetworkNbOutput = IntVar()
        #self.neuralNetworkNbOutput.set(10)
        #self.menu_neuralNetworkNbOutput = OptionMenu(Frame2, self.neuralNetworkNbOutput, 10, 4)
        #self.menu_neuralNetworkNbOutput.pack(side=LEFT)

        # Parameter For Configuring the NEural Network

        Frame3 = Frame(self.frameNeuralNetwork, width=400, height=100)
        Frame3.pack(side=TOP,fill=Y)

        self.label_nbNeuronsByClass = Label(Frame3,
                                                text="Number of Neuron By Class =")  # [40, self.NbOutput]  # Modify for a table with Independant Nb Neurons for each Hidden Layer
        self.label_nbNeuronsByClass.pack(side=LEFT)

        self.nbNeuronsByClass = IntVar()
        self.nbNeuronsByClass.set(40)
        self.entry_nbNeuronsByClass = Entry(Frame3, textvariable=self.nbNeuronsByClass, width=10)
        self.entry_nbNeuronsByClass.pack(side=LEFT)

        Frame4 = Frame(self.frameNeuralNetwork, width=400, height=100)
        Frame4.pack(side=TOP,fill=Y)

        self.label_learningRate = Label(Frame4,
                                        text="Learning Rate ")  # taux d'apprentissage (need to be a value higher than 0)
        self.label_learningRate.pack(side=LEFT)

        self.learningRate = DoubleVar()
        self.learningRate.set(0.10)
        self.entry_learningRate = Entry(Frame4, textvariable=self.learningRate, width=4)
        self.entry_learningRate.pack(side=LEFT)


        self.label_learningRateDrop = Label(Frame4,text="Drop rate ")  # learningRateDrop optionnel ( need to be a value of minimum 0)
        self.label_learningRateDrop.pack(side=LEFT)

        self.learningRateDrop = DoubleVar()
        self.learningRateDrop.set(0.10)
        self.entry_learningRateDrop = Entry(Frame4, textvariable=self.learningRateDrop, width=4)
        self.entry_learningRateDrop.pack(side=LEFT)


    def LoadData(self,listData):
        self.data = listData

        # configure column headings
        for c in self.dataCols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=75, anchor=CENTER)

        # add data to the tree
        for item in self.data:
            self.tree.insert('', 'end', values=item)

            # and adjust column widths if necessary
            for idx, val in enumerate(item):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width=iwidth)


    def TreeviewResult(self,container):

        f= ttk.Frame(container,width=60, height=100)
        f.pack(side = TOP)

        self.dataCols = ("# cycle","Train", 'C-Validation', 'Test')
        self.tree = ttk.Treeview(columns=self.dataCols,
                                 show = 'headings')


        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)

        self.tree['yscroll'] = ysb.set


        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
       # xsb.grid(in_=f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def BrowseFile(self):
        name = askopenfilename(#initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                               filetypes=(("Text File", "*.txt"),),
                               title="Choose a file."
                               )
        print(name)
        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            with open(name, 'r') as UseFile:
                return name
        except:
            print("No file exists")


    def SavenetworkInfoFile(self):
        self.networkInfoFile = asksaveasfilename(#initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                               filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        if(self.networkInfoFile!=None):

            self.networkInfoFile = self.networkInfoFile+ cf.const_FileExtension
            print(self.networkInfoFile)
            self.learningNetwork.SaveCurrentNetwork(self.networkInfoFile)
            base = os.path.basename(self.networkInfoFile)

            self.label_networkInfoFile.config(text=const_networkInfoFile+self.networkInfoFile)
            # Using try in case user types in unknown file or closes without choosing a file.
