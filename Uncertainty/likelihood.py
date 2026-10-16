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

def likelihood_sampling(model, query, evidence, N=10000):
    # Support boolean 'T'/'F' query values by accumulating weights per value
    weights = {"T": 0.0, "F": 0.0}

    for _ in range(N):
        weight = 1.0
        samples = {}
        for state in model.states:
            var = state.name
            dist = state.distribution
            # Evidence case: don't sample, but weight by likelihood of evidence
            if var in evidence:
                samples[var] = evidence[var]
                if isinstance(dist, ConditionalProbabilityTable):
                    parent_names = model._parents.get(var, [])
                    parent_values = [samples[pn] for pn in parent_names]
                    weight *= dist.prob(evidence[var], parent_values)
                else:
                    weight *= dist.prob(evidence[var])
            else:
                # Non-evidence: sample from the prior / conditional
                if isinstance(dist, ConditionalProbabilityTable):
                    parent_names = model._parents.get(var, [])
                    parent_values = [samples[pn] for pn in parent_names]
                    samples[var] = dist.sample(parent_values)
                else:
                    samples[var] = dist.sample()
        weights[samples[query]] += weight

    total = weights.get("T", 0.0) + weights.get("F", 0.0)
    if total == 0:
        return 0.0
    print(len(weights), weights)
    return weights["T"] / total

prob = likelihood_sampling(model, "sprinkler", {"wetGrass":"T"}, N=100000)
print(f"Estimated prior probability of sprinkler being True: {prob}")
# print(model.sample(10))
