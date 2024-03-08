import argparse

class Encoder():
    def __init__(self, path, p, q):
        print("numStates 8194\nnumActions 10\nend 0 8193")
        self.p = p
        self.q = q
        f = open(path, "r")
        f.readline()
        line = f.readline().split()
        while len(line) > 1:
            state = line[0]
            b1 = 10*int(state[0]) + int(state[1])
            b2 = 10*int(state[2]) + int(state[3])
            r = 10*int(state[4]) + int(state[5])
            pos = int(state[6])
            probs = [float(prob) for prob in line[1:]]
            self.encode_movement(state, b1, b2, r, pos, probs)
            self.encode_pass(state, b1, b2, r, pos, probs)
            self.encode_shoot(state, b1, b2, r, pos, probs)
            line = f.readline().split()
        f.close()
        print("mdptype episodic\ndiscount 1")
        
    def state_to_index(self, state):
        return str(2*(256*(10*int(state[0])+int(state[1])-1)+16*(10*int(state[2])+int(state[3])-1)+10*int(state[4])+int(state[5])-1)+int(state[6]))

    def in_field(self, x, y):
        return (0 <= x <= 3) and (0 <= y <= 3)
    
    def position_to_state_string(self, x1, y1, x2, y2, xr, yr, pos):
        b1 = x1 + 4*y1 + 1
        b2 = x2 + 4*y2 + 1
        r = xr + 4*yr + 1
        return str(b1).zfill(2) + str(b2).zfill(2) + str(r).zfill(2) + str(pos)

    def encode_movement(self, state, b1, b2, r, pos, probs):
        x1, y1 = (b1-1)%4, (b1-1)//4
        x2, y2 = (b2-1)%4, (b2-1)//4
        xr, yr = (r-1)%4, (r-1)//4
        for a in range(8):
            x1_new, y1_new, x2_new, y2_new = x1, y1, x2, y2
            if a < 4:
                x1_new = [x1-1, x1+1, x1, x1][a]
                y1_new = [y1, y1, y1-1, y1+1][a]
                if not self.in_field(x1_new, y1_new):
                    print("transition " + self.state_to_index(state) + " " + str(a) + " 8193 0 1")
                    continue
            else:
                x2_new = [x2-1, x2+1, x2, x2][a-4]
                y2_new = [y2, y2, y2-1, y2+1][a-4]
                if not self.in_field(x2_new, y2_new):
                    print("transition " + self.state_to_index(state) + " " + str(a) + " 8193 0 1")
                    continue
            move_prob = 0
            for i, prob in enumerate(probs):
                if prob == 0: continue
                r_new = [r-1, r+1, r-4, r+4][i]
                xr_new, yr_new = (r_new-1)%4, (r_new-1)//4
                if a < 4:
                    if pos == 1:
                        if (b1 == r_new and (x1_new, y1_new) == (xr, yr)) or ((x1_new, y1_new) == (xr_new, yr_new)):
                            success = prob * (1 - 2 * self.p) / 2
                        else:
                            success = prob * (1 - 2 * self.p)
                    else:
                        success = prob * (1 - self.p)
                else:
                    if pos == 2:
                        if (b2 == r_new and (x2_new, y2_new) == (xr, yr)) or ((x2_new, y2_new) == (xr_new, yr_new)):
                            success = prob * (1 - 2 * self.p) / 2
                        else:
                            success = prob * (1 - 2 * self.p)
                    else:
                        success = prob * (1 - self.p)
                move_prob += success
                print("transition " + self.state_to_index(state) + " " + str(a) + " " + self.state_to_index(self.position_to_state_string(x1_new, y1_new, x2_new, y2_new, xr_new, yr_new, pos)) + " 0 " + str(success))
            print("transition " + self.state_to_index(state) + " " + str(a) + " 8193 0 " + str(1 - move_prob))
        
    def encode_pass(self, state, b1, b2, r, pos, probs):
        x1, y1 = (b1-1)%4, (b1-1)//4
        x2, y2 = (b2-1)%4, (b2-1)//4
        pass_prob = 0
        for i, prob in enumerate(probs):
            if prob == 0: continue
            r_new = [r-1, r+1, r-4, r+4][i]
            xr, yr = (r_new-1)%4, (r_new-1)//4
            cond0 = (x1==x2==xr) and ((y1 <= yr <= y2) or (y2 <= yr <= y1))
            cond1 = (x1 <= xr <= x2) or (x2 <= xr <= x1)
            cond2 = (y1==y2==yr) # and cond1
            cond3 = (x1+y1==x2+y2==xr+yr) # and cond1
            cond4 = (x1-y1==x2-y2==xr-yr) # and cond1
            success = prob * (self.q - 0.1 * max(abs(x1-x2), abs(y1-y2)))
            if (cond0 or (cond1 and (cond2 or cond3 or cond4))): success /= 2
            pass_prob += success
            print("transition " + self.state_to_index(state) + " 8 " + self.state_to_index(self.position_to_state_string(x1, y1, x2, y2, xr, yr, 3-pos)) + " 0 " + str(success))
        print("transition " + self.state_to_index(state) + " 8 8193 0 " + str(1 - pass_prob))
    
    def encode_shoot(self, state, b1, b2, r, pos, probs):
        goal_prob = 0
        for i, prob in enumerate(probs):
            if prob == 0: continue
            r_new = [r-1, r+1, r-4, r+4][i]
            success = prob * (self.q - 0.2 * (3 - (((b1, b2)[pos-1]-1) % 4)))
            if ((r_new == 8) or (r_new == 12)): success /= 2
            goal_prob += success
        print("transition " + self.state_to_index(state) + " 9 0 1 " + str(goal_prob))
        print("transition " + self.state_to_index(state) + " 9 8193 0 " + str(1 - goal_prob))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--opponent", type=str)
    parser.add_argument("--p", type=float)
    parser.add_argument("--q", type=float)
    args = parser.parse_args()
    encoded = Encoder(args.opponent, args.p, args.q)