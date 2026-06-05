import os

from config import settings


def save_image(filename: str, data: bytes):
    os.makedirs(settings.images_dir, exist_ok=True)
    with open(os.path.join(settings.images_dir, filename), "wb") as f:
        f.write(data)


def is_image_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(settings.images_dir, filename))


def del_image(filename: str) -> bool:
    try:
        os.remove(os.path.join(settings.images_dir, filename))
        return True
    except FileNotFoundError:
        return False
