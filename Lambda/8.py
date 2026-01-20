import json
from PIL import Image, UnidentifiedImageError
import boto3
import os
from io import BytesIO
import urllib.parse

s3_client = boto3.client("s3")

UPLOAD_PREFIX = "uploads/"
THUMBNAIL_PREFIX = "thumbnails/"
MAX_SIZE = 1600

def lambda_handler(event, context):

    try:
        record = event["Records"][0]
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        print(f"Bucket: {bucket_name}")
        print(f"Key: {object_key}")

        # Prevent recursive invocation
        if object_key.startswith(THUMBNAIL_PREFIX):
            print("Thumbnail detected, skipping")
            return "Skipped thumbnail"

        # Process only uploads/
        if not object_key.startswith(UPLOAD_PREFIX):
            print("Not an upload object, skipping")
            return "Skipped non-upload"

        # Download image
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=object_key
        )
        image_data = response["Body"].read()

        image = Image.open(BytesIO(image_data))
        original_format = image.format

        print(f"Original format: {original_format}")

        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        ratio = min(
            MAX_SIZE / image.width,
            MAX_SIZE / image.height
        )
        new_size = (
            int(image.width * ratio),
            int(image.height * ratio)
        )

        resized_image = image.resize(
            new_size,
            Image.Resampling.LANCZOS
        )

        buffer = BytesIO()

        if original_format in ("JPEG", "JPG"):
            resized_image.save(
                buffer,
                format="JPEG",
                quality=85,
                optimize=True
            )
            extension = ".jpg"

        elif original_format == "PNG":
            resized_image.save(
                buffer,
                format="PNG",
                optimize=True,
                compress_level=9
            )
            extension = ".png"

        elif original_format == "WEBP":
            resized_image.save(
                buffer,
                format="WEBP",
                quality=85,
                method=6
            )
            extension = ".webp"

        elif original_format == "GIF":
            resized_image.save(
                buffer,
                format="GIF",
                optimize=True
            )
            extension = ".gif"

        else:
            resized_image.save(
                buffer,
                format="JPEG",
                quality=85,
                optimize=True
            )
            extension = ".jpg"

        buffer.seek(0)

        filename = os.path.basename(object_key)
        name_without_ext = os.path.splitext(filename)[0]
        thumbnail_key = f"{THUMBNAIL_PREFIX}{name_without_ext}{extension}"

        print(f"Uploading thumbnail to {thumbnail_key}")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=thumbnail_key,
            Body=buffer,
            ContentType=response["ContentType"]
        )

        print("Thumbnail created successfully")

    except UnidentifiedImageError:
        print(f"Unsupported image format: {object_key}")
        raise

    except MemoryError:
        print(f"Memory error while processing {object_key}")
        raise

    except Exception as e:
        print(f"Error processing {object_key}: {str(e)}")
        raise

    return {
        "statusCode": 200,
        "body": json.dumps("Thumbnail created")
    }
