# of rows using Python 
import xlrd 
  
loc = ('test.xlsx') 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
names = [sheet.row_values(row)[2] for row in range(1, sheet.nrows)]

print(names)
