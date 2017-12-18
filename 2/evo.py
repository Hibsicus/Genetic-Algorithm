# -*- coding: utf-8 -*-
import numpy as np

TARGET_PHARSE = 'Hello world!'
POP_SIZE = 300
CROSS_RATE = 0.4
MUTATION_RATE = 0.01
N_GENERATIONS = 1000

DNA_SIZE = len(TARGET_PHARSE)
TARGET_ASCII = np.fromstring(TARGET_PHARSE, dtype=np.uint8)
ASCII_BOUND = [32, 126]

class GA(object):
    def __init__(self, DNA_size, DNA_bound, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size
        DNA_bound[1] += 1
        self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        
        self.pop = np.random.randint(*DNA_bound, size=(pop_size, DNA_SIZE)).astype(np.int8)
    
    def translateDNA(self, DNA):
        return DNA.tostring().decode('ascii')
    
    def get_fitness(self):
        match_count = (self.pop == TARGET_ASCII).sum(axis=1)
        return match_count
    
    def select(self):
        fitness = self.get_fitness() + 1e-4
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p = fitness / fitness.sum())
        return self.pop[idx]
    
    def crossover(self, parent, pop):
        if np.random.rand() <self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_point = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parent[cross_point] = pop[i_, cross_point]
        return parent
    
    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] = np.random.randint(*self.DNA_bound)
        return child
    
    
    def evolve(self):
        pop = self.select()
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop

if __name__ == '__main__':
    ga = GA(DNA_size=DNA_SIZE, DNA_bound=ASCII_BOUND, cross_rate=CROSS_RATE, mutation_rate=MUTATION_RATE, pop_size=POP_SIZE)
    
    for generation in range(N_GENERATIONS):
        fitness = ga.get_fitness()
        best_DNA = ga.pop[np.argmax(fitness)]
        best_phrase = ga.translateDNA(best_DNA)
        print('Gen', generation, ':', best_phrase)
        if best_phrase == TARGET_PHARSE:
            break
        ga.evolve()
    
