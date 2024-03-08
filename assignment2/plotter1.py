import subprocess
import matplotlib.pyplot as plt

def find_winning_prob(p,q,file,s):

    #run commands to find optimal policy and value function
    command1 = f"python encoder.py --opponent data/football/test-{file}.txt --p {p} --q {q} > football_mdp.txt"
    command2 = "python planner.py --mdp football_mdp.txt > value.txt"
    command3 = f"python decoder.py --value-policy value.txt --opponent data/football/test-{file}.txt > policyfile.txt"

    commands = [command1,command2,command3]
                
    for command in commands:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)

    #now read the policyfile.txt and return value function
    path = './policyfile.txt'
    with open(path, "r") as file: # read the result file
        for line in file:
            parts = line.strip().split()
            state = str(parts[0])
            value = float(parts[2])
            if state == s:
                return value

if __name__ == "__main__":

    state = '0509081' 
    file = 1 #greedy defence
    p_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5] # q = 0.7
    q_list = [0.6, 0.7, 0.8, 0.9, 1] # p = 0.3

    #plot Graph 1
    winning_probs = []
    for p in p_list:
        winning_probs.append(find_winning_prob(p,0.7,1,state))
    print(winning_probs)

    plt.plot(p_list,winning_probs,marker='o')
    # plt.title(f'Winning Probability vs p (q=0.7) in Greedy defence')
    plt.title("Probability of winning from 05,09,08,1")
    plt.xlabel('p')
    plt.xticks(p_list)
    plt.ylabel('Probability of winning')
    plt.grid()
    plt.savefig("fig1.png")
    plt.clf()

    #plot Graph 2
    winning_probs = []
    for q in q_list:
        winning_probs.append(find_winning_prob(0.3,q,1,state))
    print(winning_probs)
    
    plt.plot(q_list,winning_probs,marker='o')
    # plt.title(f'Probability')
    plt.title("Probability of winning from 05,09,08,1")
    plt.xlabel('q')
    plt.xticks(q_list)
    plt.ylabel('Probability of winning')
    plt.grid()
    plt.savefig("fig2.png")
    plt.clf()




    