import arcpy
import ctypes
import os

loaded_dll = ctypes.cdll.LoadLibrary(os.path.join(os.path.abspath(os.path.dirname(__file__)), "pythoncppdll.dll"))
cpp_implementation = loaded_dll.AddAreaFieldToFeatureClassCPlusPlus
csharp_implementation = loaded_dll.AddAreaFieldToFeatureClassCSharp

cpp_implementation.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
cpp_implementation.restype = ctypes.c_int

csharp_implementation.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
csharp_implementation.restype = ctypes.c_int

def execute_tool(language):
    featureclass_path = arcpy.GetParameterAsText(0)
    field_name = arcpy.GetParameterAsText(1)
    arcpy.SetParameterAsText(2, featureclass_path)

    if language == 'C++':
        fn = cpp_implementation
    elif language == 'C#':
        fn = csharp_implementation
    else:
        raise ValueError("Invalid language: {0}".format(language))

    arcpy.AddMessage("Adding field {0}".format(field_name))
    arcpy.AddField_management(featureclass_path, field_name, "DOUBLE", "#", "#", "#", "#", "NULLABLE", "NON_REQUIRED", "#")

    arcpy.AddMessage("Executing {0} function...".format(language))
    returncode = fn(featureclass_path, field_name)

    if returncode == -1:
        arcpy.AddError("Error opening Feature Class")
    elif returncode == -2:
        arcpy.AddError("Field does not exist on Feature Class")
    elif returncode == -3:
        arcpy.AddError("Shape field is not Polygon")
    elif returncode == -4:
        arcpy.AddError("Function Error")
    elif returncode == 0:
        arcpy.AddMessage("Computed value")
    else:
        arcpy.AddError("Unknown failure")
