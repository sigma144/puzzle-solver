from solver import Solver
import re

class LockpickState:
    def __init__(self, access, stock, edges):
        self.access = set(access)
        self.stock = dict(stock)
        self.edges = [(v1, v2[:], v3) for v1, v2, v3 in edges]
    def __eq__(self, state):
        if self.stock != state.stock:
            return False
        for i in range(len(self.edges)):
            if ''.join(self.edges[i][1]) != ''.join(state.edges[i][1]):
                return False
        return True
    def __hash__(self):
        return hash(str(self))
    def __repr__(self) -> str:
        s = 'Access:' + str(self.access) + '\n'
        s += 'Stock:' + str(self.stock) + '\n'
        for e in self.edges:
            s += str(e[0]) + '-' + ''.join(e[1]) + '-' + str(e[2]) + '\n'
        return s
    def unlock(self, i, back=False, master=False):
        state = LockpickState(self.access, self.stock, self.edges)
        start, seq, end = state.edges[i]
        si = -1 if back else 0
        lock = seq.pop(si)
        if not lock[0].isalpha():
            newlock = lock
            if '!' in lock and self.stock.get('r', 0) >= 1:
                newlock = newlock.replace('!', '')
            if '#' in lock and self.stock.get('b', 0) >= 3:
                newlock = newlock.replace('#', '')
            if '@' in lock and self.stock.get('g', 0) >= 5:
                newlock = newlock.replace('@', '')
            if lock == newlock:
                return None
            if newlock:
                state.edges[i][1].insert(0, newlock)
            return state
        if len(lock) == 1:
            lock += '1'
        stock = state.stock
        if lock[0].islower():
            if lock[1] == '=':
                stock[lock[0]] = int(lock[2:])
            else:
                if lock[0] not in stock:
                    stock[lock[0]] = 0
                stock[lock[0]] += int(lock[1:])
        else:
            if master:
                if lock[0] == 'M' or lock[0] == 'U':
                    return None
                stock['m'] -= 1
                if stock['m'] == 0:
                    del stock['m']
            elif lock[1] == 'x':
                if stock.get(lock[0].lower(), 0) == 0:
                    return None
                stock[lock[0].lower()] = 0
            elif lock[1] == '0':
                if stock.get(lock[0].lower(), 0) != 0:
                    return None
            elif stock.get(lock[0].lower(), 0) < int(lock[1:]):
                return None
            else:
                stock[lock[0].lower()] -= int(lock[1:])
            if lock[0].lower() in stock and stock[lock[0].lower()] == 0:
                del stock[lock[0].lower()]
        if len(seq) == 0:
            state.edges.pop(i)
            toadd = start if back else end
            if toadd is not None:
                state.access.add(start if back else end)
        return state

def parse(stock, edges):
    if isinstance(edges, str):
        edges = [edges]
    state = LockpickState({0}, {}, [])
    parse = re.findall(r"[a-zA-Z]\d*", stock)
    for k in parse:
        if len(k) == 1:
            state.stock[k[0]] = 1
        else:
            state.stock[k[0]] = int(k[1:])
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
            end = False
            if s and s[-1] == '*':
                s = s[:-1]
                end = True
            parse = re.findall(r"[a-zA-Z]x|[a-zA-Z]=\d*|[a-zA-Z]\d*|[!#@]+", s)
            state.edges.append((a, parse, 144 if end else b))
    return state

class LockpickSolver(Solver):
    def solve(self, state):
        self.start = 0
        self.end = max([e[2] for e in state.edges if e[2]])
        self.num_edges = max([len(e[1]) for e in state.edges])
        #moves = self.solve_optimal_debug(state)
        moves = self.solve_optimal(state, prnt=False)
        for i, m in enumerate(moves):
            for i2 in range(len(m.edges)):
                if i == 0:
                    break
                if m.edges[i2][1] != moves[i-1].edges[i2][1]:
                    if len(m.edges) != len(moves[i-1].edges):
                        print(''.join(moves[i-1].edges[i2][1]), '->', end='')
                        break
                    else:
                        print(''.join(moves[i-1].edges[i2][1]), '->', ''.join(m.edges[i2][1]), end='')
            else:
                if i > 0 and len(m.edges) != len(moves[i-1].edges):
                    print(''.join(moves[i-1].edges[-1][1]), '->', end='')
            if i > 0 and m.stock.get('m', 0) < moves[i-1].stock.get('m', 0):
                print(" (MASTER)")
            else:
                print()
            #print(m)
    def get_next_states(self, state):
        next_states = [[] for _ in range(self.num_edges)]
        for i, (start, seq, end) in enumerate(state.edges):
            access = []
            if start in state.access: access.append(False)
            if end in state.access: access.append(True)
            for a in access:
                s = state
                if s.stock.get('m', 0) > 0:
                    s2 = s.unlock(i, back=a, master=True)
                    if s2:
                        next_states[0].append(s2)
                for si in range(len(seq)):
                    s = s.unlock(i, back=a)
                    if not s:
                        break
                    next_states[si].append(s)
        return sum(next_states, start=[])
    def check_finish(self, state):
        return self.end in state.access

