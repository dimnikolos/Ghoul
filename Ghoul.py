#-*- coding: utf-8 -*-
import sys
from os.path import basename

from JSONinfo import *
from StatsGen import *
from CompCUs import *
from CUGraph import *
from ScratchReader import *

def getBasename(filename,projectInfo):
    """getBasename(filename,projectInfo)
       if there is a projectID then the basename is the projectID
       otherwise the original filename is used
    """
    if (projectInfo.getProjectID() is not None):
        return projectInfo.getProjectID()
    else:
        return basename(filename)

def main():
    """main
       read file and write three reports and the svg files
    """
    filename = sys.argv[1]
    aScratchReader = ScratchReader(filename)
    projectJSON = aScratchReader.parseJSON()
    if (not projectJSON):
        print("Something went terribly wrong!")
    else:
        projectInfo  = JSONinfo(projectJSON)
        projectBasename = getBasename(filename,projectInfo)

        (floatingScripts,sprites) = jsontoSprites(projectJSON)
        sg = StatsGen(projectInfo,sprites,floatingScripts)
        #CSV report is a CSV with the number of commands used
        #in the projects
        sg.writeStatstoCSV(projectBasename)
        cu = CompCUs(projectInfo,sprites)
        #CUR report is a statistics report about 
        #communication units
        cu.writeCUReporttoFile(projectBasename)
        cul = cu.parseCUs()
        #CUS report is a detailed report of all communication
        #units in the project
        cul.writeCUStoFile(projectBasename)
        #there are four graphs for the communication units
        #1.variables
        #2.messages
        #3.lists
        #4.all communication units
        cug = CUGraph(cul,sprites)
        cug.writeGraph(projectBasename+"_v_","variable")
        cug.writeGraph(projectBasename+"_m_","message")
        cug.writeGraph(projectBasename+"_l_","list")
        cug.writeGraph(projectBasename+"_a_")
   

main()