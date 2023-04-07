from solver import Solver
import re, time

class LockpickState:
    def __init__(self, access, stock, edges):
        self.access = access
        self.stock = dict(stock)
        self.edges = edges[:]
        self.last_move = None
        self.last_access = None
        self.master = []
        self.win = False
        self.terminate = False
        self.mimic = False
    def __eq__(self, state):
        if self.stock != state.stock:
            return False
        return self.edges == state.edges
    def __hash__(self):
        return hash((str(self.edges), str(sorted([(k, v) for k, v in self.stock.items()]))))
    def __repr__(self) -> str:
        s = 'Access:' + str(self.access) + '\n'
        s += 'Stock:' + str(self.stock) + '\n'
        s += 'Master:' + str(self.master) + '\n'
        if self.previous:
            s += 'Last move:' + str(self.last_move) + ' ' + str(self.last_access) + '\n'
            edge = self.edges[self.last_move][1]
            pedge = self.previous.edges[self.last_move][1]
            if self.last_access:
                s += "Last opened: " + str(pedge[len(edge) - len(pedge)]) + '\n'
            else:
                s += "Last opened: " + str(pedge[len(pedge) - len(edge) - 1]) + '\n'
        for e in self.edges:
            s += str(e[0]) + '-' + ''.join(str(e[1])) + '-' + str(e[2]) + '\n'
        return s
    def can_open(self, color, num):
        stock = self.stock
        req = color[-1].lower()
        if num == '0': return stock.get(req, 0) == 0
        elif num == 'x': return stock.get(req, 0) > 0
        elif num == '-x': return stock.get(req, 0) < 0
        elif int(num) < 0: return stock.get(req, 0) <= int(num)
        else: return stock.get(req, 0) >= int(num)
    def spend_amount(self, color, num):
        stock = self.stock
        req = color[-1].lower()
        if num == '0': return 0
        elif num[-1] == 'x': return stock[req]
        else: return int(num)
    def spend_keys(self, key, amount):
        if key + '*' not in self.stock:
            if key not in self.stock: self.stock[key] = 0
            self.stock[key] -= amount
            if self.stock[key] == 0: del self.stock[key]
    def mimic_color(self, mimic):
        for i, e in enumerate(self.edges):
            self.edges[i] = (e[0], e[1][:], e[2])
            for i2, l in enumerate(self.edges[i][1]):
                if l[0] and l[0][-1].isalpha() and '~' not in l[0]:
                    self.edges[i][1][i2] = (l[0][:-1]+mimic, l[1], l[2])
    def open(self, i, si, aura, sign=1):
        seq = self.edges[i][1]
        color = seq[si][1]; num = seq[si][2]
        if 'X' in num:
            num, stacks = num.split('X')
            if sign is None:
                sign = -1 if int(stacks) < 0 else 1
            stacks = int(stacks) - sign
            if stack_limit and abs(stacks) > stack_limit:
                return False
            if stacks == 1:
                seq[si] = (aura, color, num)
                self.terminate = True
                return True
            if stacks != 0:
                seq[si] = (aura, color, num + 'X' + str(stacks))
                self.terminate = True
                return True
        elif sign == -1:
            seq[si] = (aura, color, num + 'X2')
            self.terminate = True
            return True
        seq.pop(si)
        if len(seq) == 0:
            new_access = self.edges[i][0] if si == -1 else self.edges[i][2]
            if new_access is not None:
                self.access = set(self.access)
                self.access.add(new_access)
        return True
    def unlock(self, i, back=False):
        state = LockpickState(self.access, self.stock, self.edges)
        if self.last_move == i and self.last_access == back and not self.terminate:
            state.master = self.master
        state.last_move = i
        state.last_access = back
        next_states = []
        stock = state.stock
        state.edges[i] = (state.edges[i][0], state.edges[i][1][:], state.edges[i][2])
        seq = state.edges[i][1]
        if len(seq) == 0:
            return []
        si = -1 if back else 0
        lock = seq[si]
        aura, color, num = lock
        #specials
        if color == '$':
            state.win = True
            state.open(i, si, aura)
            return [state]
        elif color == '>':
            if back: return []
            state.access = set()
            state.open(i, si, aura)
            return [state]
        elif color == '<':
            if not back: return []
            state.access = set()
            state.open(i, si, aura)
            return [state]
        #Auras
        if stock.get('r', 0) >= 1 and '!' in aura:
            aura = aura.replace('!', '')
        if stock.get('g', 0) >= 5 and '@' in aura:
            aura = aura.replace('@', '')
        if stock.get('b', 0) >= 3 and '#' in aura:
            aura = aura.replace('#', '')
        if stock.get('n', 0) > 0 and color[0].isupper() and \
            'U' not in color and color != 'N' and '~' not in aura and \
                not ('Z' in color and aura[-1] in 'MU'):
            aura = '~'+aura
        elif stock.get('n', 0) < 0 and '~' in aura:
            aura = aura.replace('~', '')
        if aura != lock[0] and not (aura.replace('~', '') == lock[0] and num != '0' and 'M' not in color and 'Z' not in color):
            s = LockpickState(state.access, state.stock, state.edges)
            s.edges[i] = (s.edges[i][0], s.edges[i][1][:], s.edges[i][2])
            s.edges[i][1][si] = (aura, color, num)
            s.last_move = i
            s.last_access = back
            s.master = state.master
            next_states.append(s)
        if '!' in aura or '@' in aura or '#' in aura:
            return next_states
        if '~' in aura:
            if type(color) is list:
                color = ['N', [(l[0], 'N', l[2]) for l in color[1]]]
            else: color = 'N'
        elif mimic_color and aura and type(color) is str:
            color = color.replace('z', aura[-1].lower()).replace('Z', aura[-1])
        stacks = 1
        if 'X' in num:
            num, stacks = num.split('X')
            stacks = int(stacks)
        if not num: num = '1'
        #Keys
        if type(color) is str and color.islower():
            if color + '*' in stock:
                if num == '-*': del stock[color + '*']
            elif num[0] == '=': stock[color] = int(num[1:])
            elif num == '-': stock[color] = -stock.get(color, 0)
            elif num == '*': stock[color + '*'] = 1
            elif num != '-*':
                if color not in stock: stock[color] = 0
                stock[color] += int(num)
                if stock[color] == 0: del stock[color]
            state.open(i, si, aura)
            return next_states + [state]
        #Master Key
        master = stock.get('m', 0)
        if master: master = 1 if master > 0 else -1
        if master and 'U' not in color and 'M' not in color and not ('Z' in color and aura[-1] in 'MU'):
            s = LockpickState(state.access, state.stock, state.edges)
            s.edges[i] = (s.edges[i][0], s.edges[i][1][:], s.edges[i][2])
            s.master = state.master[:] + [len(seq)-1]
            s.last_move = i
            s.last_access = back
            if s.open(i, si, aura, master):
                s.spend_keys('m', master)
                next_states.append(s)
        #Combo Doors
        if type(color) is list:
            spend = color[0]
            if spend == 'Z':
                spend = aura[-1]
            seq = color[1]
            amount = 0
            for lock in seq:
                _, color, num = lock
                if not num: num = '1'
                if 'Z' in color:
                    color = aura[-1]
                if not state.can_open(color, num):
                    return next_states
                amount += state.spend_amount(color, num)
            state.spend_keys(spend.lower(), amount)
            if mimic_color:
                state.mimic_color(spend)
        #Regular Doors
        else:
            if not state.can_open(color, num):
                return next_states
            state.spend_keys(color[0].lower(), state.spend_amount(color, num))
            if mimic_color:
                state.mimic_color(color[0])
        state.open(i, si, aura, None)
        next_states.append(state)
        return next_states

