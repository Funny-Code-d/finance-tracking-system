from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_category
from db.settelites import set_purchase, set_purchase_detail
from db.links import link_group_category
from models.purchase import PurchaseIn, Purchase
from models.category import Category, CategoryIn, CategoryOut, CategoryPost, CategoryItemPost
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime


class CategoryEntity(BaseEntity):


    async def add_category(self, category: CategoryIn):
        values = {
            "name_category" : category.category_name
        }
        query = hub_category.insert().values(**values)
        category_sk = await self.database.execute(query=query)

        values = {
            "category_sk" : category_sk,
            "group_sk" : category.group_sk
        }

        query = link_group_category.insert().values(**values)
        await self.database.execute(query=query)

        return True
    

    async def delete_category(self, category_data: CategoryItemPost):
        query = link_group_category.delete().where(
            link_group_category.c.category_sk==category_data.category_sk
        )
        await self.database.execute(query=query)
                
                

    async def get_all(self, category_data: CategoryPost):
        query = select(
            hub_category.c.category_sk,
            hub_category.c.name_category
        ).join_from(link_group_category, hub_category).where(link_group_category.c.group_sk==category_data.group_sk)

        responce_db = await self.database.fetch_all(query=query)
        result = list()
        for row in responce_db:
            result.append(Category.parse_obj(row))
        print(result)
        
        return CategoryOut(
            customer_sk=category_data.customer_sk,
            group_sk=category_data.group_sk,
            categories=result
        )

    async def get_by_category(self):
        pass

    async def get_by_date_and_category(self):
        pass