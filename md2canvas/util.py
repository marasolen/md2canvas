import json
import jupytext as jp
from jupytext.cli import jupytext

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

def strip_cells(nb_in, nb_out, the_string):
    """
    Remove all cells with metadata['ctype']==the_string from
    cell list.

    Parameters
    ----------
    nb_in: str
        the path of the notebook to strip cells from

    nb_out: str
        the path of the notebook to write to

    the_string: str
        the cell type to strip

    Returns
    -------
    obj
        a new notebook object with cells stripped
    """
    nb_obj = jp.readf(nb_in)
    new_list = []
    for the_cell in nb_obj['cells']:
        if 'ctype' in the_cell['metadata']:
            if the_cell['metadata']['ctype']==the_string:
                continue
        new_list.append(the_cell)
    nb_obj['cells'] = new_list
    jp.writef(nb_obj, str(nb_out))
    return nb_obj