def parse(stock, edges, target_moves=None):
    if isinstance(edges, str):
        edges = [edges]
    state = LockpickState({0}, {}, [])
    state.target_moves = target_moves
    state.previous = None
    pattern = r'([!#@]*)((?:[A-WYZ]/)?(?:[a-wyzA-WYZ$<>]|\[[^\[]*\]))(-?\d*X-?\d+|-?x|=?-?\*?\d*)'
    parse = re.findall(pattern, stock)
    for k in parse:
        if len(k[2]) == 0:
            state.stock[k[1]] = 1
        elif '*' in k[2]:
            state.stock[k[1] + k[2]] = 1
        else:
            state.stock[k[1]] = int(k[2])
    end = False
    for e in edges:
        tup = ()
        if isinstance(e, str):
            tup = (0, e, None)
        elif len(e) == 1:
            tup = (0, e[0], None)
        elif len(e) == 2 and isinstance(e[0], str):
            tup = (0, e[0], e[1])
        elif len(e) == 2 and isinstance(e[1], str):
            tup = (e[0], e[1], None)
        else:
            tup = e
        a, seq, b = tup
        seq = seq.split('|')
        for s in seq:
            if '$' in s:
                end = True
            parse = re.findall(pattern, s)
            for i, lock in enumerate(parse):
                aura, color, num = lock
                if 'Z' in color or 'z' in color:
                    aura = aura+'Z'
                    parse[i] = (aura, color, num)
                    state.mimic = True
                if '[' in color:
                    if '/' in color:
                        spend, color = color.split('/')
                    else:
                        spend = color[1]
                    locks = [spend, re.findall(pattern, color[1:-1])]
                    for c in 'MUZ':
                        if spend != c and any([c in l[1] for l in locks[1]]):
                            locks.append(c)
                    parse[i] = (aura, locks, num)
            state.edges.append((a, parse, b))
    if not end:
        print(state)
        print('Goal is missing')
        return None
    return state

