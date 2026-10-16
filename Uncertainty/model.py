from itertools import product
from typing import Dict, List, Any


class DiscreteDistribution(dict):
    """Simple discrete distribution mapping values -> probability.

    Behaves like a tiny subset of pomegranate.DiscreteDistribution used by
    the example: normalizes probabilities and exposes a `prob(value)` helper.
    """
    def __init__(self, probabilities: Dict[Any, float]):
        super().__init__(probabilities)
        self.normalize()

    def normalize(self) -> None:
        s = sum(self.values())
        if s > 0:
            for k in list(self.keys()):
                self[k] = self[k] / s

    def prob(self, value: Any) -> float:
        return float(self.get(value, 0.0))

    def __repr__(self) -> str:  # helpful when printed by the example
        return f"DiscreteDistribution({dict(self)})"
    
    def sample(self) -> Any:
        """Draw a sample from the distribution."""
        import random
        r = random.random()
        cumulative = 0.0
        for k, p in self.items():
            cumulative += p
            if r <= cumulative:
                return k
        # fallback, should not reach here if normalized correctly
        return k
    
class ConditionalProbabilityTable:
    """A small CPT implementation.

    The rows are expected in the form used in the example: for N parents each
    row is [parent1_val, parent2_val, ..., child_val, probability]. The
    ``parents`` argument is a list of the parent DiscreteDistribution objects
    (the same objects passed when the example constructs the CPT).
    """
    def __init__(self, table: List[List[Any]], parents: List[DiscreteDistribution]):
        self.table = table
        self.parents = parents

    def prob(self, child_value: Any, parent_values: List[Any]) -> float:
        """Return P(child_value | parents = parent_values) by table lookup."""
        n_parents = len(self.parents)
        for row in self.table:
            row_parents = row[:n_parents]
            child = row[n_parents]
            p = row[n_parents + 1]
            if list(row_parents) == list(parent_values) and child == child_value:
                return float(p)
        return 0.0

    def child_domain(self) -> List[Any]:
        n_parents = len(self.parents)
        return sorted({row[n_parents] for row in self.table})
    
    def sample(self, parent_values: List[Any]) -> Any:
        """Draw a sample of the child variable given parent values."""
        filtered_rows = [row for row in self.table if row[:len(self.parents)] == parent_values]
        dist = DiscreteDistribution({row[len(self.parents)]: row[len(self.parents) + 1] for row in filtered_rows})
        return dist.sample()

class State:
    def __init__(self, distribution: Any, name: str):
        self.distribution = distribution
        self.name = name

    def __repr__(self) -> str:
        return f"State(name={self.name})"

