#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#License:
#
#
# Revit Batch Processor Sample Code
#
# Copyright (c) 2020  Jan Christel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

# this sample moves revit link instances onto a workset specified in list

import clr
import System

# flag whether this runs in debug or not
debug_ = False

# --------------------------
#default file path locations
# --------------------------
#store output here:
rootPath_ = r'C:\temp'
#path to Common.py
commonlibraryDebugLocation_ = r'C:\temp'
#debug mode revit project file name
debugRevitFileName_ = r'C:\temp\Test_Files.rvt'

# Add batch processor scripting references
if not debug_:
    import revit_script_util
    import revit_file_util
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
     # NOTE: these only make sense for batch Revit file processing mode.
    doc = revit_script_util.GetScriptDocument()
    revitFilePath_ = revit_script_util.GetRevitFilePath()
else:
    #get default revit file name
    revitFilePath_ = debugRevitFileName_

#set path to common library
import sys
sys.path.append(commonlibraryDebugLocation_)

#import common library
import Common
from Common import *

clr.AddReference('System.Core')
clr.ImportExtensions(System.Linq)

from Autodesk.Revit.DB import *

#output messages either to batch processor (debug = False) or console (debug = True)
def Output(message = ''):
    if not debug_:
        revit_script_util.Output(str(message))
    else:
        print (message)

# -------------
# my code here:
# -------------

#save file under new name in given location
def SaveAs(doc, currentFullFileName, nameData):
    status = True
    revitFileName = GetRevitFileName(currentFullFileName)
    newFileName= ''
    match = False
    for oldName, newName in nameData:
        if (revitFileName.startswith(oldName)):
            match = True
            # save file under new name
            newFileName = rootPath_ + '\\'+ newName +'.rvt'
            break
    if(match == False):
        # save under same file name
        newFileName = rootPath_ + '\\'+ revitFileName +'.rvt'
    try:
        SaveAsWorksharedFile(doc, newFileName)
    except Exception as e:
        status = False
        Output('Failed to save revit file to new location!')
        Output (str(e))
    return status

# -------------
# main:
# -------------

#list containing the default file names:
# [[revit host file name before save, revit host file name after save]]
defaultFileNames_ = [
['Test_Files', 'Test_Files_new']
]

#save revit file to new location
Output('Modifying Revit File.... start')
result_ = SaveAs(doc, revitFilePath_, defaultFileNames_)

#make further changes as required....


Output('Modifying Revit File.... status: ' + str(result_))

#sync changes back to central
if (doc.IsWorkshared and debug_ == False):
    Output('Syncing to Central: start')
    SyncFile (doc)
    Output('Syncing to Central: finished')

Output('Modifying Revit File.... finished ')
