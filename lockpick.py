from solver import Solver
import re

class LockpickState:
    def __init__(self, access, stock, edges):
        self.access = access
        self.stock = dict(stock)
        self.edges = edges[:]
        self.last_move = None
        self.last_access = None
        self.master = []
        self.win = False
    def __eq__(self, state):
        if self.stock != state.stock:
            return False
        #return self.hashstr() == state.hashstr() #Better with duplicated edges, otherwise about 2x slower
        return self.edges == state.edges
    def __hash__(self):
        #return hash(self.hashstr()) #Better with duplicated edges, otherwise about 2x slower
        return hash(str(self.stock) + str(self.edges))
    def hashstr(self):
        strs = [str(e) for e in self.edges if e[1]]
        return str(self.stock) + ''.join(sorted(strs))
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
    def unlock(self, i, back=False):
        state = LockpickState(self.access, self.stock, self.edges)
        if self.last_move == i and self.last_access == back:
            state.master = self.master
        state.last_move = i
        state.last_access = back
        next_states = []
        stock = state.stock
        state.edges[i] = (state.edges[i][0], state.edges[i][1][:], state.edges[i][2])
        start, seq, end = state.edges[i]
        if len(seq) == 0:
            return []
        si = -1 if back else 0
        lock = seq.pop(si)
        aura, color, num = lock
        if aura == '$':
            state.win = True
            return [state]
        elif aura == '>':
            state.access = set(state.access)
            state.access.remove(start)
            return [] if back else [state]
        elif aura == '<':
            state.access = set(state.access)
            state.access.remove(end)
            return [state] if back else []
        if stock.get('r', 0) >= 1 and '!' in aura:
            aura = aura.replace('!', '')
        if stock.get('g', 0) >= 5 and '@' in aura:
            aura = aura.replace('@', '')
        if stock.get('b', 0) >= 3 and '#' in aura:
            aura = aura.replace('#', '')
        if stock.get('n', 0) > 0 and color.isupper() and \
            'U' not in color and 'N' not in color and '~' not in aura:
            aura = '~'+aura
        elif stock.get('n', 0) < 0 and '~' in aura:
            aura = aura.replace('~', '')
        if aura != lock[0] and not (aura.replace('~', '') == lock[0] and lock[2] != '0' and 'M' not in lock[1]):
            s = LockpickState(state.access, state.stock, state.edges)
            s.edges[i] = (s.edges[i][0], s.edges[i][1][:], s.edges[i][2])
            if back: s.edges[i][1].append((aura, color, num))
            else: s.edges[i][1].insert(0, (aura, color, num))
            s.last_move = i
            s.last_access = back
            s.master = state.master
            next_states.append(s)
        if '~' in aura:
            color = 'N'
        if aura.replace('~', ''):
            return next_states
        if not num: num = '1'
        if len(seq) == 0:
            toadd = start if back else end
            if toadd is not None:
                state.access = set(state.access)
                state.access.add(start if back else end)
        if color.islower():
            if color + '*' in stock:
                if num == '-*':
                    del stock[color + '*']
                next_states.append(state)
                return next_states
            if num[0] == '=':
                stock[color] = int(num[1:])
            elif num == '-':
                stock[color] = -stock.get(color, 0)
            elif num == '*':
                stock[color + '*'] = 1
            elif num != '-*':
                if color not in stock:
                    stock[color] = 0
                stock[color] += int(num)
        else:
            req = color[-1].lower()
            key = color[0].lower()
            if stock.get('m', 0) > 0 and 'U' not in color and 'M' not in color:
                s = LockpickState(state.access, state.stock, state.edges)
                s.master = state.master[:] + [len(seq)]
                s.last_move = i
                s.last_access = back
                s.stock['m'] -= 1
                if s.stock['m'] == 0:
                    del s.stock['m']
                next_states.append(s)
            if num == 'x':
                if stock.get(req, 0) < 1:
                    return next_states
                if key + '*' not in stock:
                    stock[key] = stock.get(key, 0) - stock[req]
            elif num == '-x':
                if stock.get(req, 0) > -1:
                    return next_states
                if key + '*' not in stock:
                    stock[key] = stock.get(key, 0) - stock[req]
            elif num == '0':
                if stock.get(req, 0) != 0:
                    return next_states
            elif int(num) > 0 and stock.get(req, 0) < int(num):
                return next_states
            elif int(num) < 0 and stock.get(req, 0) > int(num):
                return next_states
            elif key + '*' not in stock:
                stock[key] = stock.get(key, 0) - int(num)
            if key in stock and stock[key] == 0:
                del stock[key]
        next_states.append(state)
        return next_states

