import datetime as d
from util import parse_amount, clean_date
from parse import parse

def make_sodexo_transaction(row, label = "Sodexo eLunch wallet", category = "Food"):
    transaction = parse_sodexo_row(row)
    amount = parse_amount(transaction["amount"])
    if amount > 0:
        return clean_sodexo_deposit(transaction, label, category)
    else:
        return clean_sodexo_payment(transaction, label, category)

def parse_sodexo_row(row, ncolumns = 3):
    if len(row) == ncolumns:
        return {
            "date": row[0],
            "partner": row[1],
            "amount": row[2]
        }
    else:
        raise ValueError("Invalid Sodexo transaction: " + str(row))

def clean_sodexo_payment_partner(description):
    if type(description) is str:
        transaction_ref_idx = description.find("(Transaction")
        return description[:transaction_ref_idx].replace("Dépense", "").strip().title()
    else:
        raise TypeError("invalid description type.")

def clean_sodexo_deposit_partner(partner):
    if type(partner) is str:
        result = parse("{} eLunch Pass d'une valeur de {} de {}", partner)
        return result[2].title()
    else:
        raise TypeError("Invalid description type.")

def clean_sodexo_deposit(deposit, destination = "", category = ""):
    return {
        "date": clean_date(deposit["date"]),
        "source": clean_sodexo_deposit_partner(deposit["partner"]),
        "destination": destination,
        "amount": parse_amount(deposit["amount"]),
        "category": category
    }

def clean_sodexo_payment(payment, source = "", category = ""):
    return {
        "date": clean_date(payment["date"]),
        "source": source,
        "destination": clean_sodexo_payment_partner(payment["partner"]),
        "amount": parse_amount(payment["amount"]),
        "category": category
    }