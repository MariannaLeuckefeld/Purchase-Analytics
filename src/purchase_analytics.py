"""
Script to gather the input files and create an output file as report.csv

q1 = implies output of question 1
    number_of_orders. How many times was a product requested from this department?
    (If the same product was ordered multiple times, we count it as multiple requests)
q2 = implies output of question 2
    number_of_first_orders. How many of those requests contain products ordered for the first time?
q3 implies output of question 3
    percentage. What is the percentage of requests containing products ordered for the first time compared with the
    total number of requests for products from that department?
    (e.g., number_of_first_orders divided by number_of_orders)
"""

import csv
import argparse

parser = argparse.ArgumentParser(description='process')
parser.add_argument('order_products_path')
parser.add_argument('products_path')
parser.add_argument('report_path')
args = parser.parse_args()


def get_input(path):
    """Opens both input files and encodes as well. The results will be saved in a list"""
    with open(path, encoding="utf8") as fh:
        file = csv.DictReader(fh)
        res = []
        for row in file:
            res.append(row)
    return res


def merge(orders, products):
    """merge together based on product_id"""
    res = []
    for row in orders:
        for row1 in products:
            if row['product_id'] == row1['product_id']:
                batch_dict = {**row, **row1}
                res.append(batch_dict)
    return res


def number_of_orders(results):
    """calculate the number_of_orders greater than 0"""
    res = {}
    department_ids = [r['department_id'] for r in results]
    for department_id in department_ids:
        res[department_id] = 0
    for row in results:
        res[row['department_id']] += 1
    return res


def number_of_first_orders(results):
    """calculate the number_of_first_orders (when reordered ==0) for every department ID"""
    res = {}
    department_ids = [r['department_id'] for r in results]
    for department_id in department_ids:
        res[department_id] = 0
    for row in results:
        if row['reordered'] == '0':
            res[row['department_id']] += 1
    return res


def percentage(q1, q2):
    """# We are creating one output and merging q1 and q2 based on the department ID together
      # calculate percentage (number_of_first_orders divided by number_of_orders)"""
    res = []
    for id in q1.keys():
        res.append({'department_id': id, 'number_of_orders': q1[id], 'number_of_first_orders': q2[id],
                    'percentage': (q2[id]/q1[id])})
    return res


def output(q3):
    """creation of final csv """
    with open(args.report_path, 'w', newline='') as fh_report:
        writer = csv.DictWriter(fh_report, fieldnames=q3[0])
        writer.writeheader()
        for data in q3:
            writer.writerow(data)


if __name__ == '__main__':
    orders = get_input(args.order_products_path)
    products = get_input(args.products_path)
    results = merge(orders, products)
    q1 = number_of_orders(results)
    q2 = number_of_first_orders(results)
    q3 = percentage(q1, q2)
    output(q3)
