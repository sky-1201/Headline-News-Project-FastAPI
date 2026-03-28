#配置缓存连接
import json
from typing import Any

import redis.asyncio as redis
from fastapi.encoders import jsonable_encoder


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

#创建Redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)

#封装缓存操作方法

# 设置 和 读取（字符串 和 列表或字典）"[{}]"
# 读取：字符串
async def get_cache(key: str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None


# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)  # 序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败：{e}")
        return None


# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        # 核心改造：第一步，把任何复杂对象“降维”成普通字典/列表/基础类型
        # 它会自动帮你处理好麻烦的 datetime 时间格式和 Pydantic 模型
        compatible_data = jsonable_encoder(value)

        # 第二步，把降维后绝对安全的普通数据，转成 JSON 字符串（保留中文）
        json_str = json.dumps(compatible_data, ensure_ascii=False)

        # 第三步，存入 Redis
        await redis_client.setex(key, expire, json_str)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False