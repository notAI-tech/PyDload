from .download import dload

import argparse

parser = argparse.ArgumentParser(description='CLI for pydload')

parser.add_argument('url', type=str, help='URL of the file to be downloaded.')

parser.add_argument('save_to_path', type=str, nargs='?', help='save as file path/name')

parser.add_argument('--max_time', type=int, help='Maximum time to be spent on download')
parser.add_argument('--timeout', type=int, help='Reuest timeout')

args = parser.parse_args()

url = args.url
save_to_path = args.save_to_path
max_time = args.max_time
timeout = args.timeout
if not timeout: timeout=10

dload(url, save_to_path=save_to_path, timeout=timeout, max_time=max_time, verbose=True)
