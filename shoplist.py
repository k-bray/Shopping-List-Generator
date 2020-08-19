import pandas as pd
from pandas import DataFrame
import csv
from csv import writer, reader
import re

# directory where python file and recipe_master saved
path = 'C:\\Users\\kerry\\dev\\shopping_list'
recipe_master = 'recipe_master.csv'  # name of recipe master csv file


def recipe_list(filename=recipe_master):
    # gets list of available recipes from master recipe csv file
    with open(filename, "r") as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header != None:
            recipes = list(csv_reader)
    recipename_dict = {}
    for recipe in recipes:
        recipename_dict[recipe[0]] = recipe[1]
    return recipes, recipename_dict


def input_recipe():
    # user can input ingredients for a recipe, save to csv file, and add to master recipe csv
    meal_name = input("\n\nMeal name: ")
    meal_dict = {}
    originalservings = int(input("Number of servings: "))
    i = 1
    arewefinished = 'N'

    while True:
        while arewefinished == 'N':
            ingredient = (
                input(f"Ingredient {i} (when done, type 'fin'): ")).lower()

            if ingredient == 'fin':
                break
            else:
                if ingredient in meal_dict:
                    edit_amount = (input(
                        f"\n{ingredient} already exists in this recipe! Edit amount? (Y/N): ")).upper()
                    if edit_amount == "Y":
                        print(
                            f"\nExisting amount of {ingredient}: {meal_dict[ingredient]}")
                        amount = input(f"Updated amount of {ingredient}: ")

                else:
                    amount = input(f"Amount of {ingredient}: ")

                meal_dict.update({ingredient: amount})

                i += 1
                continue

        meal_data = DataFrame(list(meal_dict.items()),
                              columns=['Ingredient', 'Amount'])

        arewefinished = (input(
            f"Is this all the ingredients for {meal_name}?:\n\n {meal_data} \n\n (Y/N): ")).upper()
        if arewefinished == "Y":
            break
        else:
            continue

    print("\nAll finished!\n")
    meal = input("What do you want to save your recipe as?: ")

    meal_csv = path + '\\meals\\' + f"{meal}.csv"
    meal_data.to_csv(meal_csv, index=False)

    def append_list_as_row(file_name, list_of_elem):
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)
    row_contents = [meal, meal_name, originalservings]
    append_list_as_row(recipe_master, row_contents)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def ingredient_adjust(originalservings, servings, ingredients):
    # adjusts ingredients for a meal based on stated servings
    scale = servings / originalservings
    for key, value in ingredients.items():
        valuelist = value.split()
        if len(valuelist) == 1:

            if is_number(value):
                n_ingredient = round((float(value) * scale), 1)
                if str(n_ingredient)[-1] == '0':
                    n_ingredient = int(n_ingredient)  # remove .0
                ingredients[key] = str(n_ingredient)

            elif value[-1:] == 'g' and is_number(value[:-1]):
                n_ingredient = float(value[:-1]) * scale
                ingredients[key] = str(int(n_ingredient)) + value[-1:]

            elif value[-1:] == 'l' and is_number(value[:-1]):
                n_ingredient = float(value[:-1]) * scale
                ingredients[key] = str(int(n_ingredient)) + value[-1:]

            elif value[-2:] == 'ml' and is_number(value[:-2]):
                n_ingredient = float(value[:-2]) * scale
                ingredients[key] = str(int(n_ingredient)) + value[-2:]

            else:
                if str(scale)[-1] == '0':
                    ingredients[key] = value + f'(x{(int(scale))})'
                else:
                    ingredients[key] = value + f'(x{float(round(scale, 1))})'

        elif len(valuelist) > 1:
            if is_number(valuelist[0]):
                n_ingredient = float(valuelist[0]) * scale
                n_ingredient = round(n_ingredient, 1)
                if str(n_ingredient)[-1] == '0':
                    n_ingredient = int(n_ingredient)  # remove .0
                valuelist[0] = str(n_ingredient)
                ingredients[key] = (' ').join(valuelist)

            else:
                if (str(scale))[-1] == 0:
                    ingredients[key] = value + f'(x{int(scale)})'
                else:
                    ingredients[key] = value + f'(x{round(scale, 1)})'
    return ingredients


