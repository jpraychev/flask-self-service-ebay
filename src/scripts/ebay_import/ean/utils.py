import typing as t

def load_data(fname:str) -> t.List[str]:
    """ Load data read from a file

    Args:
        fname (str): Name of a txt file

    Returns:
        t.List[str]: List of str items
    """
    # assert fname.endswith('txt')
    with open(fname) as f:
        data = f.read().splitlines()
    return data

def save_data(fname:str, items:t.List[str]) -> None:
    with open(fname, 'w') as f:
        f.writelines([str(item) + '\n' for item in items])