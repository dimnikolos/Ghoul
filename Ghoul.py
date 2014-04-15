#-*- coding: utf-8 -*-
import sys
import Tkinter
import tkFileDialog
import tkMessageBox
from os.path import basename,split

from JSONinfo import *
from StatsGen import *
from CompCUs import *
from CUGraph import *
from ScratchReader import *

class Main:

    def __init__(self):
        self.labelText = Tkinter.StringVar()
    def setFilename(self):
        projectFile = tkFileDialog.askopenfilename(title="Choose a file...", filetypes=[('Scratch 2.0 projects','*.sb2'),('All files',"*.*")])
        print projectFile
        self.filename = split(projectFile)[1]
        self.labelText.set(self.filename)
        self.compute()

    def getBasename(self):
        """getBasename(self,projectInfo)
           if there is a projectID then the basename is the projectID
           otherwise the original filename is used
        """
        if (self.projectInfo.getProjectID() is not None):
            return self.projectInfo.getProjectID()
        else:
            return basename(self.filename)

    def compute(self):
        if (self.filename is not None):
            self.aScratchReader = ScratchReader(self.filename)
            self.projectJSON = self.aScratchReader.parseJSON()
            if (not self.projectJSON):
                print("Something went terribly wrong!")
            else:
                self.projectInfo  = JSONinfo(self.projectJSON)
                self.projectBasename = self.getBasename()

                (self.floatingScripts,self.sprites) = jsontoSprites(self.projectJSON)
                self.cu = CompCUs(self.projectInfo,self.sprites)
                self.cul = self.cu.parseCUs()
        else:
            tkMessageBox.showinfo("File first", "Choose project file first!")

    def writeStats(self):
        self.sg = StatsGen(self.projectInfo,self.sprites,self.floatingScripts)
        #CSV report is a CSV with the number of commands used
        #in the projects
        self.sg.writeStatstoCSV(self.projectBasename)
        tkMessageBox.showinfo("OK", "Generated csv file!")
    def writeCUR(self):
        #CUR report is a statistics report about 
        #communication units
        self.cu.writeCUReporttoFile(self.projectBasename)
        tkMessageBox.showinfo("OK", "Generated cur file!")
    def writeCUS(self):
        #CUS report is a detailed report of all communication
        #units in the project
        self.cul.writeCUStoFile(self.projectBasename)
        tkMessageBox.showinfo("OK", "Generated cus file!")
    def writeSVGs(self):
        #there are four graphs for the communication units
        #1.variables
        #2.messages
        #3.lists
        #4.all communication units
        cug = CUGraph(self.cul,self.sprites)
        cug.writeGraph(self.projectBasename+"_v_","variable")
        cug.writeGraph(self.projectBasename+"_m_","message")
        cug.writeGraph(self.projectBasename+"_l_","list")
        cug.writeGraph(self.projectBasename+"_a_")
        tkMessageBox.showinfo("OK", "Generated png files!")








    

def main():
    """main
       read file and write three reports and the svg files
    """
    
    top = Tkinter.Tk()
    mainInstance = Main()
    # Code to add widgets will go here...
    openFileButton   = Tkinter.Button(top,text="Browse (.sb2)", command = mainInstance.setFilename, width=16)
    nameLabel        = Tkinter.Label(top,textvariable=mainInstance.labelText,width=16)
    writeStatsButton = Tkinter.Button(top,text="Write Statistics", command = mainInstance.writeStats, width=16)
    writeCUSButton   = Tkinter.Button(top,text="Write CUS report", command = mainInstance.writeCUS, width=16)
    writeCURButton   = Tkinter.Button(top,text="Write CUR report", command = mainInstance.writeCUR, width=16)
    writeSVGButton   = Tkinter.Button(top,text="Generate graphs", command = mainInstance.writeSVGs, width=16)
    openFileButton.pack()
    nameLabel.pack()
    writeStatsButton.pack()
    writeCUSButton.pack()
    writeCURButton.pack()
    writeSVGButton.pack()
    top.mainloop()
    
main()