def add_meal(meal_dict, meal_original_dict):
    # adds a meal from the available meals in master recipe csv to the shopping list
    add_meal = 0
    recipes, recipename_dict = recipe_list()

    while add_meal == 0:
        print("\nPlease enter the corresponding number of the meal you want to add to the shopping list.\n")

        for i in range(len(recipes)):
            print(f"{i}: {recipes[i][1]} ({recipes[i][2]} servings)")
        meal_i = (input("\nMeal no.: ")).lower()

        if int(meal_i) in range(len(recipes)):
            meal = recipes[int(meal_i)][0]
            meal_name = recipes[int(meal_i)][1]
            originalservings = int(recipes[int(meal_i)][2])

        else:
            print("\nDidn't catch that, try again.")
            continue

        servings = int(input(
            f"\nHow many servings of {meal_name}? ({originalservings} servings in original recipe): "))

        meal_dict[meal] = servings
        meal_original_dict[meal] = originalservings

        print(f"\n{servings} servings of {meal_name} added to the list")
        add_meal = 1

    return meal_dict, meal_original_dict


def remove_meal(meal_dict, recipename_dict, recipes):
    # remove meal from shopping list
    newdict = {}
    print("\nWhich meal do you want to remove?\n")
    i = 0
    for m, s in meal_dict.items():
        newdict[i] = m
        print(f"{i}: {recipename_dict[m]} ({s} servings)")
        i += 1
    meal_to_remove = input("\nPlease input corresponding number: \n")
    meal_dict.pop(newdict[int(meal_to_remove)])
    print(
        f"\n{(recipename_dict[newdict[int(meal_to_remove)]])} removed from list\n")

    return meal_dict


def change_servings(meal_dict, recipename_dict, recipes):
    # edit servings of meal on shopping list
    newdict = {}
    print("\nWhich meal do you want to change the servings for?\n")
    i = 0
    for m, s in meal_dict.items():
        newdict[i] = m
        print(f"{i}: {recipename_dict[m]} ({s} servings)")
        i += 1
    meal_to_edit = input("\nPlease input corresponding number: ")
    new_servings = input("\nNew serving size: ")
    meal_dict[newdict[int(meal_to_edit)]] = new_servings
    print(
        f"\n{(recipename_dict[newdict[int(meal_to_edit)]])} changed to {new_servings} servings\n")

    return meal_dict


def combine_amounts(ingredients):
    # combines all similar amounts from ingredient amounts (e.g. 100g, 50g; 1 tsp, 3 tsp) to create clean ingredients list
    for key, value in ingredients.items():
        comb_amount = []
        str_amount = []

        ingredients[key] = value + ','

        # change 'a handful' to '1 handful' for example
        regex_a = re.compile(r'a (?P<u> ?[a-zA-Z]*( [a-zA-Z]*)?)(,|$)')
        a = regex_a.search(value)
        if a:
            for match in regex_a.finditer(value):
                value = '1' + match.group('u')

        regex = re.compile(
            r'(?P<n>\d+|\d+\.\d+)(?P<u> ?[a-zA-Z]*( [a-zA-Z]*)?)(,|$)')
        i = 0
        u = regex.search(value)
        unit_list = []
        num_list = []
        if u:
            for match in regex.finditer(value):
                unit_list.append(match.group('u'))
            #print(f"raw unit list: {unit_list}")

            plural_dict = {'tins': 'tin',
                           'cans': 'can',
                           'cups': 'cup',
                           'pinches': 'pinch',
                           'handfuls': 'handful',
                           'sprigs': 'sprig',
                           'bunches': 'bunch',
                           'stalks': 'stalk',
                           'florets': 'floret',
                           'cloves': 'clove',
                           'bulbs': 'bulb'}

            def convert_plurals(unit, conversion):
                def translate(match):
                    word = match.group(0)
                    if word in conversion:
                        return conversion[word]
                    return word

                return re.sub(r'\w+', translate, unit)

            new_unit_list = []
            for unit in unit_list:
                newunit = convert_plurals(unit, plural_dict)
                new_unit_list.append(newunit)

            unit_list = new_unit_list
            

            unit_list = list(dict.fromkeys(unit_list))

            for unit in unit_list:
                amountslist = []
                if unit == '':
                    regex_num = re.compile(r'(\d+|\d+\.\d+)(,|$)')
                    for n in regex_num.findall(value):
                        n_amount = (list(n))[0]

                        amountslist.append(float(n_amount))

                    amount = sum(amountslist)
                    s_amount = str(amount)
                    if s_amount[-2:] == '.0':
                        amount = int(amount)
                    else:
                        amount = float(amount)
                    comb_amount.append(amount)

                else:
                    amountslist = []
                    regex2 = re.compile(fr'(\d+|\d+\.\d+)({unit})')
                    for n in regex2.findall(value):
                        n_amount = (list(n))[0]

                        amountslist.append(float(n_amount))
                    amount = sum(amountslist)
                    s_amount = str(amount)
                    if s_amount[-2:] == '.0':
                        amount = int(amount)
                    else:
                        amount = float(amount)

                    amount_unit = str(amount) + unit
                    comb_amount.append(amount_unit)

            

        x = value.split(", ")
        for x in x:
            if x[0].isalpha():
                str_amount.append(x)

        

        comb_amount = [str(a) for a in comb_amount]
        full_amount = comb_amount + str_amount
        ingredients[key] = ', '.join(full_amount)

        
    return ingredients


