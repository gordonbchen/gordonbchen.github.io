"""Serve the blog locally and rebuild on source changes. No extra dependencies."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parent.parent
IGNORED = {'_site', '__pycache__', 'node_modules', 'vendor'}


def snapshot():
    files = {}
    for directory, folders, names in os.walk(ROOT):
        folders[:] = [name for name in folders if not name.startswith('.') and name not in IGNORED]
        for name in names:
            path = Path(directory) / name
            if name.startswith('.'):
                continue
            try:
                stat = path.stat()
                files[path.relative_to(ROOT)] = (stat.st_mtime_ns, stat.st_size)
            except FileNotFoundError:
                pass  # An editor may replace a file while it is being scanned.
    return files


def rebuild():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/build.py')], cwd=ROOT)
    if result.returncode:
        print('Build failed. Fix the source and save again to retry.', flush=True)
    return result.returncode == 0


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def watch(stop, previous):
    while not stop.wait(0.5):
        current = snapshot()
        if current != previous:
            previous = current
            print('Source changed; rebuilding…', flush=True)
            rebuild()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    handler = partial(Handler, directory=str(ROOT / '_site'))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError as error:
        parser.exit(1, f'Could not start preview: {error}. Try --port {args.port + 1}.\n')
    previous = snapshot()
    if not rebuild():
        server.server_close()
        return 1
    stop = threading.Event()
    watcher = threading.Thread(target=watch, args=(stop, previous), daemon=True)
    watcher.start()
    print(f'Preview: http://localhost:{args.port}\nWatching source files. Refresh your browser after edits. Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping preview.', flush=True)
    finally:
        stop.set()
        watcher.join()
        server.server_close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
