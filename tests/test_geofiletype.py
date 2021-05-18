# -*- coding: utf-8 -*-
"""
Tests for functionalities in geofileops.general.
"""

from pathlib import Path
import sys

# Add path so the local geofileops packages are found 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from geofileops.util.geofiletype import GeofileType
from tests import test_helper

def test_geofiletype_enum():
    ### Test ESRIShapefile geofiletype ###
    # Test getting a geofiletype for a suffix 
    assert GeofileType('.shp') == GeofileType.ESRIShapefile

    # Test getting a geofiletype for a Path (case insensitive)
    path = Path("/testje/path_naar_file.sHp") 
    assert GeofileType(path) == GeofileType.ESRIShapefile

    # Test getting a geofiletype for an ogr driver
    assert GeofileType('ESRI Shapefile') == GeofileType.ESRIShapefile

    ### GPKG geofiletype ###
    # Test getting a geofiletype for a suffix 
    assert GeofileType('.gpkg') == GeofileType.GPKG

    # Test getting a geofiletype for a Path (case insensitive)
    path = Path("/testje/path_naar_file.gPkG") 
    assert GeofileType(path) == GeofileType.GPKG

    # Test getting a geofiletype for an ogr driver
    assert GeofileType('GPKG') == GeofileType.GPKG

    ### SQLite geofiletype ###
    # Test getting a geofiletype for a suffix 
    assert GeofileType('.sqlite') == GeofileType.SQLite

    # Test getting a geofiletype for a Path (case insensitive)
    path = Path("/testje/path_naar_file.sQlItE")
    assert GeofileType(path) == GeofileType.SQLite

    # Test getting a geofiletype for an ogr driver
    assert GeofileType('SQLite') == GeofileType.SQLite

if __name__ == '__main__':
    # Init
    tmpdir = test_helper.init_test_for_debug(Path(__file__).stem)

    # Run!
    test_geofiletype_enum()