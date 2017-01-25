# Author: Danny Straus

### Export cache and version up tool

import maya.cmds as mc;
import os;


frameInput = 0;


if mc.window("SpeedCache", exists=True):
    mc.deleteUI("SpeedCache", window=True)
    
mc.window("SpeedCache", title="SpeedTree Cache Export", wh=[290,200], s=False);
mc.columnLayout("columnIntro", adj=True, parent="SpeedCache");
mc.separator(h=10);
mc.text("Alembic cache export tool for SpeedTree & Cycles", font="boldLabelFont")
mc.separator(h=10);
mc.rowColumnLayout("row", parent="SpeedCache", numberOfRows=1);
mc.intField("frames", maxValue=1000, minValue=1, value=240, width=50, step=1, parent="row");
mc.separator(horizontal=False, style="single", width=10, vis=False)
mc.text("inputFrames", label="Input length of cache in frames", parent="row");
mc.columnLayout("columnMain", adj=True, parent="SpeedCache");
mc.separator(h=10);
mc.checkBox("scenePrep", label="Scene prep", value=1);
mc.separator(h=10);
mc.checkBox("save", label="Save scene", value=1);
mc.separator(h=10);
mc.checkBox("newScene", label="Create new scene for publish", value=0);
mc.separator(h=10);
mc.checkBox("delWindow", label="Close window on completion", value=1);
mc.separator(h=10);
mc.button(label="Export cache", c="buttonPress()");
mc.showWindow("SpeedCache");




def buttonPress():
    frameInput = mc.intField("frames", query=True, value=True);
    print frameInput;
    
    # Scene prep
    if mc.checkBox("scenePrep", query=True, value=True) == True:
        scenePrep(frameInput);
    
    # Save scene
    if mc.checkBox("save", query=True, value=True) == True:
        saveScene();
    


    # Export cache
    cacheMoney(frameInput);
        
        
    # New scene for publish
    if mc.checkBox("newScene", query=True, value=True) == True:
        newScene();
    
    
    # Delete window
    if mc.checkBox("delWindow", query=True, value=True) == True:
        closeWindow();
    



def scenePrep(numFrames):
    # Frame all
    mel.eval("fitPanel -all;")
    # Set timeline range
    mc.playbackOptions(edit=True, maxTime=numFrames);
    # Load abc plugin
    mel.eval("loadPlugin \"/usr/autodesk/maya2016/bin/plug-ins/AbcExport.so\";")


def saveScene():
    mc.file(force=True, save=True, type="mayaAscii");
    print "Scene saved";



def closeWindow():
    if mc.window("SpeedCache", exists=True):
        mc.deleteUI("SpeedCache", window=True)



def cacheMoney(numFrames):
    
    
    ######################### Export Cache
    # Get the current file path
    currentPath = mc.file(expandName=True, query=True);
    # Split the path at the last / to get the file name and path
    partPath = currentPath.rpartition("/");
    # Split the file name at the _ to get just the name of the asset
    fileName = partPath[2].rpartition("_");
    print fileName
    # Add this part to the file name for exporting alembic cache
    fileName = fileName[0] + "_merged.abc";
    
    # Split the path at the last / to get the model folder and not the master folder
    filePath = partPath[0].rpartition("/");
    # Add this part to the path as this will be where the cache needs to go
    filePath = filePath[0] + "/cache_export";
    # If path does not exist, make it
    if os.path.exists(filePath) == False:
        os.mkdir(filePath);
    # Create full path where the cache will go
    cachePath = filePath + "/" + fileName;
    
    # Select the geometry group
    cacheSelection = mc.ls("*geometry_GRP*");
    
    
    
    ### Setting string for export
    abcString = "AbcExport -j \"-frameRange 1 %d" % numFrames + " -uvWrite -dataFormat ogawa -root |master|";
    abcString += cacheSelection[0];
    abcString += " -file ";
    abcString += cachePath;
    abcString += "\";";
    
    print cachePath
    
    # Export cache
    mel.eval(abcString);

    
    mc.select(clear=True);
    print "Cache has been exported";
    
    

    
    ######################### Save scene
    mc.file(force=True, save=True, type="mayaAscii");
    print "File has been saved";



        
        
def newScene():
    # Version up WIP
    from app_manager.rmaya.menu import execute_menu_action;
    execute_menu_action('mnu_item_Version_Up_WIP');
    print "New version has been made"
    
    # Delete history on all objects
    mc.select("*geometry_GRP*");
    mc.select(hi=True)
    mc.DeleteHistory();
    mc.select(clear=True);
    print "History has been deleted";
    
    # Save scene
    mc.file(force=True, save=True, type="mayaAscii");
    print "File has been saved";
