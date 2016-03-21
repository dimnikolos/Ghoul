from os import listdir
from os.path import isfile
import zipfile
import json
from itertools import chain

SCRATCH_EXTENSION = ".sb2"
DELIMETER = ";"#for the CSV
TREE_PREFIX = "|-"#for printing the TREE

catNames = [#Command Categories Names
"operators",
"sensing",
"data",  
"looks",
"motion",
"events",
"control",
"pen",
"sound",
"MoreBlocks"]
catCommands = {}#all scratch commands
catCommands["operators"] = [
  "-",
  "*",
  "/",
  "&",
  "%",
  "+",
  "<",
  "=",
  ">",
  "|",
  "abs",
  "computeFunction:of:",
  "concatenate:with:",
  "letter:of:",
  "not",
  "randomFrom:to:",
  "rounded",
  "sqrt",
  "stringLength:"]
catCommands["sensing"] = [
  "answer",
  "color:sees:",
  "distanceTo:",
  "doAsk",
  "getAttribute:of:",
  "isLoud",
  "keyPressed:",
  "mousePressed",
  "mouseX",
  "mouseY",
  "senseVideoMotion",
  "sensor:",
  "sensorPressed:",
  "setVideoState",
  "setVideoTransparency",
  "soundLevel",
  "timeAndDate",
  "timer",
  "timerReset",
  "timestamp",
  "touching:",
  "touchingColor:",
  "yScroll",
  "xScroll"]
catCommands["data"] = [
  "append:toList:",
  "changeVar:by:",
  "CLR_COUNT",
  "contentsOfList:",
  "COUNT",
  "deleteLine:ofList:",
  "getLine:ofList:",
  "getUserId",
  "getUserName",
  "hideList:",
  "hideVariable:",
  "INCR_COUNT",
  "insert:at:ofList:",
  "lineCountOfList:",
  "list:contains:",
  "readVariable",
  "setLine:ofList:to:",
  "setVar:to:",
  "showList:",
  "showVariable:"]
catCommands["looks"] = [
  "backgroundIndex",
  "changeGraphicEffect:by:",
  "changeSizeBy:",
  "comeToFront",
  "costumeIndex",
  "filterReset",
  "goBackByLayers:",
  "hide",
  "hideAll",
  "lookLike:",
  "nextBackground",
  "nextCostume",
  "nextScene",
  "say:",
  "say:duration:elapsed:from:",
  "scale",
  "sceneName",
  "setGraphicEffect:to:",
  "setSizeTo:",
  "show",
  "showBackground:",
  "startScene",
  "startSceneAndWait",
  "think:",
  "think:duration:elapsed:from:"]
catCommands["motion"] = [
  "bounceOffEdge",
  "changeXposBy:",
  "changeYposBy:",
  "glideSecs:toX:y:elapsed:from:",
  "forward:",
  "gotoSpriteOrMouse:",
  "gotoX:y:",
  "heading",
  "heading:",
  "pointTowards:",
  "scrollAlign",
  "scrollRight",
  "scrollUp",
  "setRotationStyle",
  "turnLeft:",
  "turnRight:",
  "xpos",
  "xpos:",
  "ypos",
  "ypos:"]
catCommands["events"] = [
  "broadcast:",
  "doBroadcastAndWait",
  "whenClicked",
  "whenGreenFlag",
  "whenIReceive",
  "whenKeyPressed",
  "whenSceneStarts",
  "whenSensorGreaterThan"]
catCommands["control"] = [
  "createCloneOf",
  "deleteClone",
  "doForever",
  "doForeverIf",
  "doForLoop",
  "doIf",
  "doIfElse",
  "doRepeat",
  "doReturn",
  "doUntilRepeat",
  "doWaitUntil",
  "doWhile",
  "stopAll",
  "stopScripts",
  "wait:elapsed:from:",
  "warpSpeed",
  "whenCloned"]
catCommands["pen"] = [
  "changePenHueBy:",
  "changePenSizeBy:",
  "clearPenTrails",
  "penColor:",
  "penSize:",
  "putPenDown",
  "putPenUp",
  "setPenHueTo:",
  "setPenShadeTo:",
  "changePenShadeBy:"
  "stampCostume"]
catCommands["sound"] =  [
  "changeTempoBy:",
  "changeVolumeBy:",
  "doPlaySoundAndWait",
  "drum:duration:elapsed:from:",
  "instrument:",
  "midiInstrument:",
  "noteOn:duration:elapsed:from:",
  "playDrum",
  "playSound:",
  "rest:elapsed:from:",
  "setTempoTo:",
  "setVolumeTo:",
  "stopAllSounds",
  "tempo",
  "volume"]

