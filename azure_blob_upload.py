import pandas as pd
import numpy as np
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
import logging

class AzureBlobFileUploader:
    def __init__(self):
        # print("Intializing AzureBlobFileUploader")
        #self.doc_folder=doc_folder
        self.logger = logging.getLogger("dextract")
    
        # Initialize the connection to Azure storage account
        self.blob_service_client =  BlobServiceClient(account_url="",
                                            credential="SmgKZVarv......+AStoCr3qQ==")
        # self.container_name = self.blob_service_client.get_container_client("test-file-sync")
        #self.upload_files_from_folder(doc_folder)

    def upload_files_from_folder(self,doc_folder):
    # Get all files with jpg extension and exclude directories
        for file in os.listdir(doc_folder):
            self.upload_file(file)           
 
    def upload_file(self,filename):
    # Create blob with same name as local file name
        #upload_file_path = os.path.abspath(__filename__)
        try:
            blob_client = self.blob_service_client.get_blob_client(container="win-blob-di",
                                                                blob=f"Output/{filename}")
        
            #print(f"uploading file - {file_name}")
            with open(filename, "rb") as data:
                blob_client.upload_blob(data,overwrite=True)
        except Exception as err:
            self.logger.error(f"Failed to upload files to blob storage: {err}")
 
if __name__ == "__main__":
    # Initialize class and upload files
    doc_folder="C:\Blob_Data\Input"
    azure_blob_file_uploader = AzureBlobFileUploader()
    azure_blob_file_uploader.upload_files_from_folder(doc_folder)
    print("done")