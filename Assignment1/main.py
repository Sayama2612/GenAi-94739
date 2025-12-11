'''Write a Python program that takes a sentence from the user and prints:

Number of characters

Number of words

Number of vowels

Hint: Use split(), loops, and vowel checking.'''

import analyze_sentence as an

sentence = input("Enter a sentence :")
num_char, num_words, num_vowels = an.analyze(sentence)
print("Number of characters :", num_char)
print("Number of words :", num_words)
print("Number of vowels :", num_vowels)

'''Count Even and Odd Numbers

Take a list of numbers as input (comma-separated).

Count how many are even and how many are odd.

Print results.

Example Input:
10, 21, 4, 7, 8'''

import count

numbers = input("Enter numbers separated by commas: ")

num_list = [int(x.strip()) for x in numbers.split(",")]

even_count, odd_count = count.even_odd_count(num_list) 

print("Even numbers:", even_count)
print("Odd numbers:", odd_count)




'''Given a CSV file Products.csv with columns:
Write a Python program to:'''

import csv

# a) Read the CSV file
filename = "products.csv"

rows = []    

with open(filename, mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        rows.append(row)


# b) Print each row in clean format
print("\n--- Product Details ---")
for r in rows:
    print(f"ID: {r['product_id']}, Name: {r['product_name']}, Category: {r['category']}, "
          f"Price: {r['price']}, Quantity: {r['quantity']}")

# c) Total number of rows
print("\nTotal number of rows:", len(rows))

# d) Total number of products priced above 500
above_500 = [r for r in rows if float(r['price']) > 500]
print("Products priced above 500:", len(above_500))

# e) Average price of all products
avg_price = sum(float(r['price']) for r in rows) / len(rows)
print("Average price of products:", avg_price)

# f) List all products of a specific category
user_category = input("\Enter category to filter products: ")

filtered = [r for r in rows if r['category'].lower() == user_category.lower()]

print("\nProducts in category:", user_category)
for r in filtered:
    print(f"{r['product_name']} - Rs.{r['price']}")

# g) Total quantity of all items in stock
total_quantity = sum(int(r['quantity']) for r in rows)
print("\nTotal quantity of items in stock:", total_quantity)
        