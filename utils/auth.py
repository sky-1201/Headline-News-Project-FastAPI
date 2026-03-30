from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users


# 整合 根据 Token 查询用户，返回用户
from fastapi import Header, Depends, HTTPException
from starlette import status
from utils import security


async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)  # 如果你确实需要查询完整的 User 对象，可以保留这个
):
    token = authorization.replace("Bearer ", "")

    # 1. 验印章（纯内存 CPU 计算，不查数据库！）
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 无效或已过期")

    user_id = payload.get("sub")

    # 2. 如果你的接口只需要用到 user_id（比如添加收藏），你甚至可以直接 return {"id": user_id}
    # 但为了兼容你之前的代码，我们还是去库里查一下完整的 user 返回
    user = await users.get_user_by_id(db, int(user_id))  # 假设你在 crud/users.py 里写了这个方法
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")

    return user