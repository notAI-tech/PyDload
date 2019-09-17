import requests
import progressbar
import time

mb = 1024 * 1024

def dload(url, save_to_path=None, timeout=10, max_time=30, verbose=True):
    if not save_to_path:
        save_to_path = url.split('/')[-1]
        if verbose:
            print('Saving the file at', save_to_path)

    if max_time:
        if verbose:
            print("The download will be auto-terminated in", max_time, "if not completed.")

    try:
        request = requests.get(url, timeout=timeout, stream=True, verify=True)
    except:
        if verbose:
            print('SSL certificate not verified...')
        request = requests.get(url, timeout=timeout, stream=True, verify=False)

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
