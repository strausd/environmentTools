# Duplicate objects along a curve

import maya.cmds as mc
import random


# If the window already exists, delete it
if mc.window("DAC", exists=True):
    mc.deleteUI("DAC", window=True)


# Create the window 
mc.window("DAC", title = "Duplicate Along Curve", wh=[374,335], s=False)
mc.columnLayout("ColumnIntro", adj=True, parent="DAC")
mc.separator(h=10)

# Basic intro text
mc.text("Duplicate objects along path.")
mc.text("Select the object(s) and the curve in any order, then go for it.")
mc.separator(h=10)

# Instance or duplicate button
mc.radioButtonGrp("type", label="Instance or Duplicate: ", labelArray2=["Instance", "Duplicate"], nrb=2, sl=2, cw3=[120, 70,70])
mc.separator(h=10);

# Make a row
mc.rowColumnLayout("row5", parent="DAC", numberOfRows=1)
# Rotation order
mc.text("    Select rotation order   ")
mc.optionMenu("rOrder", w=50)
mc.menuItem("xyz")
mc.menuItem("yzx")
mc.menuItem("zxy")
mc.menuItem("xzy")
mc.menuItem("yxz")
mc.menuItem("zyx")
mc.separator(h=10, parent="ColumnIntro");


# Make a row
mc.rowColumnLayout("row1", parent="DAC", numberOfRows=1)
# Randomize translation
mc.text("    Randomize translate  ")
mc.floatFieldGrp("randTran", numberOfFields=3)
mc.separator(h=10, parent="ColumnIntro");


# Make a row
mc.rowColumnLayout("row2", parent="DAC", numberOfRows=1)
# Randomize rotation
mc.text("    Randomize rotation    ")
mc.floatFieldGrp("randRot", numberOfFields=3)
mc.separator(h=10, parent="ColumnIntro");


# Make a row
mc.rowColumnLayout("row3", parent="DAC", numberOfRows=1)
# Randomize scale
mc.text("    Randomize scale %   ")
mc.floatFieldGrp("randScale", numberOfFields=3)
mc.separator(h=10, parent="ColumnIntro");


# Make a row
mc.rowColumnLayout("row4", parent="DAC", numberOfRows=1)
# Randomize scale uniformly
mc.text("    Randomize scale % uniform                 ")
mc.floatFieldGrp("randScaleU", numberOfFields=1)
mc.separator(h=10, parent="ColumnIntro");


# Make a row
mc.rowColumnLayout("row6", parent="DAC", numberOfRows=1)
# Duplicate amount
mc.text("inputDuplicates", label="    Input number of duplicates", parent="row6")
mc.separator(horizontal=False, style="single", width=60, vis=False)
mc.intField("duplicates", maxValue=2000, minValue=1, value=5, width=50, step=1, parent="row6")



mc.separator(h=10, parent="ColumnIntro");
# Make a row
mc.rowColumnLayout("row7", parent="DAC", numberOfRows=1)
# Checkbox for closing window
mc.text(label="    Close window on completion    ", parent="row7")
mc.checkBox("closeWindow", label="", value=0)


