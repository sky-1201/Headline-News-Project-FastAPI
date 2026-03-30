from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# 创建密码上下文对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 这是你的防伪印章密钥，千万不要泄露！（生产环境中应该写在 .env 文件里）
SECRET_KEY = "your_super_secret_key_here_a_very_long_string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7  # 7天过期

#密码加密
def get_hash_password(password:str):
    return pwd_context.hash(password)

#密码验证
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data: dict):
    """生成 JWT Token"""
    to_encode = data.copy()
    # 设置过期时间
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    # 用密钥进行签名，生成手环
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """解析并验证 JWT Token"""
    try:
        # 这一步会自动验证签名是否正确，以及是否过期
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 已过期
    except jwt.InvalidTokenError:
        return None  # Token 被篡改或无效