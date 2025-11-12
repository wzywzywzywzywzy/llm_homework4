from passlib.context import CryptContext
from passlib.exc import MissingBackendError

# 初始化密码上下文，添加错误处理
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except MissingBackendError:
    # 如果bcrypt不可用，使用默认的方案
    pwd_context = CryptContext(schemes=["django_pbkdf2_sha256"], deprecated="auto")
    print("警告: bcrypt不可用，使用默认密码哈希方案")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    try:
        return pwd_context.hash(password)
    except MissingBackendError:
        # 如果首选方案不可用，使用任何可用的方案
        return pwd_context.hash(password, scheme=None)