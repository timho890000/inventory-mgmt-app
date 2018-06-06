import csv
import os

departments = ["snacks","pantry","beverages","frozen","personal care","dairy eggs","household","babies","meat seafood","dry goods pasta"]
aisles = ["cookies cakes","spices seasonings","tea","frozen meals","marinades meat preparation","cold flu allergy","juice nectars","frozen produce","yogurt","water seltzer sparkling water","refrigerated","frozen dessert","dish detergents","diapers wipes","ice cream toppings","poultry counter","frozen pizza","grains rice dried goods"]

def menu(username, products_count):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome to our application, {username}!
    There are currently {products_count} products in the database.

        Operation | Description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset to default inventory
        'Finish'  | Close the application
     """ # end of multi- line string. also using string interpolation
    return menu

def second_menu(username, products_count):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    There are currently {products_count} products.
    Please enter your next operation, {username}!
    -----------------------------------
        Operation | Description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset to default inventory
        'Finish'  | Close the application
     """ # end of multi- line string. also using string interpolation
    return menu

def read_products_from_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []
    #TODO: open the file and populate the products list with product dictionaries
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            #print(row["name"], row["price"])
            products.append(dict(row))

    return products #returns list of products

def list_products_from_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print("------------------------")
    print("Current list of products")
    print("------------------------")
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print("ID: "+row['id']+"| Name: "+row['name']+"| Department: "+row['department']+"| Aisle: "+row['aisle']+"| Price: "+"(${0:.2f})".format(float(row['price'])))#"(${0:.2f})".format(raw_total*1.08875)
    print()

def matching_product(product_identifier,products):
    products_list = [p for p in products if p["id"] == product_identifier] #makes a list of p in products that have product ID as ID. (will only have one item in this case)
    return products_list[0]

def show_product_from_file(filename):

    pid_to_show = input("Please input a product ID to show: ")
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        products = list(reader)
        while True:
            try:
                shown_product = matching_product(pid_to_show,products)#pid is not an integer !!!
                print("ID: "+shown_product['id']+"| Name: "+shown_product['name']+"| Department: "+shown_product['department']+"| Aisle: "+shown_product['aisle']+"| Price: "+"(${0:.2f})".format(float(shown_product['price'])))
                break
            except:
                pid_to_show = input("ID does not exist. Please enter another ID: ")

def update_product_from_file(filename):
    pid_to_update = input("Please input a product ID to update: ")
    products = read_products_from_file(filename)
    while True:
        try:
            updating_product = matching_product(pid_to_update,products) #this is a dictionary of one product
            break
        except:
            pid_to_update = input("ID does not exist. Please enter another ID: ")
    product_name = input("OK. What is the product's new name: (currently: "+updating_product["name"]+")")
    product_aisle = (input("OK. What is the product's new aisle: (currently: "+updating_product["aisle"]+")")).lower()
    while True:
        if(product_aisle not in aisles):
            print("Aisle does not exist. Please choose from the following aisles, or type 'new aisle' to create a new one:  ")
            for a in aisles:
                print(a)
            print()
            product_aisle = input().lower()
            if(product_aisle.title() == "New Aisle"):
                product_aisle = (input("What is the name of the new aisle? ")).lower()
                aisles.append(product_aisle)
                break
            else:
                continue
        else:
            break
    product_department = (input("OK. What is the product's new department: (currently: "+updating_product["department"]+")")).lower()
    while True:
        if(product_department not in departments):
            print("Department does not exist. Please choose from the following departments or type 'new department' to create a new one:  ")
            for d in departments:
                print(d)
            product_department = input().lower()
            if(product_department.title() == "New Department"):
                product_department = (input("What is the name of the new department? ")).lower()
                departments.append(product_department)
                break
            else:
                continue
        else:
            break
    product_price = input("OK. What is the product's new price: (currently: "+updating_product["price"]+")")
    while True:
        try:
            product_price = float(product_price)
            if(num_after_point(product_price)>2 or product_price<0):
                product_price = input("Please input a positive price formatted as a number with two decimal places, like 0.77: ")
                continue
            else:
                break
        except:
            product_price = input("Please input a price formatted as a number with two decimal places, like 0.77: ")
    updating_product["name"] = product_name
    updating_product["aisle"] = product_aisle
    updating_product["department"] = product_department
    updating_product["price"] = product_price
    print("Product has been updated!")
    print("ID: "+str(updating_product['id'])+"| Name: "+updating_product['name']+"| Department: "+updating_product['department']+"| Aisle: "+updating_product['aisle']+"| Price: "+"(${0:.2f})".format(float(updating_product['price'])))
    write_products_to_file(filename,products)

