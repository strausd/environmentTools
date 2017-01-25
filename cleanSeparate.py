# Clean separate tool

import maya.cmds as mc

origSel = mc.ls(sl=True)
if mc.listRelatives(origSel, parent=True) == None:
    worldParent = True
else:
    worldParent = False
    prnt = mc.listRelatives(origSel, parent=True)

fullNames = mc.listRelatives(origSel, fullPath=True)
separated = mc.polySeparate(fullNames)

sepObjects = []

for obj in separated:
    if mc.objectType(obj) == "transform":
        sepObjects.append(obj)


if worldParent == True:
    mc.parent(sepObjects, world=True)
else:
    mc.parent(sepObjects, prnt)
mc.DeleteHistory(sepObjects)
mc.select(clear=True)