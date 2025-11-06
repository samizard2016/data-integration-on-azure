import pandas as pd
import numpy as np
from azure.storage.blob import BlobClient
from table_extraction import TableExtraction
from table_headers import TableHeader
from pptx_chart_extraction import ChartExtraction
import os
import aspose.slides as slides
import logging
from azure_blob_download import AzureBlobFileDownloader
from azure_blob_upload import AzureBlobFileUploader

class DataExtraction:
    def __init__(self,doc_folder):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            level=logging.INFO,
            filename="data_integration.log",
        )
        self.logger = logging.getLogger("data_integration")
        #self.pptx_file=pptx_file
        #html_file=self.convert_pptx_to_html(self.pptx_file)
        DataExtraction.set_folders()
        self.doc_folder=doc_folder       
        #self.get_data(html_file)
        # self.get_extracted_data()           
       
    def get_extracted_data(self):        
        cwf = os.getcwd()
        os.chdir(self.doc_folder)
        for file in os.listdir(self.doc_folder):
            if file.endswith('pptx'):                
                try:                
                    html_file = self.convert_pptx_to_html(file)
                except Exception as e:
                    self.logger.error(f"Problem in converting {file} to html:{e} ")                
                self.Upload_files_to_storage(file) 
                self.Upload_files_to_storage(html_file)      
                self.get_data(html_file,file)
                self.logger.info(f"Sucessfully extracted all the data from {file}")
                try:
                    self.delete_inputfiles_from_storage(file)
                except Exception as e:
                    self.logger.info(f"problem in removing file from storage {file}:{e}") 
        self.logger.info(f"extracted all files")       
        os.chdir(cwf)       

    def convert_pptx_to_html(self,pptx_file):
        with slides.Presentation(pptx_file) as presentation:
            try:
                file_name = os.path.basename(pptx_file).split('.')[0]           
                html_file=f"{file_name}_ExtractedHTML.html"
                presentation.save(html_file, slides.export.SaveFormat.HTML)                 
            except Exception as e:
                self.logger.error(f"Problem in reading {file_name} :{e} ")         
            self.logger.info(f'{html_file} file created') 
            return html_file

    def get_data(self,html_file,pptx_file):
        try:
            te=TableExtraction(html_file)                        
        except Exception as err:
            self.logger.error(f"Problem in table data extraction of {html_file} - {err}")        
        try:
            th=TableHeader(html_file)            
        except Exception as err:
            self.logger.error(f"Problem in table headers extraction of {html_file}:{err}")
        try:
            ce=ChartExtraction(pptx_file)            
        except Exception as err:
            self.logger.error(f"Problem in chart data extraction of {pptx_file}:{err}")     
    ##upload files to azure storage    
    def Upload_files_to_storage(self,file_name):
        try:
            azure_blob_file_uploader = AzureBlobFileUploader()
            azure_blob_file_uploader.upload_file(file_name)
            #print(f"Sucessfully uploaded {file_name}")                         
        except Exception as err:
            self.logger.error(f"problem in uploading {file_name} to azure storage:{err}")
        self.logger.info(f"Sucessfully uploaded the {file_name} to azure storage") 
    
    def delete_inputfiles_from_storage(self,file):
        abd=AzureBlobFileDownloader()
        abd.delete_blob_from_storage(file)
        self.logger.info(f"Deleted the input file {file} from the storage")
    @classmethod
    def set_folders(cls):
        azure_blob_file_downloader = AzureBlobFileDownloader()
        azure_blob_file_downloader.download_all_blobs_in_container()   

if __name__ == "__main__":

    # blob1 = BlobClient(account_url="https://winstacktsadev01.blob.core.windows.net",
    #                 container_name="test-file-sync",
    #                 blob_name="SegmentSolution_Collated_SEG-UK_C01 (2).pptx",
    #                 credential="QDFCEKk2Ki0Rhx54S3oPxaPa/WTEib56nCIfk0NIl3tLC7U1KUx0DuaZNiuR6GpDryzc2ej4uNX2cFDypCdfXQ==")
    
    # with open("SegmentSolution_Collated_SEG-UK_C01 (2).pptx","wb") as f:
    #     data = blob1.download_blob()
    #     data.readinto(f)    
    # pptx_file_name = "SegmentSolution_Collated_SEG-UK_C01 (2).pptx"
    # #print(pptx_file_name)
    # di=DataExtraction(pptx_file_name)
    # print('Done') 

    ##download files from azure storage
    azure_blob_file_downloader = AzureBlobFileDownloader()
    azure_blob_file_downloader.download_all_blobs_in_container()
    

    ##get Extracted data
    _d={'pptx_folder':'C:\Azure_Blob_Data\Input'}
    doc_folder = _d['pptx_folder'] 
    DataExtraction(doc_folder)
    print('done')

    
    