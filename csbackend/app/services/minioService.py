from minio import Minio
from minio.error import S3Error
from io import BytesIO

class MinioService:
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.client = Minio(endpoint, access_key, secret_key, secure=False)
        self.bucket_name = bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(self, file_data, file_name, content_type):
        try:
            file_data = BytesIO(file_data)  # Wrap the bytes object in a BytesIO object
            self.client.put_object(
                self.bucket_name, file_name, file_data, len(file_data.getvalue()), content_type=content_type
            )
            return f"{self.client._base_url}/{self.bucket_name}/{file_name}"
        except S3Error as e:
            print(f"Error occurred: {e}")
            return None