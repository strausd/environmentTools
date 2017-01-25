# Author: Danny Straus

### Tool for cleaning up speedTree assets

import maya.cmds as mc;


if mc.window("SpeedClean", exists=True):
    mc.deleteUI("SpeedClean", window=True)
    
mc.window("SpeedClean", title="SpeedTree Cleanup", resizeToFitChildren=True, s=False);
mc.columnLayout(adj=True);


mc.separator();
mc.checkBox("saveStart", label="Save current scene", value=0);

mc.separator();
mc.checkBox("group", label="Auto group", value=1);

mc.separator();
mc.checkBox("subD", label="Combine subD objects", value=1);

mc.separator();
mc.checkBox("rename", label="Auto rename", value=1);

mc.separator();
mc.checkBox("shaders", label="Apply standard shaders", value=1);

mc.separator();
mc.checkBox("dun", label="Delete Unused Nodes", value=1);

mc.separator();
mc.checkBox("merge", label="Merge vertices", value=1);

mc.separator();
mc.checkBox("lam", label="Delete lamina faces", value=1);

mc.separator();
mc.checkBox("nonMani", label="Cleanup nonmanifold geo", value=1);

mc.separator();
mc.checkBox("renderStats", label="Reset render stats", value=1);

mc.separator();
mc.checkBox("PRX", label="Create proxy from LO", value=0);

mc.separator();
mc.checkBox("uvs", label="Delete extra UV Sets", value=1);

mc.separator();
mc.checkBox("FT", label="Freeze Transforms", value=1);

mc.separator();
mc.checkBox("normals", label="Unlock normals", value=1);

mc.separator();
mc.checkBox("history", label="Delete history", value=0);

mc.separator();
mc.checkBox("WIP", label="Version Up WIP", value=1);

mc.separator();
mc.checkBox("closeWindow", label="Close window on completion", value=1);

mc.separator();
mc.button("Clean that crap up", command="cleanup()");
mc.separator();

mc.showWindow("SpeedClean");


def cleanup():
    if mc.checkBox("saveStart", query=True, value=True) == 1:
        saveScene()
    if mc.checkBox("group", query=True, value=True) == 1:
        autoGroup()
    if mc.checkBox("subD", query=True, value=True) == 1:
        subdivisionCombine()
    if mc.checkBox("rename", query=True, value=True) == 1:
        autoRename()
    if mc.checkBox("shaders", query=True, value=True) == 1:
        fastShaders()
    if mc.checkBox("dun", query=True, value=True) == 1:
        delUnusedNodes()
    if mc.checkBox("merge", query=True, value=True) == 1:
        mergeVerts()
    if mc.checkBox("lam", query=True, value=True) == 1:
        delLaminaFaces()
    if mc.checkBox("nonMani", query=True, value=True) == 1:
        cleanNonmanifoldGeo()
    if mc.checkBox("renderStats", query=True, value=True) == 1:
        resetRenderStats()
    if mc.checkBox("PRX", query=True, value=True) == 1:
        proxyMesh()
    if mc.checkBox("uvs", query=True, value=True) == 1:
        delExtraUVSets()
    if mc.checkBox("FT", query=True, value=True) == 1:
        freezeTransforms()
    if mc.checkBox("normals", query=True, value=True) == 1:
        unlockNormals()
    if mc.checkBox("history", query=True, value=True) == 1:
        delHistory()
    if mc.checkBox("WIP", query=True, value=True) == 1:
        versionUp()
    if mc.checkBox("closeWindow", query=True, value=True) == 1:
        closeWindow()
    print "Done!"
        
        
def saveScene():
	# Save scene
	mc.file(force=True, save=True, type="mayaAscii");
	print "Scene saved";





