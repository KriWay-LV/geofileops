# -*- coding: utf-8 -*-
"""
Tests for functionalities in vector_util, regarding geometry operations.
"""

from pathlib import Path
import sys

import shapely.geometry as sh_geom

# Add path so the local geofileops packages are found 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from geofileops import geofile
from geofileops.util import vector_util

def get_testdata_dir() -> Path:
    return Path(__file__).resolve().parent / 'data'

def test_numberpoints():
    # Test Point
    point = sh_geom.Point((0, 0))
    numberpoints = vector_util.numberpoints(point)
    numberpoints_geometrycollection = numberpoints
    assert numberpoints == 1

    # Test MultiPoint
    multipoint = sh_geom.MultiPoint([(0, 0), (10, 10), (20, 20)])
    numberpoints = vector_util.numberpoints(multipoint)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 3
    
    # Test LineString
    linestring = sh_geom.LineString([(0, 0), (10, 10), (20, 20)])
    numberpoints = vector_util.numberpoints(linestring)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 3
    
    # Test MultiLineString
    multilinestring = sh_geom.MultiLineString(
            [linestring.coords, [(100, 100), (110, 110), (120, 120)]])
    numberpoints = vector_util.numberpoints(multilinestring)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 6

    # Test Polygon
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    numberpoints = vector_util.numberpoints(poly)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 11

    # Test MultiPolygon
    poly2 = sh_geom.Polygon(shell=[(100, 100), (100, 110), (110, 110), (110, 100), (100,100)])
    multipoly = sh_geom.MultiPolygon([poly, poly2])
    numberpoints = vector_util.numberpoints(multipoly)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 16

    # Test GeometryCollection (as combination of all previous ones)
    geometrycollection = sh_geom.GeometryCollection([point, multipoint, linestring, multilinestring, poly, multipoly])
    numberpoints = vector_util.numberpoints(geometrycollection)
    assert numberpoints == numberpoints_geometrycollection

def test_simplify_ext_lang_basic():
    # Test LineString lookahead -1 
    linestring = sh_geom.LineString([(0, 0), (10, 10), (20, 20)])
    geom_simplified = vector_util.simplify_ext(
            geometry=linestring, 
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1,
            lookahead=-1)
    assert isinstance(geom_simplified, sh_geom.LineString)
    assert len(geom_simplified.coords) < len(linestring.coords)
    assert len(geom_simplified.coords) == 2

    # Test Polygon lookahead -1 
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    geom_simplified = vector_util.simplify_ext(
            geometry=poly, 
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1,
            lookahead=-1)
    assert isinstance(geom_simplified, sh_geom.Polygon)
    assert len(geom_simplified.exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified.exterior.coords) == 5

    # Test Point simplification
    point = sh_geom.Point((0, 0))
    geom_simplified = vector_util.simplify_ext(
            geometry=point, 
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.Point)
    assert len(geom_simplified.coords) == 1

    # Test MultiPoint simplification
    multipoint = sh_geom.MultiPoint([(0, 0), (10, 10), (20, 20)])
    geom_simplified = vector_util.simplify_ext(
            geometry=multipoint,
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiPoint)
    assert len(geom_simplified) == 3

    # Test LineString simplification
    linestring = sh_geom.LineString([(0, 0), (10, 10), (20, 20)])
    geom_simplified = vector_util.simplify_ext(
            geometry=linestring, 
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.LineString)
    assert len(geom_simplified.coords) < len(linestring.coords)
    assert len(geom_simplified.coords) == 2
    
    # Test MultiLineString simplification
    multilinestring = sh_geom.MultiLineString(
            [list(linestring.coords), [(100, 100), (110, 110), (120, 120)]])
    geom_simplified = vector_util.simplify_ext(
            geometry=multilinestring, 
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiLineString)
    assert len(geom_simplified) == 2
    assert len(geom_simplified[0].coords) < len(multilinestring[0].coords)
    assert len(geom_simplified[0].coords) == 2

    # Test Polygon simplification
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    geom_simplified = vector_util.simplify_ext(
            geometry=poly,
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.Polygon)
    assert len(geom_simplified.exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified.exterior.coords) == 5

    # Test MultiPolygon simplification
    poly2 = sh_geom.Polygon(shell=[(100, 100), (100, 110), (110, 110), (110, 100), (100,100)])
    multipoly = sh_geom.MultiPolygon([poly, poly2])
    geom_simplified = vector_util.simplify_ext(
            geometry=multipoly,
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiPolygon)
    assert len(geom_simplified) == 2
    assert len(geom_simplified[0].exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified[0].exterior.coords) == 5

    # Test GeometryCollection (as combination of all previous ones) simplification
    geom = sh_geom.GeometryCollection([point, multipoint, linestring, multilinestring, poly, multipoly])
    geom_simplified = vector_util.simplify_ext(
            geometry=geom,
            algorithm=vector_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.GeometryCollection)
    assert len(geom_simplified) == 6

