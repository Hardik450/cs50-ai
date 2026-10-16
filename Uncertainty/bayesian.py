from model import *

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

probabilities = model.predict_proba({
    "wetGrass": "T"
})


predictions = model.predict({
    "wetGrass": "T"
})
print(f"{predictions}")

print("Predicted Rain:", predictions[0])
print("Predicted Sprinkler:", predictions[1])
print("Probability Distribution of rain:", probabilities[0])
print("Probability Distribution of sprinkler:", probabilities[1])