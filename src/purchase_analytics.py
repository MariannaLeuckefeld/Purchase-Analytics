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

#merge together based on product_id
def merge(orders, products):
    res=[]
    for row in orders:
        for row1 in products:
            if row['product_id']==row1['product_id']:
                batch_dict = {**row, **row1}
                res.append(batch_dict)
    return res

#calculate the number_of_orders greater than 0

def number_of_orders(results):
    res = {}
    department_ids = [r['department_id'] for r in results]
    for department_id in department_ids:
        res[department_id] = 0
    for row in results:
        res[row['department_id']] += 1
    return res


#calculate the number_of_first_orders
def number_of_first_orders(results):
     res = {}
     department_ids = [r['department_id'] for r in results]
     for department_id in department_ids:
         res[department_id] = 0
     for row in results:
         if row['reordered'] == '0':
             res[row['department_id']] +=1
     return res



# calculate percentage (number_of_first_orders divided by number_of_orders)
def percentage(q1,q2):
    res=[]
    for id in q1.keys():
        res.append({'department_id':id,'number_of_orders':q1[id],'number_of_first_orders':q2[id],'percentage':(q2[id]/q1[id])})
    return res





# creation and writing into the final csv file
def output(q1):
    result=[]
    result.append(q1)



    with open(args.report_path,'w') as fh_report:
        wr =csv.writer(fh_report, quoting=csv.QUOTE_ALL)
     #   wr.writerow()





if __name__=='__main__':
    orders = get_input(args.order_products_path)
    products = get_input(args.products_path)
    results = merge(orders,products)
    print(results)
    q1 = number_of_orders(results)
    print(q1)
    q2 = number_of_first_orders(results)
    print(q2)
    q3 = percentage(q1,q2)
    print(q3)