class LockpickSolver(Solver):
    def get_next_states(self, state):
        next_states = []
        for i, (start, seq, end) in enumerate(state.edges):
            access = []
            if start in state.access: access.append(False)
            if end in state.access: access.append(True)
            if state.terminate and i == state.last_move and state.last_access not in access:
                access.append(state.last_access) #Allow additional moves on edge after one way drop
            for a in access:
                if i == state.last_move and a == state.last_access and not state.terminate:
                    continue
                states = state.unlock(i, back=a)
                i2 = 0
                while i2 < len(states):
                    if not states[i2].terminate:
                        next = states[i2].unlock(i, back=a)
                        states += next
                    i2 += 1
                next_states += states
        return next_states
    def check_state(self, state): #Place to add some extra logic
        if not self.special:
            return True
        if self.special == '1-B':
            if state.last_move != 8 and len(state.edges[state.last_move][1]) != 2:
                return False
        elif self.special == '2-10':
            prev = state.previous
            if state.last_move in [3, 4] and prev.last_move not in [3, 4]:
                if len(prev.edges[0][1]) < 2 or prev.stock.get('o', 0) == 0:
                    return False
            elif prev.last_move in [3, 4] and state.last_move not in [3, 4, 0]:
                if prev.stock.get('o', 0) == 0:
                    return False
        elif self.special == '5-3':
            for edge in state.edges:
                for lock in edge[1]:
                    if '~' in lock:
                        return False
        elif self.special == '5-B':
            if state.last_move == 3 and state.stock.get('u', 0) == 0:
                return False
        elif self.special == '6-10':
            if len(state.edges[0][1]) <= 1:
                return True
            total = abs(state.stock.get('u', 0)) + sum([sum([abs(int(lock[2])) for lock in edge[1] if lock[1] == 'u' and lock[2] != '-']) for edge in state.edges])
            return total >= 25
        elif self.special == '7-E':
            if state.last_move == 0 and state.stock.get('c', 0) == 0: return False
            if state.last_move == 1 and state.stock.get('o', 0) == 0: return False
            if state.last_move == 2 and state.stock.get('p', 0) == 0: return False
            if state.last_move == 3 and state.previous.stock.get('c', 0) != 0: return False
            if state.last_move == 4 and state.previous.stock.get('o', 0) != 0: return False
            if state.last_move == 5 and state.previous.stock.get('p', 0) != 0: return False
        elif self.special == '8-5':
            if not state.edges[4][1] and state.stock.get('w', 0) == 0 and (not state.edges[3][1] or ('', 'W', '0') in state.edges[3][1]):
                return False
        elif self.special == '9-3':
            if state.last_move == 8:
                return False
            if state.last_move == 2 and 1 not in state.access and len(state.edges[1][1]) == 5:
                return False
            if state.last_move == 3 and 1 not in state.access and len(state.edges[2][1]) == 5:
                return False
            total = sum(state.stock.values())
            for e in state.edges:
                for l in e[1]:
                    if type(l[1]) is str and l[1].islower():
                        total += int(l[2][-1]) if l[2] else 1
            if total < 32:
                return False
        elif self.special == '9-B':
            if state.last_move == 19:
                return False
            if state.last_move < 8 and state.stock.get('c', 0) != 0:
                return False
        elif self.special == '9-C':
            for k, v in state.stock.items():
                if v < 0 and k != 'm':
                    return False
        elif self.special == '9-E':
            for i, i2 in ((6, 7), (7, 6), (10, 11), (11, 10)):
                if state.last_move == i and len(state.edges[i][1]) == 0 and len(state.edges[i2][1]) > 0:
                    state.open(i2, -1, '')
                    return True
        elif self.special == '10-3':
            prev = state.previous
            if state.last_move in [3, 4] and prev.last_move not in [3, 4]:
                if len(prev.edges[0][1]) < 2 or prev.stock.get(prev.edges[0][1][0][0][-1].lower(), 0) > 0:
                    return False
            elif prev.last_move in [3, 4] and state.last_move not in [3, 4, 0]:
                if prev.stock.get(prev.edges[0][1][0][0][-1].lower(), 0) > 0:
                    return False
        elif self.special == '10-6':
            prev = state.previous
            if state.last_move == 6 and len(state.edges[6][1]) <= 3 and prev.stock.get('n', 0) > 0:
                if 'U' not in prev.edges[7][1][0][0] and '~' not in prev.edges[7][1][0][0]:
                    return False
        elif self.special == '10-A':
            prev = state.previous
            if 0 < state.last_move < 7 and prev.stock.get('n', 0) > 0:
                if prev.edges[state.last_move-1][1] and '~' not in prev.edges[state.last_move-1][1][0][0]:
                    return False
        elif self.special == '10-B':
            prev = state.previous
            if state.last_move == 10 and prev.edges[9][1] and prev.edges[9][1][0][2] == '0':
                return False
        return True
    def check_finish(self, state):
        return state.win
    def print_moves(self, moves, verbose=False):
        red, yellow, green, blue, black = '\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[00m'
        for i, m in enumerate(moves):
            if i == 0: continue
            pm = moves[i-1]
            print(str(i)+': ', end='')
            locks = pm.edges[m.last_move][1]
            next = m.edges[m.last_move][1]
            for i2, lock in enumerate(locks):
                if type(lock[1]) is list:
                    if lock[1][1] and lock[1][0] == lock[1][1][0][1]:
                        lock = (lock[0], '['+''.join([l[0] + l[1] + l[2] for l in lock[1][1]])+']', lock[2])
                    else:
                        lock = (lock[0], lock[1][0] + '/['+''.join([l[0] + l[1] + l[2] for l in lock[1][1]])+']', lock[2])
                masterloc = i2 if m.last_access else len(locks) - i2 - 1
                if '~' in lock[0]:
                    lock = (lock[0].replace('~', ''), 'N', lock[2])
                if lock[0] and lock[0][-1].isalpha():
                    lock = (lock[0][:-1], lock[1], lock[2])
                if m.last_access and i2 >= len(next) or \
                 not m.last_access and i2 < len(locks) - len(next):
                    if masterloc in m.master:
                        print(yellow + lock[0] + lock[1] + lock[2], end=' ')
                    else:
                        print(red + lock[0] + lock[1] + lock[2], end=' ')
                else:
                    next_lock = next[i2] if m.last_access else next[i2 + len(next) - len(locks)]
                    if '~' in next_lock[0]:
                        next_lock = (next_lock[0].replace('~', ''), 'N', next_lock[2])
                    if next_lock[0] and next_lock[0][-1].isalpha():
                        next_lock = (next_lock[0][:-1], next_lock[1], next_lock[2])
                    aura = next_lock[0]
                    for c in lock[0]:
                        color = black if c in aura else red
                        print(color + c, end='')
                    if masterloc in m.master:
                        print(yellow + lock[1] + lock[2], end=' ')
                    elif lock[2] != next_lock[2]:
                        print(red + lock[1] + lock[2] + black, end=' ')
                    elif lock[1] != next_lock[1] and type(next_lock[1]) is not list:
                        print(blue + next_lock[1] + lock[2] + black, end=' ')
                    else:
                        print(black + lock[1] + lock[2], end=' ')
            print(black)
            if verbose: print(m)
    def solve(self, state, debug=False, print_moves=True, verbose=False):
        #print(state)
        self.start = 0
        self.special = None
        cases = {p1B: '1-B', p210:'2-10', p53:'5-3', p5B:'5-B', p610:'6-10', p7E:'7-E',
            p85:'8-5', p93: '9-3', p9B: '9-B', p9C: '9-C', p9E: '9-E',
            p103:'10-3', p106:'10-6', p10A:'10-A', p10B:'10-B', finale:'finale'}
        if state in cases:
            self.special = cases[state]
        limit = {p87: 2, p8A: 3, p1010: 2, p10C: 2}
        global stack_limit
        if state in limit:
            stack_limit = limit[state]
        else:
            stack_limit = None
        target = state.target_moves
        global mimic_color
        mimic_color = state.mimic
        if debug: moves = self.solve_optimal_debug(state)
        else: moves = self.solve_optimal(state, prnt=False)
        red, green, black = '\033[91m', '\033[92m', '\033[00m'
        if moves and target and len(moves)-1 > target:
            print(red, moves[0], 'Len', len(moves)-1, 'exceeded target of ', target, black)
        if moves and target and len(moves)-1 < target:
            print(green, moves[0], 'Target beaten! New target:', len(moves)-1, black)
        if print_moves:
            self.print_moves(moves, verbose)
        return moves

def practice():
    solver = LockpickSolver()
    tests = [
        p11, p12, p13, p14, p15, p16, p17, p18, p19, p110, p1A, p1B, p1C,
        p21, p22, p23, p24, p25, p26, p27, p28, p29, p210, p2A, p2B, p2C, p2D,
        p31, p33, p34, p35, p36, p37, p3A, p3B, p3D,
        p41, p42, p43, p44, p45, p46, p47, p4A, p4B, 
        p51, p52, p53, p54, p55, p56, p57, p5A, p5B,
        p62, p63, p64, p65, p66, p67, p68, p69, p610, p6A, p6B, p6C,
        p71, p72, p73, p74, p75, p76, p77, p78, p710, p7A, p7B, p7C, p7D, p7E,
        p81, p82, p83, p84, p85, p86, p87, p8A, p8B,
        ]
    for i, puzzle in enumerate(tests):
        sol = solver.solve(puzzle, print_moves=False)
        input()
        solver.print_moves(sol)

