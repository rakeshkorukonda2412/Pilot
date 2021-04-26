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


#Trigger package module and perform action requested
def execute(args_dict):
  keys_list = args_dict.keys()
  #check if supported arguments are passed
  check_supported_args(keys_list,supported_args)
  #chef if service action is uptodate, if not update the service
  isUptoDate(args_dict['comment'],args_dict['name'],args_dict['action'])

#Run command and get exit code and output
def run_command(command):
  p = Popen(command , shell=True, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate()
  if(p.returncode == 0):
    return p.returncode,out
  else:
    return p.returncode,err

#Check if service status is uptodate, if not update the service with respective action
def isUptoDate(comment,name,action):
  rc,status = isPackageInstalled(name,action)
  if(action == "install"):
    if(rc == 0):
      modules.display.output(f"package({name})  (action: {action})(uptodate)",'OKCYAN') 
    else:    
      updatePackage(name,action)
  elif(re.search("delete|remove",action)):
    if(rc == 0):
      updatePackage(name,action)
    else:
      modules.display.output(f"package({name})  (action: {action})(uptodate)",'OKCYAN')
      

def isPackageInstalled(name,action):
  rc,status = run_command(f"dpkg-query --list | grep {name} | grep ii")
  return rc,status

def updatePackage(name,action): 
  if(action == 'install'):
    rc,status = run_command(f"apt-get install {name} -y")
    print(rc)
    print(status)
    if( rc == 0):
      modules.display.output(f"Package {name} installed successfully: {action}",'OKGREEN')
    else:
      modules.display.output(f"Error in installing package {name} with action {action}",'FAIL')
  elif(re.search("delete|remove",action)):
    rc,status = run_command(f"apt-get remove {name} -y")
    print(rc)
    print(status)
    if( rc == 0):
      modules.display.output(f"Package {name} installed successfully: {action}",'OKGREEN')
    else:
      modules.display.output(f"Error in uninstalling package {name} with action {action}",'FAIL')
    
