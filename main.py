import os
import argparse
from PIL import Image
from pathlib import Path
from watchfiles import watch, Change

target_types = ['.png']
output_type = '.jpg'
output_dir = 'jpg'
jpeg_quality = 95

def process_file(path):
    path = Path(path)
    try:
        if path.parts[0] != output_dir and path.suffix in target_types:
            target_path = (output_dir / path).with_suffix(output_type)
            os.makedirs(target_path.parent, exist_ok=True)
            Image.open(path).save(target_path, quality=jpeg_quality)
            print(target_path)
    except Exception as e:
        print(e)

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
args = parser.parse_args()
os.chdir(args.path)
cwd = os.getcwd()

print(f'Watching directory: {cwd}')
for changes in watch('.'):
    for type, path in changes:
        if type in [Change.added, Change.modified]:
            path = Path(path).relative_to(cwd)
            process_file(path)
