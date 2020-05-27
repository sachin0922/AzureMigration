# AzureMigration
Repo for Azure Migration related stuff


#Using SAS url to upload from Azure storage service.
curl --location --request PUT 'https://<storage_account>.blob.core.windows.net/<container_path>/<file_name as needed in blob>?<Generated SAS Token>' --header 'x-ms-blob-type:BlockBlob' --data-binary '@/<absolute path to file>'
