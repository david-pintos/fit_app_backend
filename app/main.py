from fastapi import FastAPI

from app.security.routes import auth

app = FastAPI()

# Inlcude all API routers with endpoints
app.include_router(auth)
