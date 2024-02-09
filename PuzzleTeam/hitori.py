from solver import Solver, GridSolver, DIRECTIONS, DIRECTIONS8, DIRECTIONS8_HALF
from math import sqrt

class HitoriState:
    def __init__(self, grid, x, y):
        self.grid = [row[:] for row in grid]
        self.x = x
        self.y = y

    def __repr__(self):
        string = ""
        for row in self.grid:
            for char in row:
               #string += "0" if char == -1 else "." 
               string += chr(char - 10 + ord('A')) if char > 9 else str(char) if char > 0 else "-" 
            string += "\n"
        return string

class HitoriSolver(GridSolver):
    def solve(self, board):
        width = height = int(sqrt(len(board)))
        starting_state = HitoriState([[0 for x in range(width)] for y in range(height)], 0, 0)
        starting_state.width, starting_state.height = width, height
        self.numbers = [[ord(board[y * width + x]) - ord('0') if board[y * width + x] < 'a' else ord(board[y * width + x]) - ord('a') + 10 for x in range(width)] for y in range(height)]
        self.solve_recursive(starting_state)
    def get_next_states(self, state):
        states = []
        if self.can_place_num(state, state.x, state.y):
            new_state = HitoriState(state.grid, state.x, state.y)
            new_state.grid[state.y][state.x] = self.numbers[state.y][state.x]
            states.append(new_state)
        if self.can_place_space(state, state.x, state.y):
            new_state = HitoriState(state.grid, state.x, state.y)
            if state.x < len(state.grid[0]) - 1:
                new_state.grid[state.y][state.x + 1] = self.numbers[state.y][state.x + 1]
            if state.y < len(state.grid) - 1:
                new_state.grid[state.y + 1][state.x] = self.numbers[state.y + 1][state.x]
            new_state.grid[state.y][state.x] = -1
            states.append(new_state)
        return states
    def can_place_num(self, state, x, y):
        if state.grid[y][x]:
            return True
        #Check row
        num = self.numbers[y][x]
        if num in state.grid[y]:
            return False
        #Check column
        for Y in range(y):
            if state.grid[Y][x] == num:
                return False
        return True
    def can_place_space(self, state, x, y):
        if x < len(state.grid[0]) - 1 and not self.can_place_num(state, x+1, y) or y < len(state.grid) - 1 and not self.can_place_num(state, x, y+1):
            return False
        if y == 0:
            return True
        if y == len(state.grid) - 1:
            if x > 0 and state.grid[y-1][x-1] == -1 and not self.check_boundary(state, x, y-1) or \
                x < len(state.grid[0]) - 1 and state.grid[y-1][x+1] == -1 and not self.check_boundary(state, x, y-1):
                return False
        elif (x == 0 or state.grid[y-1][x-1] == -1) and (x == len(state.grid[0]) - 1 or state.grid[y-1][x+1] == -1) and not self.check_boundary(state, x, y-1):
            return False
        return True
    def check_boundary(self, state, x, y):
        if (x == 0 or state.grid[y][x-1] == -1) and (x == len(state.grid[0]) - 1 or state.grid[y][x+1] == -1) and (y == 0 or state.grid[y-1][x] == -1):
            return False
        destx, desty = (x+1, y+1) if x < len(state.grid[0]) - 1 and state.grid[y][x+1] == -1 else (x-1, y+1)
        #Flow right
        if x < len(state.grid[0]) - 1:
            result = self.flow_boundary(state, x, y, destx, desty, False)
            if result != None:
                return result
        #Flow left
        if x > 0:
            result = self.flow_boundary(state, x, y, destx, desty, True)
            if result != None:
                return result
        return False

    def flow_boundary(self, state, startx, starty, destx, desty, flow_left):
        dir = 2 if flow_left else 0
        x, y = startx, starty
        rot1 = 1 if flow_left else 3
        rot2 = 3 if flow_left else 1
        while True:
            dx, dy = x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]
            if not self.on_grid(state, dx, dy):
                return None
            elif state.grid[dy][dx] == -1 or dx == startx and dy == starty + 1:
                dir = (dir + rot1) % 4
            elif dx == destx and dy == desty:
                return True
            elif dx == startx and dy == starty:
                return False
            else:
                x, y = dx, dy
                dir = (dir + rot2) % 4

puzzle_easy = '17a392527892774a76898741379a72a4a9a68a5a238961a493486a74241441187379763794a51523a996323537aa5a186848'
#Hard 10x10 - ID: 4048768

puzzle_medium = 'dc8243kb4id8e4a67kj4i2a286fj4i576h393d6ceh36f5h99jgf47bgah2f8g81985de8ac8k878f83436aeb182fjak25ad39a824b2i232h9d9a459e4j267b3f82kah21f9acaeb5a69gcaifb6fg8gd6kf2k4ecfg6a8abkha3g5gikk1cka63hfgi56bi268hdgij5692f28c4id4b1ik6deda5k7diafa9d2kdca1a6g368i56dib616he974392fc3j2b273d243i3g3fh1hij765ei9hch4273868b4hb92gceg361jgagfc32i5ae3h3938gkf4fd51581721k141i161c1b1e2k5hj5a865i8c5d3b48ggbk12hg4d316g98gfgcd'
#Hard 20x20 - ID: 10348311