def destroy_product_from_file(filename):
    pid_to_destroy = input("Please input a product ID to destroy: ")
    products = read_products_from_file(filename)
    while True:
        try:
            destroying_file = matching_product(pid_to_destroy,products) #this is a dictionary of one product
            break
        except:
            pid_to_destroy = input("ID does not exist. Please enter another ID: ")
    number = products.index(destroying_file)
    del products[number]
    write_products_to_file(filename,products)
    print("Product ID# "+str(pid_to_destroy)+" has been destroyed!")
    #write_products_to_file(filename,products)

def write_products_to_file(filename, products):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id","name","aisle","department","price"] , lineterminator = '\n')
        writer.writeheader() # uses fieldnames set above
        for p in products:
            writer.writerow(p)

        #writer.writerow({"city": "New York", "name": "Yankees"})
        #writer.writerow({"city": "New York", "name": "Mets"})
        #writer.writerow({"city": "Boston", "name": "Red Sox"})
        #writer.writerow({"city": "New Haven", "name": "Ravens"})

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

def create_product_from_file(filename):
    products = read_products_from_file(filename)
    last_id=0
    if(len(products)==0):
        last_id=0
    else:
        last_id = products[-1]["id"]
    #print(last_id)
    product_id = int(last_id)+1
    product_name = input("OK. Please input the product's name: ")
    product_aisle = input("OK. Please input the product's aisle: ").lower()
    while True:
        if(product_aisle not in aisles):
            print("Aisle does not exist. Please choose from the following aisles, or type 'new aisle' to create a new one: ")
            for a in aisles:
                print(a)
            product_aisle = input().lower()
            if(product_aisle.title() == "New Aisle"):
                product_aisle = input("What is the name of the new aisle? ").lower()
                aisles.append(product_aisle)
                break
            else:
                continue
        else:
            break
    product_department = input("OK. Please input the product's department: ").lower()
    while True:
        if(product_department not in departments):
            print("Department does not exist. Please choose from the following departments, or type 'new department' to create a new one: ")
            for d in departments:
                print(d)
            product_department = input().lower()
            if(product_department.title() == "New Department"):
                product_department = input("What is the name of the new department? ").lower()
                departments.append(product_department)
                break
            else:
                continue
        else:
            break
    product_price = input("OK. Please input the product's price: ")

    while True:
        try:
            product_price = float(product_price)
            if(num_after_point(product_price)>2 or product_price<0):
                product_price = input("Please input a positive price formatted as a number with two decimal places, like 0.77: ")
                continue
            else:
                break
        except:
            product_price = input("Please input a price formatted as a number with two decimal places, like 0.77: ")
    new_product = {"id":product_id,"name":product_name,"aisle":product_aisle,"department":product_department,"price":product_price}
    products.append(new_product)
    write_products_to_file(filename,products)
    print("New product has been created!")
    print("ID: "+str(new_product['id'])+"| Name: "+new_product['name']+"| Department: "+new_product['department']+"| Aisle: "+new_product['aisle']+"| Price: "+"(${0:.2f})".format(float(new_product['price'])))

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

def run():
    filename = "products.csv"
    # First, read products from file...
    products = read_products_from_file(filename)
    username = input("Please enter your name: ")
    # Then, prompt the user to select an operation...
    print(menu(username,products_count=len(products))) #TODO instead of printing, capture user input

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    #TODO: handle selected operation


    while True:
        action = input("Please select an operation: ").title()
        if(action=="List"):
            list_products_from_file(filename)
        elif(action=="Show"):
            show_product_from_file(filename)
        elif(action=="Create"):
            create_product_from_file(filename)
        elif(action=="Update"):
            update_product_from_file(filename)
        elif(action=="Destroy"):
            destroy_product_from_file(filename)
        elif(action=="Reset"):
            reset_products_file()
        elif(action=="Finish"):
            break
        else:
            print()
            print("Operation is not recognized. Please choose from 'List', 'Show', 'Create', 'Update', 'Destroy', 'Reset', or 'Finish'")
            print()
            continue
        products=read_products_from_file(filename)
        print(second_menu(username,products_count=len(products))) #TODO instead of printing, capture user input
    print()
    print("--------------------------------------")
    print("Thank you for using our application!")
    print("--------------------------------------")
    # Finally, save products to file so they persist after script is done...
    #write_products_to_file(products=products)

    # only prompt the user for input if this script is run from the command-line
    # this allows us to import and test this application's component functions

if __name__ == "__main__": ## this will run only when this program is invoked from the command line. So if we run the reset function, it wont run the whole thing
    run()
