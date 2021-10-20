"""API endpoints for modules"""

from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from app import modules_util
from app.core._logging import logger
from app.models.modules import ModuleDefinition

router = APIRouter()


# Helper Functions
# ================================================================
def get_module_definition(module_name: str):
    try:
        module_definition = next(
            (
                module_definition
                for module_definition in modules_util.module_definitions
                if module_definition.module == module_name
            )
        )
    except StopIteration:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Module not found."
        )
    return module_definition


# Endpoints
# ================================================================
@router.get("/", response_model=List[ModuleDefinition])
async def get_module_definitions():
    return modules_util.module_definitions


@router.get("/names", response_model=List[str])
async def get_module_names():
    return [
        module_definition.module
        for module_definition in modules_util.module_definitions
    ]


@router.get("/{module_name}", response_model=ModuleDefinition)
async def get_module_definitions(module_name: str):
    return get_module_definition(module_name)
