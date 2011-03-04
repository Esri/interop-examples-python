using System;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Geometry;

namespace dotnettoolfrompython
{
    public class ExecuteTool
    {
        public int AddAreaFieldToFeatureClass(String feature_class, String field_name)
        {
            try
            {

                IGPUtilities ipUtils = new GPUtilities();
                IFeatureClass ipFeatureClass;

                // Open FC
                try
                {
                    ipFeatureClass = ipUtils.OpenFeatureClassFromString(feature_class);
                }
                catch(Exception)
                {
                    return -1;
                }

                // Find field
                int fieldIndex;
                try
                {
                    fieldIndex = ipFeatureClass.FindField(field_name);
                }
                catch(Exception)
                {
                    return -2;
                }

                // Set up query and filter
	            IQueryFilter ipFilter = new QueryFilter();
	            IFeatureCursor ipCursor;
	            IFeature ipRow;
	            IGeometry ipShape;

                // Open cursor on feature class
                ipCursor = ipFeatureClass.Update(ipFilter, false);

                for (ipRow = ipCursor.NextFeature();
                     ipRow != null;
                     ipRow = ipCursor.NextFeature())
                {
                    ipShape = ipRow.ShapeCopy;
                    if (ipShape.GeometryType != esriGeometryType.esriGeometryPolygon)
                        return -3;

                    IArea ipArea = ipShape as IArea;
                    double area = ipArea.Area;
                    ipRow.Value[fieldIndex] = area;

                    ipRow.Store();
                }

                return 0;
            }
            catch (Exception)
            {
                return -4;
            }
        }
    }
}
