from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_management_system.db.database import get_db
from inventory_management_system.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from inventory_management_system.services.product_service import (
    create_product,
    delete_product,
    get_product_by_id,
    get_products,
    update_product,
)

router = APIRouter(prefix="/products", tags=["Products"])


# Obtener todos los productos con filtros y paginación (ASYNC)
@router.get("/", response_model=List[ProductResponse])
async def read_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    stock: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await get_products(db, category, min_price, max_price, stock, skip, limit)


# Obtener detalle de un producto (ASYNC)
@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: str, db: AsyncSession = Depends(get_db)):
    return await get_product_by_id(db, product_id)


# Crear un nuevo producto (ASYNC)
@router.post("/", response_model=ProductResponse, status_code=201)
async def create_new_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)


# Actualizar un producto existente (ASYNC)
@router.put("/{product_id}", response_model=ProductResponse)
async def update_existing_product(product_id: str, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await update_product(db, product_id, product_data)


# Eliminar un producto (ASYNC)
@router.delete("/{product_id}")
async def delete_existing_product(product_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_product(db, product_id)
