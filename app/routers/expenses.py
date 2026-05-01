from fastapi import APIRouter, status, HTTPException

from .. import schemas, models
from ..database import conn, cursor

router = APIRouter()

@router.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def expenses(post: schemas.PostCreate):
    cursor.execute("""INSERT INTO expense (item, quantity, price)
                    VALUES (%s, %s, %s) RETURNING *""",
                    (post.item, post.quantity, post.price))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post