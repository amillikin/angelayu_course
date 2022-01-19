from os import system
from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_machine = CoffeeMaker()
cash_register = MoneyMachine()
                                                                  
machineIsOn = True

while machineIsOn:
    valid_order = False                                                        
    valid_orders = ["off","report"]
    for item in menu.get_items().split("/"):
        if not item == "":
            valid_orders.append(item)
    customer_order = ""
    while not valid_order:
        prompt_string = "What would you like?\n"
        for item in valid_orders[2:len(valid_orders)+1]:
            menu_item = menu.find_drink(item)
            prompt_string += f"{menu_item.name.title()}: ${menu_item.cost}\n"
        customer_order = input(prompt_string + "> ").lower()
        valid_order = customer_order in valid_orders
        if not valid_order:
            print(f'"{customer_order} is not a valid order."')
    
    if customer_order == "off":
        machineIsOn = False
    elif customer_order == "report":
        coffee_machine.report()
        cash_register.report()
    else:
        ordered_item = menu.find_drink(customer_order)
        if (coffee_machine.is_resource_sufficient(ordered_item) and 
            cash_register.make_payment(ordered_item.cost)):
            coffee_machine.make_coffee(ordered_item)

    if not customer_order == "off":                                            
        order_again = input("Do you have another order? y(es)/n(o)").lower()   
        machineIsOn = order_again in ("yes", "y")                              
                                                                               
    system("clear")                  
