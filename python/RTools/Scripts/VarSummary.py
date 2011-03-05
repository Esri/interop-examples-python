import arcpy 
import os
import re
import sys
import subprocess
import tempfile

class TempShapefile(object):
    def __init__(self, featureclass):
        self._fcname = featureclass
        self._shapefilename = None
    def __enter__(self):
        if self._fcname.lower().endswith('.shp') and os.path.isfile(self._fcname):
            arcpy.AddMessage("Using shape file {0}".format(self._fcname))
            return self._fcname
        assert not self._shapefilename, "Already have a temp shapefile"
        self._shapefilename = tempfile.mktemp('.shp')
        arcpy.AddMessage("Creating temp shapefile {0}".format(self._shapefilename))
        arcpy.CopyFeatures_management(self._fcname, self._shapefilename)
        return self._shapefilename
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._shapefilename and arcpy.Exists(self._shapefilename):
            arcpy.AddMessage("Deleting temp shapefile {0}".format(self._shapefilename))
            arcpy.Delete_management(self._shapefilename)
        self._shapefilename = None

def VarSummary():
    # Use a context manager to make sure we have a shapefile to work with
    with TempShapefile(arcpy.GetParameterAsText(0)) as shapefile_path:
        # Assemble command line
        commandlineargs = ['R', '--slave', '--vanilla', '--args',
                           shapefile_path,
                           str(arcpy.GetParameterAsText(1))]

        # Locate and read R input script
        rscriptname = os.path.join(os.path.abspath(
                                        os.path.dirname(__file__)),
                                    "VarSummary.r")
        scriptsource = open(rscriptname, 'rb')

        # Open R and feed it the script
        rprocess = subprocess.Popen(commandlineargs,
                                    stdin=scriptsource,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)

        # Grab the printed output
        stdoutstring, stderrstring = rprocess.communicate()

        # Push output to messages window
        if stderrstring and "Calculations Complete..." not in stdoutstring:
            arcpy.AddError(stderrstring)
        else:
            # Just grab the tables
            tables = re.findall('\[1\] "Begin Calculations[.]{4}"\n(.*)\n\[1\] "Calculations Complete[.]{3}"',
                                stdoutstring.replace('\r', ''),
                                re.DOTALL)
            # Push to output window
            arcpy.AddMessage(" ")
            arcpy.AddMessage("\n".join(tables))
            arcpy.AddMessage(" ")

if __name__ == '__main__':
    test = VarSummary() 
