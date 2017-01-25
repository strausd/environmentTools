# Clean extract tool

import maya.cmds as mc

origSel = mc.ls(sl=True)

if mc.objectType(origSel[0]) == "transform":
    object = origSel
elif mc.objectType(origSel[0]) == "mesh":
    object = mc.listRelatives(origSel, parent=True)
    object = mc.listRelatives(object, parent=True)
else:
    mc.warning("No proper selection for extraction!")
    

if mc.listRelatives(object, parent=True) == None:
    worldParent = True
else:
    worldParent = False
    prnt = mc.listRelatives(object, parent=True)


fullNames = mc.listRelatives(origSel, fullPath=True)
extracted = mc.ExtractFace(fullNames)

extracted = mc.ls(sl=True)

extObjects = []

for obj in extracted:
    if mc.objectType(obj) == "transform":
        extObjects.append(obj)

if worldParent == True:
    mc.parent(extObjects, world=True)
else:
    mc.parent(extObjects, prnt)
mc.DeleteHistory(extObjects)
mel.eval("changeSelectMode -object;")
mc.select(extObjects[1])