import csv

lines = list()

filter_by = "Kurisu"

with open('../data/kurisu_dialogue.csv', 'r', encoding='utf-8', errors='ignore') as readFile:
    reader = csv.reader(readFile, delimiter="|")

    for row in reader:
        if row[0].strip() == filter_by:
            print(row[1])
            lines.append(row[1])

with open('../data/amadeus_dialogue.csv', 'w', encoding='utf-8') as writeFile:
    new_lined_lines = [ line + "\n" for line in lines ]
    writeFile.writelines(new_lined_lines)