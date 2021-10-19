"""
Module for working with Jarvis modules
"""

import importlib
import inspect
from pathlib import Path
from typing import Callable

from app import config
from app.core._logging import logger

# Globals
# ================================================================
MODULES_PATH = f"{config.APP_DIR_NAME}.{config.MODULES_DIR_NAME}"
INVALID_PREFIXES = ("_", "__")
_func_map = {}


# Helper Functions
# ================================================================
def is_valid_module(module_filepath: Path):
    if module_filepath.name.startswith(INVALID_PREFIXES):
        return False
    return True


def is_valid_function(func: Callable):
    logger.debug(func)
    if func.__name__.startswith(INVALID_PREFIXES):
        return False
    return True


# Public Functions
# ================================================================
def get_function_callable(function_name: str) -> Callable:
    return _func_map[function_name]


def register_functions():
    logger.info("Registering functions")
    global _func_map

    for module_filepath in config.MODULES_DIR.rglob("*.py"):
        if not is_valid_module(module_filepath):
            continue

        module_name = module_filepath.stem
        if module_filepath.parent != config.MODULES_DIR:
            package_name = f"{MODULES_PATH}.{module_filepath.parent.stem}"
            absolute_path = f"{package_name}.{module_name}"
        else:
            absolute_path = f"{MODULES_PATH}.{module_name}"

        module = importlib.import_module(absolute_path)
        module_name = module.__name__.removeprefix(f"{MODULES_PATH}.")

        funcs = inspect.getmembers(module, inspect.isfunction)
        for name, func in funcs:
            if not is_valid_function(func):
                continue
            _func_map[f"{module_name}.{func.__name__}"] = func


# Execute on import
# ================================================================
register_functions()
