from typing import Set, List

import psycopg2
from flask import jsonify


class DrinkBase:
    def __init__(self, database):
        self.database = database
        self.connection = psycopg2.connect(
            host="localhost",
            dbname=self.database,
            user="postgres",
            password="password",
        )

        # self.cursor can be used to define any SQL query
        # use self.cursor.fetchall() to actually run query
        self.cursor = self.connection.cursor()

        # set of every drink named in the database
        self.cursor.execute("SELECT DISTINCT name FROM recipes")
        temp = set()
        for i in self.cursor:
            temp.add(i[0])
        self.all_drinks = temp

    def send_all_drinks(self) -> Set[str]:
        """returns sorted list of all drink names"""
        return self.all_drinks

    def calc_brightness(self, drink) -> float:
        """returns brightness value for 'drink' as a float"""
        self.cursor.execute(
            """
            SELECT 
                SUM(recipes.amount * units.conversion *
                ingredients.brightness)
            FROM recipes 
            INNER JOIN units ON recipes.unit = units.unit
            INNER JOIN ingredients ON recipes.ingredient =
                ingredients.ingredient
            WHERE recipes.name = %s
            GROUP BY recipes.name
            """,
            (drink,),
        )
        brightness = self.cursor.fetchone()
        try:
            return brightness[0]
        except IndexError:
            return 0

    def calc_sweetness(self, drink) -> float:

        """returns sweetness value of 'drink' as a float"""
        self.cursor.execute(
            """
            SELECT 
                SUM(recipes.amount * units.conversion *
                ingredients.sweetness)
            FROM recipes 
            INNER JOIN units ON recipes.unit = units.unit
            INNER JOIN ingredients ON recipes.ingredient =
                ingredients.ingredient
            WHERE recipes.name = %s
            GROUP BY recipes.name
            """,
            (drink,),
        )
        sweetness = self.cursor.fetchone()
        try:
            return sweetness[0]
        except IndexError:
            return 0

    def calc_alcohol_units(self, drink) -> float:

        """returns alcohol value of 'drink' as a float"""
        self.cursor.execute(
            """
            SELECT 
                SUM(recipes.amount * units.conversion *
                    ingredients.ingAbv)
            FROM recipes 
            INNER JOIN units ON recipes.unit = units.unit
            INNER JOIN ingredients ON recipes.ingredient =
                ingredients.ingredient
            WHERE recipes.name = %s
            GROUP BY recipes.name
            """,
            (drink,),
        )
        alcohol_units = self.cursor.fetchone()
        try:
            return alcohol_units[0]
        except IndexError:
            return 0

    def get_style(self, drink) -> str:
        """returns style of 'drink' as string"""
        self.cursor.execute(
            """
            SELECT style 
            FROM prep 
            WHERE name = %s
            """,
            (drink,),
        )
        style = self.cursor.fetchone()
        try:
            return style[0]
        except IndexError:
            return ""

    def get_glass(self, drink) -> str:
        """returns glass of 'drink' as string"""
        self.cursor.execute(
            """
            SELECT glass 
            FROM prep 
            WHERE name = %s
            """,
            (drink,),
        )
        glass = self.cursor.fetchone()
        try:
            return glass[0]
        except IndexError:
            return ""

    def get_garnish(self, drink) -> str:
        """returns garnish of 'drink' as string"""
        self.cursor.execute(
            """
            SELECT garnish 
            FROM prep 
            WHERE name = %s
            """,
            (drink,),
        )
        garnish = self.cursor.fetchone()
        try:
            return garnish[0]
        except IndexError:
            return ""

    def calc_volume(self, drink) -> float:
        """returns volume of 'drink' as float"""
        self.cursor.execute(
            """
            SELECT 
                SUM (recipes.amount * units.conversion * (1.0 + style.melt))
            FROM recipes
            INNER JOIN units ON recipes.unit = units.unit
            INNER JOIN prep ON recipes.name = prep.name
            INNER JOIN style ON prep.style = style.style
            WHERE recipes.name = %s
            GROUP BY recipes.name
            """,
            (drink,),
        )
        volume = self.cursor.fetchone()
        try:
            return volume[0]
        except IndexError:
            return 0

    def get_notes(self, drink) -> str:
        """returns notes for 'drink' as string"""
        self.cursor.execute(
            """
            SELECT notes 
            FROM prep 
            WHERE name = %s
            """,
            (drink,),
        )
        notes = self.cursor.fetchone()
        try:
            return notes[0]
        except IndexError:
            return ""

    def ing_search(self, ingredient) -> List[str]:
        """returns drinks that contain 'ingredient' as a list"""
        self.cursor.execute(
            """
            SELECT DISTINCT name 
            FROM recipes 
            WHERE LOWER(ingredient) LIKE %s
            ORDER BY name
            """,
            ("%" + ingredient.lower() + "%",),
        )
        drinks = []
        for i in self.cursor:
            drinks.append(i[0])
        return drinks

    def get_ing_string(self, drink) -> str:
        """returns ingredients in 'drink' as formatted string for API"""
        self.cursor.execute(
            """
            SELECT ingredient 
            FROM recipes 
            WHERE name = %s
            """,
            (drink,),
        )
        ingredients = []
        for i in self.cursor:
            ingredients.append(i[0])
        ingredients.sort()
        ingredient_string = ""
        for i in range(len(ingredients) - 1):
            ingredient_string += ingredients[i] + " | "
        ingredient_string += ingredients[-1]

        return ingredient_string

    def get_recipe(self, drink) -> List[dict]:
        """returns full recipe for 'drink'"""
        self.cursor.execute(
            """
            SELECT ingredient
            FROM recipes
            WHERE name = %s
            """,
            (drink,),
        )
        ingredients = []
        for i in self.cursor:
            ingredients.append(i[0])
        recipe = []
        for i in ingredients:
            self.cursor.execute(
                """
                SELECT amount 
                FROM recipes
                WHERE name = %s AND ingredient = %s
                """,
                (drink, i),
            )
            amount = self.cursor.fetchone()
            amount = amount[0]
            self.cursor.execute(
                """
                SELECT unit 
                FROM recipes 
                WHERE name = %s AND ingredient = %s
                """,
                (drink, i),
            )
            unit = self.cursor.fetchone()
            unit = str(unit[0])
            recipe.append({"Ingredient": i, "Amount": amount, "Unit": unit})
        return recipe

    def name_search(self, name_query) -> List[str]:
        """returns drink names matching 'nameQuery'"""
        self.cursor.execute(
            """
            SELECT DISTINCT name 
            FROM recipes 
            WHERE LOWER(name) LIKE %s
            ORDER BY name
            """,
            ("%" + name_query.lower() + "%",),
        )
        drinks = []
        for i in self.cursor:
            drinks.append(i[0])
        return drinks

    def getBuild(self, drink):
        """returns how to build 'drink' as a string"""
        # build and glass notes
        self.cursor.execute(
            """
            SELECT 
              (SELECT regexp_replace(
                (SELECT style.description FROM style WHERE style.style = prep.style),
                '@',
                prep.glass))
            FROM prep
            INNER JOIN style on prep.style = style.style
            WHERE prep.name = %s
            """,
            (drink,),
        )
        build = self.cursor.fetchone()

        # garnish notes
        self.cursor.execute(
            """
            SELECT 
              CASE WHEN prep.garnish = 'none'
                THEN ' No garnish.'
              ELSE ' Garnish with ' || prep.garnish || '.'
              END
              FROM prep
              WHERE prep.name = %s
              """,
            (drink,),
        )
        garnish = self.cursor.fetchone()
        try:
            return build[0] + garnish[0]
        except IndexError:
            return ""

    def sendData(self, drink):
        """returns API-ready data for 'drink' as a dictionary"""
        # define structure to be jsonified
        data = {}

        # results for each drink
        alcohol = self.calc_alcohol_units(drink)
        volume = self.calc_volume(drink)
        abv = alcohol / volume
        bright = self.calc_brightness(drink)
        build = self.getBuild(drink)
        ingredientString = self.get_ing_string(drink)
        garnish = self.get_garnish(drink)
        glass = self.get_glass(drink)
        notes = self.get_notes(drink)
        style = self.get_style(drink)
        sweet = self.calc_sweetness(drink)

        # add values to dictionary
        data["ABV"] = abv
        data["AlcoholUnits"] = alcohol
        data["Brightness"] = bright
        data["Build"] = build
        data["IngredientString"] = ingredientString
        data["Garnish"] = garnish
        data["Glass"] = glass
        data["Notes"] = notes
        data["Style"] = style
        data["Sweetness"] = sweet
        data["Volume"] = volume

        return data

    def sendRecipe(self, drinks):
        """returns full dataset for list of 'drinks' as JSON"""

        drinkList = []
        for i in drinks:
            drinkDict = {}
            recipe = self.get_recipe(i)
            data = self.sendData(i)
            recipeDict = {"Recipe": recipe}
            drinkDict["Name"] = i
            drinkDict["Recipe"] = recipe
            drinkDict["Data"] = data
            drinkList.append(drinkDict)
        drinks = jsonify({"Drinks": drinkList})
        return drinks
