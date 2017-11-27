# ![Terracoin](logo.png) Terracoin

``` bash
su mn1
```

``` bash
cd
```

``` bash
terracoin-cli stop
```

``` bash
rm -rf .terracoincore/banlist.dat .terracoincore/blocks .terracoincore/chainstate .terracoincore/backups .terracoincore/governance.dat .terracoincore/mncache.dat .terracoincore/mnpayments.dat .terracoincore/netfulfilled.dat .terracoincore/peers.dat .terracoincore/fee_estimates.dat
```

``` bash
wget https://dl.dropboxusercontent.com/s/a848ccq6illuy488/terracoin_blockchain_20171127.rar
```

``` bash
unrar x terracoin_blockchain_20171127.rar .terracoincore/
```

``` bash
terracoind
```

``` bash
terracoin-cli getinfo
```


# Support

| Coin      | Symbol | Address                                    |
| ----------| -------| -------------------------------------------|
| Terracoin | TRC    | 1Ly4iQhJrECfwYcm8Np4tDUMYoDMhB1Dnb          |
| Ethereum	| ETH    | 0x9a794240b456B8dD5593a7e8d7AE92f4ca4D9D2f |
| Bitcoin	| BTC    | 33CrDPyMpcwJFyMTceVMTLJYLR8zBSsnWm          |
