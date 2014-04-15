#-*- coding: utf-8 -*-
import igraph
import igraph.vendor.texttable #needed for py2exe
import cairo
import pygr2gl
from Sprites import *


class CUGraph():
	"""
	class CUGraph is a class
	that is used to create
	graph of communication units
	"""
	def __init__(self,CUCollection,spriteList):
		self.CUCollection = CUCollection
		#nameList is a list of the names of the sprites
		#it is used to get a consistent index of a sprite
		self.nameList = [sp.name for sp in spriteList]

	def graphEdges(self,cuType):
		"""
		graphEdges(self,cuType)
		returns list of tuples
		to be used for graphs
		"""
		
		edges = []
		for cu in self.CUCollection.getCollection():
			#cuType filters the communication units
			#according to the type
			if (cu.getCUType() == cuType):
				for aReader in cu.getReaders():
					for aWriter in cu.getWriters():
						#do not remove duplicates
						#if ((self.nameList.index(aReader),self.nameList.index(aWriter)) not in edges):
							edges.append((self.nameList.index(aWriter),self.nameList.index(aReader)))
		return edges
	
	def writeGraph(self,filename,cuType="all"):
		if (cuType == "all"):
			#allEdges is consists of edges from variables/messages/lists
			
			allEdges = self.graphEdges("variable")
			#REMOVE DUPLICATES
			#allEdges.extend([edge for edge in self.graphEdges("list") if edge not in allEdges])
			#allEdges.extend([edge for edge in self.graphEdges("message") if edge not in allEdges])
			allEdges.extend([edge for edge in self.graphEdges("list")])
			allEdges.extend([edge for edge in self.graphEdges("message")])
		else:
			allEdges = self.graphEdges(cuType)
		
		if (len(allEdges)>0):
			bbox = igraph.BoundingBox(800,600)
			surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,800,600)
			g = igraph.Graph(allEdges,directed = True)
			#multiple lines are depicted
			igraph.autocurve(g)

			#all sprites are depicted in the graph 
			#connected or not
			#labels converted to greeklish
			g.vs["label"] = [pygr2gl.convert(label) for label in self.nameList]
			g.es["label"] = ["hi" for x in g.es]

			#layout = g.layout("kk")
			#g.write_svg(filename + ".svg")#,layout = layout)
			plot = igraph.plot(g,surface,bounding_box = bbox)
			plot.background = None
			plot.redraw()
			surface.write_to_png(filename + ".png")
		else:
			print("No edges for type: %s") % (cuType)
		
