import cloudinary
import cloudinary.uploader
from ...app.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

def upload_image_fileobj(fileobj, public_id=None):
    # fileobj: file-like object (BytesIO or starlette UploadFile.file)
    response = cloudinary.uploader.upload(fileobj, public_id=public_id, overwrite=False)
    return response.get("secure_url")
