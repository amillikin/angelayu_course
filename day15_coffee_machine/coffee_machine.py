MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}


def generate_report(resources, coins_received):
    print(f"Water: {resources['water']}\n" + 
          f"Milk: {resources['milk']}\n" +
          f"Coffee: {resources['coffee']}\n" +
          f"Money: ${coins_received}")


def check_resources(beverage, resources):
    resources_insufficient = False
    insufficient_resources = ""
    for ingredient in MENU[beverage]["ingredients"].keys():
        if resources[ingredient] > MENU[beverage]["ingredients"][ingredient]:
            resources_insufficient = True
            insufficient_resources += f", {ingredient}"
    if resources_insufficient:
        print(f"Sorry, there is not enough {insufficient_resources}.")
    return resources_insufficient


def validate_coins(beverage):
    beverage_cost = MENU[beverage]["cost"]
    print(f"A {beverage} costs {beverage_cost}. Please insert coins.\n")
    sufficient_payment = False
    try_again = "yes"
    while not sufficient_payment and try_again in ("yes","y"):
        while True:
            try: 
                quarters = int(input("Quarter: "))
                dimes = int(input("Dimes: "))
                nickles = int(input("Nickles: "))
                pennies = int(input("Pennies: "))
            except ValueError:
                print("Sorry, that is not a valid coin amount.")
                continue
            else:
                break
        payment_received = {"quarters": quarters*.25,
                            "dimes": dimes*.1,
                            "nickles": nickles*.05,
                            "pennies": pennies*.01}
        if sum(payment_received.values()) >= beverage_cost:
            sufficient_payment = True
        else:
            try_again = input("Sorry, that's not enough money. Money refunded.\n" +
                              "Would you like to try again? y(es)/n(o)").lower()
            for coin in payment_received:
                payment_received[coin] = 0

    return sum(payment_received.values())


def make_order(beverage, resources):
    for ingredient in MENU[beverage]["ingredients"].keys():
        resources[ingredient] -= MENU[beverage]["ingredients"][ingredient]
    return resources


# for the sake of this exercise, we'll assume the machine is fully stocked
# each time it is turned on
resources_available = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

# and the coins are emptied, considering there is no persistence
total_coins_received = 0

machineIsOn = True

while machineIsOn:

    customer_order = ""
    while customer_order not in MENU.keys() or customer_order not in ("off", "report"):
        prompt_string = "What would you like?\n"
        for item in MENU:
            menu_item = item.title()
            item_cost = MENU[item].get("cost")
            prompt_string += f"{menu_item}: ${item_cost}"
        customer_order = input(prompt_string).lower()
    
    if customer_order == "off":
        machineIsOn = False
    elif customer_order == "report":
        generate_report(resources_available, total_coins_received)
    elif check_resources(customer_order, resources_available):
        customer_payment = validate_coins(customer_order)
        if customer_payment > 0:
            # make customer's order and decrement resources used
            resources_available = make_order(customer_order, resources_available)
            total_coins_received += customer_payment


