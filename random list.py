import random
import time
from time import ticks_us as us
n_values = [1000,5000,10000,20000,30000,40000]
for i in range(len(n_values)):
    random_list = []
    times = []
    for k in range(1000):
        for j in range(n_values[i]):
            random_list.append(random.randint(1,1000000))
        random_int = random.randint(1,1000000)
        found = False
        start_time = us()
        while not found:
            for j in range(n_values[i]):
                if random_int == random_list[j]:
                    found = True
                else:
                    found = False 
        end_time = us()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
    mean = sum(times)/len(times)
    print(f'the average time to search a string of length {n_values[i]} is {mean} microseconds')
