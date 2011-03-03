// pythoncppdll.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

using namespace dotnettoolfrompython;

extern "C"
{

  __declspec(dllexport) int AddAreaFieldToFeatureClassCPlusPlus(const wchar_t* feature_class, const wchar_t* field_name)
  {
	  // Convert char*s to bstring
	  _bstr_t catalogPath(feature_class),
	          newfieldname(field_name);

	  // Coinitialize GP utilities class
	  IGPUtilitiesPtr ipUtil(CLSID_GPUtilities);

	  // Feature class holder
	  IFeatureClassPtr ipFeatureclass(0);

	  HRESULT hr;

	  // Try to fetch feature class from catalog path
	  if (FAILED(hr = ipUtil->OpenFeatureClassFromString(catalogPath, &ipFeatureclass)))
	  {
		  return -1;
	  }

	  // Field index of the field of interest
	  long fieldIndex;
	  if (FAILED(ipFeatureclass->FindField(newfieldname, &fieldIndex)))
      return -2;

	  // Set up query and filter
	  IQueryFilterPtr ipFilter(CLSID_QueryFilter);
	  IFeatureCursorPtr ipCursor;
	  IFeaturePtr ipRow;
	  IGeometryPtr ipShape;

	  // Open cursor on feature class
	  ipFeatureclass->Update(ipFilter, VARIANT_FALSE, &ipCursor);

	  // Iterate
	  esriGeometryType gt;
	  for (ipCursor->NextFeature(&ipRow);
		   ipRow != NULL;
		   ipCursor->NextFeature(&ipRow))
	  {
		  // Get row's associated geometry
		  ipRow->get_Shape(&ipShape);
		  // Ensure we've got a polygon
		  ipShape->get_GeometryType(&gt);
		  if (gt != esriGeometryPolygon)
			  return -3;
		  // Get area
		  IAreaPtr ipArea(ipShape);
		  double area;
		  ipArea->get_Area(&area);
		  // Pop double into a variant
		  VARIANT value;
      ::VariantInit(&value);
		  value.vt = VT_R8;
		  value.dblVal = area;
		  // Set double variant onto target field
		  ipRow->put_Value(fieldIndex, value);
		  // Save
		  ipRow->Store();
	  }

	  return 0;
  }


  __declspec(dllexport) int AddAreaFieldToFeatureClassCSharp(const wchar_t* feature_class, const wchar_t* field_name)
  {
    ExecuteTool et;
    System::String ^fc_string(gcnew System::String(feature_class)),
                   ^field_name_string(gcnew System::String(field_name));
    return et.AddAreaFieldToFeatureClass(fc_string, field_name_string);
  }
}