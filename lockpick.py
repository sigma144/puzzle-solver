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
            parse = re.findall(r"[a-zA-Z]x|[a-zA-Z]=\d*|[a-zA-Z]\d*", s)
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
p13 = parse('w', 'Wo|Pk|Wp|Ob|K*')
p14 = parse('', ['OO*|WWoo', ('wW|gG', 1), (1, 'Gww|Go')])
p15 = parse('w', 'WwBbOw|OwBoo|WoOw|OoWb|WW*')
p16 = parse('o', 'OoOObBO*|ObBobBB*|OoOoBoB*')
p17 = parse('wp', [('BoPkBoP|OoBkPwOwW|WbKbPwKbWoO', 0), 'KP*'])
p18 = parse('w2', 'O3w4|W2ow3|W6*|O2w2|W2o2w')
p19 = parse('w16', [('W2W3W2W3W|WW6WW|W4WW2W3', 1), (1, 'W3W2W3|W2W3W2', 2)])
p110 = parse('p16o8g4b2', ['W6*|O4w|G2B2w', ('WP4wGP2O2|GP2wGO2', 0), 'P6O2b2|B3Gw|P6w|G2B2w|BBw'])
p1A = parse('k', ['PwWbPb', ('KkOpP|OpWwB|KoPkK', 1), (1, 'p|PpOw|OoWp|BoKoWwK*')])
#p1B = parse('w5o2p3g4k2', [('PPbGG|WKbWW|WKbPG|GWbOK|WWbGW|OObOK|GPbWP|GObWO', 0), 'B8*']) #Timeout
p1C = parse('w2', 'WkKoObBw|WpPbBkKw|WgGkKpPw|WoOpPgGw|WbBgGoOw|P2p2K2k2B2b2O2*')

p21 = parse('m', [('WmwWPm', 1), (1, 'W2w2|Wm|W2W*')])
p22 = parse('m', ['W2w3|W2mO2m', ('Wo2O4K4m', 1), (1, 'PmBmW6m|R8w6P*')])
p23 = parse('m', [('OgGmW|WoPmRgP|PgGoOpWpP|GwOoPwWmGoO', 1), (1, 'mRwBgKpN*')])
p24 = parse('m3w11', [('W3W2W3|W3W8', 1), (1, 'W2W6|W12W|WW3W', 2), (2, 'W5W6|W3W3W3W3', 3), (3, 'W3*')])
p25 = parse('w', 'W2w|wW|W0WwW0*')
p26 = parse('mo4', ['O2p2WWp2|O2w2WWp2|WWp2PPPPo4', ('PPO0', 1), (1, 'O2O2*|OOw4')])
p27 = parse('w15o15b15', ['B2W8B4|BO6B12|W2O2B2|O4|W0O0B0*', ('B6|W2O12B2', 1), (1, 'B3OW3W|W6O')])
p28 = parse('o3p3b3', 'B3P3O3m|O12o3p3O3b3P3o3P3o3|O3p3O3p3P6o3o3O6o3b3|B3b3P6o3b3B3p3O3p3B3p3|B6b6O6o6P3P3B3*')
p29 = parse('o24', ['O24W3w5', ('O2o2O4', 1), (1, 'W8o2|Ow2|O4o4w4'), (1, 'W2oO2W0o4W2', 2), (2, "O0WW0*|O8|O6W2w2|O0w4|O2W6o2w8|W0w4o6|O8")])
#p210 = Bridge, Weird edge case
p2A = parse('m3w2k2o2b3p4', [('RW|KO', 1), (1, 'BB|OK', 2), (2, 'OK|WP', 3), (3, 'BB|WO', 4), (4, 'OR|OW', 5), (5, 'PP|KO', 6), (6, 'OR|RW', 7), (7, 'BB|PP', 8)])
p2B = parse('m', ['O4mK2mp4|W2k24w3', ('K24', 1), (1, 'B2k2W8wb|W3mWBR*|P4m')])
p2C = parse('m3p16o3', [('O2', 1), ('O4', 3), (1, 'O2P4|O2o6|O2P2'), (1, 'O4P2', 2), (2, 'O2p2o6|OOOOO3P3P6'), (2, 'O2', 3), (3, 'P4o|P0P0P0P0*')])
p2D = parse('o4p6', ['P3O2|P6o4', ('O4', 1), (1, 'P3o2O2p3|PP0*'), (1, 'o6', 2), (2, 'O2O0p3|OO0p2|P6O6p12'), (2, 'P0Oo2O', 3), (3, 'O2o4p3|P3P0P3o2O6p5')])

p31 = parse('', ['pp', ('Px', 1), (1, 'Pxo|Pxo2'), (1, 'Ox', 2), (2, 'p|OO*')])
p32 = parse('b4', 'P8*|BkKp|BkKp|BkKp|BkK0p|KKxb4|BkK0p|BkK0p|BkKp|BkK0p') #Takes a long time
p33 = parse('b6w20o40', ['B6Wx|B6Ox', ('O24W5|WO5O|O5W5', 1), (1, 'W5O2W|W4OO5|W5W5', 2), (2, 'O5O2W5W2O0W0*')])
p34 = parse('w3', 'Ww=3|Ww=2|WW3W2*')
p35 = parse('', 'Oo3b4|O4b4|O3o3b4|B24*|O2o4b4|O6o=3b4|O5o5b4|o3OOOo3')
p36 = parse('w2', ['WW0w=8WW0w=5W2W0w=50WW0*|W0w4W2w4|W2w4W2w8', ('W6|W2w=2', 1), (1, 'W2W1|W2W0w8'), (1, 'W0', 2), (2, 'W8w=1|W24w')])
p37 = parse('', ['p=6p=4p=5p=8p=6p=2p=3p=2b', ('P6P0', 1), (1, 'P3P0P2P0Pxb'), (1, 'P4P0|P5P0', 2), (2, 'P8P0b|P2P0B3P0*')])
p3A = parse('w', 'Kwb3|B2w|WkWkWkBb|KwWkOww|WkKw|WWW*|BxKwKwKkWwBo')
p3B = parse('p4', [('Pp=0WwPp=0Oo=0Pp=0PoO', 0), 'PoPp=0o|OoOp|PpWow|Ow=0Www|WW*'])
#p3C = parse('b15', 'O2B4b=27B2B2|O4b4b4b4|O2b4O0b8B4|O2b4B4b12B8|O2B4B4|O2O0O2O0b4O6|o4O0o4O0o16O0o8O0B|O2B4B4b4Ox|B0B0*') #Timeout
p3D = parse('m3o24', ['W3w6W3O5|WRKm=0O0W0K0*|W3k15O4K4w2|m=0K3W3O|m=0K3O3k6', ('K4m=0O3K3', 1), (1, 'WK3O2|WO6|W4w8')]) #Takes a long time

LockpickSolver().solve(p3D)
