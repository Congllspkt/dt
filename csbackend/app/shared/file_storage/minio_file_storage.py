from io import BytesIO
from minio import Minio, S3Error

from app.shared.file_storage.file_storage import FileStorage
from app.core.config import settings


class MinioFileStorage(FileStorage):

    StorageType = 'MinIO'

    def __init__(self):
        
        self.endpoint = settings.MINIO_ENDPOINT
        access_key = settings.MINIO_ACCESS_KEY
        secret_key = settings.MINIO_SECRET_KEY
        self.bucket_name = settings.MINIO_BUCKET_NAME

        self.client = Minio(self.endpoint, access_key, secret_key, secure=False)

        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def store(self, file_data, file_name, content_type=None):
        try:
            if content_type is None:
                import mimetypes
                content_type = mimetypes.guess_type(file_name) or "application/octet-stream"

            dd = self.client.put_object(
                self.bucket_name,
                file_name,
                data=BytesIO(file_data),
                length=len(file_data),
                content_type=content_type,
            )
            base_url = self.client._base_url.host
            return f"http://{base_url}/{self.bucket_name}/{file_name}"

        except Exception as e:
            print(f"Upload Error: {e}")
            return {"success": False, "error": str(e)}

    def read(self, file_name):
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=file_name,
            )
            file_content = response.read()
            return file_content
        except S3Error as e:
            if e.code == 'NoSuchBucket':
                print(f"Error: Bucket '{self.bucket_name}' does not exist")
            else:
                print(f"MinIO Error: {e}")
            return None

        except Exception as e:
            print(f"Download Error: {e}")
            return None
        
minioFileStorage = MinioFileStorage()