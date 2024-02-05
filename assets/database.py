from datetime import datetime
from .pool import db_pool

class Database:
    def __init__(self):
        pass

    async def insert_helping(self, member, channel_id, date):
        query = "INSERT INTO `tickets` (member, channel_id, date) VALUES (%s, %s, %s)"
        await db_pool.execute_query(query, (member, channel_id, date))

    async def get_from_helping(self, member):
        query = "SELECT member FROM `tickets` WHERE member = %s"
        result = await db_pool.execute_query(query, (member,))
        return result[0][0] if result else None
    
    async def create_all(self):
        query = "CREATE TABLE IF NOT EXISTS `supports` (`member` bigint(50) NOT NULL, `channel_id` bigint(50) NOT NULL, `date` timestamp NOT NULL, PRIMARY KEY (`member`))"
    
    async def get_user_id(self, channel_id):
        query = "SELECT member FROM `tickets` WHERE channel_id = %s"
        result = await db_pool.execute_query(query, (channel_id,))
        return result[0][0] if result else None


    async def get_channel_id(self, member):
        query = "SELECT channel_id FROM `tickets` WHERE member = %s"
        result = await db_pool.execute_query(query, (member,))
        return result[0][0] if result else None

    async def delete_helping(self, member):
        query = "DELETE FROM `tickets` WHERE member = %s"
        await db_pool.execute_query(query, (member,))

#############################################################################################################

    async def add_staff(self, member, add, closes, date):
        query = "INSERT INTO `tickets-staff` (member, `add`, closes, date) VALUES (%s, %s, %s, %s)"
        await db_pool.execute_query(query, (member, add, closes, date))

    async def get_in_staff(self, member):
        query = "SELECT member FROM `tickets-staff` WHERE member = %s"
        result = await db_pool.execute_query(query, (member,))
        return result[0][0] if result else None
    
    async def delete_from_staff(self, member):
        query = "DELETE FROM `tickets-staff` WHERE member = %s"
        await db_pool.execute_query(query, (member,))