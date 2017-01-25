# Clean combine tool

import maya.cmds as mc

origSel = mc.ls(sl=True)
fullNames = mc.listRelatives(origSel, fullPath=True)

combinedName = ""

for obj in origSel:
    combinedName += obj + "-"
    
combinedName = combinedName[:-1]

combined = mc.polyUnite(fullNames, name=combinedName)
mc.DeleteHistory(combined)