def autoGroup():
    grps = mc.ls("*group*", transforms=True)
    
    if len(grps) > 2:
        mc.warning("Too many default group nodes for auto group")
    
    elif len(grps) > 1:
    
        # Obtain a list of LO objects
        lo = mc.ls("*LO*", transforms=True);
        # Get the parent of the LO objects
        loParent = mc.listRelatives(lo[0], parent=True);
        
        # Obtain a list of HI objecys
        hi = mc.ls("*REN*", transforms=True);
        # Get the parent of the HI objects
        hiParent = mc.listRelatives(hi[0], parent=True);
        
        
        startName = lo[0];
        
        startSize = len(startName);
        charIndex = 0;
        
        vegType = "";
        
        for i in range(startSize-1, 0, -1):
            if startName[i].isupper() == True:
                charIndex = i;
        
        for i in range(0, charIndex, 1):
            vegType += startName[i];
            
        
        # Group all HI objects
        hiGRP = mc.group(hi, name=vegType + "_HI_GRP", world=True);
        # Delete old HI group
        mc.delete(hiParent);
        
        # Group all LO objects
        loGRP = mc.group(lo, name=vegType + "_LO_GRP", world=True);
        # Delete old HI group
        mc.delete(loParent);
        
        mc.group([hiGRP, loGRP], name="geometry_GRP", world=True)
        
        from app_manager.rmaya.menu import execute_menu_action;
        execute_menu_action('mnu_item_Start_Model_Publish_Scene')
        
        mc.select(clear=True);
        print "Grouping done"
        
    elif len(grps) > 0:
        # Get a list of all objects
        objs = mc.listRelatives(grps[0], children=True)
        
        
        # Get the veg type
        startName = objs[0]
        
        
        startSize = len(startName);
        charIndex = 0;
        
        vegType = "";
        
        for i in range(startSize-1, 0, -1):
            if startName[i].isupper() == True:
                charIndex = i;
        
        for i in range(0, charIndex, 1):
            vegType += startName[i];

        # Group the objects
        GRP = mc.group(objs, name=vegType + "_HI_GRP", world=True);
        # Delete the old group
        mc.delete(grps[0]);
        
        # Make geometry_GRP
        mc.group([GRP], name="geometry_GRP", world=True)
        
        # Start model publish
        from app_manager.rmaya.menu import execute_menu_action;
        execute_menu_action('mnu_item_Start_Model_Publish_Scene')
        
        mc.select(clear=True);
        print "Grouping done"

        
    else:
        mc.warning("No default group nodes for auto group")
    
    





def subdivisionCombine():
    # Get a list of the groups under geometry_GRP
    geoChild = mc.listRelatives("*geometry_GRP*", children=True)
    
    # For each group...
    for grp in geoChild:
        # Get all the children
        children = mc.listRelatives(grp, children=True)
        subD = []
        newName = ""
        
        # For each child object
        for obj in children:
            # Put that object in a list if it contains subD
            if "subd" in obj.lower():
                subD.append(obj)
        
        
        if subD == [] or len(subD) <= 1:
            mc.warning("No subD objects to combine")
        else:
            # For each subD object
            for obj in subD:
                # Check to see if there is a trunk. If so, store that trunks name
                if "trunk" in obj.lower():
                    newName = obj
            
            # If there is no trunk, just store the name of the first subD object
            if "trunk" not in newName.lower():
                newName = subD[0]
            newName += "_combined"
            # Unparent all subD objects so their left over nodes are outside the groups
            mc.parent(subD, world=True)
            # Combine objects
            mc.polyUnite(subD, name=newName)
            # Parent the object back in the original group
            mc.parent(newName, grp)
    mc.select(clear=True)