catCommands["MoreBlocks"] = ["procDef", "call"]

countDict = {} #a global Dictionary

def CatofCommand(command):
  """
  Returns the category name of the command
  if this is not a command it returns None
  """
  for cat in catNames:
    if (command in catCommands[cat]):
      return(cat)
  return(None)

def CountCommand(command):
  """
  Count the command in countDict
  Returns True if command is in command
  list, and False if command is not a 
  valid Scratch Command
  """
  cat = CatofCommand(command)
  if (cat):
    if (cat in countDict.keys()):
      countDict[cat] += 1
      if (command in countDict.keys()):
        countDict[command] += 1
      else:
        countDict[command] = 1
    else:
      countDict[cat] = 1
      countDict[command] = 1
    return(True)
  else:
    return(False)

class Node(object):
  """
  Basic tree structure
  """
  def __init__(self, data):
    self.data = data
    self.children = []

  def addChild(self,child):
    self.children.append(child)

  def printNode(self,prefix):
    line = unicode(prefix) + unicode(self.data) + "\n"
    print(line)
    newPrefix = TREE_PREFIX + prefix
    for child in self.children:
      child.printNode(newPrefix)

  def hasChild(self):
    return(self.children != [])

  def countinTree(self):
    """
    Recursively counts every command in the tree structure
    """
    if (not CountCommand(self.data)):
      print("ALERT %s seems to be a command but is not on Scratch Commands list!") %(self.data)
    for child in self.children:
      if (child):
        child.countinTree()

def makeTree(aScript):
  """
  Parses the list of lists into a tree
  """
  if (type(aScript) is list):
    try:
      theTree = makeTree(aScript[0])
    except IndexError:
      theTree = None
    for aChild in aScript[1:]:
      if (type(aChild) is list):#all commands are represented as lists
        theTree.addChild(makeTree(aChild))
      #if aChild is not a list it means it is a parameter and it is not
      #added to the tree
    return theTree
  else:
    return(Node(aScript))


def file2Json(sb2File):
  """
  Opens sb2file unzips it and parses the json object in project.json
  """
  try:
    zfile = zipfile.ZipFile(sb2File)
  except:
    print("Problem with %s") % (sb2File)
    return(None)
          
  try:
    zfile.extract("project.json")
  except:
    print("Error extracting project.json. Not sb2 file? Not write permissions?")
    return(None)
  
  try:
    f = open('project.json')
    projectString = f.read().decode('utf-8')
  except:
    print("Problem reading project.json. Permission problems?")
    return(None)

  try:
    parsedJson = json.loads(projectString.replace('\t', '').replace('\n','').replace('\r',''))
    return(parsedJson)
  except:
    print("Not A JSON file?")
    return(None)

def countCommands(parsedJson):
  """
  Counts all commands in json
  """
  if ("children" in parsedJson.keys()):
    for sprite in parsedJson["children"]:
      if ("scripts" in sprite.keys()):#if there are scripts
        for aScript in sprite["scripts"]:
          currentScript = aScript[2]#first two elements
                                     #of aScript are for x and y
          scriptTree = makeTree(currentScript)
          #scriptTree.printNode(TREE_PREFIX)
          if (scriptTree):
            scriptTree.countinTree()

def main():
  """
  Count commands in the sb2 files it finds in the folder
  and writes the result as a csv in ScratchCount.csv
  """
  sb2List = []#the list of .sb2 filenames
  for aFile in listdir("."):
    if aFile.endswith(SCRATCH_EXTENSION):
      sb2List.append(aFile)
  #make caption of csv file
  line = "Scratch Project" + DELIMETER
  for cat in catNames:
    line += (cat + DELIMETER)
  for cat in catNames:
    for command in catCommands[cat]:
      line += (command + DELIMETER)
  line += "\n"
  with open("ScratchCount.csv","w") as csvfile:
    #write caption of csv file
    csvfile.write(line)
    for sb2File in sorted(sb2List):
      countDict.clear()#countDict is erased for every file
      projectJson = file2Json(sb2File)
      countCommands(projectJson)
      #make line of csv file
      line = sb2File + DELIMETER
      for cat in catNames:
        if cat in countDict.keys():
          line+= (str(countDict[cat]) + DELIMETER)
        else:
          line+=("0" + DELIMETER)
      for cat in catNames:
        for command in catCommands[cat]:
          if command in countDict.keys():
            line+=(str(countDict[command]) + DELIMETER)
          else:
            line+=("0" + DELIMETER)
      line += "\n"
      csvfile.write(line)

main()