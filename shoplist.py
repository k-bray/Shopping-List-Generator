
import pandas as pd
from pandas import DataFrame
import csv
from csv import writer, reader

path = 'C:\\Users\\kerry\\dev\\shopping_list' #directory where python file and recipe_master saved
recipe_master = 'recipe_master.csv' #name of recipe master csv file

def recipe_list(filename = recipe_master):
	with open(filename,"r") as read_obj:
		csv_reader = reader(read_obj)
		header = next(csv_reader)
		if header != None:
			recipes = list(csv_reader)
	recipename_dict = {}
	for recipe in recipes:
		recipename_dict[recipe[0]] = recipe[1]
	return recipes, recipename_dict

def input_recipe():
	
	meal_name = input("\n\nMeal name: ")

	meal_dict = {}
	
	originalservings = int(input("Number of servings: "))
	#total_ingredients = int(input(f"How many ingredients does {meal_name} have?: "))

	i = 1
	arewefinished = 'N'
			
	while True:
		while arewefinished == 'N':
			ingredient = (input(f"Ingredient {i} (when done, type 'fin'): " )).lower()

			if ingredient == 'fin':
				break
			else:
				amount = input(f"Amount of {ingredient}: ")
			
				meal_dict.update( {ingredient : amount} )

				i += 1
				continue

		meal_data = DataFrame(list(meal_dict.items()),columns = ['Ingredient', 'Amount'])

		arewefinished = (input(f"Is this all the ingredients for {meal_name}?:\n\n {meal_data} \n\n (Y/N): ")).upper()
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