def test_simplify_ext_keep_points_on(tmpdir):
    
    #### Test if keep_points_on works properly ####
    
    ## First init some stuff ##
    # Read the test data
    input_path = get_testdata_dir() / 'simplify_onborder_testcase.gpkg'
    geofile.copy(input_path, tmpdir / input_path.name)
    input_gdf = geofile.read_file(input_path)

    # Create geometry where we want the points kept
    grid_gdf = vector_util.create_grid(
            total_bounds=(210431.875-1000, 176640.125-1000, 210431.875+1000, 176640.125+1000),
            nb_columns=2,
            nb_rows=2,
            crs='epsg:31370')
    geofile.to_file(grid_gdf, tmpdir / "grid.gpkg")
    grid_coords = [tile.exterior.coords for tile in grid_gdf['geometry']]
    grid_lines_geom = sh_geom.MultiLineString(grid_coords)
    
    ## Test rdp (ramer–douglas–peucker) ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by rdp 
    point_on_input_and_border = sh_geom.Point(210431.875, 176599.375)
    tolerance_rdp = 0.5

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                    tolerance=tolerance_rdp))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_rdp{tolerance_rdp}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                    tolerance=tolerance_rdp, keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_rdp{tolerance_rdp}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input
    
    ## Test vw (visvalingam-whyatt) ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by vw 
    point_on_input_and_border = sh_geom.Point(210430.125, 176640.125)
    tolerance_vw = 16*0.25*0.25   # 1m²

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.VISVALINGAM_WHYATT, 
                    tolerance=tolerance_vw))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_vw{tolerance_vw}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.VISVALINGAM_WHYATT, 
                    tolerance=tolerance_vw, 
                    keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_vw{tolerance_vw}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input
    
    ## Test lang ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by lang 
    point_on_input_and_border = sh_geom.Point(210431.875,176606.125)
    tolerance_lang = 0.25
    step_lang = 8

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.LANG, 
                    tolerance=tolerance_lang, lookahead=step_lang))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_lang;{tolerance_lang};{step_lang}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.geometry.apply(
            lambda geom: vector_util.simplify_ext(
                    geom, algorithm=vector_util.SimplifyAlgorithm.LANG, 
                    tolerance=tolerance_lang, lookahead=step_lang, 
                    keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_lang;{tolerance_lang};{step_lang}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input

def test_simplify_ext_no_simplification():
    # Backup reference to simplification module
    _temp_simplification = None
    if sys.modules.get('simplification'):
        _temp_simplification = sys.modules['simplification']
    try:
        # Fake that the module is not available
        sys.modules['simplification'] = None

        # Using RDP needs simplification module, so should give ImportError
        vector_util.simplify_ext(
                geometry=sh_geom.LineString([(0, 0), (10, 10), (20, 20)]), 
                algorithm=vector_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                tolerance=1)
        assert True is False
    except ImportError as ex:
        assert True is True
    finally:
        if _temp_simplification:
            sys.modules['simplification'] = _temp_simplification
        else:
            del sys.modules['simplification']

if __name__ == '__main__':
    import os
    import tempfile
    tmpdir = Path(tempfile.gettempdir()) / "test_vector_util_geometry"
    os.makedirs(tmpdir, exist_ok=True)
    #test_numberpoints()
    test_simplify_ext_lang_basic()
    #test_simplify_ext_keep_points_on(tmpdir)
    #test_simplify_ext_no_simplification()