test = parse('r5m', {
    (0, 'R2b4', 1),
    (0, 'R2YB4', 2),
})

p11 = parse('w', 'Wo|Op|P*')
p12 = parse('w', 'Wo|WwO*')
p13 = parse('w', 'Wo|Pk|Wp|Oc|K*')
p14 = parse('', ['OO*|WWoo', ('wW|gG', 1), (1, 'Gww|Go')])
p15 = parse('w', 'WwCcOw|OwCoo|WoOw|OoWc|WW*')
p16 = parse('o', 'OoOOcCO*|OcCocCC*|OoOoCoC*')
p17 = parse('wp', [('CoPkCoP|OoCkPwOwW|WcKcPwKcWoO', 0), 'KP*'])
p18 = parse('w2', 'O3w4|W2ow3|W6*|O2w2|W2o2w')
p19 = parse('w16', [('W2W3W2W3W|WW6WW|W4WW2W3', 1), (1, 'W3W2W3|W2W3W2', 2)])
p110 = parse('p16o8g4c2', ['W6*|O4w|G2C2w', ('WP4wGP2O2|GP2wGO2', 0), 'P6O2c2|C3Gw|P6w|G2C2w|CCw'])
p1A = parse('k', ['PwWcPc', ('KkOpP|OpWwC|KoPkK', 1), (1, 'p|PpOw|OoWp|CoKoWwK*')])
p1B = parse('w5o2p3g4k2', [('PPcGG|WKcWW|WKcPG|GWcOK|WWcGW|OOcOK|GPcWP|GOcWO', 0), 'C8*']) #Timeout
p1C = parse('w2', 'WkKoOcCw|WpPcCkKw|WgGkKpPw|WoOpPgGw|WcCgGoOw|P2p2K2k2C2c2O2*')

p21 = parse('m', [('WmwWPm', 1), (1, 'W2w2|Wm|W2W*')])
p22 = parse('m', ['W2w3|W2mO2m', ('Wo2O4K4m', 1), (1, 'PmCmW6m|R8w6P*')])
p23 = parse('m', [('OgGmW|WoPmRgP|PgGoOpWpP|GwOoPwWmGoO', 1), (1, 'mRwCgKpN*')])
p24 = parse('m3w11', [('W3W2W3|W3W8', 1), (1, 'W2W6|W12W|WW3W', 2), (2, 'W5W6|W3W3W3W3', 3), (3, 'W3*')])
p25 = parse('w', 'W2w|wW|W0WwW0*')
p26 = parse('mo4', ['O2p2WWp2|O2w2WWp2|WWp2PPPPo4', ('PPO0', 1), (1, 'O2O2*|OOw4')])
p27 = parse('w15o15c15', ['C2W8C4|CO6C12|W2O2C2|O4|W0O0C0*', ('C6|W2O12C2', 1), (1, 'C3OW3W|W6O')])
p28 = parse('o3p3c3', 'C3P3O3m|O12o3p3O3c3P3o3P3o3|O3p3O3p3P6o3o3O6o3c3|C3c3P6o3c3C3p3O3p3C3p3|C6c6O6o6P3P3C3*')
p29 = parse('o24', ['O24W3w5', ('O2o2O4', 1), (1, 'W8o2|Ow2|O4o4w4'), (1, 'W2oO2W0o4W2', 2), (2, "O0WW0*|O8|O6W2w2|O0w4|O2W6o2w8|W0w4o6|O8")])
#p210 = Bridge, Weird edge case
p2A = parse('m3w2k2o2c3p4', [('RW|KO', 1), (1, 'CC|OK', 2), (2, 'OK|WP', 3), (3, 'CC|WO', 4), (4, 'OR|OW', 5), (5, 'PP|KO', 6), (6, 'OR|RW', 7), (7, 'CC|PP', 8)])
p2B = parse('m', ['O4mK2mp4|W2k24w3', ('K24', 1), (1, 'C2k2W8wc|W3mWCR*|P4m')])
p2C = parse('m3p16o3', [('O2', 1), ('O4', 3), (1, 'O2P4|O2o6|O2P2'), (1, 'O4P2', 2), (2, 'O2p2o6|OOOOO3P3P6'), (2, 'O2', 3), (3, 'P4o|P0P0P0P0*')])
p2D = parse('o4p6', ['P3O2|P6o4', ('O4', 1), (1, 'P3o2O2p3|PP0*'), (1, 'o6', 2), (2, 'O2O0p3|OO0p2|P6O6p12'), (2, 'P0Oo2O', 3), (3, 'O2o4p3|P3P0P3o2O6p5')])

