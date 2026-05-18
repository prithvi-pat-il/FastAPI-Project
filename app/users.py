import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import(
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import user, get_user_db

SECRET = "Prithvi"

class UserManager(UUIDIDMixin, BaseUserManager[user,uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: user, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: user, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: user, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has requested verification. Verification token: {token}")

def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[user, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)   