class BayesianNetwork:
    """A tiny Bayesian network implementation using full enumeration.

    This is sufficient for small examples and for the educational example in
    `bayesian.py`.
    """
    def __init__(self, name: str):
        self.name = name
        self.states: List[State] = []
        self.edges: List[tuple] = []
        self._baked = False

    def add_states(self, *states: State) -> None:
        self.states.extend(states)

    def add_edge(self, parent: State, child: State) -> None:
        self.edges.append((parent, child))

    def bake(self) -> None:
        """Finalize the network: infer parent relationships and domains."""
        # map state name -> State
        self._state_map = {s.name: s for s in self.states}

        # infer parent names for CPTs (users pass parent distributions when
        # constructing the CPT, so we match them to states by identity)
        self._parents: Dict[str, List[str]] = {}
        self._domains: Dict[str, List[Any]] = {}

        for s in self.states:
            dist = s.distribution
            if isinstance(dist, ConditionalProbabilityTable):
                parent_names = []
                for pd in dist.parents:
                    found = next((st for st in self.states if st.distribution is pd), None)
                    if not found:
                        raise ValueError("Parent distribution does not match any registered State")
                    parent_names.append(found.name)
                self._parents[s.name] = parent_names
                self._domains[s.name] = dist.child_domain()
            else:
                self._parents[s.name] = []
                if isinstance(dist, DiscreteDistribution):
                    self._domains[s.name] = sorted(list(dist.keys()))
                else:
                    # fallback: if distribution doesn't expose keys, try to
                    # coerce by asking for a .prob method over 'T'/'F'
                    self._domains[s.name] = ["T", "F"]

        self._baked = True

    def _joint_probability(self, assignment: Dict[str, Any]) -> float:
        p = 1.0
        for s in self.states:
            val = assignment[s.name]
            dist = s.distribution
            if isinstance(dist, DiscreteDistribution):
                p *= dist.prob(val)
            elif isinstance(dist, ConditionalProbabilityTable):
                parent_vals = [assignment[pn] for pn in self._parents[s.name]]
                p *= dist.prob(val, parent_vals)
            else:
                raise ValueError("Unsupported distribution type")
        return p

    def predict_proba(self, evidence: Dict[str, Any]) -> List[Any]:
        """Return per-state posterior distributions or the observed value.

        The return value is a list with one element per registered State in the
        same order they were added: either the observed value (if present in
        evidence) or a DiscreteDistribution over possible values.
        """
        if not self._baked:
            raise RuntimeError("Call bake() before running inference")

        # enumerate all assignments
        var_names = [s.name for s in self.states]
        domains = [self._domains[name] for name in var_names]

        total_prob = 0.0
        # accumulator: var -> value -> prob mass
        marginals: Dict[str, Dict[Any, float]] = {name: {v: 0.0 for v in self._domains[name]} for name in var_names}

        for prod in product(*domains):
            assignment = dict(zip(var_names, prod))
            # check consistency with evidence
            consistent = all(assignment.get(k) == v for k, v in evidence.items())
            if not consistent:
                continue
            jp = self._joint_probability(assignment)
            total_prob += jp
            for name in var_names:
                marginals[name][assignment[name]] += jp

        if total_prob == 0:
            # evidence impossible under model: return empty distributions
            result = []
            for name in var_names:
                if name in evidence:
                    result.append(evidence[name])
                else:
                    result.append(DiscreteDistribution({v: 0.0 for v in self._domains[name]}))
            return result

        # normalize marginals
        for name in marginals:
            for v in marginals[name]:
                marginals[name][v] /= total_prob

        # build result list preserving order of states
        result = []
        for name in var_names:
            if name in evidence:
                result.append(evidence[name])
            else:
                result.append(DiscreteDistribution(marginals[name]))

        return result

    def predict(self, evidence: Dict[str, Any]) -> List[Any]:
        """Return the MAP (most probable) value for each State given evidence."""
        post = self.predict_proba(evidence)
        out = []
        for item in post:
            if isinstance(item, DiscreteDistribution):
                # pick argmax
                best = max(item.items(), key=lambda kv: kv[1])[0]
                out.append(best)
            else:
                out.append(item)
        return out
    
    def sample(self, n) -> Dict[str, Any]:
        """Draw a sample from the joint distribution represented by the network."""
        if not self._baked:
            raise RuntimeError("Call bake() before sampling")

        samples = {}
        for i in range(n):
            samples[i] = self._sample_single()
        return samples
    
    def _sample_single(self) -> Dict[str, Any]:
        sample = {}
        for state in self.states:
            dist = state.distribution
            if isinstance(dist, DiscreteDistribution):
                sample[state.name] = dist.sample()
            elif isinstance(dist, ConditionalProbabilityTable):
                parent_names = self._parents[state.name]
                parent_values = [sample[pn] for pn in parent_names]
                sample[state.name] = dist.sample(parent_values)
            else:
                raise ValueError("Unsupported distribution type")
        return sample
    
