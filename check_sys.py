import os
import subprocess
import datetime
import tarfile
import shutil

# Function for logging errors
def log_error(error_message):
    log_file = "error_log.txt"
    with open(log_file, "a") as file:
        file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

# Function to check if a command exists
def check_command(command):
    try:
        subprocess.check_output(['which', command])
    except subprocess.CalledProcessError:
        log_error(f"Error: command {command} not found.")
        exit(1)

# Check for necessary commands
commands = ['dmidecode', 'ip', 'fdisk', 'smartctl']
for command in commands:
    check_command(command)

# Function to get free space on all available disks
def get_free_space():
    disks = subprocess.check_output(['lsblk', '-d', '-o', 'NAME,TYPE']).decode().split('\n')
    free_space = {}
    for disk in disks:
        if 'disk' in disk:
            disk_name = disk.split()[0]
            try:
                output = subprocess.check_output(['sudo', 'df', f'/dev/{disk_name}']).decode().split('\n')[1]
                free_blocks = ''.join(filter(str.isdigit, output))
                free_gb = round(int(free_blocks) / 1048576, 2)
                free_space[disk_name] = free_gb
            except IndexError:
                continue
    return free_space

# Get free space information
free_space = get_free_space()
for disk, free_gb in free_space.items():
    print(f"**Free space on disk {disk}: {free_gb} GB**")

# Function to write content to a file
def write_to_file(content, filename):
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"**Data successfully written to file: {filename}**")
    except Exception as e:
        log_error(f"Error writing to file: {filename}")

# Function to create an archive
def create_archive(files, archive_name):
    with tarfile.open(archive_name, "w:gz") as tar:
        for file in files:
            tar.add(file)
    print(f"**Archive {archive_name} created successfully.**")

# Function to send the archive to a server
def send_archive_to_server(archive_name, server_address, username, remote_directory):
    try:
        subprocess.check_call(['scp', archive_name, f'{username}@{server_address}:{remote_directory}'])
        print(f"**Archive {archive_name} successfully sent to {server_address}.**")
    except subprocess.CalledProcessError as e:
        log_error(f"Error sending archive to server: {e}")

# Script execution
hostname = subprocess.check_output(['hostname']).decode().strip()
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archive_name = f"diag_collector_{hostname}_{date_time}.tar.gz"

# System information collection
system_info_dir = "/tmp/system_info"
os.makedirs(system_info_dir, exist_ok=True)

commands_info = {
    'dmidecode': 'dmidecode.txt',
    'ip -s a': 'ip_info.txt',
    'hostname': 'hostname.txt',
    'date': 'date.txt'
}

for command, filename in commands_info.items():
    write_to_file(subprocess.check_output([command], shell=True).decode(), f"{system_info_dir}/{filename}")

# Disk information collection
for disk, _ in free_space.items():
    write_to_file(subprocess.check_output(['sudo', 'fdisk', '-l', f'/dev/{disk}'], stderr=subprocess.DEVNULL).decode(), f"{system_info_dir}/fdisk_{disk}.txt")
    write_to_file(subprocess.check_output(['sudo', 'smartctl', '-x', f'/dev/{disk}'], stderr=subprocess.DEVNULL).decode(), f"{system_info_dir}/smartctl_{disk}.txt")

# Additional system information collection
additional_commands = [
    'lspci -vv',
    'lsmod',
    'netstat -an',
    'sysctl -A',
    'route -n',
    'dpkg -l',
    'uptime',
    'netstat -i',
    'netstat -s',
    'vmstat -a',
    'ps aux',
    'mpstat -A',
    'iostat -x'
]

for command in additional_commands:
    write_to_file(subprocess.check_output([command], shell=True).decode(), f"{system_info_dir}/{command.replace(' ', '_')}.txt")

# Create archive
files_to_archive = ['/var/log', '/etc', system_info_dir]
create_archive(files_to_archive, archive_name)

# Send archive to server
server_address = 'your_server_address'
username = 'your_username'
remote_directory = '/path/to/remote/directory'
send_archive_to_server(archive_name, server_address, username, remote_directory)

# Cleanup
shutil.rmtree(system_info_dir)

print("*****************************************************************")
print("**Script completed successfully!**")
print(f"**Create archive {archive_name}**")
print(f"**The directory where the archive is saved {os.getcwd()}**")
