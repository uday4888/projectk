from fastapi import APIRouter, HTTPException
from database import engine
from sqlalchemy import text
from schemas import ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def get_items():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM items"))
        return [dict(row._mapping) for row in result]


@router.post("/")
def create_item(item: ItemCreate):
    query = text("""
        INSERT INTO items (name, description, price)
        VALUES (:name, :description, :price)
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {
            "name": item.name,
            "description": item.description,
            "price": item.price
        })

        item_id = result.lastrowid

    return {
        "message": "Item created successfully",
        "id": item_id
    }


@router.put("/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    query = text("""
        UPDATE items
        SET name = :name,
            description = :description,
            price = :price
        WHERE id = :item_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "item_id": item_id
        })

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

    return {"message": "Item updated successfully"}


@router.delete("/{item_id}")
def delete_item(item_id: int):
    query = text("""
        DELETE FROM items
        WHERE id = :item_id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"item_id": item_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

    return {"message": "Item deleted successfully"}