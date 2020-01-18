import uuid

def clean_url(url, verbose):
    url = url.rstrip('/')
    if 'http://' not in url[:7] and 'https://' not in url[:8]:
        if verbose:
            print('Assuming http://')
        url = 'http://' + url
    
    return url

def get_save_to_path(url, save_to_path, verbose):
    if not save_to_path:
        save_to_path = url.split('/')[-1].split('?')[0]
        if not save_to_path.strip():
            save_to_path = url.split('/')[-2]

        if not save_to_path.strip():
            save_to_path = str(uuid.uuid4())
            if verbose:
                print('Saving file as', save_to_path)

        if verbose:
            print('Saving the file at', save_to_path)
    
    return save_to_path