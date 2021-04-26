from subprocess import Popen, PIPE

def run_command(command):
  p = Popen(command , shell=True, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate()
  if(p.returncode == 0):
    return out.decode('ascii').strip()
  else:    
    return err.decode('ascii')

print(run_command("echo $PATH"))

