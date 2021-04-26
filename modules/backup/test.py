import os,stat
import grp
import pwd,re
import display
from pathlib import Path


data = os.stat('/etc/passwd')
print(data)
uid = data.st_uid
gid = data.st_gid
print(uid)
print(gid)
print(data.st_mode)
perms = oct(stat.S_IMODE(data.st_mode))
print(perms)
user = pwd.getpwuid(uid)[0]
group = grp.getgrgid(gid)[0]
print(user)
print(group)

if(user != 'nroot'):
  print("root user")

if(re.search('644',perms)):
  print("mode matches")

print(pwd.getpwnam('root'))
#OKGREEN = '\033[92m'
#WARNING = '\033[93m'
#FAIL = '\033[91m'
#ENDC = '\033[0m'
#print(f"{WARNING}Warning: No active frommets remain. Continue?{ENDC}")
#print(f"{OKGREEN}Warning: No active frommets remain. Continue?{ENDC}")
#print(f"{FAIL}Warning: No active frommets remain. Continue?{ENDC}")
display.output('display success','OKGREEN')
display.output('display error','FAIL')
display.output('display warning','WARNING')

with open('/tmp/file1.txt') as f:
    data = f.read()
    print(data)

content = "Hello Rakesh"

if(data.strip() == content):
  print("data matched")
else:
  print("data not matched")
  with open('/tmp/file1.txt','w') as f:
    f.write(content)
    f.close 
