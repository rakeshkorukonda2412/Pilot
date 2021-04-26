args_dict = {'comment': 'create file in /tmp', 'path': '/tmp/file1.txt', 'owner': 'root', 'group': 'root', 'mode': 755, 'content': 'Hello Rakesh Korukonda. Welcome to SLACK', 'action': 'Remove'}
#args_dict = {'file': {'comment': 'create file in /tmp', 'owner': 'root', 'group': 'root', 'mode': 755, 'content': 'Hello Rakesh Korukonda. Welcome to SLACK'}}

keys_list = args_dict.keys()

print(keys_list)
supported_args = ['comment','path','owner','group','mode','content','action']
#required_args = ['path','action']

def check_supported_args(keys_list,supported_args):
  try:
    if(set(keys_list).issubset(supported_args)):
      check_required_args(keys_list,supported_args)  
    else:
      raise
  except:
    print(f"Unsupported options passed in the files module. Please check the options {keys_list-supported_args} and try again")  

def check_required_args(keys_list,required_args):
  try:
    if(set(required_args).issubset(keys_list)):
      print ("Yes, list is subset of other.")
    else :
      raise
  except:
    print(f"All the required options are not passed. please check and update options {required_args-keys_list}")

#check_supported_args(keys_list,supported_args,required_args)



def actionCreate(comment,filepath,owner,group,mode,action,content):
  print(filepath)  

actionCreate(args_dict['comment'],args_dict['path'],args_dict['owner'],args_dict['group'],args_dict['mode'],args_dict['action'],args_dict['content'])

#def listargs(**options):
#  print(options.items())

#listargs(name="rakesh",age="30",sex="male") 
#listargs(name="rakesh",age="29")