# Switch to column layout
mc.columnLayout("columnMain", adj=True, parent="DAC")
mc.separator(h=10)
# Final button
mc.button(label="Do it", c="buttonPress()")
mc.separator(h=10)
mc.showWindow("DAC")
 
 
def buttonPress():
    
    # Store the selection at the time of button press    
    sel = mc.ls(sl=True)
         
    # Defaults to using instances
    useInstance = True
     
    # If radio button is set to duplicate, turn useInstance to false
    if mc.radioButtonGrp("type", query=True, sl=True) == 2:
        useInstance = False
 
    
    ####################
    # Section for auto detecting objects and curves    
    meshes = []
    nurbCurve = []
    # Look at every object in selection
    for obj in sel:
        child = mc.listRelatives(obj, children=True, fullPath=True)
        
        # If it is a curve, add it to the curve list
        if mc.objectType(child[0]) == "nurbsCurve":
            nurbCurve.append(obj)
        # Otherwise add it to the meshes list
        else:
            meshes.append(obj)
    
    # Make sure only 1 curve is selected
    if len(nurbCurve) > 1 or len(nurbCurve) < 1:
        mc.error("YOU MUST SELECT EXACTLY 1 NURBS CURVE")
        
    # Make sure at least 1 mesh object is selected
    if meshes == []:
        mc.error("YOU MUST SELECT AT LEAST 1 MESH TO BE DUPLICATED")
    
    
    # Set the curve as path
    path = nurbCurve[0]
    ####################
    
     
    # Get the parent of the mesh to be duplicated, or the first mesh of all the meshes
    meshParent = mc.listRelatives(meshes[0], parent=True, fullPath=True)

    
    # Create a group for the duplicated objects
    if meshParent == None:
        objGroup = mc.group(name="GRP_duplicatedAlongCurve_01", empty=True)
    else:
        objGroup = mc.group(name="GRP_duplicatedAlongCurve_01", empty=True, parent=meshParent[0])
    
     
    # Store the input as number of duplicates. 
    numDuplicates = mc.intField("duplicates", query=True, value=True)
    # Get the value to increment along the motion path. For example, if there are 5 duplicates: 1/(5-1), or 1/4. 
    # This will be .25. Increments will be at 0, .25, .50, .75, and 1
    incValue = 1.0/(numDuplicates-1.0)
     
     
    # Create a locator
    loc = mc.spaceLocator()
     
    # Select the locator first and then the motionpath
    mc.select(loc, path)
     
 
    # Make the motion path animation
    motPath = mc.pathAnimation(follow=True, followAxis = "x", upAxis = "y", fractionMode=True)
     
    # Create strings for later use    
    motPathU = motPath + ".u"
    motPathUV = motPath + ".uValue"
     
    # Break connections on the uValue so the locator won't be animated
    mc.cutKey(motPathU, clear=True)
     
    # Empty list to store all duplicates as they are made
    allDups = []
    
    
    
    
    
    #################### 
    # For each duplicate...
    for i in range(0, numDuplicates, 1):
        
        multObjIndex = 0
        
        if len(meshes) > 1:
            multObjIndex = random.randint(0, len(meshes)-1)
        
        # Either create an instance or a duplicate based on radio button
        if useInstance == True:
            dup = mc.instance(meshes[multObjIndex])
        else:
            dup = mc.duplicate(meshes[multObjIndex])
         
        # Set the rotate order to the selection
        rotateOrder = mc.optionMenu("rOrder", query=True, select=True)
        mc.setAttr(dup[0] + ".rotateOrder", rotateOrder-1)
        

        mc.cycleCheck(dup[0], e=False)

        # Snap the duplicate to the locator using a parent constrain
        pCon = mc.parentConstraint(loc, dup[0], maintainOffset=False)
        # Delete the parent constrain
        mc.delete(pCon)
        # Add the duplicate to the list of all duplicates
        allDups.append(dup[0])
         
        # If the next motion path value is less than or equal to 1, set that value on the motion path U Value so the locator goes to the next step
        if incValue * (i+1) <= 1:
            mc.setAttr(motPathUV, incValue * (i+1))
    
    # Parent the duplicates to the group created earlier
    mc.parent(allDups, objGroup)
    
    
    ####################
         
    
    
    ####################    
    # Store randomized attributes
    randTX = mc.floatFieldGrp("randTran", query=True, v1=True)
    randTY = mc.floatFieldGrp("randTran", query=True, v2=True)
    randTZ = mc.floatFieldGrp("randTran", query=True, v3=True)
    
    randRX = mc.floatFieldGrp("randRot", query=True, v1=True)
    randRY = mc.floatFieldGrp("randRot", query=True, v2=True)
    randRZ = mc.floatFieldGrp("randRot", query=True, v3=True)
    
    randSX = mc.floatFieldGrp("randScale", query=True, v1=True)
    randSY = mc.floatFieldGrp("randScale", query=True, v2=True)
    randSZ = mc.floatFieldGrp("randScale", query=True, v3=True)
    
    randSU = mc.floatFieldGrp("randScaleU", query=True, v1=True)
    ####################
    
    
    ####################
    # Randomize translate
    if randTX != 0:
        for obj in allDups:
            objX = mc.getAttr(obj + ".translateX")
            mc.setAttr(obj + ".translateX", random.uniform(objX-randTX, objX+randTX))
            
    if randTY != 0:
        for obj in allDups:
            objY = mc.getAttr(obj + ".translateY")
            mc.setAttr(obj + ".translateY", random.uniform(objY-randTY, objY+randTY))    
            
    if randTZ != 0:
        for obj in allDups:
            objZ = mc.getAttr(obj + ".translateZ")
            mc.setAttr(obj + ".translateZ", random.uniform(objZ-randTZ, objZ+randTZ))
    ####################        
            
    
    ####################        
    # Randomize rotate
    if randRX != 0:
        for obj in allDups:
            objX = mc.getAttr(obj + ".rotateX")
            mc.setAttr(obj + ".rotateX", random.uniform(objX-randRX, objX+randRX))

    if randRY != 0:
        for obj in allDups:
            objY = mc.getAttr(obj + ".rotateY")
            mc.setAttr(obj + ".rotateY", random.uniform(objY-randRY, objY+randRY))

    if randRZ != 0:
        for obj in allDups:
            objZ = mc.getAttr(obj + ".rotateZ")
            mc.setAttr(obj + ".rotateZ", random.uniform(objZ-randRZ, objZ+randRZ))
    ####################


    ####################
    # Randomize scale
    if randSX != 0:
        for obj in allDups:
            objX = mc.getAttr(obj + ".scaleX")
            mc.setAttr(obj + ".scaleX", random.uniform(objX*((100-randSX)/100), objX*((100+randSX)/100)))
            
    if randSY != 0:
        for obj in allDups:
            objY = mc.getAttr(obj + ".scaleY")
            mc.setAttr(obj + ".scaleY", random.uniform(objY*((100-randSY)/100), objY*((100+randSY)/100)))
            
    if randSZ != 0:
        for obj in allDups:
            objZ = mc.getAttr(obj + ".scaleZ")
            mc.setAttr(obj + ".scaleZ", random.uniform(objZ*((100-randSZ)/100), objZ*((100+randSZ)/100)))
    ####################


    ####################
    # Randomize scale uniform
    if randSU != 0:
        for obj in allDups:
            objX = mc.getAttr(obj + ".scaleX")
            objY = mc.getAttr(obj + ".scaleY")
            objZ = mc.getAttr(obj + ".scaleZ")
            U_Scale = random.uniform(-randSU, randSU)
            mc.setAttr(obj + ".scaleX", objX * ((100 + U_Scale)/100))
            mc.setAttr(obj + ".scaleY", objY * ((100 + U_Scale)/100))
            mc.setAttr(obj + ".scaleZ", objZ * ((100 + U_Scale)/100))
    ####################


    
    # Delete the locator
    mc.delete(loc)
    # Close the UI window
    if mc.checkBox("closeWindow", query=True, value=True) == 1:
        mc.deleteUI("DAC", window=True)
    # Select all the duplicates
    mc.select(allDups)