def parse(stock, edges, target_moves=None):
    if isinstance(edges, str):
        edges = [edges]
    state = LockpickState({0}, {}, [])
    state.target_moves = target_moves
    state.previous = None
    parse = re.findall(r"[a-zA-Z]-?\d*", stock)
    for k in parse:
        if len(k) == 1:
            state.stock[k[0]] = 1
        else:
            state.stock[k[0]] = int(k[1:])
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
            parse = re.findall(r"[!#@]*[a-zA-Z]/[a-zA-Z]-?x|[!#@]*[a-zA-Z]-?x|[!#@]*[a-z]=-?\d*|[!#@]*[a-z]-?\*|[!#@]*[a-zA-Z]/[a-zA-z]-?\d*|[!#@]*[a-zA-Z]-?\d*|>|<|\$", s)
            for i, lock in enumerate(parse):
                if lock in '<>$':
                    parse[i] = (lock, '', '')
                    continue
                aura = color = num = None
                ai = 0
                for i2, c in enumerate(lock):
                    if aura is None and c.isalpha():
                        aura = lock[:i2]
                        ai = i2
                    if aura is not None and not c.isalpha() and c != '/' or c == 'x':
                        color = lock[ai:i2]
                        num = lock[i2:]
                        break
                if num is None:
                    color = lock[ai:]
                    num = ''
                parse[i] = (aura, color, num)
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
            for a in access:
                if i == state.last_move and a == state.last_access:
                    continue
                states = state.unlock(i, back=a)
                i2 = 0
                while i2 < len(states):
                    next = states[i2].unlock(i, back=a)
                    states += next
                    i2 += 1
                next_states += states
        return next_states
    def check_state(self, state): #Place to add some extra logic
        if not self.special:
            return True
        if self.special == '2-10':
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
        elif self.special == '6-10':
            if len(state.edges[0][1]) <= 1:
                return True
            total = abs(state.stock.get('u', 0)) + sum([sum([abs(int(lock[2])) for lock in edge[1] if lock[1] == 'u' and lock[2] != '-']) for edge in state.edges])
            return total >= 25
        return True
    def check_finish(self, state):
        return state.win
    def print_moves(self, moves):
        red, yellow, green, blue, black = '\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[00m'
        for i, m in enumerate(moves):
            if i == 0: continue
            pm = moves[i-1]
            print(str(i)+': ', end='')
            #print(m)
            locks = pm.edges[m.last_move][1]
            next = m.edges[m.last_move][1]
            for i2, lock in enumerate(locks):
                if m.last_access and i2 in m.master or \
                 not m.last_access and len(locks) - i2 - 1 in m.master:
                    if '~' in lock[0]:
                        lock = (lock[0].replace('~', ''), 'N', lock[2])
                    print(yellow + lock[0] + lock[1] + lock[2], end='')
                elif m.last_access and i2 >= len(next) or \
                 not m.last_access and i2 < len(locks) - len(next):
                    if '~' in lock[0]:
                        lock = (lock[0].replace('~', ''), 'N', lock[2])
                    print(red + lock[0] + lock[1] + lock[2], end='')
                else:
                    aura = next[i2][0] if m.last_access else next[i2 + len(next) - len(locks)][0]
                    for c in lock[0]:
                        color = black if c in aura else red
                        print(color + c, end='')
                    if '~' in aura and '~' not in lock[0]:
                        print(green + 'N' + black + lock[2], end='')
                    elif '~' in lock[0] and '~' not in aura:
                        print(green + lock[1] + black + lock[2], end='')
                    elif '~' in lock[0] and '~' in aura:
                        print(black + 'N' + lock[2], end='')
                    else:
                        print(black + lock[1] + lock[2], end='')
            print(black)
    def solve(self, state, prnt=True):
        #print(state)
        self.start = 0
        self.special = None
        if state == p210:
            self.special = '2-10'
        if state == p53:
            self.special = '5-3'
        if state == p610:
            self.special = '6-10'
        target = state.target_moves
        #moves = self.solve_optimal_debug(state)
        moves = self.solve_optimal(state, prnt=False)
        red, green, black = '\033[91m', '\033[92m', '\033[00m'
        if moves and target and len(moves)-1 > target:
            print(red, moves[0], 'Len', len(moves)-1, 'exceeded target of ', target, black)
        if moves and target and len(moves)-1 < target:
            print(green, moves[0], 'Target beaten! New target:', len(moves)-1, black)
        if prnt:
            self.print_moves(moves)

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
p1B = parse('w5o2p3g4k2', [('PPcGG|WKcWW|WKcPG|GWcOK|WWcGW|OOcOK|GPcWP|GOcWO', 0), 'C8$'], 9) #Timeout
p1Ba = parse('w5o2p3g4k2', [('PP|GG', 1), (1, 'WK|WW', 2), (2, 'WK|PG', 3), (3, 'GW|OK', 4), (4, 'WW|GW', 5), (5, 'OO|OK', 6), (6, 'GP|WP', 7), (7, 'GO$|WO$')], 8)
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
p32 = parse('c4', 'P8$|CkKp|CkKp|CkKp|CkK0p|KKxc4|CkK0p|CkK0p|CkKp|CkK0p', 14) #use hashstr()
p33 = parse('c6w20o40', ['C6Wx|C6Ox', ('O24W5|WO5O|O5W5', 1), (1, 'W5O2W|W4OO5|W5W5', 2), (2, 'O5O2W5W2O0W0$')], 7)
p34 = parse('', [('w3w=1Ww3', 1), (1, 'Ww=3|Ww=2|WW3W2$')], 7)
p35 = parse('', 'Oo3c4|O4c4|O3o3c4|C24$|O2o4c4|O6o=3c4|O5o5c4|o3OOOo3', 9)
p36 = parse('w2', ['WW0w=8WW0w=5W2W0w=50WW0$|W0w4W2w4|W2w4W2w8', ('W6|W2w=2', 1), (1, 'W2W1|W2W0w8'), (1, 'W0', 2), (2, 'W8w=1|W24w')], 15)
p37 = parse('', ['p=6p=4p=5p=8p=6p=2p=3p=2c', ('P6P0', 1), (1, 'P3P0P2P0Pxc'), (1, 'P4P0|P5P0', 2), (2, 'P8P0c|P2P0C3P0$')], 14)
p3A = parse('w', 'Kwc3|C2w|WkWkWkCc|KwWkOww|WkKw|WWW$|CxKwKwKkWwCo', 15)
p3B = parse('p4', [('Pp=0WwPp=0Oo=0Pp=0PoO', 0), 'PoPp=0o|OoOp|PpWow|Ow=0Www|WW$'], 14)
p3C = parse('c15', 'O2C4c=27C2C2|O2c4c4c4|O2c4O0c8C4|O2c4C4c12C8|O2C4C4|O2O0O2O0c4O6|o4O0o4O0o16O0o8O0C|O2C4C4c4Ox|C0C0$', 17) #Takes a long time (8.2 min)
p3D = parse('m3o24', ['W3w6W3O5|WRKm=0O0W0K0$|W3k15O4K4w2|m=0K3W3O|m=0K3O3k6', ('K4m=0O3K3', 1), (1, 'WK3O2|WO6|W4w8')], 11) #Takes a while (1 min)

