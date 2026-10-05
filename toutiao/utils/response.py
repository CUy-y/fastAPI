from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str = "success", data: Any = None) -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({"code": 200, "message": message, "data": data})
    )
