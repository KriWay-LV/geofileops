# -*- coding: utf-8 -*-
"""
Tests for functionalities in vector_util.
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

def test_create_grid2():
    # Test for small number of cells
    '''
    for i in range(1, 10):
        grid_gdf = vector_util.create_grid2(
                total_bounds=(40000.0, 160000.0, 45000.0, 210000.0), 
                nb_squarish_cells=i)
        assert len(grid_gdf) == i
    '''
    
    # Test for larger number of cells
    grid_gdf = vector_util.create_grid2(
            total_bounds=(40000.0, 160000.0, 45000.0, 210000.0), 
            nb_squarish_tiles=100,
            crs='epsg:31370')
    assert len(grid_gdf) == 96

def test_split_tiles():
    input_tiles_path = get_testdata_dir() / 'BEFL_kbl.gpkg'
    input_tiles = geofile.read_file(input_tiles_path)
    nb_tiles_wanted = len(input_tiles) * 8
    result = vector_util.split_tiles(
            input_tiles=input_tiles,
            nb_tiles_wanted=nb_tiles_wanted)

    #geofile.to_file(result, r"C:\temp\BEFL_kbl_split.gpkg")

    assert len(result) == len(input_tiles) * 8

if __name__ == '__main__':
    import os
    import tempfile
    tmpdir = Path(tempfile.gettempdir()) / "test_vector_util_grid"
    os.makedirs(tmpdir, exist_ok=True)
    test_create_grid2()
    #test_split_tiles()
    