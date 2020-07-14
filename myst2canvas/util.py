import json

hush = False

def sprint(str):
    """
    Print if not hushed.

    Parameters
    ----------
    str: str
        string to print

    Returns
    -------
    None
    """
    if not hush:
        print(str)

def pprint(obj):
    """
    Print JSON object in an easy to read format.

    Parameters
    ----------
    obj: obj
        object to print

    Returns
    -------
    None
    """
    try:
        sprint(json.dumps(obj, indent=4))
    except TypeError:
        sprint("WARNING: JSON not serializable, can't pretty print.")
        sprint(obj)