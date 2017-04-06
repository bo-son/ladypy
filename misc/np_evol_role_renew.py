import sys
import os
import logging as lg

lg.basicConfig(stream=sys.stdout, level=lg.DEBUG,
        format='%(asctime)s - %(message)s')
lg_pad = ' ' * 2

import numpy as np
import numpy.random as r

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt


N_TRY = 1
N_GEN = 100
N_POP = 100
N_OBJ = 5
N_SIG = 5


def making_f(A):
    F = np.zeros(N_POP)
    P = [A[i] / A[i].sum(1).reshape(N_OBJ, 1) for i in range(N_POP)]
    Q = [A[i] / A[i].sum(0) for i in range(N_POP)]

    for i in range(N_POP):
        fitness = 0.0
        for u in range(N_POP):
            if i == u:
                continue
            fitness += 0.5 * (P[i] * Q[u] + P[i] * Q[u]).sum()
        F[i] = fitness / (N_POP - 1)

    return F


def choosing(A, F, k):
    chosen = np.zeros((k, N_OBJ, N_SIG), 'int')
    new_f = np.zeros(k)
    f = list(F)

    if k == 1:
        i = f.index(max(f))
        A[0:N_POP] = A[i]
        F[0:N_POP] = F[i]

        return A, F

    for n in range(k):
        i = f.index(max(f))
        chosen[n] = A[i]
        new_f[n] = f[i]
        f[i] = 0.0

    for n in range(N_POP):
        new_f = np.float_(new_f) / (new_f.sum())
        chosen = r.choice(np.arange(k), N_POP, p=new_f)
        A = A[chosen]
        F = F[chosen]

    return A, F


def teaching(A, k, eps=1e-3):
    new = eps * np.ones((N_POP, N_OBJ, N_SIG))

    for n in range(N_POP):
        for i in range(N_OBJ):
            p_wrd = A[n][i] / A[n][i].sum()
            js = r.choice(np.arange(N_OBJ), k, p=p_wrd)

            for j in js:
                new[n][i][j] += 1

    return new


def simulate(gen, pop, size, k, k_rol):
    A = np.random.random((pop, size[0], size[1]))
    pts = []

    for g in range(gen):
        F = making_f(A)  # fitness
        A, F = (choosing(A, F, k_rol))
        A = teaching(A, k)  # next generation

        pts.append(F.sum() / N_POP)

        if g % 20 == 19:
            lg.info(lg_pad * 2 + 'Gen %d - %f' % (g + 1, pts[-1]))

    return pts


def draw_simulated_graph(ax, rep, gen, agent, size, k, k_rol):

    for tr in range(rep):
        lg.info(lg_pad + 'Trial %d Start' % (tr + 1))
        pts = simulate(gen, agent, size, k, k_rol)
        lg.info(lg_pad + 'Trial %d Finish' % (tr + 1))
        ax.plot(pts, ls='-', alpha=.75)

    for h in range(1, min(size) + 1):
        ax.axhline(h, ls='dotted', c='k', alpha=0.25)

    title = '%d Simulation' % rep + ('s' if rep > 1 else "") + \
            ' with %d Agent' % agent + ('s' if agent > 1 else "")
    option = '%dx%d matrix, K=%d, K_ROL=%d' % (size[0], size[1], k, k_rol)

    ax.set_title(title + '\n' + option, fontweight='bold')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Average Payoff')
    ax.axis([0, gen, 0, min(size) + 1])


if __name__ == '__main__':
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(12, 10)

    for i, ax in zip([1, 4, 7, 10], axes.flat):
        lg.info('[k = %d, K_rol = %d] Simulation Start' % (i, i))
        draw_simulated_graph(ax, N_TRY, N_GEN, N_POP, (N_OBJ, N_SIG), i, i)
        lg.info('[k = %d, K_rol = %d] Simulation Finish' % (i, i))

    plt.tight_layout()

    output_dir = os.path.join('docs', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, 'lecturer_rm.png'))