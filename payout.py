################################################################
# This is a POC implementation of the payout system listed at
# https://docs.minaexplorer.com/minaexplorer/calculating-payments
# It is not meant for production use. This will output or store the
# payments which must then be processed seperately e.g. by signing
# the tx using coda sdk and then broadcasting. A better implementation is
# at https://github.com/jrwashburn/mina-pool-payout and recommended
################################################################

from tabulate import tabulate
import Currency
import GraphQL
import Mongo
import os
import math
import pprint


################################################################
# Define the payout calculation here
################################################################
public_key = "B62qmQAFPta1Q3c7wXHxXRKnE3uWyBYZCLb8frdHEgavi3BbBVkpeC1"  # Public key of the block producer
min_height = 0  # This can be the last known payout or this could vary the query to be a starting date
block_size = 500


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

print(len(latestPayout["data"]["payouts"]))

#if there is not payout, it means there is no reward given to this account
if not latestPayout["data"]["payouts"]:
    exit("We have no payouts")

current_block_height = latestPayout["data"]["payouts"][0]["blockHeight"]
#current_block_height = 2000

# fetch payouts by block height range
while(current_block_height > 0):
    if current_block_height-block_size <=0:
        lower_block_height = 0
    else:
        lower_block_height = current_block_height-block_size
    print("query for%s %s" % (current_block_height, lower_block_height))
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
        payoutAmount = s["payout"]
        aggregated_payouts[date] = aggregated_payouts.get(date, 0) + payoutAmount
    current_block_height = current_block_height - block_size

payout_table = []
for date,payoutAmount in aggregated_payouts.items():
    payout_table.append([
        date,
        Currency.Currency(
            payoutAmount,
            format=Currency.CurrencyFormat.NANO).decimal_format()
    ])
print(
    tabulate(payout_table,
             headers=[
                 "Date", "payout amount"
             ],
             tablefmt="pretty"))