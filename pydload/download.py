import requests
import progressbar
import time
import uuid
from .utils import clean_url, get_save_to_path

mb = 1024 * 1024

def dload(url, save_to_path=None, timeout=10, max_time=30, verbose=True):
    '''

    Parameters:

    url (str): URL of the file to be downloaded.

    save_to_path (str): Save as. If not provided, will be saved in the working directory with file_name auto identified from url.

    timeout (int): timeout for the initial handshake for requests.

    max_time (int): Kill the download if it takes more than max_time seconds.

        # Useful when you don't know the size of files before hand and don't want to download very large files.
    
    verbose (bool default:True): self explanatory


    Returns:

    False if downloading failed or stopped based on max_time. file_path if download is successful.

    '''
    
    url = clean_url(url, verbose)

    save_to_path = get_save_to_path(url, save_to_path, verbose)

    if max_time:
        if verbose:
            print("The download will be auto-terminated in", max_time, "if not completed.")

    try:
        request = requests.get(url, timeout=timeout, stream=True, verify=True, allow_redirects=True)
    except:
        if verbose:
            print('SSL certificate not verified...')
        request = requests.get(url, timeout=timeout, stream=True, verify=False, allow_redirects=True)

    file_size = None
    try:
        file_size = (float(request.headers['Content-length'])// mb) + 1
    except:
        if verbose:
            print('Content-length not found, file size cannot be estimated.')
        pass

    is_stopped = False

    with open(save_to_path, 'wb') as f:
        start_time = time.time()
        if verbose:
            for chunk in progressbar.progressbar(request.iter_content(mb), max_value=file_size, prefix='MB'):
                f.write(chunk)
                if max_time:
                    if time.time() - start_time >= max_time:
                        is_stopped = True
                        break
        
        else:
            for chunk in request.iter_content(mb):
                f.write(chunk)
                if max_time:
                    if time.time() - start_time >= max_time:
                        is_stopped = True
                        break
    
    if is_stopped:
        if verbose:
            print('Stopped due to excess time')
        return False
    
    else:
        if verbose:
            print('Succefully Downloaded to:', save_to_path)
        return save_to_path


def cli():
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


if __name__ == '__main__':
    cli()
