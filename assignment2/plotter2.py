import matplotlib.pyplot as plt

winning_probs = [
    [0.7, 0.28672000000000003, 0.17999999999999997, 0.12599999999999997, 0.10799999999999997, 0.09999999999999987],
    [0.07999999999999999, 0.12599999999999997, 0.19999999999999996, 0.29999999999999993, 0.3999999999999999]
]

p_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
q_list = [0.6, 0.7, 0.8, 0.9, 1]

plt.plot(p_list,winning_probs[0],marker='o')
plt.title("Probability of winning from 05,09,08,1")
plt.xlabel('p')
plt.xticks(p_list)
plt.ylabel('Probability of winning')
plt.grid()
plt.savefig("fig1.png")
plt.clf()

plt.plot(q_list,winning_probs[1],marker='o')
plt.title("Probability of winning from 05,09,08,1")
plt.xlabel('q')
plt.xticks(q_list)
plt.ylabel('Probability of winning')
plt.grid()
plt.savefig("fig2.png")
plt.clf()