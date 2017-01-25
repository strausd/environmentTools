# Author: Danny Straus

### This script will take the cache exported from Maya for an asset and copy it to the proper location for cycles

import maya.cmds as mc
import shutil
import sys

if mc.window("copyCacheData", query=True, exists=True):
    mc.deleteUI("copyCacheData", window=True)

mc.window("copyCacheData", title="Copy Cycle Cache", wh=[256,175], sizeable=False)
mc.columnLayout(adjustableColumn=True)
mc.separator(h=3)
mc.text("This button will start the initial \nshot cache export and publish")
mc.separator(h=10)
mc.button("Shot cache export", command="shotCache()")
mc.separator(h=10)
mc.separator(h=10)
mc.separator(h=10)
mc.text("This button will copy the cache exported from Maya \nfor this asset into the proper location for cycles.")
mc.separator(h=10)
mc.text("This will only work once the publish has finished")
mc.separator(h=10)
mc.button("Just do it", command="copyCache()")
mc.separator()

mc.showWindow("copyCacheData")



def shotCache():
    from pipe_api.rmaya.ui import shot_cache_exporter
    shot_cache_exporter.main()


def copyCache():
    # Get the current file path and then get just the name of the current cycle
    cycName = mc.file(query=True, expandName=True)
    cycName = cycName.split("/")
    cycName = cycName[4]
    
    # Get rid of _cyc to get the asset
    asset = cycName.split("_")
    asset = asset[0]
    
    # Variable to hold where the uppercase letters are
    upperCaseIndex = 0
    
    ### For loop to get rid of the speed in the asset name and just get the specific asset
    # For every character in the asset...
    for i in range(0, len(asset), 1):
        # If that character is upper case...
        if asset[i].isupper():
            # Store that location in upperCaseIndex
            upperCaseIndex = i
    
    # Holds the asset name without the speed on the end
    assetName = asset[0:upperCaseIndex]
    
    # Holds the speed of the asset
    cycSpeed = asset[upperCaseIndex:len(asset)]
    
    # Name of the alembic cache file that goes into the source
    abcName = assetName + "_cyc" + cycSpeed + "_merged.abc"
    
    
    srcPath = "/work/20554_SCOOBYDAX/assets/vegetation/" + assetName + "/model/cache_export/"
    # Source for the copy
    src = srcPath + abcName
    # Destination path
    dstPath = "/cache/entertainment/20554_SCOOBYDAX/cycles/" + cycName + "/published/animation/" + assetName + "/published/"
    # Destination for the copy
    dst = dstPath + assetName + "_merged.abc"
    
    
    # If path exists, copy the file. Otherwise don't
    if mc.file(dstPath, query=True, exists=True) and mc.file(src, query=True, exists=True):
        shutil.copy(src,dst)
        sys.stdout.write("Copy success!\n")
        
        # Delete the window
        mc.deleteUI("copyCacheData", window=True)
        
    elif not mc.file(dstPath, query=True, exists=True) and not mc.file(srcPath, query=True, exists=True):
        mc.warning("Publish has not finished (or destination path does not exist) AND source file does not exist")
        
    elif not mc.file(dstPath, query=True, exists=True):
        mc.warning("Publish has not finished (or destination path does not exist)")
        
    else:
        mc.warning("Source file does not exist")