def test(full=False, print_moves=False):
    solver = LockpickSolver()
    tests = [
        p11, p21, p31, p41, p51,      p71, p81, p91, p101,
        p12, p22,      p42, p52, p62, p72, p82, p92, p102,
        p13, p23, p33, p43,      p63, p73, p83,      p103,
        p14, p24, p34, p44, p54, p64, p74, p84, p94, p104,
        p15, p25, p35, p45, p55, p65, p75, p85, p95, p105,
        p16, p26, p36, p46, p56, p66, p76, p86, p96, p106,
        p17, p27, p37, p47, p57, p67,                p107,
        p18, p28,                p68, p78,           p108,
        p19, p29,                p69, 
             p210,               p610,p710,
        p1A, p2A, p3A, p4A,                     p9A,
             p2B, p3B, p4B,      p6B, p7B, p8B,  
        p1C, p2C,                p6C, p7C,
             p2D,                               p9F]
    if full:
        tests += [p23, p44, p77, p87, p69, p79, p110, p710,
        p5A, p6A, p7A, p8A, p1B, p5B, p9B, p3D, p7D, p9D, p7E, p10B]
    #Exclude 3C, 48, 4C, 61, 93, 9C, 1010
    start_time = time.time()
    for i, puzzle in enumerate(tests):
        print('Test', str(i+1)+'/'+str(len(tests)))
        sol = solver.solve(puzzle, print_moves=print_moves)
        if len(sol)-1 != puzzle.target_moves:
            print('\033[91m')
            print(puzzle)
            print('Solve Failed, test terminated\033[00m')
            return
    elapsed = time.time() - start_time
    print("\033[92mTest Complete in {:.2f} seconds.\033[00m".format(elapsed))

p11 = parse('w', 'Wo|Op|P$', 3)
p12 = parse('w', 'Wo|WwO$', 3)
p13 = parse('w', 'Wo|Pk|Wp|Oc|K$', 3)
p14 = parse('', ['OO$|WWoo', ('wW|gG', 1), (1, 'Gww|Go')], 5)
p15 = parse('w', 'WwBbOw|OwBoo|WoOw|OoWb|WW$', 10)
p16 = parse('o', 'OoOOcCO$|OcCocCC$|OoOoCoC$', 4)
p17 = parse('wp', [('CoPkCoP|OoCkPwOwW|WcKcPwKcWoO', 0), 'KP$'], 9)
p18 = parse('w2', 'O3w4|W2ow3|W6$|O2w2|W2o2w', 4)
p19 = parse('w16', [('W2W3W2W3W|WW6WW|W4WW2W3', 1), (1, 'W3W2W3$|W2W3W2$', 2)], 2)
p110 = parse('p16o8g4c2', ['W6$|O4w|G2C2w', ('WP4wGP2O2|GP2wGO2', 0), 'P6O2c2|C3Gw|P6w|G2C2w|CCw'], 8) #Takes a bit (0.5 min)
p1A = parse('k', ['PwWcPc', ('KkOpP|OpWwC|KoPkK', 1), (1, 'p|PpOw|OoWp|CoKoWwK$')], 19)
p1B = parse('w5o2p3g4k2', [('PPcGG|WKcWW|WKcGP|GWcKO|WWcWG|OOcKO|GPcPW|GOcOW', 0), 'C8$'], 9) #Uses special logic
p1C = parse('w2', 'WkKoOcCw|WpPcCkKw|WgGkKpPw|WoOpPgGw|WcCgGoOw|P2p2K2k2C2c2O2$', 15)

p21 = parse('m', [('W', 1), (1, 'mw'), (1, 'WP', 2), (2, 'W2w2|Wm|m|W2W$')], 7)
p22 = parse('m', ['W2w3|W2mO2m', ('Wo2O4K4', 1), (1, 'PmCmW6m|mR8w6P$')], 9)
p23 = parse('m', [('OgGmW|WoPmRgP|PgGoOpWpP|GwOoPwWmGoO', 1), (1, 'mRwCgKpN$')], 15)
p24 = parse('m3w11', [('W3W2W3|W3W8', 1), (1, 'W2W6|W12W|WW3W', 2), (2, 'W5W6|W3W3W3W3', 3), (3, 'W3$')], 4)
p25 = parse('', [('W0w', 1), (1, 'W2w|wW|W0WwW0$')], 8)
p26 = parse('mo4', ['O2p2WWp2|O2w2WWp2|WWp2PPPPo4', ('PPO0', 1), (1, 'O2O2$|OOw4')], 6)
p27 = parse('w15o15c15', ['C2W8C4|CO6C12|W2O2C2|O4|W0O0C0$', ('C6|W2O12C2', 1), (1, 'C3OW3W|W6O')], 6)
p28 = parse('o3p3c3', 'C3P3O3m|O12o3p3O3c3P3o3P3o3|O3p3O3p3P6o3o3O6o3c3|C3c3P6o3c3C3p3O3p3C3p3|C6c6O6o6P3P3C3$', 9)
p29 = parse('o24', ['O24W3w5', ('O2o2O4', 1), (1, 'W8o2|Ow2|O4o4w4'), (1, 'W2oO2W0o4W2', 2), (2, "O0WW0$|O8|O6W2w2|O0w4|O2W6o2w8|W0w4o6|O8")], 14)
p210 = parse('o', ['O0o|OoP2c|OoC2p2|Oc|Po4', ('O0', 1), (1, 'P2p2C2O0P0$|Oc2Po2|PCpO2c2')], 11) #Bridge edge case (special logic)
p2A = parse('m3w2k2o2c3p4', [('RW|KO', 1), (1, 'CC|OK', 2), (2, 'OK|WP', 3), (3, 'CC|WO', 4), (4, 'OR|OW', 5), (5, 'PP|KO', 6), (6, 'OR|RW', 7), (7, 'CC$|PP$')], 8)
p2B = parse('m', ['O4mK2mp4|W2k24w3', ('K24', 1), (1, 'C2k2W8wc|W3mWCR$|P4m')], 9)
p2C = parse('m3p16o3', [('O2', 1), ('O4', 3), (1, 'O2P4|O2o6|O2P2'), (1, 'O4P2', 2), (2, 'O2p2o6|OOOOO3P3P6'), (2, 'O2', 3), (3, 'P4o|P0P0P0P0$')], 11)
p2D = parse('o4p6', ['P3O2|P6o4', ('O4', 1), (1, 'P3o2O2p3|PP0$'), (1, 'o6', 2), (2, 'O2O0p3|OO0p2|P6O6p12'), (2, 'P0Oo2O', 3), (3, 'O2o4p3|P3P0P3o2O6p5')], 16)

