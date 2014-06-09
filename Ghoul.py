#-*- coding: utf-8 -*-
import sys
import Tkinter
import tkFileDialog
import tkMessageBox
from os.path import basename,split,splitext
import unidecode

from JSONinfo import *
from StatsGen import *
from CompCUs import *
from CUGraph import *
from ScratchReader import *

class Main:

    def __init__(self):
        self.labelText = Tkinter.StringVar()
        self.parsedFile = False
    def getBasename(self):
        """getBasename(self)
           the original filename is used
        """
        return splitext(basename(self.filename))[0]
    def setFilename(self):
        self.filename = tkFileDialog.askopenfilename(title="Choose a file...", filetypes=[('Scratch 2.0 projects','*.sb2'),('All files',"*.*")])
        #self.filename = split(projectFile)[1]
        self.labelText.set(self.getBasename())
        self.compute()
        self.parsedFile = True



    def compute(self):
        self.projectBasename = self.getBasename();
        if (self.filename is not None):
            self.aScratchReader = ScratchReader(self.filename)
            self.projectJSON = self.aScratchReader.parseJSON()
            if (not self.projectJSON):
                tkMessageBox.showinfo("Project.json error!", "File project.json is corrupted. Select another .sb2 file!")
            else:
                self.projectInfo  = JSONinfo(self.projectJSON)
                if not os.path.exists('Reports'):
                    os.makedirs('Reports')
                self.projectBasename = os.path.join('Reports',self.getBasename());

                (self.floatingScripts,self.sprites) = jsontoSprites(self.projectJSON)
                self.cu = CompCUs(self.projectInfo,self.sprites)
                self.cul = self.cu.parseCUs()
        else:
            tkMessageBox.showinfo("File first", "Choose project file first!")

    def writeStats(self):
        if (self.parsedFile):
            self.sg = StatsGen(self.projectInfo,self.sprites,self.floatingScripts)
            #CSV report is a CSV with the number of commands used
            #in the projects
            self.sg.writeStatstoCSV(self.projectBasename)
            tkMessageBox.showinfo("OK", "Generated csv file!")
        else:
            tkMessageBox.showinfo("Select file first","Please select a Scratch project first!")
    def writeCUR(self):
        if (self.parsedFile):
            #CUR report is a statistics report about 
            #communication units
            self.cul.writeCUStoFile(self.projectBasename)
            self.cu.writeCUReporttoFile(self.projectBasename)
            tkMessageBox.showinfo("OK", "Generated cur file!")
        else:
            tkMessageBox.showinfo("Select file first","Please select a Scratch project first!")

    def writePNGs(self):
        if (self.parsedFile):
            #there are four graphs for the communication units
            #1.variables
            #2.messages
            #3.lists
            #4.all communication units
            cug = CUGraph(self.cul,self.sprites)
            cug.writeGraph(self.projectBasename+"_v_","variable",cuAsNode = True)
            cug.writeGraph(self.projectBasename+"_m_","message", cuAsNode = False)
            cug.writeGraph(self.projectBasename+"_l_","list", cuAsNode = True)
            cug.writeGraph(self.projectBasename+"_s_","scene", cuAsNode = True)
            cug.writeGraph(self.projectBasename+"_a_")
            tkMessageBox.showinfo("OK", "Generated png files!")
        else:
            tkMessageBox.showinfo("Select file first","Please select a Scratch project first!")

def main():
    """main
       read file and write three reports and the svg files
    """
    
    top = Tkinter.Tk()
    mainInstance = Main()
    # Code to add widgets will go here...
    openFileButton   = Tkinter.Button(top,text="Browse (.sb2)", command = mainInstance.setFilename, width=17)
    nameLabel        = Tkinter.Label(top,textvariable=mainInstance.labelText,width=17)
    writeStatsButton = Tkinter.Button(top,text="Write Statistics", command = mainInstance.writeStats, width=17)
    writeCURButton   = Tkinter.Button(top,text="Write CUR report", command = mainInstance.writeCUR, width=17)
    writePNGButton   = Tkinter.Button(top,text="Generate graphs", command = mainInstance.writePNGs, width=17)
    #writePNGButton2  = Tkinter.Button(top,text="Generate graphs 2", command = mainInstance.writePNGs2, width=17)
    openFileButton.pack()
    nameLabel.pack()
    writeStatsButton.pack()
    writeCURButton.pack()
    writePNGButton.pack()
    top.mainloop()
    
main()