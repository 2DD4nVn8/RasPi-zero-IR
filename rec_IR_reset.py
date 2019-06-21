import csv

filename = "/home/pi/WorkSpace/IR_sender/IR_recode.csv"
f = open(filename, mode='w')
header_list = ["room","id","key","signal"]
writer = csv.writer(f, lineterminator='\n')

writer.writerow(header_list)

f.close()

