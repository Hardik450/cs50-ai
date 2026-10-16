from model import MarkovChain
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
model = MarkovChain(tranisition_model, initial_distribution)
sequences = model.sample(10)
for sequence in sequences:
    print(sequence)