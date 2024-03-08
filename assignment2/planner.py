import numpy as np
import argparse, pulp

class MDP():
    def __init__(self, path):
        try:
            f = open(path, "r", encoding='utf-8')
            self.S = int(f.readline().split()[1])
        except UnicodeDecodeError as e:
            f = open(path, "r", encoding='utf-16-le')
            self.S = int(f.readline().split()[1])
        self.A = int(f.readline().split()[1])
        self.end = [int(e) for e in f.readline().split()[1:]]
        self.T = [[[] for a in range(self.A)] for s in range(self.S)]
        self.TR = np.zeros((self.S, self.A))
        line = f.readline().split()
        while line[0] == 'transition':
            s1, ac, p = int(line[1]), int(line[2]), float(line[5])
            self.T[s1][ac].append((int(line[3]), p))
            self.TR[s1][ac] += p * float(line[4])
            line = f.readline().split()
        self.mdptype = line[1]
        self.discount = float(f.readline().split()[1])
        f.close()
        self.algos = {'vi':self.value_iteration, 'lp':self.linear_programming, 'hpi':self.howards_policy_iteration}

    def value_iteration(self, epsilon=1e-9):
        V = np.zeros(self.S)
        while True:
            _ = self.TR + self.discount * np.array([[sum([p_ * V[s_] for s_, p_ in self.T[s][a]]) for a in range(self.A)] for s in range(self.S)])
            pi = np.argmax(_, axis=1)
            V_next = _[range(self.S), pi]
            if all(np.abs(V_next - V) < epsilon): break
            V = V_next.copy()
        return V_next, pi
    
    def get_policy(self, V):
        return np.argmax(self.TR + self.discount * np.array([[sum([p_ * V[s_] for s_, p_ in self.T[s][a]]) for a in range(self.A)] for s in range(self.S)]), axis=1)

    def linear_programming(self):
        prob = pulp.LpProblem('ValueFunction', pulp.LpMaximize)
        Vs = [pulp.LpVariable(f'V_{s}', 0) for s in range(self.S)]
        prob += pulp.LpAffineExpression(zip(Vs, [-1]*len(Vs)))
        for s in range(self.S):
            for a in range(self.A):
                prob += Vs[s] >= self.TR[s][a] + pulp.LpAffineExpression([(Vs[s_], self.discount * p_) for s_, p_ in self.T[s][a]])
        pulp.PULP_CBC_CMD(msg=0).solve(prob)
        V = np.array([pulp.value(v) for v in Vs])
        return V, self.get_policy(V)

    def get_value_function(self, pi, epsilon=1e-9):
        V = np.zeros(self.S)
        while True:
            V_next = self.TR[range(self.S), pi] + self.discount * np.array([sum([p_ * V[s_] for s_, p_ in self.T[s][pi[s]]]) for s in range(self.S)])
            if all(np.abs(V_next - V) < epsilon): break
            V = V_next.copy()
        return V_next

    def get_action_value_function(self, pi):
        V = self.get_value_function(pi)
        return V, self.TR + self.discount * np.array([[sum([p_ * V[s_] for s_, p_ in self.T[s][a]]) for a in range(self.A)] for s in range(self.S)])

    def howards_policy_iteration(self):
        pi = np.zeros(self.S, dtype=int)
        while True:
            V, Q = self.get_action_value_function(pi)
            if all(pi == np.argmax(Q, axis=1)): break
            pi = np.argmax(Q, axis=1)
        return V, pi

    def get_optimal_policy(self, algo):
        return self.algos[algo]()

    def policy_evaluation(self, path):
        with open(path, 'r') as f:
            pi = np.array([int(line.strip()) for line in f.readlines()])
        return self.get_value_function(pi), pi


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp", type=str)
    parser.add_argument("--algorithm", type=str, choices=['vi', 'lp', 'hpi'], default='vi')
    parser.add_argument("--policy", type=str)
    args = parser.parse_args()
    mdp = MDP(args.mdp)
    if args.policy is None:
        V, pi = mdp.get_optimal_policy(args.algorithm)
    else:
        V, pi = mdp.policy_evaluation(args.policy)
    print('\n'.join([f"{V[i]} {pi[i]}" for i in range(len(V))]))