p31 = parse('', ['pp', ('Px', 1), (1, 'Pxo|Pxo2'), (1, 'Ox', 2), (2, 'p|OO*')])
p32 = parse('c4', 'P8*|CkKp|CkKp|CkKp|CkK0p|KKxc4|CkK0p|CkK0p|CkKp|CkK0p') #Takes a long time
p33 = parse('c6w20o40', ['C6Wx|C6Ox', ('O24W5|WO5O|O5W5', 1), (1, 'W5O2W|W4OO5|W5W5', 2), (2, 'O5O2W5W2O0W0*')])
p34 = parse('w3', 'Ww=3|Ww=2|WW3W2*')
p35 = parse('', 'Oo3c4|O4c4|O3o3c4|C24*|O2o4c4|O6o=3c4|O5o5c4|o3OOOo3')
p36 = parse('w2', ['WW0w=8WW0w=5W2W0w=50WW0*|W0w4W2w4|W2w4W2w8', ('W6|W2w=2', 1), (1, 'W2W1|W2W0w8'), (1, 'W0', 2), (2, 'W8w=1|W24w')])
p37 = parse('', ['p=6p=4p=5p=8p=6p=2p=3p=2c', ('P6P0', 1), (1, 'P3P0P2P0Pxc'), (1, 'P4P0|P5P0', 2), (2, 'P8P0c|P2P0C3P0*')])
p3A = parse('w', 'Kwc3|C2w|WkWkWkCc|KwWkOww|WkKw|WWW*|CxKwKwKkWwCo')
p3B = parse('p4', [('Pp=0WwPp=0Oo=0Pp=0PoO', 0), 'PoPp=0o|OoOp|PpWow|Ow=0Www|WW*'])
p3C = parse('c15', 'O2C4c=27C2C2|O2c4c4c4|O2c4O0c8C4|O2c4C4c12C8|O2C4C4|O2O0O2O0c4O6|o4O0o4O0o16O0o8O0C|O2C4C4c4Ox|C0C0*') #Takes a long time (7.8 min)
p3D = parse('m3o24', ['W3w6W3O5|WRKm=0O0W0K0*|W3k15O4K4w2|m=0K3W3O|m=0K3O3k6', ('K4m=0O3K3', 1), (1, 'WK3O2|WO6|W4w8')]) #Takes a long time

p41 = parse('mw6', '!O0O2w2|OOp4!P4o2w2|W2W2o2P2P2r|!W3!W3R*')
p42 = parse('g5p3', ['@G0@G0*|@P3g|P3G3', ('@P0', 1), (1, 'G@P2p6G5|G2p2P3g5')])
p43 = parse('b2', ['B4b4|#Bm|Bb2', ('#B3b2#B0mB2', 1), (1, 'bB2|bB2|bB2|#B0#B0*')])
p44 = parse('o4', 'o4O0c2C3m3|O2O2c2C2m2M3m5|M5M0*')
p45 = parse('w', 'Kw!Orw|W4r|WoKo!CkR0O0!Oow|Oc2Cw3Ro|OcKoWo2Ow|OkCk!W0o|Wo!Co!Rc|!O2!W2*')
p46 = parse('b3', 'WoWow|#KwKc|BkWoWb|BkWc|R*|OwOw|Ko#Kc|BkWwOw|BkOc|#C2CCm')
p47 = parse('m2', 'Rx|Gx|Bx|!R0r2B0g2!B2g2G0b#B0m2|B2r2B0g2#G0b2G2b2G0m2|G2g2G0b@R2g2G0r2R0m2|R2bG2g2!B0r2#R0b2R2m2|M8B6*')
p48 = parse('c25p20k15m10', 'P4C3b3@K8G2P5K4|C3Bg5G3P0#C6G0K2P5|@G5C3K8C3rR!P6C6|!R@G8#B3R0G0B0!WKPC|M0K0P0C0*') #Takes a while (6.9 min)
p4A = parse('mr', ['Rr|R|!R0!R0R', ('!R0!R0', 1), (1, '!R0r!R0r!R0R|!R0!R0mrrm!R0R2'), (1, '!R0', 2), (2, 'rR!R0!R0Rr|!R0!R0!R0!R0!R0!R0*')])
p4B = parse('', ['#R0g=4|b2B3R|g4G2m|!G2B2!M0b3@R0#B0b2@B2#G0m4|m2@B3Gx|r5R4', ('!R0@G0#B0M0', 1), (1, 'G3b2#G0m|#M4r|!@#W0*')])
p4C = parse('m10k15p20c25', 'M4m2|C8KP4P4KC|K12C3KP6K4C3P5|P5C4K12P8K5C12|M0M0K0K0P0P0C0C0*') #Takes a while (3.5 min)



LockpickSolver().solve(p4C)
