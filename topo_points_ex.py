from concurrent.futures import ProcessPoolExecutor
from itertools import chain
import time
import fiona
import pandas as pd

from pathlib import Path

def process_file(input_file):
    """ returns all the points from triangles as a set"""
    all_points = set()
    print(input_file)
    with fiona.open(input_file, layer='ReliefFeature') as layer:
        for item in layer:
            for multi_poly in item.geometry.coordinates:
                for poly in multi_poly:
                    for v in poly :
                        all_points.add(v)
    return all_points


def main():
    p = Path('data/mtl_tin')
    all_files = list(p.glob('*.gml'))

    with ProcessPoolExecutor(max_workers=5) as executor:
        result = executor.map(process_file, all_files)
    all_points = set(chain.from_iterable([r for r in result]))
    df = pd.DataFrame(all_points)
    df.columns=['x','y','z']
    df.to_feather('mtl_points.feather')

if __name__ == '__main__': 
    start = time.time()
    main()
    end = time.time()
    print('took : {}m'.format((end-start) / 60))

