''' 
Class Details - Library for common blob handling functions. Implements createBlob,copyBlobToLocal and removeBlob operations.
Compiled with Python 3.7 


import sys
sys.path.insert(0, "/home/datalake/pre-pro/")
'''
# TODO - Implement rest of the common functions.

from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings
import logging


class BlobHelper:
    
    def __init__(self,acctName,acctKey):
        self.acctName=acctName
        self.acctKey=acctKey
        self.blob_handle = BlockBlobService(self.acctName, self.acctKey)

    def copyBlobToLocal(self,containerName,blobName,localPath):     
        try:
            blobToFile = self.blob_handle.get_blob_to_bytes(containerName,blobName)

            file_for_blob_copy= open(localPath+blobName,"wb+")
            file_for_blob_copy.write(blobToFile.content)
            file_for_blob_copy.close()
            return 0            

        except IOError:
            logging.error("IO Error occurred during blob copy operation!")
 
    def copyBlobToLocalUsingBlobConfig(self,acctName,acctKey,containerName,blobName,localPath):     
        try:
            blob_service = BlockBlobService(acctName, acctKey)
            blobToCopy = blob_service.get_blob_to_bytes(containerName,blobName)

            file_for_blob_copy= open(localPath+blobName,"wb+")
            file_for_blob_copy.write(blobToCopy.content)
            file_for_blob_copy.close()
            return 0

        except IOError:
            logging.error("IO Error occurred during blob copy operation!")
            


    def createBlob(self,container,blobName,localPath,localFileName):
        try:
            fileToBlob = open(localPath+localFileName,"rb+")
            ret_code = self.blob_handle.create_blob_from_bytes(container,blobName,fileToBlob.read())
            
            if ret_code is not None:
                logging.info("Successfully created blob in storage account!")
            else:
                logging.error("Error during blob creation in storage account!")

        except IOError:
            logging.error("IO Error occurred during blob copy operation!")

    def removeBlob(self,containerName,blobToRemove):
        try:
            ret_code =self.blob_handle.delete_blob(containerName,blobToRemove)
            if ret_code is None:
                logging.info("Successfully Deleted blob in storage account!")
            else:
                logging.error("Error during blob deletion!")

        except Exception as ex:
            logging.error(ex)

    def getBlobListFromContainer(self,container): 
        list=self.blob_handle.list_blobs(container)
        return list