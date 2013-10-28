from __future__ import absolute_import

import importlib

from .literals import BACKEND_CLASSES


def import_backend(backend):
    parts = BACKEND_CLASSES[backend].split('.')
    module_name = '.'.join(parts[0:-1])
    class_name = parts[-1]
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
