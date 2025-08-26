
import random

from torch import randint


cell_no = int(input("Enter the number of cells: "))
list_of_cell = []

for i in range(cell_no):
    list_of_cell.append(input("Enter cell type: ").lower())

cells_data = {}

for idx, cell_type in enumerate(list_of_cell, start=1):
    cell_key = f"cell_{idx}_{cell_type}"
    
    
    voltage = 3.2 if cell_type == "lfp" else 3.6
    min_voltage = 2.8 if cell_type == "lfp" else 3.2
    max_voltage = 3.6 if cell_type == "lfp" else 4.0
    current = 0.0
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)

    cells_data[cell_key] = {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage
    } 
print("\n--- Enter current (in Amperes) for each cell ---")
for key in cells_data:
    try:
        current = float(input(f"Enter current for {key}: "))
    except ValueError:
        print("Invalid input. Setting current to 0.")
        current = 0.0
    
    voltage = cells_data[key]["voltage"]
    cells_data[key]["current"] = current
    cells_data[key]["capacity"] = round(voltage * current, 2)

print("\n--- Updated Cell Data ---")
for key, values in cells_data.items():
    print(f"{key}: {values}")  
    







# details = {
#     'nmc' : {
#         'nomial_voltage': 3.2,
#         'min_voltage' : 2.8,
#         'max_voltage' : 3.6,
#         'capacity' : 0,
#         'current' : 0,
#         'temperature' : random.randint(20, 30)
#     },
#     'lfp' : {
#         'nomial_voltage': 3.4,
#         'min_voltage' : 3.0,
#         'max_voltage' : 3.8,
#         'capacity' : 0,
#         'current' : 0,
#         'temperature' : random.randint(20, 30)
#     }

# }

# cell_details=[]
# for i in range(cell_no):
#     cell_details.append(details[list_of_cell[i]])

# for i in cell_details:
#     for j in range()