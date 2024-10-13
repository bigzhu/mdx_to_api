import jwt
import os
import time
from fastapi import HTTPException


def checkAuthorization(authorization):
    audience = os.getenv("AUDIENCE")
    public_key = os.getenv("PUBLIC_KEY")
    if public_key is None:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Must set PUBLIC_KEY",
                "data": None,
                "error": "PUBLIC_KEY is None",
            },
        )

    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Authentication Token is missing or invalid!",
                "data": None,
                "error": "Unauthorized",
            },
        )

    token = authorization.split(" ")[1]

    try:
        # 解码并验证令牌
        decoded_token = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=audience
        )

        # 可以在这里添加额外的验证逻辑
        # 例如，检查令牌的过期时间
        if "exp" in decoded_token and decoded_token["exp"] < time.time():
            raise jwt.ExpiredSignatureError("Token has expired")

        # 检查发行者（如果需要）
        expected_issuer = os.getenv("EXPECTED_ISSUER")
        if expected_issuer and decoded_token.get("iss") != expected_issuer:
            raise jwt.InvalidIssuerError("Invalid token issuer")

        # 返回解码后的令牌信息
        return decoded_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Token has expired",
                "data": None,
                "error": "Token Expired",
            },
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail={"message": "Invalid token", "data": None, "error": str(e)},
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail={"message": "Something went wrong", "data": None, "error": str(e)},
        )


if __name__ == "__main__":
    checkAuthorization(
        "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJUUlJZVnBBcWFvM21VdlFuMExyMyJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidXNlciJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJ1c2VyIiwieC1oYXN1cmEtdXNlci1pZCI6ImJiYTUyNDBjLTdkMWMtNDIxMS05ZjViLWRlZjFlNTRjNDIzMiJ9LCJpc3MiOiJodHRwczovL2Rldi1zZTJsaWQ4YXhjbTJrN3prLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnaXRodWJ8NDg5ODE1IiwiYXVkIjpbImh0dHBzOi8vYXBpLmVudHViZS5hcHAvdjEvZ3JhcGhxbCIsImh0dHBzOi8vZGV2LXNlMmxpZDhheGNtMms3emsudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyODc5OTUyNiwiZXhwIjoxNzI4ODg1OTI2LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwiYXpwIjoiQWlHTTAzWm5Lb25yT2t1d1AzMnZDOHkxcHY0YTQ0UkMifQ.mYJatMeNZIwNqsSk3ZxNDolP5Yu0dMoY2CVtnZ3ir66jh33_6fCpK6Pzhs9WefKnVUYESaUvCfNSOi6_fAFQAcl70nxBLT4nYQR60Rg7PESenqc97Cd8uDuawg1sC58M169s4_7MK0EzvbFkkbnEnqPcv6m_2l6vC2TQ6zEHgyvhndpu_jNxDT8jeqHwh5viKuPZ6o1IMJv4YpQKz5y6QP-FLkbnNFoL0DkyhAgwMb19sNRl7r_xCdSFTJRzn_nDRZKrsTuwPEiotqmBgPbXiAXy2nSAr5cIoA_U-Ai5GzvNjDpBQGPsIB4QxKZ5QIfJrAzLf713_1HhAyBMYltGfQ"
    )
