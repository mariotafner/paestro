import time
import paramiko
import re

def ssh_exec(cmd, host, username, password):
    start = time.time()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    cmd = f'PS1="" bash -ic "{cmd}"'
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd, get_pty=True)
    ssh_stdout_content = ssh_stdout.read()
    ssh_stderr_content = ssh_stderr.read()
    ssh.close()

    ssh_stdout = ssh_stdout_content.decode('utf-8')
    ssh_stderr = ssh_stderr_content.decode('utf-8')
    
    result = ''
    if ssh_stdout.replace('\n', '') != '':
        result = ssh_stdout
    elif ssh_stderr.replace('\n', '') != '':
        result = ssh_stderr
    
    if (result.endswith('\n')):
        result = result[:-1]
        
    lines = result.split('\n')
    lines = list(filter(lambda x: x != '', lines))

    end = time.time()
    ms = (end - start) * 1000
    
    return result, lines, ms


result, lines, ms = ssh_exec('ls ./ssl', '--', '--', '--')

# result = repr(result)

parts = result.split('\x1b[')
parts_new = []

for part in parts:
    if 'm' in part:
        prefix = part.split('m')[0]
        print(prefix)
        part = part[len(prefix)+1:]

    if part != '':
        parts_new.append(part)

print(''.join(parts_new))

# print("\x1b[1;31mteste\x1b[0m")