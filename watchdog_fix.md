# watchdog_expired fix

1. Update your local wallet: [win_x32](https://github.com/terracoin/terracoin/releases/download/v0.12.1.5p-32bit/terracoin-qt.exe), [win_x64](https://github.com/terracoin/terracoin/releases/download/0.12.1.5p-x64/terracoin-qt.exe), [linux](https://github.com/terracoin/terracoin/releases/download/0.12.1.5p/terracoin-qt)
2. Start putty and login as root user. (Root password and server ip address is in vultr overview tab)
3. Run this line on the vps and answer the questions: <br>
  ```bash 
  wget https://raw.githubusercontent.com/u3mur4/terracoin/master/watchdog_fix.py && python watchdog_fix.py
  ```
4. Start your masternode after you vps wallet fully synced.
