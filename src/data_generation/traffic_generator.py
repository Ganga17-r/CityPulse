import random
times = [8, 14, 18, 23]

for time in times:
    if time == 8:
        traffic = random.randint(700, 900)
    elif time == 14:
        traffic = random.randint(400, 600)
    elif time == 18:
        traffic = random.randint(800, 1000)
    elif time == 23:
        traffic = random.randint(100, 300)

    print(time, "→ Traffic:", traffic)
if time == 8:
    temperature = random.randint(25, 30)
elif time == 14:
    temperature = random.randint(30, 36)
elif time == 18:
    temperature = random.randint(27, 32)
elif time == 23:
    temperature = random.randint(22, 27)

print(time, "→ Traffic:", traffic, "| Temperature:", temperature, "°C")