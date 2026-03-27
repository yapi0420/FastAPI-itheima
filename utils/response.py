from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(data=None, message: str ="操作成功"):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(jsonable_encoder(content))