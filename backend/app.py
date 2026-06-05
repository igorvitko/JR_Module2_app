import cgi
import uuid
import os
import math
from http.server import HTTPServer
from logger import logger

from database import ImageRepository
from handlers import BaseHandler
from config import settings
from utils import (
    get_query_params,
    validate_extension,
    validate_size,
    save_image,
    is_image_exists,
    del_image
)


class ImageAPIServer(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.repo = ImageRepository()
        super().__init__(*args, **kwargs)

    def get_images(self):
        params = get_query_params(self.path)

        page = int(params.get('page')) if params.get(
            'page').isdigit() else 1
        limit = int(params.get('limit')) if params.get(
            'limit').isdigit() else 10
        order = params.get('order', 'desc')

        images = self.repo.list(
            page=page, limit=limit, order=order
        )

        total_items = self.repo.count()
        total_pages = math.ceil(total_items/limit) if total_items > 0 else 1

        response_data = {
            "items": images,
            "pagination": {
                "total": total_items,
                "pages": total_pages,
                # "page": page,
                # "limit": limit
            }
        }

        self._send_json(200, response_data)

    def get_image(self):
        filename = self.path.split("/")[-1]
        logger.info(f"Get filename: {filename}")

        image = self.repo.get_by_filename(filename)

        if image is None:
            self._send_error(404, "Not found")

        self._send_json(200, image)

    def create_image(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_error(400, "Expected multipart/form-data")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"},
        )

        if "file" not in form:
            self._send_error(400, "No file provided")
            return

        file_item = form["file"]
        if not file_item.filename:
            self._send_error(400, "No file provided")
            return

        original_name: str = file_item.filename
        data: bytes = file_item.file.read()

        if not validate_extension(original_name):
            self._send_error(
                400, f"Invalid file type. Allowed: {settings.allowed_files_types}")
            return

        if not validate_size(len(data)):
            self._send_error(
                413, f"File too large. MAx: {settings.max_file_size_mb} MB")
            return

        ext = original_name.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"

        try:
            save_image(filename, data)

            image_id = self.repo.create(
                file_name=filename,
                original_name=original_name,
                size=len(data),
                file_type=ext
            )
        except Exception as e:
            logger.error("Error creating or saving image", e)
            delete_image(filename)

        self._send_json(201, {
            "id": image_id,
            "file_name": filename,
            "url": f"{settings.images_dir}/{filename}"
        }
        )

    def delete_image(self):
        filename = self.path.split("/")[-1]
        logger.info(f"File name: {filename}")
        # delete from db
        deleted = self.repo.delete_by_filename(filename)
        if not deleted:
            self._send_error(404, "Image not found")
            return

        # delete from filesystem
        if not del_image(filename):
            self._send_error(404, "Image not found")
            return

        self._send_json(204, {})

    def do_GET(self):
        logger.info(f"Received GET request for path: {self.path}")

        if '/images' in self.path and '&' in self.path:
            self.get_images()
        else:
            self.get_image()

    def do_POST(self):
        if '/upload' in self.path:
            self.create_image()

    def do_DELETE(self):
        logger.info(f"Received DELETE request for {self.path}")

        if '/images/' in self.path:
            self.delete_image()


def run(server_class=HTTPServer, handler_class=ImageAPIServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