p41 = parse('mw6', '!O0O2w2|OOp4!P4o2w2|W2W2o2P2P2r|!W3!W3R$', 7)
p42 = parse('g5p3', ['@G0@G0$|@P3g|P3G3', ('@P0', 1), (1, 'G@P2p6G5|G2p2P3g5')], 12)
p43 = parse('b2', ['B4b4|#Bm|Bb2', ('#B3b2#B0mB2', 1), (1, 'bB2|bB2|bB2|#B0#B0$')], 13)
p44 = parse('m3', [('M3', 1), (1, 'o4O0c2C3m3|O2O2c2C2m2M3m5|M5M0$')], 6)
p45 = parse('w', 'Kw!Orw|W4r|WoKo!CkR0O0!Oow|Oc2Cw3Ro|OcKoWo2Ow|OkCk!W0o|Wo!Co!Rc|!O2!W2$', 17)
p46 = parse('b3', 'WoWow|#KwKc|BkWoWb|BkWc|R$|OwOw|Ko#Kc|BkWwOw|BkOc|#C2CCm', 21)
p47 = parse('m2', 'Rx|Gx|Bx|!R0r2B0g2!B2g2G0b#B0m2|B2r2B0g2#G0b2G2b2G0m2|G2g2G0b@R2g2G0r2R0m2|R2bG2g2!B0r2#R0b2R2m2|M8B6$', 24)
p48 = parse('c25p20k15m10', 'P4C3b3@K8G2P5K4|C3Bg5G3P0#C6G0K2P5|@G5C3K8C3rR!P6C6|!R@G8#B3R0G0B0!WKPC|M0K0P0C0$', 7) #Takes a very long time (22 min)
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
p5A = parse('m5', ['W2CPO2n2|O2o|O2o|W2w2|Wp|Wp|Wc|Wc', ('Mxw2', 1), (1, 'WWc2|WWp2|WWo|OOP4CC$')], 8) #Takes a while (1.2 min)
p5B = parse('m2', [('B3', 1), (1, 'g8|w4U3m2U2'), ('W4', 2), (2, 'G2', 3), (3, 'u9|k12Mg2Gx'), (2, 'u=5', 4), (4, 'UU0gK4'), (4, 'RxKK6', 5),
    (5, 'G4U2w5'), (5, 'C3@U0K4m8g=2', 6), (6, 'W2G3M2u|K6G0W0u'), (6, 'K3W5W0@K0PG0W', 7), (7, 'G2@G0u|U2W2u2|U3U0$')]) #Haven't tried until I solve

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
p77 = parse('', ['c*c-*', ('c7', 1), (1, 'P/C4p*p-*p*|C4CP-1C/P-3m2'), (1, 'P-2P-3C|C2P-4', 2), (2, 'P0m'), (1, 'p-4M2P-4C4', 3), (3, 'C8P-8$|C8C0p-*p-4')]) #Haven't tried until I solve
p78 = parse('c4', 'C24$|P/C8c4|C8p-8|P8c2|P/C4p4|C-4c6|P/C4c2|C-4p8|C/P4c2|P-4p4|C/P4c4|P-4c4', 13)
p79 = parse('', [('w-32w*w=-4w=54w=-42w-8|w=-12w-1w*w=71w=-17w-16|w-64w=-18w-2w=92w-*w*|w=-1w*w-4w=77w=-99w=-3', 1), (1, 'W0$')], 10) #Takes a long time (8 min)
#Rest of World 7 has not been visited yet



LockpickSolver().solve(p210)