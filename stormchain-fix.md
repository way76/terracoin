## 1. Fix desktop wallet

1. Remove the previous wallet executable and download the right wallet version (0.12.1.5 and NOT 0.12.1.5p): [win-x64](https://github.com/terracoin/terracoin/releases/download/v0.12.1.5/terracoin-qt.exe), [win-x32](https://github.com/terracoin/terracoin/releases/download/v0.12.1.5-32bit/terracoin-qt.exe), [linux-x64](https://github.com/terracoin/terracoin/releases/download/0.12.1.5/terracoin-qt), [wallet-github](https://github.com/terracoin/terracoin/releases), [terracoin.io](http://www.terracoin.io/)

1. Backup `%appdata%/TerracoinCore/wallet.dat` file. This contains your coins. DO NOT LOSE IT!

1. Open the `%appdata%/TerracoinCore/` folder and remove everything EXCEPT `wallet.dat`, `terracoin.conf`, `masternode.conf` and `backups`.

1. Optionally download [blockchain.rar](https://dl.dropboxusercontent.com/s/ek4e5xwkw6gy6gi/terracoin_blockchain_20171130.rar) file for faster synchronization and extract it to `%appdata%/TerracoinCore/` folder. Override the necessary files.

1. Start the wallet and wait for the synchronization.

## 2. Fix remote wallet on the VPS (easier option)

### 2.1 Vultr VPS

1. Reinstall your VPS. (Click the three dot => Server reinstall)

1. Follow the original guide from 2.3. (Run the setup script again...)

The script will ask your rpc username ans password which you can find in `%appdata%/TerracoinCore/terracoin.conf` file and your masternode private key wich you can find in `%appdata%/TerracoinCore/masternode.conf` file.

### 2.2 Other VPS (no reinstall)

1. Delete your VPS instance and remove the masternode from `%appdata%/TerracoinCore/masternode.conf` file.

1. Follow the original guide from 2.2. (Create a new VPS instance and run the setup script again...)

## 3 Fix remote wallet on the VPS (manual fix)

1. Login to your vps using putty
1. Login to the masternode account: `su mn1`
1. Stop the masternode and wait around 10-15 seconds: `terracoin-cli stop`
1. Logout from mn1 using ctrl+d
1. Download the good wallet:<br>
```wget https://github.com/terracoin/terracoin/releases/download/0.12.1.5/terracoind -O /usr/local/bin/terracoind``` and <br>
```wget https://github.com/terracoin/terracoin/releases/download/0.12.1.5/terracoin-cli -O /usr/local/bin/terracoin-cli```
1. Log back to mn1 user: `su mn1`
1. Go to home directory: `cd`
1. Remove old files: `rm -rf .terracoincore/banlist.dat .terracoincore/blocks .terracoincore/chainstate .terracoincore/backups .terracoincore/governance.dat .terracoincore/mncache.dat .terracoincore/mnpayments.dat .terracoincore/netfulfilled.dat .terracoincore/peers.dat .terracoincore/fee_estimates.dat`
1. Start the masternode: `terracoind`
1. Wait until the wallet fully synced. Check the current block using `terracoin-cli getinfo` and the [explorer](https://explorer.terracoin.io/)
1. Intall sentinel: [link](https://github.com/terracoin/sentinel). You cannot install programs as mn1 user so you have to logout (ctrl+d) install the programms using `sudo apt-get`. After log back to `mn1` user and go to home directory `cd`.
1. Start the masternode using your desktop wallet
