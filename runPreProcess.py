import sys
sys.path.insert(0, <path_for_BlobHelper>)
from BlobHelper import BlobHelper
import os

obj=BlobHelper(<account_name>,<account_key>)
list=obj.getBlobListFromContainer(<container_name>)

for blob in list:
    obj.copyBlobToLocal('pre-landing-zone',blob.name,'/home/datalake/pre-pro/')	
	obj.createBlob('landing-zone',blob.name,'/home/datalake/pre-pro/',blob.name)
	obj.removeBlob('pre-landing-zone',blob.name)
exit(0)