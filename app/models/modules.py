from typing import Any, Dict, List, Union

from pydantic import UUID4, BaseModel


class ModuleDefinition(BaseModel):
    module: str
    functions: List[str]
