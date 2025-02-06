import csv

reader_file = 'products.csv'
writer_file = 'products_summary.csv'
products = []
category_totals = {}

with open(reader_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        product = {
            'product_id': int(row['product_id']),
            'product_name': row['product_name'],
            'category': row['category'],
            'price': float(row['price']),
            'quantity': int(row['quantity'])
        }

        if product['category'] not in category_totals:
            category_totals[product['category']] = 0
        category_totals[product['category']] += product['price']*product['quantity']

        products.append(product)
    print(products)

with open(writer_file, 'w', newline="") as file:
    header_names = ['product_id',
                    'product_name',
                    'category',
                    'total_value']

    writer = csv.DictWriter(file, header_names)
    writer.writeheader()

    for row in range(len(products)):
        names_products = {
            header_names[0]: products[row]['product_id'],
            header_names[1]: products[row]['product_name'],
            header_names[2]: products[row]['category'],
            header_names[3]: products[row]['price']*products[row]['quantity']
        }

        writer.writerow(names_products)

    writer.writerow({})

    for category, total in category_totals.items():
        writer.writerow({'category': category, 'total_value': total})