def autoRename():
    import string
    alphabet = string.uppercase
        
    HI_GRP = "*_HI_GRP*";
    LO_GRP = "*_LO_GRP*";
    
    trunks = "trunk";
    roots = "root";
    leaves = "leave";
    terrain = "terrain"
    flower = "flower"
    stem = "stem"
    blade = "blade"
    
    
    def getObjs(groupName, filterText):
    
        GRP = mc.ls(groupName);
        GRPChildren = mc.listRelatives(GRP, c=True, type="transform");
        objects = [];
        
        for i in GRPChildren:
            if filterText in i.lower():
                objects.append(i);
        
        if objects == []:
            return None;
        else:
            return objects;
    
    
    
    def getBranches(groupName):
        GRP = mc.ls(groupName);
        GRPChildren = mc.listRelatives(GRP, c=True, type="transform");
        objects = [];
        
        for i in GRPChildren:
            if "branch" in i.lower():
                objects.append(i);
            if "level" in i.lower():
                objects.append(i);
            if "twig" in i.lower():
                objects.append(i);
        
        if objects == []:
            return None;
        else:
            return objects;
    
    
    
    def int_to_letters(n):
        final_letters = ''
        n += 1
        while n:
            remainder = (n - 1) % 26
            n = int((n - remainder) / 26)
            final_letters += alphabet[remainder]
        return final_letters[::-1]
    
    
    
    
    def renameObjects(objs, objType):
        if objs == None:
            return None;
        else:
            numObjs = len(objs);
            groupType = mc.listRelatives(objs, parent=True);
            
            if "_HI_" in groupType[0]:
                res = "_HI_";
            else:
                res = "_LO_";
            for i in range(0, numObjs, 1):
                char = int_to_letters(i);
                mc.rename(objs[i], objType + char + res + "REN");
    
    
    
    grps = mc.listRelatives("*geometry_GRP*", children=True)
        
    if len(grps) > 1:
        hiTrunk = getObjs(HI_GRP, trunks);
        renameObjects(hiTrunk, "trunk");
        loTrunk = getObjs(LO_GRP, trunks);
        renameObjects(loTrunk, "trunk");
        
        hiTerrain = getObjs(HI_GRP, terrain);
        renameObjects(hiTerrain, "terrain");
        loTerrain = getObjs(LO_GRP, terrain);
        renameObjects(loTerrain, "terrain");
        
        hiBranches = getBranches(HI_GRP);
        renameObjects(hiBranches, "branches");
        loBranches = getBranches(LO_GRP);
        renameObjects(loBranches, "branches");
        
        hiLeaves = getObjs(HI_GRP, leaves);
        renameObjects(hiLeaves, "leaves");
        loLeaves = getObjs(LO_GRP, leaves);
        renameObjects(loLeaves, "leaves");
        
        hiRoots = getObjs(HI_GRP, roots);
        renameObjects(hiRoots, "roots");
        loRoots = getObjs(LO_GRP, roots);
        renameObjects(loRoots, "roots");
        
        hiFlowers = getObjs(HI_GRP, flower);
        renameObjects(hiFlowers, "flowers");
        loFlowers = getObjs(LO_GRP, flower);
        renameObjects(loFlowers, "flowers");
        
        hiStems = getObjs(HI_GRP, stem);
        renameObjects(hiStems, "stems");
        loStems = getObjs(LO_GRP, stem);
        renameObjects(loStems, "stems");
        
        hiBlades = getObjs(HI_GRP, blade);
        renameObjects(hiBlades, "blades");
        loBlades = getObjs(LO_GRP, blade);
        renameObjects(loBlades, "blades");
    
    else:
        hiTrunk = getObjs(HI_GRP, trunks);
        renameObjects(hiTrunk, "trunk");
        
        hiTerrain = getObjs(HI_GRP, terrain);
        renameObjects(hiTerrain, "terrain");
        
        hiBranches = getBranches(HI_GRP);
        renameObjects(hiBranches, "branches");
        
        hiLeaves = getObjs(HI_GRP, leaves);
        renameObjects(hiLeaves, "leaves");
        
        hiRoots = getObjs(HI_GRP, roots);
        renameObjects(hiRoots, "roots");
        
        hiFlowers = getObjs(HI_GRP, flower);
        renameObjects(hiFlowers, "flowers");
        
        hiStems = getObjs(HI_GRP, stem);
        renameObjects(hiStems, "stems");
        
        hiBlades = getObjs(HI_GRP, blade);
        renameObjects(hiBlades, "blades");       


    print "Renaming done";


    
