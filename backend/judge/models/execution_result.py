from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    status: str
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float = Field(ge=0)
    memory_used: int = Field(ge=0)