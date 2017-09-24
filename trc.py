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

SERVER_IP = urlopen('http://ip.42.pl/raw').read()
BOOTSTRAP_URL = "https://transfer.sh/sHxsj/blockchain.rar"
MN_PORT = 13333


DEFAULT_COLOR = "\x1b[0m"
PRIVATE_KEY = ""

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
        if(len(lines) >= 5):
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
    print_info("Terracoin masternode installer v1.0")

def update_system():
    print_info("Updating the system...")
    run_command("apt-get update")
    run_command("apt-get upgrade -y")
    run_command("apt-get dist-upgrade -y")

def chech_root():
    print_info("Check root privileges")
    user = os.getuid()
    if user != 0:
        print_error("This program requires root privileges.  Run as root user.")
        sys.exit(-1)

def secure_server():
    print_info("Securing server...")
    run_command("ufw allow OpenSSH")
    run_command("ufw allow {}".format(MN_PORT))
    run_command("ufw default deny incoming")
    run_command("ufw default allow outgoing")
    run_command("ufw --force enable")

def setup_wallet():
    print_info("Allocating swap...")
    run_command("fallocate -l 2G /swapfile")
    run_command("chmod 600 /swapfile")
    run_command("mkswap /swapfile")
    run_command("swapon /swapfile")
    f = open('/etc/fstab','r+b')
    line = '/swapfile   none    swap    sw    0   0 \n'
    lines = f.readlines()
    if (lines[-1] != line):
        f.write(line)
        f.close()

    print_info("Installing wallet dependencies...")
    run_command("add-apt-repository ppa:bitcoin/bitcoin -y")
    run_command("apt-get update")
    run_command("apt-get --assume-yes install git unzip libboost-system-dev libboost-filesystem-dev libboost-chrono-dev "
                "libboost-program-options-dev libboost-test-dev libboost-thread-dev software-properties-common libdb4.8-dev "
                "libdb4.8++-dev libminiupnpc-dev libevent-dev libzmq3-dev")

    print_info("Downloading wallet...")
    run_command("wget --continue https://github.com/terracoin/terracoin/releases/download/0.12.1.5/terracoind -O /usr/local/bin/terracoind")
    run_command("chmod +x /usr/local/bin/terracoind")
    run_command("wget --continue https://github.com/terracoin/terracoin/releases/download/0.12.1.5/terracoin-cli -O /usr/local/bin/terracoin-cli")
    run_command("chmod +x /usr/local/bin/terracoin-cli")

def setup_masternode():
    print_info("Setting up masternode...")
    run_command("useradd --create-home -G sudo mn1")
    
    print_info("Open your desktop wallet config file (%appdata%/terracoincore/terracoin.conf) and copy\n    your rpc username and password! If it is not there create one! E.g.:\n\trpcuser=[SomeUserName]\n\trpcpassword=[DifficultAndLongPassword]")
    rpc_username = raw_input("rpcuser: ")
    rpc_password = raw_input("rpcpassword: ")

    print_info("Open your wallet console (Help => Debug window => Console) and create a new masternode private key: masternode genkey")
    masternode_priv_key = raw_input("masternodeprivkey: ")
    global PRIVATE_KEY
    PRIVATE_KEY = masternode_priv_key
    
    config = """rpcuser={}
rpcpassword={}
rpcallowip=127.0.0.1
rpcport=22350
port={}
server=1
listen=1
daemon=1
logtimestamps=1
mnconflock=1
masternode=1
externalip={}:{}
masternodeprivkey={}
""".format(rpc_username, rpc_password, MN_PORT, SERVER_IP, MN_PORT, masternode_priv_key)

    run_command('su - mn1 -c "{}" '.format("mkdir -p /home/mn1/.terracoincore/"))
    
    print_info("Saving config file...")
    with open('/home/mn1/.terracoincore/terracoin.conf', 'w') as f:
        f.write(config)      
        
    run_command('chown mn1:mn1 /home/mn1/.terracoincore/terracoin.conf')

    print_info("Downloading blockchain file...")
    run_command('su - mn1 -c "{}" '.format("cd && wget --continue " + BOOTSTRAP_URL))
    
    print_info("Unzipping the file...")
    filename = BOOTSTRAP_URL[BOOTSTRAP_URL.rfind('/')+1:]
    run_command('su - mn1 -c "{}" '.format("cd && unzip -d .terracoincore -o " + filename))

       
    os.system('su - mn1 -c "{}" '.format('terracoind -daemon'))
    print_warning("Masternode started syncing in the background...")

def autostart_masternode():
    job = "@reboot /usr/local/bin/terracoind\n"
    
    p = Popen("crontab -l -u mn1 2> /dev/null", stderr=STDOUT, stdout=PIPE, shell=True)
    p.wait()
    lines = p.stdout.readlines()
    if job not in lines:
        print_info("Cron job doesn't exist yet, adding it to crontab")
        lines.append(job)
        p = Popen('echo "{}" | crontab -u mn1 -'.format(''.join(lines)), stderr=STDOUT, stdout=PIPE, shell=True)
        p.wait()
    

def porologe():

    mn_base_data = """
    Alias: Masternode1
    IP: {}
    Private key: {}
    Transaction ID: [5k desposit transaction id. 'masternode outputs']
    Transaction index: [5k desposit transaction index. 'masternode outputs']
    --------------------------------------------------
"""

    mn_data = mn_base_data.format(SERVER_IP + ":" + str(MN_PORT), PRIVATE_KEY)

    imp = """Vs lbh sbhaq gur thvqr naq guvf fpevcg hfrshy pbafvqre gb fhccbeg zr.\\a        GEP: 1SfWQqo14w1Zff8ICNSt8GvRI9wfuDKCH\\a\\g    RGU: 0k9n794240o456O8qQ5593n7r8q7NR92s4pn4Q9Q2s\\a        OGP: 33PeQClZcpjWSlZGprIZGYWLYE8mOFfaJz\\a"""

    print('')
    print_info(
"""Masternodes setup finished!
    Wait until the masternode is fully synced. To check the progress login the 
    masternode account (su mn1) and run the 'terracoin-cli getinfo' command to get
    the actual block number. Go to https://bchain.info/TRC/ website to check 
    the latest block number or use your wallet. After the syncronization is done 
    add your masternode to your desktop wallet.

Masternode data:""" + mn_data)

    print_warning(imp.decode('rot13').decode('unicode-escape'))

def main():
    print_welcome()
    chech_root()
    update_system()
    secure_server()
    setup_wallet()
    setup_masternode()
    autostart_masternode()
    porologe()

if __name__ == "__main__":
    main()
