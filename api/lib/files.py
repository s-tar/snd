import os
from enum import Enum
from io import BytesIO
from uuid import uuid4

from PIL import Image
from starlette.datastructures import UploadFile

UPLOAD_FOLDER = "uploads"
IMAGE_MIMES = ("image/jpeg", "image/png", "image/gif")


class FILL(Enum):
    COVER = 1
    CONTAINS = 2


def save_file(file, name, upload_folder):
    if not (isinstance(file, UploadFile) and file.filename):
        return

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    remove_by_name(upload_folder, name)
    file.save(os.path.join(upload_folder, name))

    return file


async def save_image(
    file,
    name,
    upload_folder,
    size=None,
    crop=None,
    fill=FILL.CONTAINS,
):
    if not (isinstance(file, UploadFile) and file.filename):
        return

    if file.content_type not in IMAGE_MIMES:
        return

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    await file.seek(0)
    image = Image.open(BytesIO(await file.read()))
    extension = image.format.lower()
    if crop:
        image = image.crop(crop)

    if size:
        ratio_x = size[0] / image.size[0]
        ratio_y = size[1] / image.size[1]
        if fill == FILL.CONTAINS:
            ratio = min(ratio_x, ratio_y)
        else:
            ratio = max(ratio_x, ratio_y)

        width = round(image.size[0] * ratio)
        height = round(image.size[1] * ratio)
        image = image.resize((width, height), resample=Image.LANCZOS)
        if fill == FILL.COVER:
            left = round((width - size[0]) / 2)
            top = round((height - size[1]) / 2)
            image = image.crop((left, top, left + size[0], top + size[0]))

    filename = f"{name}.{extension}"
    if file.content_type == "image/jpeg":
        image.save(
            os.path.join(upload_folder, filename),
            optimize=True,
            quality=90,
        )
    else:
        image.save(os.path.join(upload_folder, filename))

    return filename


def remove_by_name(path, name, exclude=''):
    if not name:
        return
    name = name + "."
    if not os.path.exists(path):
        return

    for file in os.listdir(path):
        if os.path.isdir(file):
            continue

        if file.startswith(name) and not file.startswith(exclude):
            os.remove(os.path.join(path, file))

