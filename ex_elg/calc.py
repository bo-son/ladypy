from .context import np
from .agent import Agent


def payoff(A, B):
    return 0.5 * (
        np.einsum('ij,ji->', A.P, B.Q) + np.einsum('ij,ji->', B.P, A.Q))


def total_payoff(A, Agents):
    return sum([payoff(A, B) for B in Agents])


def calc_payoff(Agents):
    return np.array([payoff(A, A) for A in Agents])


def calc_payoff_total(Agents):
    return np.array([
        total_payoff(a, Agents[:i] + Agents[(i + 1):])
        for i, a in enumerate(Agents)
    ])


def calc_payoff_avg(Agents):
    return calc_payoff_total(Agents) / (len(Agents) - 1)


def calc_probs(Agents):
    tp = calc_payoff_total(Agents)
    return tp / tp.sum()