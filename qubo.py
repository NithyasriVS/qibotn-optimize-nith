import numpy as np

# Initialize variables
file_path = 'belgium-road-km-n50-k10.txt'  # Replace with your actual file path
dimension = 0
distance_matrix = np.zeros((500, 500))  # Initialize with a max of 100 nodes (adjust as needed)
in_weight_edge_section = False

# Parse the file to extract the dimension and distance matrix
with open(file_path, 'r') as file:
    for line in file:
        # Check for dimension information
        if "DIMENSION" in line:
            dimension = int(line.split(":")[1].strip())  # Assuming format: "DIMENSION: 50"
        
        # Check if we've reached the start of DEMAND_SECTION
        if line.strip() == "DEMAND_SECTION":
            break
        
        # Otherwise, collect the lines in the weight edge section
        if not in_weight_edge_section:
            if line.strip() == "EDGE_WEIGHT_SECTION":
                in_weight_edge_section = True
                continue  # Skip this line as it's the section header
        elif in_weight_edge_section:
            # Parse the distance weights and update the distance matrix
            parts = line.strip().split()
            if len(parts) > 1:

                    # Parse indices and distance as floats (not integers)
                    i, j = map(int, parts[:2])
                    distance = float(parts[2])  # Allow floating-point numbers
                    
                    # Debugging: Check the values of i, j, and distance
                    print(f"i: {i}, j: {j}, distance: {distance}")
                    
                    # Check if the indices are within bounds
                    if i > 0 and j > 0 and i <= dimension and j <= dimension:
                        distance_matrix[i-1, j-1] = distance  # Adjust to 0-based indexing
                        distance_matrix[j-1, i-1] = distance  # Symmetric matrix, undirected graph
    
distance_matrix = distance_matrix[:dimension, :dimension]

# Print dimension and distance matrix
print(f"Dimension: {dimension}")
print("Distance Matrix:")
print(distance_matrix)

# Build the QUBO matrix for the TSP problem
Q = np.zeros((dimension * dimension, dimension * dimension))  # Initialize the QUBO matrix

# Fill the QUBO matrix based on the distance matrix
for i in range(dimension):
    for j in range(dimension):
        if i != j:
            # Objective function: Minimize travel cost for each pair (i, j)
            Q[i * dimension + j, i * dimension + j] = distance_matrix[i, j]

            # Additional constraints for ensuring exactly one path is chosen
            for k in range(dimension):
                if k != i:
                    Q[i * dimension + k, j * dimension + i] += 2  # Linear constraint for each node

# Print the QUBO matrix
print("QUBO Matrix:")
print(Q)

