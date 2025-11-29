import pydantic


class BaseSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True, extra="ignore")


class BaseReponse(BaseSchema): ...