p31 = parse('', ['o', ('Oxo2Ox', 1), (1, 'pp'), (1, 'Px', 2), (2, 'Pxo|Pxo2'), (2, 'Ox', 3), (3, 'p|OO$')], 10)
p32 = parse('c4', 'P8$|CkKp|CkKp|CkKp|CkK0p|KKxc4|CkK0p|CkK0p|CkKp|CkK0p', 14) #Takes a while (2.9 min)
p33 = parse('c6w20o40', ['C6Wx|C6Ox', ('O24W5|WO5O|O5W5', 1), (1, 'W5O2W|W4OO5|W5W5', 2), (2, 'O5O2W5W2O0W0$')], 7)
p34 = parse('', [('w3w=1Ww3', 1), (1, 'Ww=3|Ww=2|WW3W2$')], 7)
p35 = parse('', 'Oo3c4|O4c4|O3o3c4|C24$|O2o4c4|O6o=3c4|O5o5c4|o3OOOo3', 9)
p36 = parse('w2', ['WW0w=8WW0w=5W2W0w=50WW0$|W0w4W2w4|W2w4W2w8', ('W6|W2w=2', 1), (1, 'W2W1|W2W0w8'), (1, 'W0', 2), (2, 'W8w=1|W24w')], 15)
p37 = parse('', ['p=6p=4p=5p=8p=6p=2p=3p=2c', ('P6P0', 1), (1, 'P3P0P2P0Pxc'), (1, 'P4P0|P5P0', 2), (2, 'P8P0c|P2P0C3P0$')], 14)
p3A = parse('w', 'Kwc3|C2w|WkWkWkCc|KwWkOww|WkKw|WWW$|CxKwKwKkWwCo', 15)
p3B = parse('p4', [('Pp=0WwPp=0Oo=0Pp=0PoO', 0), 'PoPp=0o|OoOp|PpWow|Ow=0Www|WW$'], 14)
p3C = parse('c15', 'O2C4c=27C2C2|O2c4c4c4|O2c4O0c8C4|O2c4C4c12C8|O2C4C4|O2O0O2O0c4O6|o4O0o4O0o16O0o8O0C|O2C4C4c4Ox|C0C0$', 17) #Takes a long time (8.2 min)
p3D = parse('m3o24', ['W3w6W3O5|WRKm=0O0W0K0$|W3k15O4K4w2|m=0K3W3O|m=0K3O3k6', ('K4m=0O3K3', 1), (1, 'WK3O2|WO6|W4w8')], 11) #Takes a bit (0.5 min)

p41 = parse('mw6', '!O0O2w2|OOp4!P4o2w2|W2W2o2P2P2r|!W3!W3R$', 7)
p42 = parse('g5p3', ['@G0@G0$|@P3g|P3G3', ('@P0', 1), (1, 'G@P2p6G5|G2p2P3g5')], 12)
p43 = parse('b2', ['B4b4|#Bm|Bb2', ('#B3b2#B0mB2', 1), (1, 'bB2|bB2|bB2|#B0#B0$')], 13)
p44 = parse('m3', [('M3', 1), (1, 'o4O0c2C3m3|O2O2c2C2m2M3m5|M5M0$')], 6)
p45 = parse('w', 'Kw!Orw|W4r|WoKo!CkR0O0!Oow|Oc2Cw3Ro|OcKoWo2Ow|OkCk!W0o|Wo!Co!Rc|!O2!W2$', 17)
p46 = parse('b3', 'WoWow|#KwKc|BkWoWb|BkWc|R$|OwOw|Ko#Kc|BkWwOw|BkOc|#C2CCm', 21)
p47 = parse('m2', 'Rx|Gx|Bx|!R0r2B0g2!B2g2G0b#B0m2|B2r2B0g2#G0b2G2b2G0m2|G2g2G0b@R2g2G0r2R0m2|R2bG2g2!B0r2#R0b2R2m2|M8B6$', 24)
p48 = parse('c25p20k15m10', 'P4C3b3@K8G2P5K4|C3Bg5G3P0#C6G0K2P5|@G5C3K8C3rR!P6C6|!R@G8#B3R0G0B0!WKPC|M0K0P0C0$', 7) #Takes a very long time (10.1 min)
p4A = parse('mr', ['Rr|R|!R0!R0R', ('!R0!R0', 1), (1, '!R0r!R0r!R0R|!R0!R0mrrm!R0R2'), (1, '!R0', 2), (2, 'rR!R0!R0Rr|!R0!R0!R0!R0!R0!R0$')], 40)
p4B = parse('', ['#R0g=4|b2B3R|g4G2m|!G2B2!M0b3@R0#B0b2@B2#G0m4|m2@B3Gx|r5R4', ('!R0@G0#B0M0', 1), (1, 'G3b2#G0m|#M4r|!@#W0$')], 20)
p4C = parse('m10k15p20c25', 'M4m2|C8KP4P4KC|K12C3KP6K4C3P5|P5C4K12P8K5C12|M0M0K0K0P0P0C0C0$', 7) #Takes a long time (6 min)

p51 = parse('w2', ['W2o3|Cn2|C2c3|O3c2', ('C4n13', 1), (1, 'KC6|P4|N4|W3O2|W0$')], 9)
p52 = parse('w', 'CCCBxCCC$|WpPwPpPoWoc2|WoOwOwOoPwc2|WnWnOpOpPnc2', 13)
p53 = parse('m24', [('M4M2|N3MM3', 1), (1, 'M3M2M3|MM8', 2), (2, 'M6n10'), (2, 'M3M2', 3), (3, 'M3M3N3|M3M0N0|MM4M3M', 4), (4, 'M2N2N4M2|M2M4M2M', 5), (5, 'M24M0$')], 9) #Uses special logic
p54 = parse('', ['W2W2W4|W2W2W6p2|n8N0C0mM0C0OOKKPP$', ('c7', 1), (1, 'C5o2|C0C2k2')], 10)
p55 = parse('k10', ['K4|N2k25|K2n10K5N6|K2N4|K3K2', ('K0K12', 1), (1, 'N2K4|N2n15|K6n15K6|K0K2K0K0$')], 14)
p56 = parse('u4', ['U2m4U3n5O5O5u4', ('C2M2uU4m', 1), (1, 'KCm|O6c6|BxOPCu|U$|C4n2|C2n2')], 12)
p57 = parse('', 'c30|n20|u10|K24U$|U3C6C2N0C3C3Cxk8|U3C2N3C12NN0Ck8|U3C5N5CxC2N2k8|U3C0C8C6CxCk8', 13)
p5A = parse('m5', ['W2CPO2n2|O2o|O2o|W2w2|Wp|Wp|Wc|Wc', ('Mxw2', 1), (1, 'WWc2|WWp2|WWo|OOP4CC$')], 8) #Takes a bit (0.5 min)
p5B = parse('m2', ['B3g8w4U3m2U2', ('W4', 2), (2, 'G2u9k12Mg2Gx'), (2, 'u=5', 4), (4, 'UU0gK4'), (4, 'RxKK6', 5),
    (5, 'G4U2w5'), (5, 'C3@U0K4m8g=2', 6), (6, 'W2G3M2u|K6G0W0u'), (6, 'K3W5W0@K0PG0W', 7), (7, 'G2@G0u|U2W2u2|U3U0$')], 23) #Takes a while (1.9 min), uses special logic