def fastShaders():
    # Create green shader
    mc.shadingNode("lambert", asShader=True, name="green_FS")
    mc.sets(renderable=True, noSurfaceShader=True, name="green_FSSG", empty=True);
    mc.connectAttr( "green_FS.outColor", "green_FSSG.surfaceShader");
    mc.setAttr("green_FS.color", 0.377284, 0.825806, 0.250716, type="double3");
    
    # Create brown shader
    mc.shadingNode("lambert", asShader=True, name="brown_FS")
    mc.sets(renderable=True, noSurfaceShader=True, name="brown_FSSG", empty=True);
    mc.connectAttr( "brown_FS.outColor", "brown_FSSG.surfaceShader");
    mc.setAttr("brown_FS.color", 0.374194, 0.24199, 0.124731, type="double3");
    
    # Create yellow shader
    mc.shadingNode("lambert", asShader=True, name="yellow_FS")
    mc.sets(renderable=True, noSurfaceShader=True, name="yellow_FSSG", empty=True);
    mc.connectAttr( "yellow_FS.outColor", "yellow_FSSG.surfaceShader");
    mc.setAttr("yellow_FS.color", 1, 1, 0, type="double3");
    
    mc.select(clear=True);
    
    # Select all objects
    mc.select("geometry_GRP");
    mc.select(hierarchy=True);
    
    # Assign brown shader
    mel.eval("sets -e -forceElement brown_FSSG;");
    
    ##### Get green objects
    green = []
    leaves = mc.ls("*leaves*", transforms=True)
    blades = mc.ls("*blades*", transforms=True)
    if leaves != []:
        for obj in leaves:
            green.append(obj)
    
    if blades != []:
        for obj in blades:
            green.append(obj)
    #####
    
    mc.select(green);
    # Deselect Cache objects to avoid error
    #mc.select("*Cache*", deselect=True);
    # Assign green shader
    mel.eval("sets -e -forceElement green_FSSG;");
    
    
    
    
    ##### Get yellow objects
    yellow = []
    flowers = mc.ls("*flowers*", transforms=True)
    if flowers != []:
        for obj in flowers:
            yellow.append(obj)

    #####
    
    
    # Select all flowers
    mc.select(yellow);
    # Deselect Cache objects to avoid error
    #mc.select("*Cache*", deselect=True);
    # Assign green shader
    mel.eval("sets -e -forceElement yellow_FSSG;");
    
    mc.select(clear=True);

    print "New shaders have been applied";


    
    
    
def delUnusedNodes():
    # Evaluate the echoed mel command for delete unused nodes
    mel.eval("hyperShadePanelMenuCommand(\"hyperShadePanel1\", \"deleteUnusedNodes\")");
    print "Hypershade clean!";
    
    
    
            
        
        
        
        
def mergeVerts():
    # Get the geometry_GRP
    geoGrp = mc.ls("*geometry_GRP*");
    # Get the children
    children = mc.listRelatives(geoGrp, allDescendents=True, type="transform");

    noLeaves = [];
    
    for obj in children:
        # If the object is not a group, continue on
        if "GRP" not in obj:
            if "leaves" not in obj.lower() and "flowers" not in obj.lower():
                # If leaves are not in the name, add this item to a new list
                noLeaves.append(obj);
            
    for obj in noLeaves:
        # For every item in the new list that does not include leaves, merge verts
        mc.polyMergeVertex(obj);
    
    mc.select(clear=True);
        
    
    
    
def delLaminaFaces():
    # Evaluate the echoed mel command for selecting lamina faces
    mel.eval("polyCleanupArgList 3 { \"1\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"1e-05\",\"1\",\"1e-05\",\"0\",\"1e-05\",\"0\",\"-1\",\"1\" };");
    # Run a delete command. This will delete whatever is selected
    mc.delete();
    # Go to object mode
    mc.selectMode(object=True);
    # Clear selection so nothing is selected
    mc.select(clear=True);
    print "No more lamina faces!";
        
        
        
        
        
        
def cleanNonmanifoldGeo():
    # Evaluate the echoed mel command for cleaning up non manifold geo
    mel.eval("polyCleanupArgList 3 { \"1\",\"1\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"1e-05\",\"1\",\"1e-05\",\"0\",\"1e-05\",\"0\",\"1\",\"0\" };");
    # Go to object mode
    mc.selectMode(object=True);
    # Clear selection so nothing is selected
    mc.select(clear=True);
    print "Non manifold geo has been cleaned up!"
        




