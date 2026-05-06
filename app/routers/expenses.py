from fastapi import APIRouter, status, HTTPException
from typing import Optional, List
from datetime import datetime

from .. import schemas
from ..database import conn, cursor
from ..month_dict import monthdict, reverse_monthdict
 



router = APIRouter(
    prefix="/expenses",
    tags=['Posts']
)


#POST/expenses
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
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



#PATCH/expenses/{id}
@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update(id: int, data: schemas.UserUpdate):

    cursor.execute("""SELECT * FROM expense WHERE id = %s""", (id,))
    entity = cursor.fetchone()

    if not entity:
        raise HTTPException(status_code=404, detail="Id not found")
    
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    if "quantity" in update_data and update_data["quantity"] <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")

    if "price" in update_data and update_data["price"] <= 0:
        raise HTTPException(status_code=400, detail="Price must be > 0")
    

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



#DELETE /expenses/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update(id: int):

    cursor.execute("""SELECT * FROM expense 
                   WHERE id = %s""", (id,))
    entity = cursor.fetchone()

    if not entity:
        raise HTTPException(status_code=404, detail="Id does not exist")


    cursor.execute("""DELETE  FROM expense 
                   WHERE id = %s RETURNING *""", (id,))
    deleted_entity = cursor.fetchone()
    conn.commit()



#GET /expenses  (Without Filter) 
#GET /expenses?month=january  (With filter) 
@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def get_expenses( month: Optional[str] = "" ):
    #print(month)
    try:
        if month == "":
            cursor.execute("""SELECT * FROM expense""")
        else:
            int_month = monthdict[month]
            cursor.execute("""SELECT * FROM expense 
                           WHERE EXTRACT(MONTH FROM created_at) = %s""", (int_month,))
        
        data = cursor.fetchall()

    except:
            raise HTTPException(status_code=400, detail="Data not found")

    return data



#GET /expenses/summary?year=2024
@router.get("/summary", status_code=status.HTTP_200_OK)#,response_model=schemas.SummaryResponse)
def get_expenses(year: Optional[int] = None):

    if year is None:
        year = datetime.now().year

    if year <= 0:
        raise HTTPException(status_code=400, detail="Year must be a positive integer")

    cursor.execute("""
        SELECT * FROM expense
        WHERE EXTRACT(year from created_at) = %s
    """, (year,))

    rows = cursor.fetchall()
    print(rows)
    

    monthly_totals = {}

    for month in range(1,13):
        monthly_totals[month] = 0

    yearly_total = 0
    
    for row in rows:
        month = row["created_at"].month
        total = row['quantity'] * row['price']
        monthly_totals[month] += total

        yearly_total += total

    monthly_data = []

    current_year = datetime.now().year
    current_month = datetime.now().month

    for month, total in sorted(monthly_totals.items()):
        if year <= current_year:
            monthly_data.append({"month": reverse_monthdict[month],
                                "monthly_expenditure": monthly_totals[month]})
        else:
            return "Future years are invalid"


        
    return {"year": year,
            "yearly_expenditure": yearly_total,
            "monthly_summary": monthly_data}











# #GET /expenses/summary?year=2024
# @router.get("/summary", status_code=status.HTTP_200_OK, response_model=schemas.SummaryResponse)
# def get_expenses(year: Optional[int] = None):

#     if year is None:
#         year = datetime.now().year

#     if year <= 0:
#         raise HTTPException(status_code=400, detail="Year must be a positive integer")

#     cursor.execute("""
#         SELECT 
#             EXTRACT(MONTH FROM created_at) AS month,
#             COALESCE(SUM(quantity * price), 0) AS total
#         FROM expense
#         WHERE EXTRACT(YEAR FROM created_at) = %s
#         GROUP BY ROLLUP(month)
#         ORDER BY month;
#     """, (year,))

#     rows = cursor.fetchall()
#     print(rows)

#     monthly_data = []
#     yearly_total = 0

#     for row in rows:
#         if row["month"] is None:
#             yearly_total = row["total"]
#         else:
#             monthly_data.append({
#                 "month": reverse_monthdict[int(row["month"])],
#                 "total": row["total"]
#             })

#     return {
#         "year": year,
#         "monthly": monthly_data,
#         "yearly_total": yearly_total 
#     }


#GET /expenses/summary?year=2024
# @router.get("/summary", status_code=status.HTTP_200_OK)
# def get_expenses(year: Optional[int] = None):

#     if year is None:
#         year = datetime.now().year

#     if year <= 0:
#         raise HTTPException(status_code=400, detail="Year must be a positive integer")

#     cursor.execute("""
#         SELECT * FROM expense
#         WHERE EXTRACT(year from created_at) = %s
#     """, (year,))

#     rows = cursor.fetchall()
#     print(rows)
    

#     monthly_data = []
#     yearly_total = 0
#     annual_summary = []

#     for row in rows:
#         if row["created_at"]:
#             date = row["created_at"]
#             monthly_total = row['quantity'] * row['price']
#             monthly_data.append({'month': reverse_monthdict[int(date.month)],
#                                 'monthly_total': monthly_total})
#             yearly_total += monthly_total
#     if not monthly_data:
#         annual_summary.append({"yearly_total" : yearly_total})
#     else:
#         annual_summary.append({"yearly_total": yearly_total, "monthly_summary": monthly_data} )


#     return annual_summary
    

    # for item in monthly_data:
    #     yearly_total = {}
    #     else:
    #         monthly_data.append({
    #             "month": reverse_monthdict[int(row["month"])],
    #             "total": row["total"]
    #         })

    # return {
    #     "year": year,
    #     "monthly": monthly_data,
    #     "yearly_total": yearly_total 
    # }






#GET /expenses/summary?year=2024
# @router.get("/summary",status_code=status.HTTP_200_OK, response_model=schemas.PostOutAnnual)
# def get_expenses( year: Optional[int] = datetime.now().year):

#     cursor.execute("""
#                 SELECT EXTRACT(YEAR FROM created_at)
#                 FROM expense 
#                 WHERE EXTRACT(YEAR FROM created_at) = %s""", (year,))
    
#     data = cursor.fetchall()
#     print(data)

#     if len(data) > 0:
#         if year:
#             cursor.execute("""
#                         SELECT SUM(quantity * price) AS sum_annually 
#                         FROM expense 
#                         WHERE EXTRACT(YEAR FROM created_at) = %s""", (year,))

#         else:
#             cursor.execute(""""
#                         SELECT SUM(quantity * price) AS sum_annually 
#                         FROM expense 
#                         WHERE EXTRACT(YEAR FROM created_at) = %s""", (year,))
    
#         data = cursor.fetchone()
#         data['year'] = year

#     else:
#         if year > 0:
#             data={"year" : year, "sum_annually": 0}
#         else:
#             raise HTTPException(status_code=400, detail="Invalid year must be a postive integer")

#     return data





    