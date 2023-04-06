# This script takes the movies_tagdl.csv file, changes all the tags into common tags (if those are available) and excludes the rest
import pandas as pd
import csv

#common_tags_dict = pd.read_csv("common_tags.csv").to_dict()
#print(common_tags_dict)

common_tags_dict = {}

with open("common_tags2.csv", 'r') as common_tags_file: # muuta: common_tags2.csv
    common_tags_dict = csv.reader(common_tags_file)
    common_tags_dict = {rows[0]:rows[1] for rows in common_tags_dict}

#print(len(common_tags_dict))
#print(common_tags_dict)

del common_tags_dict['common_tag']
print(len(common_tags_dict))
print(common_tags_dict)

counter = 1
discarded = 0

with open("./book_dataset/scores/tagdl.csv", "r") as file, open("books_tagdl_common_all.csv", "w", newline='') as file2: # testissä "books_tagdl.csv"
    rows = csv.reader(file)
    new_rows = csv.writer(file2)
    header_row = ["item_id", "score", "common_tag_id"] # "tag" ekana
    new_rows.writerow(header_row)
    for row in rows:
        print(counter)
#        print(row)
#        print(row[0])
        if (row[0]) in common_tags_dict:
#            print(f"{row[0]} is in dictionary")
            new_row = [row[1], row[2], str(common_tags_dict[row[0]])] # row[0] entinen tagi
#            print(new_row)
            new_rows.writerow(new_row) # PALAUTA TÄMÄ
#            new_row.to_csv(file2, mode='a', index=False, header=False)
        else:
#            print(f"{row[0]} is not in dictionary")
            discarded +=1
        counter +=1

    file.close()
    file2.close()

print(f"{counter} lines handled, {discarded} discarded")
