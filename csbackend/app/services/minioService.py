from minio import Minio
from minio.error import S3Error
from io import BytesIO
import os
from dotenv import load_dotenv
import secrets



# Load environment variables
load_dotenv()
new_key = secrets.token_bytes(32)
MINIO_SSE_KEY = new_key.hex()
retrieved_key = bytes.fromhex(MINIO_SSE_KEY)


class MinioService:
    def __init__(self):
        # Fetch environment variables
        self.endpoint = os.getenv("MINIO_ENDPOINT")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")

        # Initialize Minio client
        self.client = Minio(self.endpoint, access_key, secret_key, secure=False)

        # Ensure the bucket exists
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file_data, file_name, content_type=None):
        try:
            # Automatic content type detection (if not provided)
            if content_type is None:
                import mimetypes
                content_type = mimetypes.guess_type(file_name) or "application/octet-stream"

            # Use put_object with BytesIO for better memory management
            dd = self.client.put_object(
                self.bucket_name,
                file_name,
                data=BytesIO(file_data),
                length=len(file_data),
                content_type=content_type,
            )
            print(dd.object_name)
            base_url = self.client._base_url.host
            return f"http://{base_url}/{self.bucket_name}/{file_name}"

        except Exception as e:
            print(f"Upload Error: {e}")
            return {"success": False, "error": str(e)}

    def read_file(self, file_name):
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