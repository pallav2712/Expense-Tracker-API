from fastapi import APIRouter, status, HTTPException

from .. import schemas
from ..database import conn, cursor



router = APIRouter()



@router.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def expenses(post: schemas.PostCreate):

    if post.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    if post.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
    
    cursor.execute("""INSERT INTO expense (item, quantity, price)
                    VALUES (%s, %s, %s) RETURNING *""",
                    (post.item, post.quantity, post.price))
    
    new_post = cursor.fetchone()
    conn.commit()
    return new_post




@router.patch("/expenses/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update(id: int, data: schemas.UserUpdate):

    cursor.execute("SELECT * FROM expense WHERE id = %s", (id,))
    entity = cursor.fetchone()

    if not entity:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")
    
    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(id)

    query = f"""
        UPDATE expense
        SET {set_clause}
        WHERE id = %s
        RETURNING *
    """

    cursor.execute(query, values)
    updated_user = cursor.fetchone()
    conn.commit()

    return updated_user