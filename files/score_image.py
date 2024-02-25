import matplotlib.pyplot as plt

# Valori dei dati
situations = ['Broadcast', 'Naive', 'Optimized']
total_messages = [120, 37, 17]
average_value = [17.54, 22.42, 22.89]
redundancy_count = [106, 18, 2.0]
redundancy_percentage = [88.33, 48.65, 11.76]

# Creazione del plot per i Total Messages
plt.figure(figsize=(10, 6))
plt.bar(situations, total_messages, color='blue')
plt.title('Total Messages')
plt.xlabel('Simulation Type')
plt.ylabel('Total Messages')
plt.grid(True)
plt.show()

# Creazione del plot per l'Average Value
plt.figure(figsize=(10, 6))
plt.plot(situations, average_value, marker='o', color='green')
plt.title('Average Value')
plt.xlabel('Simulation Type')
plt.ylabel('Average Value')
plt.grid(True)
plt.show()

# Creazione del plot per la Redundancy Count
plt.figure(figsize=(10, 6))
plt.plot(situations, redundancy_count, marker='s', color='red')
plt.title('Redundancy Count')
plt.xlabel('Simulation Type')
plt.ylabel('Redundancy Count')
plt.grid(True)
plt.show()

# Creazione del plot per la Redundancy Percentage
plt.figure(figsize=(10, 6))
plt.plot(situations, redundancy_percentage, marker='^', color='orange')
plt.tit
