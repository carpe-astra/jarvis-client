"""
Module for working with Jarvis modules
"""

import importlib
import inspect
from pathlib import Path
from types import ModuleType
from typing import Callable, List

from app import config
from app.core._logging import logger
from app.models.modules import FunctionDefinition, ModuleDefinition

# Globals
# ================================================================
MODULES_PATH = f"{config.APP_DIR_NAME}.{config.MODULES_DIR_NAME}"
INVALID_PREFIXES = ("_", "__")
_callable_map = {}
module_definitions = []


# Exception Classes
# ================================================================
class InvalidModuleError(Exception):
    pass


class InvalidFunctionError(Exception):
    pass


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
def get_function_callable(module_name: str, function_name: str) -> Callable:
    module_map = _callable_map.get(module_name, None)
    if module_map is None:
        raise InvalidModuleError

    callable = module_map.get(function_name, None)
    if callable is None:
        raise InvalidFunctionError

    return callable


def import_module(module_filepath: Path) -> ModuleType:
    module_name = module_filepath.stem

    if module_filepath.parent != config.MODULES_DIR:
        package_name = f"{MODULES_PATH}.{module_filepath.parent.stem}"
        absolute_path = f"{package_name}.{module_name}"
    else:
        absolute_path = f"{MODULES_PATH}.{module_name}"

    module = importlib.import_module(absolute_path)
    return module


def get_function_definition(func: Callable) -> FunctionDefinition:
    function_definition = None
    if not is_valid_function(func):
        return function_definition

    function_definition = FunctionDefinition(
        name=func.__name__,
        description=func.__doc__,
        signature=str(inspect.signature(func)),
    )

    return function_definition


def get_module_definition(module: ModuleType) -> ModuleDefinition:
    global _callable_map

    module_name = module.__name__.removeprefix(f"{MODULES_PATH}.")
    funcs = inspect.getmembers(module, inspect.isfunction)
    _callable_map[module_name] = {}

    function_definitions = []
    for _, func in funcs:
        function_definition = get_function_definition(func)

        if function_definition:
            _callable_map[module_name][func.__name__] = func
            function_definitions.append(function_definition)

    if function_definitions:
        module_definition = ModuleDefinition(
            module=module_name, functions=function_definitions
        )

    return module_definition


def register_modules(module_definitions: List[ModuleDefinition] = []):
    logger.info("Registering modules")

    module_filepaths = sorted(config.MODULES_DIR.rglob("*.py"))
    for module_filepath in module_filepaths:
        if not is_valid_module(module_filepath):
            continue

        module = import_module(module_filepath)
        module_definition = get_module_definition(module)

        if module_definition:
            module_definitions.append(module_definition)


# Execute on import
# ================================================================
register_modules(module_definitions)
