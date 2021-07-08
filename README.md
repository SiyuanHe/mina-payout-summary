## MinaExplorer Account Payout History Script

To run, pls specifying the account/public key you want to query in `payout.py`
```
public_key = "B62qmQAFPta1Q3c7wXHxXRKnE3uWyBYZCLb8frdHEgavi3BbBVkpeC1"  # Public key 
```

```
pip3 install -r requirements.txt
python3 payout.py
```

Will output:

```
generating payout summary for account  B62qmQAFPta1Q3c7wXHxXRKnE3uWyBYZCLb8frdHEgavi3BbBVkpeC1
fetching payouts for blocks between 2000 and 1500
fetching payouts for blocks between 1500 and 1000
fetching payouts for blocks between 1000 and 500
fetching payouts for blocks between 500 and 0
+------------+---------------+
|    Date    | payout amount |
+------------+---------------+
| 2021-03-23 | 284.393193579 |
| 2021-03-21 | 379.190924772 |
| 2021-03-18 | 284.393193579 |
+------------+---------------+
```

Pls note this repo is based on https://github.com/garethtdavies/mina-payout-script

## Thought process
1. the historical staking rewards will be given throught "payouts". 

2. based on this doc: https://docs.minaexplorer.com/minaexplorer/exporting-data, we are able to fetch all the payouts. 

3. overall algorithm
   
3.a get the block height of the latest payout

3.b start fetching payouts by chuncks starting from latest block height to "latest_block_height - chuck_size". and then aggegate the payout amounts by date. 

3.c repeat b until we fetech all payouts when block height reaches 0

3.d the reason to fetch by chunks is to avoid hitting performance issue of the backend. 