def ingredient_adjust(originalservings, servings, ingredients):
	def is_number(s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	scale = servings / originalservings
	for key,value in ingredients.items():
			
		valuelist = value.split()
		
		if len(valuelist) == 1:

			if is_number(value):
				n_ingredient = round((float(value) * scale), 1)
				if str(n_ingredient)[-1] == '0':
					n_ingredient = int(n_ingredient) #remove .0 
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
					ingredients[key] = value + ' ' + f'x{int(scale)}'
				else:
					ingredients[key] = value + ' ' + f'x{round(scale, 1)}'
		

		elif len(valuelist) > 1:
			if is_number(valuelist[0]):
				n_ingredient = float(valuelist[0]) * scale
				n_ingredient = round(n_ingredient, 1)
				if str(n_ingredient)[-1] == '0':
					n_ingredient = int(n_ingredient) #remove .0 
				valuelist[0] = str(n_ingredient)
				ingredients[key] = (' ').join(valuelist)
			
			else:
				if (str(scale))[-1] == 0:
					ingredients[key] = value + ' ' + f'x{int(scale)}'
				else:
					ingredients[key] = value + ' ' + f'x{round(scale, 1)}'
	return ingredients
	
def add_meal(meal_dict, meal_original_dict):
	
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

		servings = int(input(f"\nHow many servings of {meal_name}? ({originalservings} servings in original recipe): "))
	
		meal_dict[meal] = servings
		meal_original_dict[meal] = originalservings
	
		print(f"\n{servings} servings of {meal_name} added to the list")
		add_meal = 1
	
	return meal_dict, meal_original_dict

def remove_meal(meal_dict, recipename_dict, recipes):
	newdict = {}
	print("\nWhich meal do you want to remove?\n")
	i = 0
	for m, s in meal_dict.items():
		newdict[i] = m
		print(f"{i}: {recipename_dict[m]} ({s} servings)")
		i += 1
	meal_to_remove = input("\nPlease input corresponding number: \n")
	meal_dict.pop(newdict[int(meal_to_remove)])
	print(f"\n{(recipename_dict[newdict[int(meal_to_remove)]])} removed from list\n")

	return meal_dict

def change_servings(meal_dict, recipename_dict, recipes):
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
	print(f"\n{(recipename_dict[newdict[int(meal_to_edit)]])} changed to {new_servings} servings\n")

	return meal_dict

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
			meal_dict, meal_original_dict = add_meal(meal_dict, meal_original_dict)
			continue
		elif meal_edit == "B": 
			meal_dict = remove_meal(meal_dict, recipename_dict, recipes)
			continue
		elif meal_edit == "C":
			meal_dict = change_servings(meal_dict, recipename_dict, recipes)
			continue
		elif meal_edit == "D":

			for m, s in meal_dict.items():
				with open(f"{m}.csv", mode="r", encoding = "utf-8-sig") as infile:
					mealreader = reader(infile,)
					header = next(mealreader)
					if header != None:
						DICT = {rows[0]:rows[1] for rows in mealreader if len(rows) == 2}
					recipe_ingredients = DICT
				
				ingredient_adjust(int(meal_original_dict[m]), int(s), recipe_ingredients)
			
				
				#check if ingredient already somewhere in main ingredients dictionary - if so append to existing key
				for key, value in recipe_ingredients.items():
					if key in ingredients:
						ingredients[key] = ingredients[key] + ", " + value
					else:
						ingredients[key] = value
	
				

			#clean up combined ingredients list - combine amounts together for each ingredient
			for key, value in ingredients.items():
				amount_digit, amount_grams, amount_tsp, amount_tbsp, amount_litres, amount_mlitres, amount_string = [], [], [], [], [], [], []
				for x in value.split(", "):
					if x.isdigit():
						amount_digit.append(int(x))
			
					#e.g. '100g', '300ml' '1l'			
					elif x[-1] == "g" and x[:-1].isdigit():
						amount_grams.append(int(x[:-1]))

					elif x[-1] == "l" and x[:-1].isdigit():
						amount_litres.append(int(x[:-1]))

					elif x[-2] == "ml" and x[:-2].isdigit():
						amount_mlitres.append(int(x[:-1]))
				
					#e.g. '3 tbsp', '1 tsp'			
					elif x[-3:] == "tsp" and x[0].isdigit():
						amount_tsp.append(int(x[0]))
						
					elif x[-4:] == "tbsp" and x[0].isdigit():
						amount_tbsp.append(int(x[0]))
				
					#e.g. 'A handful', 'Pinch'			
					else: 
						amount_string.append(x)

				#for each ingredient, sum up the totals for each measure type
				total_digit = str(sum(amount_digit))
				total_grams = str(sum(amount_grams)) + "g"
				total_litres = str(sum(amount_litres)) + "l"
				total_mlitres = str(sum(amount_mlitres)) + "ml"
				total_tsp = str(sum(amount_tsp)) + " " + "tsp"
				total_tbsp = str(sum(amount_tbsp)) + " " + "tbsp" 
				total_string = ", ".join(amount_string)

				full_amounts = ''
				for total in [total_digit, total_grams, total_litres, total_mlitres, total_tsp, total_tbsp, total_string]:
					if total not in ['0', '0.0', '0g', '0l', '0ml', '0 tsp', '0 tbsp', '']:
						if full_amounts != '':
							full_amounts = full_amounts + ", " + total
						else:
							full_amounts = total
					else:
						continue


				ingredients[key] = full_amounts

			#save ingredients dictionary as data frame and export to CSV
			ingredients_data = DataFrame(list(ingredients.items()),columns = ['Ingredient', 'Amount'])

			print("All finished! Here's your shopping list:")
			print(ingredients_data)


			date = input("Today's date (DDMMYY): ") #for generating a file name for exported shopping list
			i = 2
			csv_name = f'shopping_list_{date}_1.csv'
			while i>0: 
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
		else:
			print("\nPlease type the corresponding letter of the option you want to select.\n")
			continue


def shopping_helper():
	
	print("\nWelcome to the grocery shopping helper! What can I do for you?\n")
	nav = (input(" A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: Forgot why I came in... Bye!\n  ->  ")).upper()

	while nav != '':
		if nav == "A": #View saved recipes
			recipes, recipename_dict = recipe_list(filename = recipe_master)
			print("\n-----------Saved meals-----------\n")
			for i in range(len(recipes)):
				print(f"{recipes[i][1]} ({recipes[i][2]} servings)")
			print("\n---------------------------------\n")
			nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  ->  ")).upper()
			continue
		if nav == "B": #Add to saved recipes
			input_recipe()
			nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  ->  ")).upper()
			continue
		if nav == "C": #Generate shopping list
			shopping_list()
			nav = (input("\nAnything else I can do for you?\n\n A: View saved recipes.\n B: Add a meal to saved recipes.\n C: Generate a shopping list.\n D: No thanks, bye!\n  -> ")).upper()
			continue
		if nav == "D": #Exit
			print("\nUntil next time!\n")
			break

shopping_helper()

