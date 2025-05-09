import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import numpy as np


def generate_qr_code(text):
    qr = qrcode.make(text)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return buffer
