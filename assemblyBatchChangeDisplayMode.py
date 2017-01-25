# Author: Danny Straus

####################################
# CDM - Change Display modes for selected objects
# 
# This tool will automatically figure out
# if you are in an assembly file or a shot
# file. Based on that, some controls might 
# be disabled. If in the shot file, it will
# only change display mode on the parent, 
# thus utilizing the "extra attributes"
# for that node.
#
####################################

import maya.cmds as mc


##########################
# Determine context
fullPath = mc.file(expandName=True, query=True)

# shot     - /work/20554_SCOOBYDAX/sequences/env_test/0001/env/set/env_test_0001_set_003.ma
# assembly - /work/20554_SCOOBYDAX/assemblies/landscape/testGrounds/asm/dannyTest/testGrounds_dannyTest_001.ma

context = fullPath.split("/")[3]
isAssembly = True

if context == "sequences":
    isAssembly = False

##########################

if mc.window("assemblyAssetDisplay", exists=True):
    mc.deleteUI("assemblyAssetDisplay", window=True)
    
mc.window("assemblyAssetDisplay", title="Assembly Asset Display", wh=[260,244], s=False)
mc.columnLayout("columnMain", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)
mc.text("Batch adjust display modes", font="boldLabelFont")
mc.text("for selected assets", font="boldLabelFont")
mc.separator(h=10)

# Display Mode
mc.rowColumnLayout("row1", parent="assemblyAssetDisplay", numberOfColumns=2, columnWidth=[(1, 120), (2, 120)])
mc.text("Display Mode", height=20)
mc.optionMenu("displayMode", w=100)
mc.menuItem("Geometry")
mc.menuItem("Proxy")
mc.menuItem("ShapeBounds")
mc.menuItem("Bounds")
mc.menuItem("Hidden")
mc.optionMenu("displayMode", edit=True, select=2)


mc.columnLayout("sepCol1", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)


# Level Of Detail
mc.rowColumnLayout("row2", parent="assemblyAssetDisplay", numberOfColumns=2, columnWidth=[(1, 120), (2, 120)])
mc.text("Level Of Detail", height=20, enable=isAssembly)
mc.optionMenu("levelOfDetail", w=100, enable=isAssembly)
mc.menuItem("None")
mc.menuItem("High")
mc.menuItem("Low")
mc.optionMenu("levelOfDetail", edit=True, select=2)


mc.columnLayout("sepCol2", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)


# Colors Mode
mc.rowColumnLayout("row3", parent="assemblyAssetDisplay", numberOfColumns=2, columnWidth=[(1, 120), (2, 120)])
mc.text("Colors Mode", height=20, enable=isAssembly)
mc.optionMenu("colorsMode", w=100, enable=isAssembly)
mc.menuItem("None")
mc.menuItem("FromFile")
mc.optionMenu("colorsMode", edit=True, select=2)


mc.columnLayout("sepCol3", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)

# Force wireframe
mc.rowColumnLayout("row4", parent="assemblyAssetDisplay", numberOfColumns=2, columnWidth=[(1, 180), (2, 60)])
mc.text("Force Wireframe", height=20, enable=isAssembly)
mc.checkBox("forceWireframe", label="", value=0, width=240, enable=isAssembly)

mc.columnLayout("sepCol4", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)


mc.rowColumnLayout("row5", parent="assemblyAssetDisplay", numberOfColumns=2, columnWidth=[(1, 180), (2, 60)])
mc.text("Close window on completion", height=20)
mc.checkBox("delWindow", label="", value=0, width=240)



mc.columnLayout("sepCol5", adj=True, parent="assemblyAssetDisplay")
mc.separator(h=10)


mc.button(label="Submit", c="buttonPress()")

mc.showWindow("assemblyAssetDisplay")


def buttonPress():
    delWindow = mc.checkBox("delWindow", query=True, value=True)
    
    dm_Int = mc.optionMenu("displayMode", query=True, select=True) - 1
    LOD_Int = mc.optionMenu("levelOfDetail", query=True, select=True) - 1
    cm_Int = mc.optionMenu("colorsMode", query=True, select=True) - 1
    wf_Int = mc.checkBox("forceWireframe", query=True, value=True)
    
    dm_Str = ".displayMode"
    LOD_Str = ".levelOfDetail"
    cm_Str = ".colorsMode"
    wf_Str = ".forceWireframe"
    
    sel = mc.ls(sl=True)
    linkAssets = mc.listRelatives(sel, allDescendents=True, type="RAsset")
    
    


    if linkAssets:
        for obj in sel:
            if mc.objectType(obj) == "RAsset":
                linkAssets.append(obj)
        linkAssetShapes = mc.listRelatives(linkAssets, allDescendents=True, shapes=True)
    else:
        linkAssetShapes = mc.listRelatives(sel, allDescendents=True, shapes=True)
        linkAssets = sel

    if isAssembly:
        for obj in linkAssetShapes:
            mc.setAttr(obj + dm_Str, dm_Int)
            mc.setAttr(obj + LOD_Str, LOD_Int)
            mc.setAttr(obj + cm_Str, cm_Int)
            mc.setAttr(obj + wf_Str, wf_Int)
    else:
        for obj in linkAssets:
            mc.setAttr(obj + dm_Str, dm_Int)
        
        
    if delWindow:
        mc.deleteUI("assemblyAssetDisplay", window=True)