p61 = parse('', [('c-5c9c-4c-4|c-2c4c4c-2|c2c3c-8c3c4c-4|c-1c-1c-2c7c-1c-1', 1), (1, 'C24$|c-1c-2c-3c8|c-2c3c-4c3|c-6c2c2c')], 8) #Takes a while (3.8 min)
p62 = parse('', [('O-2c4o-2|C2o5|o-4O-5$'), ('O-3o-2C4c-4O-2o4', 1), (1, 'C-2o-5|O8|C-2o-2|C-2o3|C-2c2')], 9)
p63 = parse('m', [('P-2p-2P-4P0p2P-3p-4P-2p3P8', 1), (1, 'P3p-2|P2p7|P2p-10'), 'P8p2P2P0P4p-2p-4P0p8P-8|M0p6P0p-6P0p6P0$'], 13)
p64 = parse('r2', 'R2r2R-2r-2R2r2R2r-2|R2r-2R-2r-2R2r2R-2r2|R2r2R2r2R-2r-2R-2r2|R-2r-2R2r2R-2r-2R2$', 12)
p65 = parse('', [('r4r-R-4m3', 1), (1, 'R12R-1|!R-4R-1R|R-4R12|R-12R4|r-34r-M0R0$')], 10)
p66 = parse('n10', ['W3N5|K2C-4R3|N8N-4|O6G-3|B2N-3', ('N0n-7N0n7', 1), (1, 'C3N-4|K12R-3|W0N-3|n-9N0n8N0$')], 14)
p67 = parse('g3', 'K12K12K12K12|K-12K-12K-12K-12|k-11k-12k10k-23k13k-2k=6G|k-15k14k24k-16k-9k43k=-6G|G2G0K0$', 5)
p68 = parse('', 'OO0PP0CC0$|P0o2O2p-2P0o2P-2c2O-2p-2P0p-2C-2o2O|O0p2P0c-2C0o-2O0p2C2c2P-2o-2C2p2P|O2p-2C2o-2C-2o2O0c2P2p2P0c-2O-2c2C', 18)
p69 = parse('', [('w-2w-W2', 1), (1, 'g4R-2r-2g-@R-2G3w6|wr2G2r-2|w-2g-w-2R-2w3g|wR2wr-2|w-r-!W16$')], 13)
p610 = parse('m', ['U25$', ('PxbUu4#B3|Uxu4U2bC-x|p-5P-xu5B0c-C3n3U|c9C3b#P0u-#P0u-4u-M-3u4N0|P-4p4C-xu-U3u3b=0c-U-3', 1), (1, 'u-6')], 18) #Uses special logic
p6A = parse('ur-1g-1b-1k', 'Uk=-1r=1b=1|Uk-b=1g=-1u|Ug=1r-b-u|Uk=-1r=0b=0u|Uk-r=1g=-1u|Ur=-1g=-1b=-1|Ub-g-r-u|Ub-g-r-u|>R-1G-1B-1K-1U$', 7) #Edge case (1-way drop)
p6B = parse('', 'n2M4$|o2O2c2C2p-2P2c-2P2o-2|P2n-4m2|C-2o2C2p2P2c2O-2o2|O2p2P0o2C2o2P2o2|O2c2P-2p2O2c2O2p2N2o2O0p2C2c2C2o-2O2N-2', 23)
p6C = parse('', 'RR0GG0BB0g2CC0$|C-2r2R2b2G-2b2R-2g-2C2r-2B2g2!R-2R|G0c-2B2g-2B-2g2G2b2C2c2#R0c-2!C-2G|C0r-2G-2b-2B0c2R2g2@C0b2B2r2G0B|!R-2b2B0r2G0b-2#G2c2C2r-2!B0c2G2C', 29)

p71 = parse('w6', [('O/W6', 1), (1, 'Ox|O-x|W2o6|W2o-4'), ('W/O6', 2), (2, 'O2O0o12o-4W/O-4|W0$')], 10)
p72 = parse('', [('o2O/P0c4', 1), (1, 'C2O0P0$|C4O2'), ('p2P/O0c4', 2), (2, 'C4P2|C2P/O2')], 6)
p73 = parse('o5c7', [('C/OxO/Cx', 1), (1, 'C/Ox', 2), (2, 'c-|C/Oxc'), (1, 'O0C0$'), (1, 'O/Cx', 3), (3, 'o-|O/Cxo')], 8)
p74 = parse('', 'W/C-xW/C-xW/C-x|W24W24W0$|c-1|c-8|c-3|c4|c-3|c-3', 7)
p75 = parse('', [('w4w*Wxw2', 1), (1, 'mP/W4M0P0pP0$|P6W5p*|W/P2w5P4p-6|W/P-4p-|P-4W/P-2p-p4')], 7)
p76 = parse('cm5', ['k60C', ('M/C0c8', 1), (1, 'CK20KK4K|K2K3C3K20C2K|CK6C8K20', 2), (2, 'M/C0M/K0$')], 6)
p77 = parse('', ['c*c-*', ('c7', 1), (1, 'P/C4p*p-*p*|C4CP-1C/P-3m2'), (1, 'P-2P-3C|C2P-4', 2), (2, 'P0m'), (1, 'p-4M2P-4C4', 3), (3, 'C8P-8$|C8C0p-*p-4')], 15) #Takes a bit (0.5 min)
p78 = parse('c4', 'C24$|P/C8c4|C8p-8|P8c2|P/C4p4|C-4c6|P/C4c2|C-4p8|C/P4c2|P-4p4|C/P4c4|P-4c4', 13)
p79 = parse('', [('w-32w*w=-4w=54w=-42w-8|w=-12w-1w*w=71w=-17w-16|w-64w=-18w-2w=92w-*w*|w=-1w*w-4w=77w=-99w=-3', 1), (1, 'W0$')], 10) #Takes a long time (8 min)
p710 = parse('m3b-5o8c9', ['M/C0M/O0M/B0$|B-3B4O/B5|B-xC-2#C3|CO4M/B-1b5B2O/B3C3', ('B/M4M2B-4', 1), (1, 'C/O-1|#O-4m|B/C8|Bx#B-5C3')], 16)
p7A = parse('p4', 'P/C-xC/Px|C-4P/C-xP/C-x|P24P/C-x|P2C/Px|PC/Px|P8C/PxP/C-xC/Px|PxP/C-x|C-xC/Px|C-2P/C-x|P256$', 10) #Max possible score is 568
p7B = parse('o4', 'n17|N-3!N0$|N/O5u7O-4r|O/N8o-R2|O4r-2R2o=4|N!N-1|U/R-1UU0r2r=0N/O4|U/R-1U2U0r-r=0N/U7', 10)
p7C = parse('m1m*', 'U3@C-8$|G/PC2G/P-1G/PN3G/P2P-3P2p-u|P-4P/G2G-5G/PP2W4pu|RP/G-2G/P-4P/G-1G-4G/P-4G/P-1p-4u', 6)
p7D = parse('', ['!W12$|C2C0O2w2|KC2Ow2|KR2w2|K12', ('o10k10c10', 1), (1, 'NN0K0O0C2w6|NC3KO6|OKk2|C4n13|N/K4rN8w6')], 16) #Takes a bit (0.7 min)
p7E = parse('', ['c-|o-|p-|cccccccc|oooooooo|pppppppp', ('>', 1), (1, 'W/Cx|W/C-x', 2), (2, 'W/OxW/Ox|W/O-xW/O-x', 3), (3, 'W/PxW/PxW/Px|W/P-xW/P-xW/P-x', 4), 
    (4, 'W17W0', 5), (5, 'W/Px|W/P-x', 6), (6, 'W/CxW/Cx|W/C-xW/C-x', 7), (7, 'W/OxW/OxW/Ox|W/O-xW/O-xW/O-x', 8),
    (8, 'W2W0', 9), (9, 'W/Ox|W/O-x', 10), (10, 'W/PxW/Px|W/P-xW/P-x', 11), (11, 'W/CxW/CxW/Cx|W/C-xW/C-xW/C-x', 12), (12, 'W17W0$')], 18) #Uses special logic

