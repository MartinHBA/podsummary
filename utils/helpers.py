from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Function to read the text file content
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_secret_from_key_vault(vault_url, secret_name):
    """
    Retrieves a secret from Azure Key Vault.

    Parameters:
    - vault_url: The URL of your Azure Key Vault (e.g., "https://yourkeyvaultname.vault.azure.net/")
    - secret_name: The name of the secret you want to retrieve.

    Returns:
    - The value of the secret.
    """
    # Authenticate to Azure Key Vault using the DefaultAzureCredential
    credential = DefaultAzureCredential()
    
    # Create a SecretClient using the vault URL and credential
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    
    # Retrieve the secret value
    retrieved_secret = secret_client.get_secret(secret_name)
    
    return retrieved_secret.value

