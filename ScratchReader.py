#-*- coding: utf-8 -*-
import zipfile
import json

class ScratchReader():
    def __init__(self,filename):
        self.filename = filename
        self.projectJSON = [];
        self.projectString = "";
  
    def readfile(self):
        try:
            zfile = zipfile.ZipFile(self.filename)
        except:
            print("Problem with %s") % (self.filename)
            return(None)
            
        try:
            zfile.extract("project.json")
        except:
           print("Error extracting project.json. Not sb2 file? Not write permissions?")
           return(None)
        try:
            f = open('project.json')
            return(f.read().decode('utf-8'))
        except:
            print("Problem reading project.json. Permission problems?")
            return(None)
                

    
    def parseJSON(self):
        self.projectString = self.readfile()
        try:
            return(json.loads(self.projectString.replace('\t', '').replace('\n','').replace('\r','')))
        except:
            print("Not A JSON file?")
            return(None)
      
        
    

