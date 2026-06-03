
# List of tasks
tasks = ["write tests", "fix bug", "code review", "deploy"]

# Loop over all tasks
for task in tasks:
    print("Task:", task)

# Add an item
tasks.append("write docs")
print("Total tasks:", len(tasks))

# Filter: print only tasks that contain 'write'
for task in tasks:
    if "write" in task:
        print("Writing task found:", task)



numbers = [1, 2, 3, 4, 5]

for number in numbers:
    if number % 2 == 0:
        print("Even number:", number)
    else:
        print("Odd number:", number)