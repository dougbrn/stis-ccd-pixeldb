import csv

#File used to generate static pixel entity maps for initial data ingestion
num_rows = 1024 #CCD Rows
num_cols = 1024 #CCD Columns

with open("pixel_map.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in range(num_rows):
        for col in range(num_cols):
            writer.writerow([row,col,'CCD'])
