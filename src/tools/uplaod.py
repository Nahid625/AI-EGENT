import cloudinary.uploader
from fastapi import UploadFile, File, HTTPException

def upload_to_cloudinary(file: UploadFile = File(...)):
    try:
        # Uploading the file stream directly
        result = cloudinary.uploader.upload(file.file)
        return result.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary error: {str(e)}")