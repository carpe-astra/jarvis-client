from typing import Any, Dict, List, Optional, Union

from pydantic import UUID4, BaseModel


class FunctionDefinition(BaseModel):
    name: str
    description: Optional[str]
    signature: str


class ModuleDefinition(BaseModel):
    module: str
    functions: List[FunctionDefinition]
