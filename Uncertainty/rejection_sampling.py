from model import *  # Assuming prior.py contains necessary imports and definitions

rain = DiscreteDistribution({
    "T": 0.2, 
    "F": 0.8
})

sprinkler = DiscreteDistribution({
    "T": 0.4,   
    "F": 0.6
})

wetGrass = ConditionalProbabilityTable(
    [
        ["T", "T", "T", 0.99],  
        ["T", "T", "F", 0.01],
        ["T", "F", "T", 0.9],   
        ["T", "F", "F", 0.1],
        ["F", "T", "T", 0.8],
        ["F", "T", "F", 0.2],
        ["F", "F", "T", 0.0],
        ["F", "F", "F", 1.0]
    ],
    [rain, sprinkler]
)

r = State(rain, name="rain")
s = State(sprinkler, name="sprinkler")
w = State(wetGrass, name="wetGrass")
model = BayesianNetwork("Rain Network")
model.add_states(r, s, w)
model.add_edge(r, w)
model.add_edge(s, w)
model.bake()

def rejection_sampling(model, query, evidence, N=10000):
    samples = []

    for _ in range(N):
        s = model.sample(1)[0]
        reject = False
        for var, value in evidence.items():
            if s[var] != value:
                reject = True
                break
            if reject:
                continue
            samples.append(s[query])
    
    print(samples.count("T"), len(samples))
    return samples.count("T") / len(samples)

prob = rejection_sampling(model, "sprinkler", {"wetGrass":"T"}, N=100000)
print(f"Estimated prior probability of sprinkler being True: {prob}")
# print(model.sample(10))