puzzle_hard = 'tkiu9dl9qa985ptr97265nt2eu3tgo3q364rcufb2oponmj1lfdo9gcefc7mh29565e2b5a5382l75mt2ks5fp5d2u6bocolm46et1qfk13sfanjui7jrj8m6amjlkikcpj4g3k8gtqksfhjj9k7u659lpljhk69u6r646alfsm9gqold8938ctji28donjg5u8k18a2478m86jhlbnrrsk48fc5ktkdcik9rqkh7lbr6rpjgt1g5k3p7gigufqfbg4fcm2gknk6hfqs2aqnmppckukopt2eq3128fi29lqgmibiri73duqjlsfgjj2uuep8jkun4p4ms3st4ijd8e1ale9g4hfsncabq8krifqi9ij662idi4i5ih7p6teis6aki8d87276iog8rfm7j8nf5f9lfu73fib7gjc7fs4qktf3g1tot6ilicrduqh9car9gco9f7smcl9tbpucn9h31epa5pqsin593etqmq75fqhi4p3ukcbs21bo36bmjmaedsefm7ehm3qmtgm4pe8mnmcm9g4i6hujok3c2c5e6msoaod7689p6143tt8tb1ugdkdr7dhdded5odn4l4md7l2krp5rtinsagaqo4ei8rlblci3lfouoeqfc8n49c623nklcbtgat5osn12c9nkj12cfchr1m678cb1ea5pciksadajkbs7t253tjnjo1jrjctuj6l68jdjkdpljb1qk8cnk2a9ikgjr964khufu5p5kjnkcm175bsak4kokrk853d5e5fk2eu6pqn282524q96dq3ob6fec7egset4p5tu8c9q868n8bp31pj2ma9lpeph84rft36ks4doc4moeqk2oj3h1o7on4epee3m454o1f9csjtsue64knndgbrr'
#Weekly 30x30 - 10/05/20

puzzle_ultra = '9wjdk3khe54on2uynbntvzv14ur97ueim9g1bc38bfbw4p72y63xys9u5t57j7o5mlk9eb52pug9ijgko4lfitgwl8kyl6dkhpckqknizgbmbju1uybsvb98uz3i3lowe6rnxu53h6pbhzt1hgduofow5dnsbtqyxdk8cadp6hi7d3o7rufutpuquaug6oue4ku3bmunuwu9hjuxu1kp1gm6prvcq5cl4i2v4w479b4uctcopsph4mpadri4p1weq8hdcbx5bzinqyvblbjsd7gqe91b126cnmeykn4681lp6fnson3nteherejbpyp9p5etskrxopdens1jpcpq3egr6puems4de5vu3optm93wypa4zhmq32kesfneg4lexs3ivjfy2ujhs4kjljaj7ds1qs9j6srspsb2u4fcip3pcrobqn1xyo9petgh6h2ozn8nv4dcb6jcxr7sc966yq7gk7u7wdf8p7n8c3vcam2m3tp1edq9q8oier6ecqyaqmgmztv7mfkmnvesc67grosfkarx77d74hsirrzuy71ntswfdmhz7ywsfigwcjsk5wbzi2sl38sm1x9nqoryjosznpvoephpp7ocipx8oqy2pmdotpbylytlw3llom8ydn6129msmrmu2vl542inc2hy7b8leozlivdf14afbqy2j5vp4ryy74svmj9l6151txhxrlicpkskk7cec3b9kd8j14kqknb8kpzlhiw95bpixp6sivj8r5d1mlcf5ug354zke7nk27lgciccrkw5dc9kyxctakmf17uvknu2lg5q1g232jzc4mqpog9x2vegrhgacypiawb8swm6ziwjvzhnzropqxv5lp9ppkwywdwjsrja8ljijzd7ekdvj6m1d5ojgjuxdydftdqm7nx99f96cldmiu4zbabsh1w1pej8moty5dhj2d4jj5jv3jqnzdgydmnlnsjejojt9d6jcbsqw2k52p2arbvb3xg62hbt2lx8giebd2fi7digviy514m5u58aqenwnj5tifcscn3oxaf6xk118n3jbsyxuxhcxdcmxwbxo4xl5cex2di4a2suzp8xbengmrft5rday5c5bkbwlzq69humhkyqhhyxh5y7t6ay46rhf6isyg66b86lgvacmxu4k2mwd9brens6i7zu6yu57bjg7hiyvxseigdznfms3jlzhdov6id4rwrqzdasv'
#Monthly 35x35 - 10/01/20

HitoriSolver().solve(puzzle_ultra)