def shopping_list():
    print("\n--------------------------------\n*   SHOPPING LIST GENERATOR   *\n--------------------------------\n")
    meal_dict = {}
    meal_original_dict = {}
    ingredients = {}
    recipes, recipename_dict = recipe_list()

    while True:
        if meal_dict == {}:
            print("\n\nMeal list is empty.")
        else:
            print("\n--------Current meal list--------\n")
            for m, s in meal_dict.items():
                print(f"{recipename_dict[m]} ({s} servings)")
            print("\n---------------------------------")

        meal_edit = (input("\n\n A: Add a meal to the list.\n B: Remove a meal from the list.\n C: Change the serving size for a meal.\n D: Confirm meals and generate shopping list.\n E: Exit.\n  ->  ")).upper()

        if meal_edit == "A":
            meal_dict, meal_original_dict = add_meal(
                meal_dict, meal_original_dict)
            continue
        elif meal_edit == "B":
            meal_dict = remove_meal(meal_dict, recipename_dict, recipes)
            continue
        elif meal_edit == "C":
            meal_dict = change_servings(meal_dict, recipename_dict, recipes)
            continue
        elif meal_edit == "D":

            for m, s in meal_dict.items():
                mfile = path + '\\meals\\' + f"{m}.csv"
                with open(mfile, mode="r", encoding="utf-8-sig") as infile:
                    mealreader = reader(infile,)
                    header = next(mealreader)
                    if header != None:
                        DICT = {rows[0]: rows[1]
                                for rows in mealreader if len(rows) == 2}
                    recipe_ingredients = DICT

                ingredient_adjust(
                    int(meal_original_dict[m]), int(s), recipe_ingredients)

                # check if ingredient already somewhere in main ingredients dictionary - if so append to existing key
                for key, value in recipe_ingredients.items():
                    if key in ingredients:
                        ingredients[key] = ingredients[key] + ", " + value
                    else:
                        ingredients[key] = value

            ingredients = {key.lower(): value for key,
                           value in ingredients.items()}

            print(f"Ingredients dict: {ingredients}")

            # clean up combined ingredients list - combine amounts together for each ingredient
            ingredients = combine_amounts(ingredients)

            # save ingredients dictionary as data frame and export to CSV

            ingredients_data = DataFrame(list(sorted(ingredients.items())), columns=[
                                         'Ingredient', 'Amount'])

            print("All finished! Here's your shopping list:")
            print(ingredients_data)

            # for generating a file name for exported shopping list
            date = input("Today's date (DDMMYY): ")
            i = 2
            csv_name = f'shopping_list_{date}_1.csv'
            while i > 0:
                try:
                    f = open(csv_name)
                    csv_name = f'shopping_list_{date}_{i}.csv'
                    i += 1
                    f.close
                except:
                    ingredients_data.to_csv(csv_name, index=False)
                    i = 0

            break
        elif meal_edit == "E":
            break
        else:  # invalid input
            print(
                "\nPlease type the corresponding letter of the option you want to select.\n")
            continue


def shopping_helper():
    # user interface
    print("\nWelcome to the grocery shopping helper! What can I do for you?\n")
    nav = (input(" A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: Forgot why I came in... Bye!\n  ->  ")).upper()

    while nav != '':
        if nav == "A":  # View saved recipes
            recipes, recipename_dict = recipe_list(filename=recipe_master)
            print("\n-----------Saved meals-----------\n")
            for i in range(len(recipes)):
                print(f"{recipes[i][1]} ({recipes[i][2]} servings)")
            print("\n---------------------------------\n")
            nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  ->  ")).upper()
            continue
        if nav == "B":  # Add to saved recipes
            input_recipe()
            nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  ->  ")).upper()
            continue
        if nav == "C":  # Generate shopping list
            shopping_list()
            nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  -> ")).upper()
            continue
        if nav == "D":  # Exit
            print("\nUntil next time!\n")
            break


shopping_helper()
