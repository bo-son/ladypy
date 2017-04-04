from .context import np
from .agent import Agent
from .sample import sample_from_P


def derive_P(A):
    return (A.transpose() / A.sum(axis=1)).transpose()


def derive_Q(A):
    return (A / A.sum(axis=0)).transpose()


def learn(Bs, props, ks, eps, rho):
    k_prt, k_rol, k_rnd = ks
    n, m = Bs[0].P.shape

    A = np.zeros(Bs[0].P.shape)
    idx = np.arange(len(Bs))

    if k_prt > 0:
        prt = np.random.choice(idx, p=props)
        idx = np.delete(idx, prt)
        A += sample_from_P(Bs[prt].P, k_prt, rho)

    if k_rol > 0:
        mdls = np.random.choice(idx, k_rol, p=props, replace=False)
        idx = np.setdiff1d(idx, mdls)
        for mdl in mdls:
            A += sample_from_P(Bs[mdl].P, k_rol, rho)

    if k_rnd > 0:
        rnds = np.random.choice(idx, k_rnd, replace=False)
        idx = np.setdiff1d(idx, rnds)
        for rnd in rnds:
            A += sample_from_P(Bs[rnd].P, k_rnd, rho)

    A += eps * np.random.rand(n, m)

    return Agent(A)