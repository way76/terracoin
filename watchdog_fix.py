#! /usr/bin/env python
from subprocess import Popen,PIPE,STDOUT
import collections
import os
import sys
import time
import math
import os
import time
from urllib2 import urlopen

DEFAULT_COLOR = "\x1b[0m"

def print_info(message):
    BLUE = '\033[94m'
    print(BLUE + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_warning(message):
    YELLOW = '\033[93m'
    print(YELLOW + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_error(message):
    RED = '\033[91m'
    print(RED + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def get_terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
    
def remove_lines(lines):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for l in lines:
        sys.stdout.write(CURSOR_UP_ONE + '\r' + ERASE_LINE)
        sys.stdout.flush()

def run_command_as(user, command):
    run_command('su - {} -c "{}" '.format(user, command))

def run_command(command):
    out = Popen(command, stderr=STDOUT, stdout=PIPE, shell=True)
    lines = []
    
    while True:
        line = out.stdout.readline()
        if (line == ""):
            break
        
        # remove previous lines     
        remove_lines(lines)
        
        w, h = get_terminal_size()
        lines.append(line.strip().encode('string_escape')[:w-3] + "\n")
        if(len(lines) >= 9):
            del lines[0]

        # print lines again
        for l in lines:
            sys.stdout.write('\r')
            sys.stdout.write(l)
        sys.stdout.flush()

    remove_lines(lines) 
    out.wait()

def print_welcome():
    os.system('clear')
    GREEN = '\033[32m'
    print(GREEN + "  _____                             _       " + DEFAULT_COLOR)
    print(GREEN + " |_   _|__ _ __ _ __ __ _  ___ ___ (_)_ __  " + DEFAULT_COLOR)
    print(GREEN + "   | |/ _ \ '__| '__/ _` |/ __/ _ \| | '_ \ " + DEFAULT_COLOR)
    print(GREEN + "   | |  __/ |  | | | (_| | (_| (_) | | | | |" + DEFAULT_COLOR)
    print(GREEN + "   |_|\___|_|  |_|  \__,_|\___\___/|_|_| |_|" + DEFAULT_COLOR)
    print(GREEN + "                                            " + DEFAULT_COLOR)
    print_info("Terracoin watchdog_expired patch v1.0")

def check_root():
    print_info("Check root privileges")
    user = os.getuid()
    if user != 0:
        print_error("This program requires root privileges.  Run as root user.")
        sys.exit(-1)

def fix():
	print_info("Stopping terracoind....")
	time.sleep(5)
	run_command_as("mn1", "terracoin-cli stop")

	MN_DAEMON = "terracoind"
	MN_CLI = "terracoin-cli"

	print_info("Updating wallet...")

	run_command("wget https://github.com/terracoin/terracoin/releases/download/0.12.1.5p/terracoind -O /usr/local/bin/{}".format(MN_DAEMON))
	run_command("chmod +x /usr/local/bin/{}".format(MN_DAEMON))
	run_command("wget https://github.com/terracoin/terracoin/releases/download/0.12.1.5p/terracoin-cli -O /usr/local/bin/{}".format(MN_CLI))
	run_command("chmod +x /usr/local/bin/{}".format(MN_CLI))

	print_info('If your local wallet shows your masternode is enabled you don\'t have to reindex your wallet!')
	while True:
		ans = raw_input('Do you want to reindex you wallet? (y/n)? ')
		if ans == 'y' or ans == 'n':
			break

	print_info('Starting your masternode...')
	command = 'terracoind -daemon '

	if ans == 'y':
		command += '-reindex'
	
	os.system('su - {} -c "{}" '.format('mn1', command))

	if ans == 'y':
		print_info('Login to your masternode account(su mn1) and check reindex status using the terracoin-cli getinfo command. Check the current block using the block explorer (http://explorer.terracoin.io/) or use your wallet.')

	print_info('Do not forget to update your local wallet. The updated wallet is available here: https://github.com/terracoin/terracoin/releases/tag/0.12.1.5p-x64')
		

def main():
	print_welcome()
	check_root()
	fix()

if __name__ == "__main__":
    main()

