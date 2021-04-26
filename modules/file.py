import os
import stat
import re
import grp
import pwd
import shutil
from pathlib import Path
import modules.display


create_supported_args = ['comment','path','owner','group','mode','content','action']
delete_supported_args = ['comment','path','action']

def check_supported_args(keys_list,supported_args):
  if(set(keys_list).issubset(supported_args)):
    check_required_args(keys_list,supported_args)
  else:
    modules.display.output(f"Unsupported options passed in the files module. Please check the options {keys_list-supported_args} and try again",'FAIL')
    raise Exception(f"Unsupported options passed in the files module. Please check the options {keys_list-supported_args} and try again") 
 
def check_required_args(keys_list,required_args):
  if(set(required_args).issubset(keys_list)):
    return 'true'  
  else :
    modules.display.output(f"All the required options are not passed. please check and update options {required_args-keys_list}",'FAIL')
    raise Exception(f"All the required options are not passed. please check and update options {required_args-keys_list}")

#check if file is uptodate, if not update 
#def execute(comment,filepath,owner,group,mode,action,content):
def execute(args_dict):
  keys_list = args_dict.keys()
  if(re.search("create|update",args_dict['action'],re.IGNORECASE)):    
    #check if supported arguments are passed or not  
    check_supported_args(keys_list,create_supported_args)  
    actionCreate(args_dict['comment'],args_dict['path'],args_dict['owner'],args_dict['group'],args_dict['mode'],args_dict['action'],args_dict['content'])  
    #actionCreate(comment,filepath,owner,group,mode,action,content)
  elif(re.search("delete|remove",args_dict['action'],re.IGNORECASE)):    
    #actionDelete(comment,filepath,action)
    check_supported_args(keys_list,delete_supported_args)  
    actionDelete(args_dict['comment'],args_dict['path'],args_dict['action'])

def actionDelete(comment,filepath,action):
  if os.path.exists(filepath):
    #delete if file exists
    os.remove(filepath)
    modules.display.output(f"File deleted successfully: {filepath}",'OKGREEN')
  else:  
    modules.display.output(f"file({comment})  (action: {action})(uptodate)",'OKCYAN')

def actionCreate(comment,filepath,owner,group,mode,action,content):    
  #check if file exists
  if os.path.exists(filepath):
    #chef if file is uptodate, if not update
    result = isUptoDate(filepath,owner,group,mode,action,content)
    if(result == 4):
      #if result matches 3, then all the checks are idempotenet  
      modules.display.output(f"file({comment})  (uptodate)",'OKCYAN')      
  else:
    #Since file doesn't exist, creating new file and updating  
    modules.display.output(f"file({comment})  (action: {action})",'OKCYAN')
    createFile(filepath)
    #Check owner,group and update if doesn't match
    changeOwnerGroup(filepath,owner,group)
    #Check file permissions and change if doesn't match
    changeMode(filepath,mode)
    #Update file with content
    writeFileContent(filepath,content)

#Check if file is uptodate    
def isUptoDate(filepath,owner,group,mode,action,content):
  checks_count = 0
  if os.path.exists(filepath):
    #get stats of file
    data = os.stat(filepath)
    #Get current user and group
    current_user = pwd.getpwuid(data.st_uid)[0]
    current_group = grp.getgrgid(data.st_gid)[0]
    #check the current_owner and file resource owner matches
    if(current_user == owner):
      checks_count += 1
    else:
      changeOwnerGroup(filepath,owner,group)  
    #check the current_group and file resource group matches
    if(current_group == group):
      checks_count += 1
    else:  
      changeOwnerGroup(filepath,owner,group)
    #get permissions of file  
    perms = oct(stat.S_IMODE(data.st_mode))
    if(re.search(str(mode),perms)):    
      checks_count += 1
    else:
      changeMode(filepath,mode)
    
    #Check and update file content
    data = getFileContent(filepath)
    if(data.strip() == content):
      checks_count += 1
    else:
      writeFileContent(filepath,content)
  return checks_count

def createFile(filepath):
  #check if directory exists
  if os.path.exists(filepath.rsplit('/',1)[0]):
    Path(os.path.join(filepath)).touch()
    modules.display.output(f"\tCreated file : {filepath}",'OKGREEN')
  else:
    #Error if directory doesn't exists  
    modules.display.output(f"Error: No such file or directory: {filepath.rsplit('/',1)[0]}",'FAIL')
    return 1

#Check if user and group exists and update file permissions
def changeOwnerGroup(filepath,owner,group):
  try:
    #Check if user exists, if not raises an exception  
    pwd.getpwnam(owner)
  except KeyError:  
    modules.display.output(f"\tUser {owner} does not exist.",'FAIL')    
    return 1
  try:
    #Check if group exists, if not raises an exception  
    grp.getgrnam(group)
  except KeyError:
    modules.display.output(f"\tGroup {group} does not exist.",'FAIL')
    return 1
  #Update user and group for a file
  shutil.chown(filepath,owner,group) 
  modules.display.output(f"\tUpdated file with owner: {owner} and group: {group}",'OKGREEN')


#Update file permissions
def changeMode(filepath,mode):
  #Update file permissions  
  os.chmod(filepath, int(str(mode), base=8))
  modules.display.output(f"\tUpdated file permissions to {mode}",'OKGREEN')

#Read file contenst and return data
def getFileContent(filepath):
  with open(filepath) as f:
    data = f.read()
    return data

#Write file content  
def writeFileContent(filepath,content):  
  with open(filepath,'w') as f:
    f.write(content)
    f.close
  modules.display.output(f"\tUpdated file content {content}",'OKGREEN')  
