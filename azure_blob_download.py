import pandas as pd
import numpy as np
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
import logging
       
class AzureBlobFileDownloader:
    
    def __init__(self):
        print("Intializing AzureBlobFileDownloader")
        self.logger = logging.getLogger("dextract")
        try:        
            # Initialize the connection to Azure storage account
            self.blob_service_client =  BlobServiceClient(account_url="",
                                                credential="SmgKZVarvcUgsK9pT...r3qQ==")
            self.container_name = self.blob_service_client.get_container_client("win-blob-di")
        #self.download_all_blobs_in_container()
            self.logger.info(f"Connection to Azure Blob was successful")
        except Exception as err:
            self.logger.error(f"Failed to connect to Azure Blob: {err}")
 
 
    def save_blob(self,file_name,file_content):
        # Get full path to the file
        download_file_path = os.path.join("C:/Azure_Blob_Data", file_name)
    
        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
    
        with open(download_file_path, "wb") as file:
            file.write(file_content)
 
    def download_all_blobs_in_container(self):
        try:
            blob_list = self.container_name.list_blobs(name_starts_with="Input")
            for blob in blob_list:
                # print(blob.name)
                bytes = self.container_name.get_blob_client(blob).download_blob().readall()
                self.save_blob(blob.name, bytes)
                self.logger.info(f"Downloaded all the blobs from azure storage")
        except Exception as err:
            self.logger.error(f"Downloaded all the blobs from azure storage failed: {err}")

    def delete_blob_from_storage(self,file):
        # blob_list = self.container_name.list_blobs(name_starts_with="Input")        
        # for blob in blob_list:
        #     print(blob.name)
        #     self.container_name.delete_blob(blob.name)
        blob=f"Input/{file}"
        #print(blob)
        self.container_name.delete_blob(blob)

 

if __name__ == "__main__":
    
    azure_blob_file_downloader = AzureBlobFileDownloader()
    azure_blob_file_downloader.download_all_blobs_in_container()
    print('done')
    

    
    