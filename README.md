# Python for AWS Workspace (`python4aws`) 🚀

This is the **python4aws** repository. This workspace is designed to help you learn cloud automation using Python, AWS CLI and the official AWS SDK (`boto3`) inside **WSL (Windows Subsystem for Linux)**.

This repository contains hands-on practice directories, utility scripts, and an isolated configuration workflow designed for completely safe, local cloud development.

---

## 📂 Repository Structure

```text
python4aws/
├── .venv/                   # Isolated Python Virtual Environment (Git-ignored)
├── aws/                     # AWS CLI binary scripts and local configurations
├── .gitignore               # Keeps secrets and system files off GitHub
└── README.md                # This setup guide
```

---

## 🛠️ Step-by-Step Setup Guide

Follow these exact steps to replicate this workspace on any new computer running WSL (Ubuntu).

### Step 1: Open WSL and Clone the Repository
Open your WSL terminal, navigate to your preferred workspace directory, and clone this repository:
```bash
git clone <your-github-repo-url>
cd python4aws
```

### Step 2: Install System Dependencies
Ubuntu requires specific packaging tools to build virtual environments safely. Run this command to update your package engine and install them:
```bash
sudo apt update && sudo apt install python3-pip python3-venv unzip -y
```

### Step 3: Initialize the Virtual Environment
To protect your global operating system from package conflicts, create and activate an isolated virtual workspace inside the project directory:
```bash
# 1. Create the virtual environment folder
python3 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate
```
*(Your terminal prompt will now display `(.venv)` at the beginning, indicating it is safely active).*

### Step 4: Install Boto3
With your virtual environment active, install the AWS SDK using pip:
```bash
pip install boto3
```

---
## AWS CLI v2 Installation (WSL)

Run the following commands to install the latest official AWS CLI v2 inside your WSL terminal:

```bash
# Install unzip dependencies
sudo apt update && sudo apt install -y unzip curl

# Download and run the official installer
curl "https://amazonaws.com" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version

# Clean up installer files
rm -rf awscliv2.zip ./aws
```

## 🔑 AWS Authentication Configuration

To grant your Python scripts access to the AWS cloud, you need to configure your local credentials. Follow these steps to map them cleanly into your environment:

### Step 1: Initialize Your Workspace Keys
Inside your `python4aws` folder, run the configuration tool to store your access keys securely:
```bash
aws configure
```
You will be prompted to provide your **AWS Access Key ID**, **AWS Secret Access Key**, and **Default region name** (e.g., `us-east-1`). 

### Step 2: Verification
The configuration values are securely stored inside your local configuration profile directory. Your `boto3` script will automatically locate and parse these files every time you execute your code.


---

## 🔍 Troubleshooting & Common Errors

### ❌ Error: `bash: .venv/bin/activate: No such file or directory`
* **Why it happens:** The virtual environment was never successfully built because the `python3-venv` package was missing from Ubuntu.
* **The Fix:** Run `sudo apt install python3.12-venv -y`, delete the broken folder using `rm -rf .venv`, and re-run `python3 -m venv .venv`.

### ❌ Error: `externally-managed-environment` (PEP 668)
* **Why it happens:** You tried to run `pip install` globally outside of your virtual workspace, and Ubuntu blocked it to prevent system file corruption.
* **The Fix:** Always make sure you run `source .venv/bin/activate` *before* running any pip commands.

### ❌ Error: `botocore.exceptions.NoCredentialsError: Unable to locate credentials`
* **Why it happens:** Boto3 is running fine, but it has no idea who you are in the AWS cloud.
* **The Fix:** Re-run the commands in the **AWS Authentication Configuration** section above to re-load your access keys.

### ❌ Error: `botocore.errorfactory.AccessDenied: (s3:ListAllMyBuckets) because no identity-based policy allows...`
* **Why it happens:** Your credentials connected to AWS successfully, but your IAM user account does not have permission to read S3.
* **The Fix:** Go to the **AWS Web Console** -> **IAM** -> **Users** -> Select your user -> click **Add Permissions** -> attach the **`AmazonS3ReadOnlyAccess`** managed policy directly.

---

## 🧪 Verification & Testing Script

To verify that your installation, virtual environment, and AWS credentials are all working in harmony, create a test file named `test_aws.py` and add the following code:

```python
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def test_s3_connection():
    print("🔄 Connecting to AWS S3 using Boto3...")
    try:
        # Initialize the high-level S3 resource
        s3 = boto3.resource('s3')

        print("📁 Fetching your S3 Buckets:\n")
        buckets = list(s3.buckets.all())

        if not buckets:
            print("✅ Success! Connected to AWS, but no buckets found in this account.")
            return

        for bucket in buckets:
            print(f"  🔹 [Bucket] {bucket.name}")

        print("\n🎉 Verification Complete: Your workspace is fully functional!")

    except NoCredentialsError:
        print("\n❌ Error: Unable to locate credentials.")
        print("💡 Fix: Run the authentication steps in the README to set your keys.")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == "AccessDenied":
            print("\n❌ Error: Access Denied.")
            print("💡 Fix: Check the IAM section in the README. Your user needs 'AmazonS3ReadOnlyAccess'.")
        else:
            print(f"\n❌ AWS Client Error: {e}")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_s3_connection()
```

### How to Run the Test:
1. Ensure your environment is active: `source .venv/bin/activate`
2. Ensure your keys are loaded using as per the AWS Authentication Configuration.
3. Run the script:
   ```bash
   python3 test_aws.py
   ```
