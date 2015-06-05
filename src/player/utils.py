#!/usr/bin/env python
# coding=utf-8

import os
import imp

def load_player_from_file(file_path):
    """
    Loads a player module and returns Player class instance that it implements
    """
    class_inst = None
    expected_class = 'Player'

    mod_name, file_ext = os.path.splitext(os.path.split(file_path)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, file_path)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, file_path)

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst