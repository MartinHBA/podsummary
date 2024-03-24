from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta


def upload_file_to_blob_and_generate_sas(account_name, account_key, container_name, blob_name, file_path):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net/", credential=account_key)
    
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    print(f"Uploading to Azure Storage as blob: {blob_name}")

    # Upload the created file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    
    # Generate SAS token for the blob
    sas_token = generate_blob_sas(account_name=account_name,
                                  container_name=container_name,
                                  blob_name=blob_name,
                                  account_key=account_key,
                                  permission=BlobSasPermissions(read=True),
                                  expiry=datetime.utcnow() + timedelta(days=3))

    # Construct the URL with the SAS token
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    
    return sas_url


