from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg import sql

from config import settings


class ImageRepository:
    # def __init__(self, db_config):
    #     self.db_config = db_config
    #     # Initialize DB connection here (e.g., using psycopg2 or SQLAlchemy)

    @contextmanager
    def _cursor(self, dict_rows: bool = False):
        with psycopg.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            dbname=settings.db_name
        ) as conn:
            kwargs = {"row_factory": dict_row} if dict_rows else {}
            with conn.cursor(**kwargs) as cur:
                yield cur

    def create(self, file_name: str, original_name: str, size: int, file_type: str) -> int:
        with self._cursor() as cur:
            cur.execute(
                """
                INSERT INTO images (filename, original_name, size, file_type)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (file_name, original_name, size, file_type)
            )
            image_id = cur.fetchone()[0]
            return image_id

    def list(self, page: int = 1, limit: int = 10, order: str = "desc") -> list[dict]:
        with self._cursor(dict_rows=True) as cur:
            offset = (page - 1) * limit
            clean_direction = "DESC" if order.lower() == "desc" else "ASC"

            query = sql.SQL(
                """
                SELECT id, filename, original_name, size, file_type, upload_time
                FROM images
                ORDER BY 1 {dir}
                LIMIT %s OFFSET %s""").format(
                dir=sql.SQL(clean_direction)
            )
            cur.execute(query, (limit, offset))

            return cur.fetchall()

    def get_by_id(self, image_id: int):
        with self._cursor(dict_rows=True) as cur:
            cur.execute(
                """
            SELECT id, filename, original_name, size, file_type, upload_time
            FROM images
            WHERE id = %s
            """,
                (image_id, ),
            )
            return cur.fetchone()

    def get_by_filename(self, image_name: str):
        with self._cursor(dict_rows=True) as cur:
            cur.execute(
                """
            SELECT id, filename, original_name, size, file_type, upload_time
            FROM images
            WHERE filename = %s
            """,
                (image_name, ),
            )
            return cur.fetchone()

    def delete_by_id(self, image_id: int) -> bool:
        with self._cursor() as cur:
            cur.execute(
                """
            DELETE FROM images 
            WHERE id = %s RETURNING id
            """,
                (image_id,),
            )
            return cur.fetchone() is not None

    def delete_by_filename(self, filename: str) -> bool:
        with self._cursor() as cur:
            cur.execute(
                """
            DELETE FROM images
            WHERE filename = %s
            RETURNING id
            """,
                (filename,),
            )
            return cur.fetchone() is not None
