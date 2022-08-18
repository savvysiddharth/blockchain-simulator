import random
import simpy
import constants
import time

env = simpy.Environment()
print(time.time())
def run(env):
    t = 0
    for i in range(1):
        print(env.now)
        #t = random.expovariate(1 / constants.Tk)
        t = t + 1
        yield env.timeout(t+1)

env.process(run(env))
#<Process(driver) object at 0x...>
env.run(until=1500)


print("bhxnjkmlbc",time.time())