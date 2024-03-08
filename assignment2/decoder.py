import argparse

def state_to_index(state):
    return 2*(256*(10*int(state[0])+int(state[1])-1)+16*(10*int(state[2])+int(state[3])-1)+10*int(state[4])+int(state[5])-1)+int(state[6])-1

def read_value_policy(path):
    v_pi = []
    try:
        f = open(path, "r", encoding='utf-8')
        int(f.readline().split()[1])
    except UnicodeDecodeError as e:
        f = open(path, "r", encoding='utf-16-le')
        int(f.readline().split()[1])
    for _ in range(1, 8193):
        line = f.readline().split()
        v_pi.append((float(line[0]), int(line[1])))
    f.close()
    return v_pi

def decode(path, v_pi):
    with open(path, "r") as f:
        f.readline()
        for line in f:
            state = line.split()[0]
            idx = state_to_index(state)
            v, pi = v_pi[idx]
            print(state + " " + str(pi) + " " + str(v))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--value-policy", type=str)
    parser.add_argument("--opponent", type=str)
    args = parser.parse_args()
    decode(args.opponent, read_value_policy(args.value_policy))