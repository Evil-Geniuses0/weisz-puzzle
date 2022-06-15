import random;

#Every tier is set up as an object that stores its chances, its prize, and how many times it is chosen each run
class Tier:
    total = 0
    #The total is added to by all of the constructors

    def __init__(self, prize, num):
        self.prize = prize
        self.num = num
        self.tally = 0
        Tier.total += num

    #Needs to generate probability after everything is constructed due to the total value still changing
    def genProb(self):
        self.prob = self.num/Tier.total

    def getProb(self):
        return self.prob

    #Unity refers to between 0 and 1 and is how the RNG works.
    #For example, a 90%, 5%, and 3% would be converted into 0.9, 0.97, and 1.0
    def genUnity(self, prev):
        self.unity = self.prob + prev

    def getUnity(self):
        return self.unity
    
    def chosen(self):
        self.tally += 1

    def getTally(self):
        return self.tally

    def getRev(self):
        return self.tally * self.prize
    
    #Each tally must be reset in between each run
    def reset(self):
        self.tally = 0

#Creates every tier and puts them into a tuple
one = Tier(1000000, 2)
two = Tier(500000, 1)
three = Tier(250000, 2)
four = Tier(100000, 5)
five = Tier(10000, 20)
six = Tier(2500, 50)
seven = Tier(1000, 200)
eight = Tier(100, 2000)
nine = Tier(1, 597720)
arr = (nine, eight, seven, six, five, four, three, two, one)

#Generates probabilities and then 0-1 stacking probabilities
for i in arr:
    i.genProb()
nine.genUnity(0)
for i in range(1, 9):
    arr[i].genUnity(arr[i-1].getUnity())

#Each entry generates a random number and then searches through each 0-1 probability from the lowest to highest
#until it finds the one that matches and increases the tally of that tier
def entry():
    val = random.random()
    for i in arr:
        if(i.getUnity() > val):
            i.chosen()
            break

#The run resets all of the tallies to zero and then does the specified number of entries
#It then calculates the total revenue, total profit, and then subtracts the $1 revenue to find profit without the $1 prize
def run(entries):
    total = 0
    for i in arr:
        i.reset()
    for i in range(entries):
        entry()
    for i in arr:
        total += i.getRev()
    wOne = total - num*0.58
    woOne = wOne - nine.getRev()
    #print(f"Total revenue is {total}")
    #print(f"Total cost is {num*0.58}")
    #print(f"Net profit is {wOne}")
    #print(f"Without $1 is {woOne}\n")
    return wOne, woOne

#Change num to change the number of entries per run
num = 20000
#Change runs to change the number of runs per simulation
runs = 10000

#These lists store the profits of every run, both with and without the $1
withOne = []
withoutOne = []
for i in range(runs):
    wO, woO = run(num)
    withOne.append(wO)
    withoutOne.append(woO)

#print(*withOne, sep = ", ")
#print(*withoutOne, sep = ", ")

#This looks through each list and returns the percentage of runs that are profitable
def percentProfit(lis):
    tot = 0
    for i in lis:
        if i >= 0:
            tot += 1
    tot = tot / len(lis) * 100
    return f"{tot}%"

print(percentProfit(withOne))
print(percentProfit(withoutOne))
