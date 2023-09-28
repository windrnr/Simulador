import csv

def r_csv(path, dic_p): 
    pid = 1
    with open(path, newline='') as process_file:
        reader = csv.reader(process_file, delimiter=',')
        for row in reader:
            dic_p[pid] = row
            pid = pid + 1
    
    return dic_p