p81 = parse('m4w13', ['M0W0p12P0$', ('W8W2W0C2P6|M/WW4P6W', 1)], 7)
p82 = parse('m-4', ['M0w12W0c4k=6P-5P0p-P5P0W0K/CxK4$|W8|P/W5|P/C8|C/K-4', ('C3K/W6|W/K-4P-1', 0)], 19)
p83 = parse('', 'm-13M0o52O0o20O0o15O0o46O0$|O|O3|O9|O27', 36)
p84 = parse('m', 'U/M0U/N0U/M0U/N0$|M6n|M5mn=1|M5mm-1|n3m11n-2', 10)
p85 = parse('w16p-8', ['P-2W4M/P-8M-2W/P-4|W2P-4M8W6M0W|M/P-2W5P-2M/W2M0P-1P-1|W0', ('M/P0M/W0', 1), (1, '$')], 10) #Special logic for bridge
p86 = parse('b', 'BU4M0M/B0M/W0M/C0$|BM0mw12C12bu|BM0C4m2bCc5u|BM0W4m-2bWw5u|BM0m-1c12W12bu', 12)
p87 = parse('m-1m*c-4', 'P/C-1|P/C-4|K/C-1|K/C-4|C-x>m-*m=1M/KxC/PxM0C-84C0C/KxC/PxC-25C0$', 18) #Special logic to limit stacking
p8A = parse('', 'm-5N/M-5b|c5M/C5b|n5N/C5b|U/M-xU/M0U/M-xU/M0U/M-xU/M0U/M-x#U/N0$', 41) #Takes a bit (0.6 min) w/special logic to limit stacking
p8B = parse('', [('w80W8X-2m4', 1), (1, 'W8X-1u|W8u|M2m-6M2m-2M-2m-3M2u|M2m4M-2m5Mxm-4M-2m-u|U4M0M/W0$')], 23)

p91 = parse('', ['B/[KC0O0W]Kx|B/[WCO3K3]Wx|B/[K0W3CO2]Cx|B/[O2C2W4]Ox|cccc|oooo|kkkk|wwww|B-8B-8B-8B/[WO0C2K4]$'], 11)
p92 = parse('', [('w2r-3[R-1R-1R-1R-1R-1]', 1), (1, '[RR]|[WW]', 2), (2, 'W2r2R-1u|B-1r-1|WRwr|R2w2!W0m'), (2, 'm-1', 3), (3, 'M0UR-1u2|U2$')], 14)
p93 = parse('', [('wWxw4Wxw|o2Oxo2Oxo3|pPxp3Pxp2|c3Cxc2Cxc', 1), (1, 'wWxwWxw=1|o2Oxo2Oxo=1|p3Pxp3Pxp=1|c3Cxc2Cxc=1', 2), (2, 'B/[WxOxPxCx]B-32$')], 16) #Timeout
p94 = parse('m', [('B/[WOPC]|C/[MWOP]', 1), (1, 'mw', 2), (2, 'O2wc4|Wc-|P-1p-3|Wo-2|O-1o2|Wm|C-1c-|P2mo'), (2, 'P/[M0W0O2]', 3), (3, '[C-8PxM0]$|C/[O-2P-1]p3|P-4p-8')], 16)
p95 = parse('b-2w4p7u3', ['B/[RxC-xM0]B0$|UM/[PxB-1]|UM/[WxB-1]|UM/[WxPxB-2]', ('b=0p-', 1), (1, 'UR/P-x|UC/Wx|UR/[WxP-xM0]|UC/[WxP-xM0]')], 23)
p96 = parse('', [('n8B/[M6BN]n10c2', 1), (1, 'B/[WRGB]m-1P/[C2W0]p-Pxm-1|K/[C2P]m-1P/[C2K-1]p-c2N/[C2P]p-k|P/[C2K]N/[P-2K-2]C/[P2C2]P-2K-2U/[P0K0C0]$')], 16) #Fix display
p9A = parse('', ['w*|o*|p*|c*', ('w2op3c3', 1), (1, 'B-4$|W/[OP0C]C/[W0P-1C-1]P/[W0OC]b-1|C/[WOP0]P/[W0OC-1]O/[OP-1C]b-1|C/[W0OC]O/[W0OC]W/[P-1C2]b-1|P/[WOC]W/[OP-1C]C/[W0P-2]b-1|P/[W0OP0]O/[W0P-1C]W/[OPC0]b-1')], 14)
p9B = parse('', 'o|o2|o4|o8|o16|o32|o64|o128|c|c2|c4|c8|c16|c32|c64|c128|o256|c256|c512|B/[OxOxOxOxOxOxOxOxOxOxOxCxCxCxCxCxCxCxCxCxCxCxCxCxCx]B-13337B0$', 8) #Takes a bit (0.5 min)
p9C = parse('wo3p6k10c15b21m-9', 'W/Bx|B/Cx|C/Kx|K/Px|P/Ox|O/Wx|[BW0M0]|[B0K0C0W0O0P0]$', 26) #Timeout
p9D = parse('p3u6', 'Uc-|Uc2|Uw|Uc-9|Up-|Up3|Uk-4|Up-4|Uk4|[BxM0][B-xM0]$|UxB/[WP0CK-x]Bxb-4|UxC6PKb-|U[MxMx]|UxB/[K4PxC-x]|Um', 11) #Takes a bit (0.5 min)
p9E = parse('', ['#U/N0$|[KU0]n90n*[BU0]b-1|k16[KxKx]|b-2[BxBx]|m4[MxMxU0]|b-*[N-xN-xU0]', (0, '[B-xB-x][M2U0][K-xK-x]M-4W/[M0U0]|B2M6B2K17W/[M0U0]', 1), (1, 'K-9|b-*'),
    (0, 'B2N-8[KU0][K3U0]W/[K0U0]|B-2[NxNxNxNx][K-1U0]K4W/[K0U0]', 2), (2, 'W70|b*')]) #Timeout
