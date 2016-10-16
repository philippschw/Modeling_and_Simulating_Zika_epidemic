#### Draw polygons more efficiently with matplotlib, 
### Returns dictionary with index as key and matplotlib polygon as value

from descartes import PolygonPatch
from shapely.geometry import MultiPolygon
import numpy as np

def add(gpdf):
    gpdf["mpl_polygon"] = np.nan
    gpdf['mpl_polygon'] = gpdf['mpl_polygon'].astype(object)
    for self_index, self_row_df in gpdf.iterrows():
        m_polygon = self_row_df['geometry']
        poly=[]
        if m_polygon.geom_type == 'MultiPolygon':
            for pol in m_polygon:
                poly.append(PolygonPatch(pol))
        else:
            poly.append(PolygonPatch(m_polygon))
        gpdf.set_value(self_index, 'mpl_polygon', poly)
    return gpdf['mpl_polygon'].to_dict()
    
