'''
Script to gather the input files and create an output file as report.csv



'''
# importing csv module
import csv
import argparse

parser = argparse.ArgumentParser(description='process')
parser.add_argument('order_products_path')
parser.add_argument('products_path')
parser.add_argument('report_path')
args = parser.parse_args()












def get_input(path):
    with open(path) as fh:
        orders = csv.DictReader(fh)
        res=[]
        for row in orders:
            res.append(row)
    return res

def merge(orders, products):
    res=[]
    for row in orders:
        for row1 in products:
            if row['product_id']==row1['product_id']:
                batch_dict = {**row, **row1}
                res.append(batch_dict)
    return res







# creation and writing into the final csv file
def output():
    with open(args.report_path,'w') as fh_report:
        wr =csv.writer(fh_report, quoting=csv.QUOTE_ALL)
     #   wr.writerow()





if __name__=='__main__':
    orders = get_input(args.order_products_path)
    products = get_input(args.products_path)
    output()
    results = merge(orders,products)
    print(results)