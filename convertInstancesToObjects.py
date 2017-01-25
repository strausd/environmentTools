# Batch convert instances to objects

import maya.cmds as mc

#mc.SelectAllTransforms()
mc.SelectAll()
mc.select(hierarchy=True)

selOld = mc.ls(sl=True)

selection = []

for obj in selOld:
    if mc.objectType(obj, isType="transform") == True:
        selection.append(obj)

for obj in selection:
    if mc.objExists(obj) == True:
        mc.select(obj)
        mc.ConvertInstanceToObject()

mc.select(clear=True)
