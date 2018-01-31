from random import randrange

# random operator for GA
def mutate(chromosome):
    random1 = randrange(0, len(chromosome))
    random2=random1
    while (random2==random1):
        random2 = randrange(0, len(chromosome))
    swap(chromosome,random1,random2)

def swap(array, i, j):
    array[i], array[j]= array[j], array[i]
