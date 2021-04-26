import os
import re
import modules.display
from subprocess import Popen, PIPE

supported_args = ['comment','name','action']

#Check if supported arguments are passed
def check_supported_args(keys_list,supported_args):
  if(set(keys_list).issubset(supported_args)):
    check_required_args(keys_list,supported_args)
  else:
    modules.display.output(f"Unsupported options passed in the files module. Please check the options {keys_list-supported_args} and try again",'FAIL')
    raise Exception(f"Unsupported options passed in the files module. Please check the options {keys_list-supported_args} and try again")

#Check if all required arguments are passed
def check_required_args(keys_list,required_args):
  if(set(required_args).issubset(keys_list)):
    return 'true'
  else :
    modules.display.output(f"All the required options are not passed. please check and update options {required_args-keys_list}",'FAIL')
    raise Exception(f"All the required options are not passed. please check and update options {required_args-keys_list}")

#Trigger service module and perform action requested
def execute(args_dict):
  keys_list = args_dict.keys()
  #check if supported arguments are passed
  check_supported_args(keys_list,supported_args)
  #chef if service action is uptodate, if not update the service
  isUptoDate(args_dict['comment'],args_dict['name'],args_dict['action'])

#Check if service status is uptodate, if not update the service with respective action
def isUptoDate(comment,name,action):
  if(action == 'restart'):  
    #trigger restart service  
    update_service(comment,name,action)
  elif(action == 'start'):
    #get current status of service  
    rc,status = get_service_status(name,action)
    status = status.decode('ascii').strip()
    if(re.search('running',status)):
      #if service is already running, skip the action  
      modules.display.output(f"service({name})  (action: {action})(uptodate)",'OKCYAN')      
    else:
      #Start the service  
      update_service(comment,name,action)
  elif(action == 'stop'):
    #get current status of service  
    rc,status = get_service_status(name,action)
    status = status.decode('ascii').strip()
    if(re.search('inactive',status)):
      #if service is already stopped, skip the action  
      modules.display.output(f"service({name})  (action: {action})(uptodate)",'OKCYAN')
    else:
      #stop service  
      update_service(comment,name,action)
    

#Run command and get exit code and output
def run_command(command):
  p = Popen(command , shell=True, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate()
  if(p.returncode == 0):
    return p.returncode,out
  else:
    return p.returncode,err

#Run the service module
def run_action(comment,name,action):
  get_service_status(name)
  #update_service(comment,name,action)

#Check current status of the service
def get_service_status(name,action):
  if(action == 'start'):  
    check = 'running'
  elif(action == 'stop'):
    check = 'inactive'
  rc,status = run_command(f"systemctl status {name} | grep {check}")
  return rc,status

#Update service based on action requested in service modules    
def update_service(comment,name,action):    
  #Update service action
  rc,status = run_command(f"systemctl {action} {name}")  
  if( rc == 0):
    modules.display.output(f"Service {name} updated successfully: {action}",'OKGREEN')
  else:  
    modules.display.output(f"Error in updating service {name} with action {action} {status}",'FAIL')
  return rc,status

