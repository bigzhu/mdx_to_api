import jwt
import os
from fastapi import HTTPException


def checkAuthorization(authorization):
    secretKey = os.getenv("SECRET_KEY")
    if secretKey is None:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Must set SECRET_KEY",
                "data": None,
                "error": "SECRET_KEY is None",
            },
        )
    token = ""
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
            },
        )
    else:
        token = authorization.split(" ")[1]
        if not token:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized",
                },
            )
    try:
        # data = jwt.decode(token, secret_key, algorithms=["HS256"])
        jwt.decode(token, secretKey, algorithms=["HS256"])
        # get user info from here
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail={"message": "Something went wrong", "data": None, "error": str(e)},
        )
