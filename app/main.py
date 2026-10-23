from fastapi import FastAPI

from .database import get_db, engine
from . import models
from routers import auth, posts , users
#default hashing algorithm and what must it use.

# Create all tables defined using SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
class OldMdethod:
    x = 1
    # ============================================================
    # OLD PSYCOPG2 / CURSOR METHODS
    # ============================================================

    # The following methods are NOT required when using SQLAlchemy ORM.
    # They are kept here only for reference.


    # ------------------------------------------------------------
    # CONNECTING TO DATABASE USING PSYCOPG2
    # ------------------------------------------------------------

    # import psycopg2
    # import time
    # from psycopg2.extras import RealDictCursor

    # while True:
    #     try:
    #         conn = psycopg2.connect(
    #             host="localhost",
    #             database="fastapi",
    #             user="postgres",
    #             password="YOUR_PASSWORD",
    #             cursor_factory=RealDictCursor
    #         )

    #         cur = conn.cursor()

    #         print("Successfully connected to database.")
    #         break

    #     except Exception as error:
    #         print("Connecting to database failed.")
    #         print("Error:", error)
    #         time.sleep(2)


    # ------------------------------------------------------------
    # FIND POST USING CURSOR
    # ------------------------------------------------------------

    # def find_post(id: int):

    #     cur.execute(
    #         """
    #         SELECT * FROM posts
    #         WHERE id = %s
    #         """,
    #         (id,)
    #     )

    #     return cur.fetchone()


    # ------------------------------------------------------------
    # CREATE POST USING CURSOR
    # ------------------------------------------------------------

    # cur.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published)
    # )

    # new_post = cur.fetchone()

    # conn.commit()


    # ------------------------------------------------------------
    # UPDATE POST USING CURSOR
    # ------------------------------------------------------------

    # cur.execute(
    #     """
    #     UPDATE posts
    #     SET title=%s,
    #         content=%s,
    #         published=%s
    #     WHERE id=%s
    #     RETURNING *
    #     """,
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         id
    #     )
    # )

    # conn.commit()

    # updated_post = cur.fetchone()


    # ------------------------------------------------------------
    # DELETE POST USING CURSOR
    # ------------------------------------------------------------

    # cur.execute(
    #     """
    #     DELETE FROM posts
    #     WHERE id=%s
    #     RETURNING *
    #     """,
    #     (id,)
    # )

    # deleted_post = cur.fetchone()

    # conn.commit()
