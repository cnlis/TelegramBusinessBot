import asyncio

from app.settings import redis_conn, secrets


async def check_user_delay(user_id):
    last_message_time = redis_conn.get(f"users:{user_id}")
    if last_message_time:
        time_since_last_message = (asyncio.get_event_loop().time() -
                                   float(last_message_time))
        if time_since_last_message < secrets.delay * 60:
            return False
    return True
