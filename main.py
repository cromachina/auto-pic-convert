import os
import argparse
from PIL import Image
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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

class EventHandler(FileSystemEventHandler):
    def on_closed(self, event):
        process_file(event.src_path)
    def on_moved(self, event):
        print(event)
        process_file(event.dest_path)

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
args = parser.parse_args()
os.chdir(args.path)

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler, '.', recursive=True)
observer.start()
observer.join()