class MarkovChain:
    """A simple Markov Chain implementation."""
    def __init__(self, transition_matrix, initial_distribution: DiscreteDistribution):
        """Create a MarkovChain.

        Accepts either:
        - a dict mapping state -> DiscreteDistribution (or dict of probs), or
        - a ConditionalProbabilityTable where each row is [from_state, to_state, prob]
        and `parents` is a single DiscreteDistribution corresponding to the source.
        """
        # If transition_matrix is a CPT, convert to mapping
        if isinstance(transition_matrix, ConditionalProbabilityTable):
            # Expect rows of form [from, to, prob] and single parent
            tm: Dict[Any, Dict[Any, float]] = {}
            for row in transition_matrix.table:
                if len(row) < 3:
                    raise ValueError("CPT rows for MarkovChain must have at least 3 entries: from, to, prob")
                frm = row[0]
                to = row[1]
                prob = row[2]
                tm.setdefault(frm, {})[to] = prob
            self.transition_matrix = {k: DiscreteDistribution(v) for k, v in tm.items()}
        elif isinstance(transition_matrix, dict):
            tm: Dict[Any, DiscreteDistribution] = {}
            for k, v in transition_matrix.items():
                if isinstance(v, DiscreteDistribution):
                    tm[k] = v
                elif isinstance(v, dict):
                    tm[k] = DiscreteDistribution(v)
                else:
                    raise ValueError("Unsupported transition_matrix value type")
            self.transition_matrix = tm
        else:
            raise ValueError("Unsupported transition_matrix type")

        if not isinstance(initial_distribution, DiscreteDistribution):
            raise ValueError("initial_distribution must be a DiscreteDistribution")
        self.initial_distribution = initial_distribution

    def sample(self, length: int, n: int = 1) -> List[List[Any]]:
        """Generate `n` sequences each of length `length`.

        Returns a list of sequences (each a list of states). For backward
        compatibility, calling `sample(10)` returns a list with a single
        sequence of length 10.
        """
        import random
        sequences: List[List[Any]] = []
        for _ in range(n):
            seq: List[Any] = []
            current_state = self.initial_distribution.sample()
            seq.append(current_state)
            for _ in range(1, length):
                if current_state not in self.transition_matrix:
                    raise KeyError(f"No transition distribution for state {current_state}")
                current_dist = self.transition_matrix[current_state]
                current_state = current_dist.sample()
                seq.append(current_state)
            sequences.append(seq)
        return sequences
    
class HiddenMarkovModel(MarkovChain):
    """A simple Hidden Markov Model implementation."""
    def __init__(self, transition_matrix, emission_matrix, initial_distribution: DiscreteDistribution):
        """Create a HiddenMarkovModel.

        transition_matrix: same format as MarkovChain
        emission_matrix: dict mapping hidden_state -> DiscreteDistribution over observations
        initial_distribution: DiscreteDistribution over hidden states
        """
        super().__init__(transition_matrix, initial_distribution)

        # Allow emission_matrix to be provided either as a dict mapping hidden
        # state -> distribution, or as a ConditionalProbabilityTable where each
        # row is [hidden_state, observation, prob]. If a CPT is provided we
        # convert it into the dict form and normalize per hidden state.
        if isinstance(emission_matrix, ConditionalProbabilityTable):
            em_tmp: Dict[Any, Dict[Any, float]] = {}
            for row in emission_matrix.table:
                if len(row) < 3:
                    raise ValueError("CPT rows for emission_matrix must have at least 3 entries: hidden_state, observation, prob")
                hidden = row[0]
                obs = row[1]
                prob = row[2]
                em_tmp.setdefault(hidden, {})[obs] = prob
            em = {k: DiscreteDistribution(v) for k, v in em_tmp.items()}
        else:
            em = {}
            for k, v in emission_matrix.items():
                if isinstance(v, DiscreteDistribution):
                    em[k] = v
                elif isinstance(v, dict):
                    em[k] = DiscreteDistribution(v)
                else:
                    raise ValueError("Unsupported emission_matrix value type")

        self.emission_matrix = em

    def sample(self, length: int, n: int = 1) -> List[List[tuple]]:
        """Generate `n` sequences of (hidden_state, observation) pairs each of length `length`.

        Returns a list of sequences (each a list of (hidden_state, observation) tuples).
        """
        import random
        sequences: List[List[tuple]] = []
        for _ in range(n):
            seq: List[tuple] = []
            current_state = self.initial_distribution.sample()
            current_observation = self.emission_matrix[current_state].sample()
            seq.append((current_state, current_observation))
            for _ in range(1, length):
                if current_state not in self.transition_matrix:
                    raise KeyError(f"No transition distribution for state {current_state}")
                current_dist = self.transition_matrix[current_state]
                current_state = current_dist.sample()
                current_observation = self.emission_matrix[current_state].sample()
                seq.append((current_state, current_observation))
            sequences.append(seq)
        return sequences