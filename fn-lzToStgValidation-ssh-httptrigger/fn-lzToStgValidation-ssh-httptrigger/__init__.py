import logging
import json
import paramiko
import os
import azure.functions as func

'''
Sample post request-
{
	"vmhost":"<IP>",
	"vmuser":"<User>",
	"vmpass":"<Pass>",
	"vmscripttoexecute":"<command to execute on VM>"
}	
'''

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info("Establishing Connection with Server")
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    inputParams = req.get_json()

    ssh_client.connect(hostname=inputParams['vmhost'],username=inputParams['vmuser'],password=inputParams['vmpass'])

    logging.info("Connection Established with Server")
    logging.info("Sending Commands")
    chan = ssh_client.get_transport().open_session()
    
    chan.exec_command(inputParams['vmscripttoexecute'])
    retCode = chan.recv_exit_status()
    logging.info("Received preprcess status back from VM- "+str(retCode))
    ssh_client.close()
    
    responseObj='{"retcode":"'+str(retCode)+'"}'

    if retCode == 0:
        HTTP_CODE=200
    else:
        HTTP_CODE=500

    return func.HttpResponse(json.dumps(json.JSONDecoder().decode(responseObj)),status_code=HTTP_CODE)