def resetRenderStats():
    # Make a new list variable that contains all mesh shapes in the scene
    meshShapes = mc.ls(type="mesh");
    
    # Look at how many items are in the list and store that in a variable
    meshShapesSize = len(meshShapes);
    
    # Go through the list and reset the render stats
    for i in range(0, meshShapesSize, 1):
        mc.setAttr(meshShapes[i] + ".castsShadows", 1);
        mc.setAttr(meshShapes[i] + ".receiveShadows", 1);
        mc.setAttr(meshShapes[i] + ".holdOut", 0);
        mc.setAttr(meshShapes[i] + ".motionBlur", 1);
        mc.setAttr(meshShapes[i] + ".primaryVisibility", 1);
        mc.setAttr(meshShapes[i] + ".smoothShading", 1);
        mc.setAttr(meshShapes[i] + ".visibleInReflections", 1);
        mc.setAttr(meshShapes[i] + ".visibleInRefractions", 1);
        mc.setAttr(meshShapes[i] + ".doubleSided", 1);
        mc.setAttr(meshShapes[i] + ".opposite", 0);
    print "Render stats have been reset";
            



def proxyMesh():
    loGRP = mc.ls("*_LO_GRP*")
    
    if loGRP != []:
    
        # Get the children of geometry_GRP
        loObjs = mc.listRelatives("*geometry_GRP*", children=True);
        # Keep the name of the first child
        objName = loObjs[0];
        objList = objName.split("_");
        
        vegType = objList[0];
        
        
        # Select the _LO_GRP
        mc.select("*_LO_GRP*");
        mc.duplicate();
        
        # Store the duplicated group's name
        dupeGroup = mc.ls(sl=True);
        # Combine the group to one mesh
        mc.polyUnite();
        # Rename this new mesh for being a proxy
        mc.rename(vegType + "_PRX");
        mc.DeleteHistory();
        #Delete the duplicated group
        mc.delete(dupeGroup);
        # Group the new proxy mesh into proxy_GRP under geometry_GRP
        mc.group(vegType + "_PRX", name="proxy_GRP", parent="geometry_GRP");
        print "Proxy mesh has been generated";
    
    else:
        mc.warning("No _LO_GRP to make proxy mesh from")





def delExtraUVSets():
    geomGroups = mc.listRelatives("*geometry_GRP*", children=True);
    
    children = []
    
    for grp in geomGroups:
        children = mc.listRelatives(grp, children=True)
    
        for child in children:
            # Selects on mesh object at a time
            mc.select(child);
            # Gets a list of all UV Sets
            UV_Sets = mc.polyUVSet(query=True, auv=True);
            
            if "prx" in child.lower():
                for set in UV_Sets:
                    if set != UV_Sets[0]:
                        mc.polyUVSet(uvSet=set, delete=True);
            
            else:
                if len(UV_Sets) > 1 and UV_Sets[0] == "map1":
                    mc.polyUVSet(create=True, uvSet="map1")
                    mc.polyUVSet(copy=True, nuv="map1", uvSet=UV_Sets[1])
                
                for set in UV_Sets:
                    if set != UV_Sets[0]:
                        mc.polyUVSet(uvSet=set, delete=True);
    
    
    mc.select(clear=True)
    print "Extra UV sets have been deleted";
                    
                    
                    
def freezeTransforms():
    mc.select("geometry_GRP");
    mc.select(hierarchy=True);
    mc.FreezeTransformations();
    mc.select(clear=True);
    print "Transforms have been frozen";

        
        
        
        
def unlockNormals():
    # Get the geometry_GRP
    geoGrp = mc.ls("*geometry_GRP*");
    # Get all the children
    children = mc.listRelatives(geoGrp, allDescendents=True, type="transform");
    # Select the children
    mc.select(children);
    # Unlock normals
    mc.polyNormalPerVertex(unFreezeNormal=True);
    
    for child in children:
        mc.select(child)
        mc.polySoftEdge(angle=180)
    
    
    # Clear selection
    mc.select(clear=True);
    print "Normals unlocked";




def delHistory():     
    mc.select("*geometry_GRP*");
    mc.select(hi=True)
    mc.DeleteHistory();
    mc.select(clear=True);
            
    # Noticed some issues where sometimes unused nodes would stick around with merged branches. So running the delete again
    # Evaluate the echoed mel command for delete unused nodes
    mel.eval("hyperShadePanelMenuCommand(\"hyperShadePanel1\", \"deleteUnusedNodes\")");
    
    print "History has been deleted";




def versionUp():
    from app_manager.rmaya.menu import execute_menu_action;
    execute_menu_action('mnu_item_Version_Up_WIP');




def closeWindow():
    if mc.window("SpeedClean", exists=True):
        mc.deleteUI("SpeedClean", window=True)