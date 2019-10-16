import csv

results = []
with open('data.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        results.append(row[0])

print(results)