## MinaExplorer Account Payout History Script

To run, change the settings to your requirements in `payout.py` specifying the account/public key you want to query

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


