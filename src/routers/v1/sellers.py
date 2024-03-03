from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations.database import get_async_session
from src.models.sellers import Seller

from src.schemas.sellers import SellerCreate, Seller as SellerSchema
from src.schemas.sellers import SellerDetail
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

sellers_router = APIRouter(tags=["sellers"])

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@sellers_router.post("/", response_model=SellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: SellerCreate, session: DBSession):
    new_seller = Seller(**seller.dict())
    session.add(new_seller)
    await session.flush()
    return new_seller

@sellers_router.get("/", response_model=list[SellerSchema])
async def get_all_sellers(session: DBSession):
    query = select(Seller)
    result = await session.execute(query)
    sellers = result.scalars().all()
    return sellers




# В вашем обработчике get_seller
@sellers_router.get("/{seller_id}", response_model=SellerDetail)
async def get_seller(seller_id: int, session: DBSession):
    result = await session.execute(
        select(Seller).options(selectinload(Seller.books)).where(Seller.id == seller_id)
    )
    seller = result.scalars().first()
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller



@sellers_router.put("/{seller_id}", response_model=SellerSchema)
async def update_seller(seller_id: int, seller: SellerCreate, session: DBSession):
    async with session.begin():
        existing_seller = await session.get(Seller, seller_id)
        if not existing_seller:
            raise HTTPException(status_code=404, detail="Seller not found")
        for var, value in vars(seller).items():
            setattr(existing_seller, var, value) if value else None
        await session.flush()
    return existing_seller

@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    async with session.begin():
        seller = await session.get(Seller, seller_id)
        if not seller:
            raise HTTPException(status_code=404, detail="Seller not found")
        await session.delete(seller)