p9F = parse('o', 'W3$|{0}{1}{1}{0}{1}{1}{0}{0}{0}{1}{0}{0}{0}{1}w|{0}{0}{0}{1}{0}{0}{1}{0}{0}{0}{1}{1}{0}{0}w|{1}{1}{1}{1}{0}{0}{1}{1}{1}{1}{1}{1}{1}{0}w'.format('[OO]', '[O-1O-1]'), 28)

p101 = parse('', [('W0z4oOz2', 1), (1, '!C8$|zz8|W6R0C0|O8r|O2z2O4c4|W2w2W4c4')], 9)
p102 = parse('w3c2', 'PPZC0$|WoWzOw|WoZpWo|WoWc*Ow|OO0C|WW0C', 9)
p103 = parse('', [(1, '[ZZZZZZ]W4|OO0Z|p16P0|WP0|OC/O0'), 'w7o6B/[W0O0P0C0]$|C0O0P/Z16|O4O0Z', ('c6W/P0', 1)], 19) #Bridge special case
p104 = parse('', [('mK0W0k6Z3Z3m2', 1), (1, 'w6|k10|b3|m-2U3[B0W0K0M0]$|WZBZBZu|WZ5K2Ku|BB5Wu')], 17)
p105 = parse('', 'B0p3n-4u|P-2n-|Cn*|Z-4|P3b-4u|P-3n-8|p-8P0b3|Z-8|U2U/[B0N0]$', 12) #Preservation
p106 = parse('w50u-7', ['U-2p*o*w-50|U-2o-7O-1n6|U-2o-4O-6O0P5|U-2p5P6P0O-4|U-2M-1m*n*z50', ('N0', 1), (1, 'W0u-4m-1|Z50$')], 10) #Curse special case
p107 = parse('', 'N/W6|M/W6|w6n=0|K0k51W/[M0N0U0CZ50]$|[KU0]M6c|[KxU0]c|z-m-', 12)
p108 = parse('', [('o12O/[]', 1), (1, 'W/[]O/[]C/[]'), (1, 'W/[]', 2), (2, 'U64$|W20u20|Z4Z3u7|z24|z19|z9|Z8Z4Z3u15|O14u14|C8u8')], 15)
p109 = parse('', ['z17Z0Z0Z0$|Z/[O2P2]m|Z/[W2O2]m|w18O12Z4|p26P8Z16Z4', ('K4W4|C4Z4|>', 1), (1, 'z*'), ('o10O4n10>ZW8P4', 0)]) #Timeout
p1010 = parse('', 'u4m-1m3M/[OxGxBxRxU0]$|U[Z-xZ-x]|U[ZxZxZx]|UZ/Mx|UZ/U|UZ/[OOOO]|U[NxN-x]|UO/[]R/[]G/[]B/[]|UM/[]N/[]M/[]N/[]', 30) #Takes a long time (4.2 min)
p10A = parse('', 'Z|Z2|Z4|Z8|Z16|Z32|Z64|B/[M-1U]|uK[M-1U]|C/[M-1U]|m-3nn-2|u-1k43b92c5W/[B0K0C0U0]$') #Curse special case, timeout
p10B = parse('', [('m-1>|k-1>|c-1>', 1), (1, 'w*', 2), (2, 'm=0Z/W5[Z-5U0]$|n-|Ck*n=0Cw-*|Kc*n=0Kw-*|Mn*k4c4w5|N0|n2')]) #Brown bridge special case
p10C = parse('c50b-90m-1m*', ['z-b-z-|[C10Zx]|[B-20Z-x]|O/[C0B0U0]$', ('n10n10', 1), (1, 'n20'), (1, 'n10', 2), (2, 'n20'), (2, 'n10', 3), (3, 'n20'), (3, 'n10', 4),
    (4, 'n20'), (4, 'n10', 5), (5, 'n20'), (5, 'n10', 6), (6, 'n30')]) #Timeout

finale = parse('m2wp8', [('C2WPg-WOx|KWO-xK12c-12', 1), (1, 'b-u'), ('W0C-2M0o=1', 2), (2, 'w', 3), (3, 'Wo=-1o=-1!C!Cg-5u|N-3O-xKWC8u'), (2, 'mWO0O0M0', 4),
    (4, 'K4C2OxBP-6W!O0u'), (4, 'c4w2', 5), (5, '#C2WP-1wG4B0|C2WPk17K12C3', 6), (6, 'ru'), (5, 'm2o=1W0C0C0O0O0O0M0c6b', 7), (7, 'p-'), (7, 'P6w2#O0u'), (7, 'm3K12BP-1w2o=-1', 8),
    (8, 'P0B@O0u'), (8, 'k31O0O0M0m', 9), (9, 'RN-3B0g-5'), (9, 'K4w2P-1@C@C|BG12Pn-99C', 10), (10, 'O0b2u'), (9, 'WWC4o=1M0m2', 11), (11, 'C0WOxKW0|PPC-12O0W0P-1P-1', 12),
    (12, 'r-RGxWc-u'), (12, 'R0W0M0', 13), (13, 'o=1!W0G-xC0C0u|m5U10M0O0K0R0G0B0n92N0$')]) #Put in for kicks and giggles, I highly doubt it will solve this!

#test(full=False, print_moves=False) #Time: ~137 sec
#practice()

LockpickSolver().solve(p105, debug=False)