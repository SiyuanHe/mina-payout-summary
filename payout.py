
from tabulate import tabulate
import Currency
import GraphQL
import os
import math
import pprint


################################################################
# Set the public key here
################################################################
public_key = "B62qmQAFPta1Q3c7wXHxXRKnE3uWyBYZCLb8frdHEgavi3BbBVkpeC1"  # Public key 
block_size = 500

print("generating payout summary for account ", public_key)
# Initialize variables
aggregated_payouts = dict()

# Get the latest payout
try:
    latestPayout = GraphQL.getLatestPayouts({
        "publicKey": public_key,
    })
except Exception as e:
    print(e)
    exit("Issue getting latest payout from GraphQL")

#if there is not payout, it means there is no reward given to this account
if not latestPayout["data"]["payouts"]:
    exit("there is no payouts in this account")

current_block_height = latestPayout["data"]["payouts"][0]["blockHeight"]
#current_block_height = 2000

# fetch payouts by block height size
while(current_block_height > 0):
    if current_block_height-block_size <=0:
        lower_block_height = 0
    else:
        lower_block_height = current_block_height-block_size
    print("fetching payouts of block height between %s and %s" %(current_block_height, lower_block_height))
    try:
        payouts = GraphQL.getPayouts({
            "publicKey": public_key,
            "blockHeight_gt": lower_block_height,
            "blockHeight_lte": current_block_height,
        })
    except Exception as e:
        print(e)
        exit("Issue getting payouts from GraphQL")

    #aggregated payout amount by date
    for s in payouts["data"]["payouts"]:      
        date = s["paymentHash"]["dateTime"][:10]
        payout_amount = s["payout"]
        aggregated_payouts[date] = aggregated_payouts.get(date, 0) + payout_amount
    current_block_height = current_block_height - block_size

#print result nicely
payout_table = []
for date,payout_amount in aggregated_payouts.items():
    payout_table.append([
        date,
        Currency.Currency(
            payout_amount,
            format=Currency.CurrencyFormat.NANO).decimal_format()
    ])
print(
    tabulate(payout_table,
             headers=[
                 "Date", "payout amount"
             ],
             tablefmt="pretty"))