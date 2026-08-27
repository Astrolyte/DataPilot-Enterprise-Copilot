from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(...,min_length=1,max_length=1000,)
    user_role: str = Field(default="admin")


class QueryResponse(BaseModel):
    route: str
    answer: str | None = None
    sql: str | None = None
    rows: list[dict] | None = None
    sources: list[dict] | None = None