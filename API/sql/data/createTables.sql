/* createAPI.sql -- creates SQL tables for drinkbase API */

--TODO: add NOT NULL to everything once data are complete

--recipes: quantity of ingredients in each drink
DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
  name TEXT NOT NULL,
  ingredient TEXT NOT NULL,
  unit TEXT NOT NULL,
  amount REAL NOT NULL,
  PRIMARY KEY(name, ingredient)
  FOREIGN KEY(ingredient) REFERENCES ingredients(ingredient)
  FOREIGN KEY(name) REFERENCES prep(name)
);
--ingredients: info on each drink ingredient
DROP TABLE IF EXISTS ingredients;
CREATE TABLE ingredients (
  ingredient TEXT NOT NULL PRIMARY KEY,
  ingClass TEXT NOT NULL,
  ingAbv REAL NOT NULL,
  sweetness REAL,
  brightness REAL
);
--prep: how to build the drink
DROP TABLE IF EXISTS prep; 
CREATE TABLE prep (
  name TEXT NOT NULL PRIMARY KEY,
  style TEXT,
  glass TEXT,
  garnish TEXT,
  notes BLOB
);
