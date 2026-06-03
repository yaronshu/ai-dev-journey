name = "Yaron"
age = 50
print("Hello, my name is", name)
print("I am", age, "yeasrs old")

def greet(person_name):
    message = "Welcome " + person_name
    return message

def whereLeave(city):
    return "I am leaving from " + city

def greet(person_name):
    message = "Welcome " + person_name
    return message

def wherePersonLives(city, person_name):
 message = person_name + " lives in " + city
 return message
result = greet("Claude")
print(result)

result = wherePersonLives("Tel Aviv", "Yaron1")
print(result)
result = wherePersonLives("Beer Sheva", "Yaron2")
print(result)
result = wherePersonLives("Jerusalem", "Yaron3")
print(result)
