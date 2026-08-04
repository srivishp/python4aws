# Import the boto3 library
import boto3

# Instantiate the AWS resource for S3 and name the bucket
s3 = boto3.resource("s3")
bucket_name = "sample-bucket-srivishp"  # Bucket name should be globally unique

# Creating a list that would show us all the buckets we have.
all_buckets = [bucket.name for bucket in s3.buckets.all()]

# Checking if the bucket exists in our account. Bucket is created if it doesn't exist.
if bucket_name not in all_buckets:
    print(f"{bucket_name} bucket does not exist. Creating it now...")
    s3.create_bucket(Bucket=bucket_name)
    print(f"{bucket_name} has been created.")
else:
    print(f"Bucket {bucket_name} already exists.")

# Creating file1 & file2 (Files created locally will be uploaded to the bucket)
file_1 = "file1.txt"
file_2 = "file2.txt"

# Upload the files
s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)

# Reading the file
obj = s3.Object(bucket_name, file_1)
body = obj.get()["Body"].read()
print(body)

# Update file_1 with contents of file_2
s3.Object(bucket_name, file_1).put(Body=open(file_2, "rb"))
obj = s3.Object(bucket_name, file_1)
body = obj.get()["Body"].read()
print(body)

# Delete file first and then the bucket
s3.Object(bucket_name, file_1).delete()
s3.Bucket(bucket_name).delete()
