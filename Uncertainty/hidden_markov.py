from model import MarkovChain, HiddenMarkovModel
from model import DiscreteDistribution, ConditionalProbabilityTable

initial_distribution = DiscreteDistribution({
    "rainy": 0.5,
    "sunny": 0.5
})

tranisition_model = ConditionalProbabilityTable(
    [   
        ["rainy", "rainy", 0.7],
        ["rainy", "sunny", 0.3],
        ["sunny", "rainy", 0.4],
        ["sunny", "sunny", 0.6]
    ],
    [initial_distribution]      
)

emission_model = ConditionalProbabilityTable(
    [
        ["rainy", "umbrella", 0.9],
        ["rainy", "no umbrella", 0.1],
        ["sunny", "umbrella", 0.2],
        ["sunny", "no umbrella", 0.8],
    ],
    [tranisition_model]
)

model = HiddenMarkovModel(tranisition_model, emission_model, initial_distribution)
sequences = model.sample(10, 1)
for sequence in sequences:
    print(sequence)