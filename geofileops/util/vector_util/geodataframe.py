# -*- coding: utf-8 -*-
"""
Module containing utilities regarding low level vector operations.
"""

import enum
import logging
from typing import Any, List

import geopandas as gpd

from . import geometry

#-------------------------------------------------------------
# First define/init some general variables/constants
#-------------------------------------------------------------
# Get a logger...
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

#-------------------------------------------------------------
# GeoDataFrame helpers
#-------------------------------------------------------------

def extract_polygons_from_gdf(
        in_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:

    # Extract only polygons
    poly_gdf = in_gdf.loc[(in_gdf.geometry.geom_type == 'Polygon')].copy()
    multipoly_gdf = in_gdf.loc[(in_gdf.geometry.geom_type == 'MultiPolygon')].copy()
    collection_gdf = in_gdf.loc[(in_gdf.geometry.geom_type == 'GeometryCollection')].copy()
    collection_polys_gdf = None
    
    if len(collection_gdf) > 0:
        collection_polygons = []
        for collection_geom in collection_gdf.geometry:
            collection_polygons.extend(geometry.extract_polygons_from_geometry(collection_geom))
        if len(collection_polygons) > 0:
            collection_polys_gdf = gpd.GeoDataFrame(geometry=collection_polygons, crs=in_gdf.crs)

    # Only keep the polygons...
    ret_gdf = poly_gdf
    if len(multipoly_gdf) > 0:
        ret_gdf = ret_gdf.append(multipoly_gdf.explode(), ignore_index=True)
    if collection_polys_gdf is not None:
        ret_gdf = ret_gdf.append(collection_polys_gdf, ignore_index=True)
    
    return ret_gdf

def polygons_to_lines(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    cardsheets_lines = []
    for cardsheet_poly in input_gdf.itertuples():
        cardsheet_boundary = cardsheet_poly.geometry.boundary
        if cardsheet_boundary.type == 'MultiLineString':
            for line in cardsheet_boundary:
                cardsheets_lines.append(line)
        else:
            cardsheets_lines.append(cardsheet_boundary)

    cardsheets_lines_gdf = gpd.GeoDataFrame(geometry=cardsheets_lines, crs=input_gdf.crs)

    return cardsheets_lines_gdf
