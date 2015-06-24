#-*- coding: utf-8 -*-
from Sprites import *
from JSONinfo import *
import os.path

class MoreBlocks():
	"""
	class MoreBlocks
	a class that is used to compute the structure of 
        user defined blocks
	"""
	def __init__(self,spriteList):
		self.sprites = spriteList

	def writeMoreBlocksReportToFile(self,filename):
		"""
		writeMoreBlocksReportToFile(self,filename)
		writes the structure of the user defined blcoks in a file
		with extension .mbs
		"""
                reportStr = ""                 
		for aSprite in self.sprites:
                    reportStr += aSprite.name
                    reportStr += ("\n"+"="*len(aSprite.name)+"\n")
                    for aMoreBlocksDef in aSprite.moreBlocks:
                        reportStr += aMoreBlocksDef
                        reportStr += ("\n"+"-"*len(aMoreBlocksDef)+"\n")
		with open(filename + ".mbs","w") as f:
                    f.write(reportStr)

	def parseMBs(self):
		"""
		parseMBs(self)
		computes the more blocks structure
		"""
		for sprite in self.sprites:
                    print sprite.name
		    for script in sprite.scripts:
			for (i,expr) in enumerate(script):
			    #script is flattened from the function jsontoSprites
			    if (expr == "procDef"):
                                sprite.moreBlocks.append(script[i+1])

