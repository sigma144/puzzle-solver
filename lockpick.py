from solver import Solver, Catalog
from lockpicklevels import *
import re, time
import pickle

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
        self.max_stacks = 100
        self.iview = False
    def __eq__(self, state):
        if self.stock != state.stock:
            return False
        return self.edges == state.edges
    def __hash__(self):
        return hash(pickle.dumps((sorted([(k, v) for k, v in self.stock.items()]), self.edges), -1))
    def __repr__(self) -> str:
        s = 'Access:' + str(self.access) + '\n'
        s += 'Stock:' + str(self.stock) + '\n'
        s += 'Master:' + str(self.master) + '\n'
        if self.previous:
            s += 'Last move:' + str(self.last_move) + ' ' + str(self.last_access) + '\n'
        for e in self.edges:
            s += str(e[0]) + ' -> ' + ' '.join([Catalog.get(l)[0]+str(Catalog.get(l)[1])+Catalog.get(l)[2] for l in e[1]]) + ' -> ' + str(e[2]) + '\n'
        return s
    def copy(self, i, back):
        s = LockpickState(self.access, self.stock, self.edges)
        s.edges[i] = (s.edges[i][0], s.edges[i][1][:], s.edges[i][2])
        s.last_move = i
        s.last_access = back
        s.master = self.master
        s.previous = self.previous
        s.mimic = self.mimic
        s.max_stacks = self.max_stacks
        return s
    def can_open(self, color, num):
        stock = self.stock
        req = color[-1].lower()
        if num[-1] == 'i':
            num = num[:-1]
            req = req+'i'
        if num == '0': return stock.get(req, 0) == 0 and stock.get(req+'i', 0) == 0
        elif num == 'x': return stock.get(req, 0) > 0
        elif num == '-x': return stock.get(req, 0) < 0
        elif num == '+': return stock.get(req+'i', 0) > 0
        elif num == '-+': return stock.get(req+'i', 0) < 0
        elif num == '=': return stock.get(req, 0) != 0 or stock.get(req+'i', 0) != 0
        elif int(num) < 0: return stock.get(req, 0) <= int(num)
        else: return stock.get(req, 0) >= int(num)
    def spend_amount(self, color, num):
        stock = self.stock
        req = color[-1].lower()
        if num[-1] == 'i':
            return 0, int(num[:-1])
        if num == '0': return 0, 0
        elif num[-1] == 'x': return stock[req], 0
        elif num[-1] == '+': return 0, stock[req+'i']
        elif num == '=': return stock.get(req, 0), stock.get(req+'i', 0)
        else: return int(num), 0
    def collect_keys(self, color, num):
        stock = self.stock
        if color + '*' in stock:
            if num == '-*':
                del stock[color + '*']
            return
        if num == 'xi':
            stock[color], stock[color+'i'] = -stock.get(color+'i', 0), stock.get(color, 0)
            if stock[color+'i'] == 0: del stock[color+'i']
        elif num == '-xi':
            stock[color], stock[color+'i'] = stock.get(color+'i', 0), -stock.get(color, 0)
            if stock[color+'i'] == 0: del stock[color+'i']
        elif num[-1] == 'i':
            real, imag = parse_complex(num)
            if real: self.collect_keys(color, real)
            self.collect_keys(color+'i', imag[:-1])
        elif num[0] == '=':
            if color[0] in stock: del stock[color[0]]
            if color[0]+'i' in stock: del stock[color[0]+'i']
            stock[color] = int(num[1:])
        elif num == '-':
            if color in stock: stock[color] = -stock[color]
            if color+'i' in stock: stock[color+'i'] = -stock[color+'i']
        elif num == '*':
            stock[color + '*'] = 1
            stock[color + 'i*'] = 1
        elif num != '-*':
            amount = int(num)
            stock[color] = stock.get(color, 0) + amount
            if stock.get(color) == 0: del stock[color]
        if stock.get(color) == 0: del stock[color]
    def spend_keys(self, key, amount):
        if key + '*' not in self.stock:
            if key not in self.stock: self.stock[key] = 0
            self.stock[key] -= amount
            if self.stock[key] == 0: del self.stock[key]
    def mimic_color(self, mimic):
        for i, e in enumerate(self.edges):
            self.edges[i] = (e[0], e[1][:], e[2])
            for i2, l in enumerate(self.edges[i][1]):
                l = Catalog.get(l)
                if l[0] and l[0][-1].isalpha() and '~' not in l[0]:
                    self.edges[i][1][i2] = Catalog.sadd((l[0][:-1]+mimic, l[1], l[2]))
    def open(self, i, si, aura, sign=1):
        seq = self.edges[i][1]
        seq[si] = Catalog.get(seq[si])
        color = seq[si][1]; num = seq[si][2]
        if 'X' in num:
            num, stacks = num.split('X')
            real, imag = 0, 0
            if stacks[-1] == 'i':
                real, imag = parse_complex(stacks)
                real, imag = int(real), int(imag[:-1])
                stacks = imag if self.iview else real
            else: real, imag = int(stacks), 0
            if sign is None:
                sign = -1 if int(stacks) < 0 else 1
            if self.iview: imag -= sign
            else: real -= sign
            if max(abs(imag), abs(real)) > self.max_stacks:
                return False
            if real == 1 and imag == 0:
                seq[si] = Catalog.sadd((aura, color, num))
                self.terminate = True
                return True
            imag_part = 0
            if imag < 0: imag_part = str(imag) + 'i'
            elif imag > 0: imag_part = '+' + str(imag) + 'i'
            if real != 0 or imag != 0:
                seq[si] = Catalog.sadd((aura, color, num + 'X' + str(real) + (imag_part or '')))
                self.terminate = True
                return True
        elif sign == -1:
            seq[si] = Catalog.sadd((aura, color, num + 'X' + ('1+1i' if self.iview else '2')))
            self.terminate = True
            return True
        seq.pop(si)
        if len(seq) == 0:
            new_access = self.edges[i][0] if si == -1 else self.edges[i][2]
            if new_access is not None:
                self.access = set(self.access)
                self.access.add(new_access)
        return True
    def unlock(self, i, back=False, iview=False):
        state = self.copy(i, back)
        state.iview = iview
        if self.last_move != i or self.last_access != back or self.terminate:
            state.master = []
        next_states = []
        stock = state.stock
        seq = state.edges[i][1]
        if len(seq) == 0:
            return []
        si = -1 if back else 0
        lock = Catalog.get(seq[si])
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
        if not iview and aura != lock[0] and not (aura.replace('~', '') == lock[0] and num != '0' \
            and 'M' not in color and 'Z' not in color and 'i' not in num):
            s = state.copy(i, back)
            s.edges[i][1][si] = Catalog.sadd((aura, color, num))
            next_states.append(s)
        if '!' in aura or '@' in aura or '#' in aura:
            return next_states
        if '~' in aura:
            if type(color) is list:
                color = ['N', [(l[0], 'N', l[2]) for l in color[1]]]
            else: color = 'N'
        elif self.mimic and aura and aura[-1].isalpha():
            if type(color) is list:
                color = [color[0].replace('Z', aura[-1]), [(l[0], l[1].replace('Z', aura[-1]), l[2]) for l in color[1]]] + color[2:]
            else: color = color.replace('Z', aura[-1]).replace('z', aura[-1].lower())
        if not num: num = '1'
        elif num == 'i': num = '1i'
        elif num == '-i': num = '-1i'
        #Keys
        if type(color) is str and color.islower():
            state.collect_keys(color, num)
            state.open(i, si, aura)
            return next_states + [state]
        #Master Key
        master = stock.get('mi' if iview else 'm', 0)
        if master: master = 1 if master > 0 else -1
        if master and 'U' not in color and 'M' not in color and not ('Z' in color and aura[-1] in 'MU'):
            s = state.copy(i, back)
            s.iview = iview
            if s.open(i, si, aura, master):
                s.master = state.master[:] + [len(seq)-1]
                s.spend_keys('mi' if iview else 'm', master)
                next_states.append(s)
        #Stacks
        stacks = '1'
        if 'X' in num:
            num, stacks = num.split('X')
            if not iview and stacks[0] == '0':
                iview = True
                state.iview = True
            if not num: num = '1'
            elif num == 'i': num = '1i'
            elif num == '-i': num = '-1i'
            if iview and '-' in stacks[1:] or not iview and stacks[0] == '-':
                if num[0] == '-': num = num[1:]
                else: num = '-'+num
        #I-View
        if iview:
            if 'i' not in stacks: return next_states
            if num == 'x': num = '+'
            elif num == '+': num = '-x'
            elif num == '-x': num = '-+'
            elif num == '-+': num = 'x'
            elif num == '=': num = '='
            else: num = num[1:-1] if num[-1] == 'i' and num[0] == '-' else '-'+num[:-1] if num[-1] == 'i' else num+'i'
        elif stacks[-1] == 'i' or stock.get('mi', 0) != 0:
            s = state.copy(i, back)
            next_states += s.unlock(i, back, True)
        #Combo Doors
        if type(color) is list:
            spend = color[0]
            seq = color[1]
            amountr = 0
            amounti = 0
            for lock in seq:
                _, color, num = lock
                if not num: num = '1'
                if not state.can_open(color, num):
                    return next_states
                amount = state.spend_amount(color, num)
                amountr += amount[0]; amounti += amount[1]
            if amountr: state.spend_keys(spend.lower(), amountr)
            if amounti: state.spend_keys(spend.lower()+'i', amounti)
            if self.mimic:
                state.mimic_color(spend)
                aura = aura[:-1] + spend
        #Regular Doors
        else:
            if not state.can_open(color, num):
                return next_states
            amountr, amounti = state.spend_amount(color, num)
            if amountr: state.spend_keys(color[0].lower(), amountr)
            if amounti: state.spend_keys(color[0].lower()+'i', amounti)
            if self.mimic:
                state.mimic_color(color[0])
                aura = aura[:-1] + color[0]
        state.open(i, si, aura, None)
        next_states.append(state)
        return next_states

pattern = r'([_~!#@]*)((?:[A-WYZ]/)?(?:[a-hj-wyzA-WYZ$<>]|\[[^\[]*\]))(-?\d*i?(?:[\+-]\d*i)?X-?\d+(?:[\+-]\d*i)?|-?xi?|-?\+|=?-?\*?\d*i?(?:[\+-]\d*i)?)'
roomi = 0

def parse(level, target_moves=0, max_stacks=100, special=None):
    global roomi
    roomi = 1
    edges = parse_edges(0, [c for c in level], None)
    edges = epsilon_closure(edges)
    state = LockpickState({0}, {}, [])
    state.target_moves = target_moves
    state.max_stacks = max_stacks
    state.special = special
    state.previous = None
    state.passing_effect = []
    for tup in edges:
        a, s, b = tup
        parse = parse_locks(state, s)
        state.edges.append((a, parse, b))
    return state
def parse_edges(start, edgechar, end):
    global roomi
    new = []
    edge = ''
    newstart = start
    while edgechar and edgechar[0] != ')':
        c = edgechar.pop(0)
        if c == '|':
            new.append((newstart, edge, end))
            edge = ''
            newstart = start
        if c == '(':
            new.append((newstart, edge, roomi))
            edge = ''
            newstart = roomi
            newend = roomi + 1
            roomi += 2
            newedges = parse_edges(newstart, edgechar, newend)
            if not (edgechar and edgechar[0] not in ')|'):
                for i, e in enumerate(newedges):
                    if e[2] == newend:
                        newedges[i] = (e[0], e[1], None)
            new += newedges
            newstart = newend
        if c not in '|().':
            edge += c
    if edgechar: edgechar.pop(0)
    new.append((newstart, edge, end))
    return new
def epsilon_closure(edges):
    epsilon = [e for e in edges if len(e[1]) == 0 and e[2] is not None]
    edges = [e for e in edges if len(e[1]) > 0]
    initial_edges = edges[:]
    for start, _, end in epsilon:
        for i, e in enumerate(edges):
            if e[0] == end: edges[i] = (start, e[1], e[2])
            if e[2] == end: edges[i] = (e[0], e[1], start)
    if edges != initial_edges:
        return epsilon_closure(edges + epsilon)
    return edges
def parse_complex(num):
    num = num.split('+')
    if len(num) == 2:
        return num
    num = num[0].split('-')
    if not num[0]:
        num.pop(0)
        num[0] = '-'+num[0]
    if len(num) == 2:
        return num[0], '-'+num[1]
    return '', num[0]
def parse_locks(state, s):
    parse = re.findall(pattern, s)
    for i, lock in enumerate(parse):
        aura, color, num = lock
        if '~' in aura:
            aura.replace('~', '')
            state.passing_effect.append(i)
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
    return parse
def add_edge(state, start, locks, end):
    state.edges.append((start, parse_locks(state, locks), end))

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
        prev = state.previous
        if not self.special:
            return True
        if self.special == '1-B':
            if state.last_move >= 1 and state.last_move <= 8 and len(state.edges[state.last_move][1]) != 2:
                return False
        elif self.special == '2-10':
            prev = state.previous
            if state.last_move in [4, 5] and prev.last_move not in [4, 5]:
                if len(prev.edges[1][1]) < 2 or prev.stock.get('o', 0) == 0:
                    return False
            elif prev.last_move in [4, 5] and state.last_move not in [4, 5, 1]:
                if prev.stock.get('o', 0) == 0:
                    return False
        elif self.special == '5-3':
            for edge in state.edges:
                for lock in edge[1]:
                    if '~' in Catalog.get(lock):
                        return False
        elif self.special == '5-B':
            if state.last_move == 4 and state.stock.get('u', 0) == 0:
                return False
        elif self.special == '6-10':
            if len(state.edges[1][1]) <= 1:
                return True
            total = abs(state.stock.get('u', 0)) + sum([sum([abs(int(Catalog.get(lock)[2])) for lock in edge[1] if Catalog.get(lock)[1] == 'u' and Catalog.get(lock)[2] != '-']) for edge in state.edges])
            return total >= 25
        elif self.special == '7-E':
            if state.last_move == 0 and state.stock.get('c', 0) == 0: return False
            if state.last_move == 1 and state.stock.get('o', 0) == 0: return False
            if state.last_move == 2 and state.stock.get('p', 0) == 0: return False
            if state.last_move == 3 and state.previous.stock.get('c', 0) != 0: return False
            if state.last_move == 4 and state.previous.stock.get('o', 0) != 0: return False
            if state.last_move == 5 and state.previous.stock.get('p', 0) != 0: return False
        elif self.special == '8-5':
            if not state.edges[5][1] and state.stock.get('w', 0) == 0 and (not state.edges[4][1] or Catalog.sadd(('', 'W', '0')) in state.edges[4][1]):
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
            if state.last_move in [7, 8] and prev.last_move not in [7, 8]:
                if len(prev.edges[4][1]) < 2 or prev.stock.get(Catalog.get(prev.edges[4][1][0])[0][-1].lower(), 0) > 0:
                    return False
            elif prev.last_move in [7, 8] and state.last_move not in [7, 8, 4]:
                if prev.stock.get(Catalog.get(prev.edges[4][1][0])[0][-1].lower(), 0) > 0:
                    return False
        elif self.special == '10-6':
            if state.last_move == 6 and len(state.edges[6][1]) <= 3 and prev.stock.get('n', 0) > 0:
                if 'U' not in Catalog.get(prev.edges[7][1][0])[0] and '~' not in Catalog.get(prev.edges[7][1][0])[0]:
                    return False
        elif self.special == '10-A':
            if 0 < state.last_move < 7 and prev.stock.get('n', 0) > 0:
                if prev.edges[state.last_move-1][1] and '~' not in Catalog.get(prev.edges[state.last_move-1][1][0])[0]:
                    return False
        elif self.special == '10-B':
            if state.last_move == 10 and prev.edges[9][1] and Catalog.get(prev.edges[9][1][0])[2] == '0':
                return False
        return True
    def check_finish(self, state):
        return state.win
    def print_moves(self, moves, verbose=False, pause=False):
        red, yellow, green, blue, black = '\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[00m'
        if verbose: print(moves[0])
        for i, m in enumerate(moves):
            if i == 0: continue
            pm = moves[i-1]
            print(str(i)+': ', end='')
            locks = pm.edges[m.last_move][1]
            next = m.edges[m.last_move][1]
            for i2, lock in enumerate(locks):
                lock = Catalog.get(lock)
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
                    next_lock = Catalog.get(next_lock)
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
            if m.last_access:
                print('<- ', end='')
            if m.iview:
                print(blue + 'I-View', end='')
            print(black, end='')
            if verbose: print(m)
            if pause: input()
            else: print()
    def solve(self, state, debug=False, print_moves=True, verbose=False, showprogress=False):
        Catalog.init()
        state.edges = [(e[0], [Catalog.sadd(l) for l in e[1]], e[2]) for e in state.edges]
        print(state)
        self.start = 0
        self.special = None
        if state.special:
            self.special = state.special
        target = state.target_moves
        moves = self.solve_optimal(state, debug=debug, prnt=False, showprogress=showprogress)
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
        p91, p92, p94, p95, p96, p9A, p9B, p9D, p9F,
        p101, p102, p103, p104, p105, p106, p107, p108, p10B,
        p111, p112, p113, p114, p115, p116, p117, p118, p119, p1110, p1111
        ]
    for i, puzzle in enumerate(tests):
        sol = solver.solve(puzzle, print_moves=False)
        input()
        solver.print_moves(sol)

def test(full=False, print_moves=False):
    solver = LockpickSolver()
    tests = [
        p11, p21, p31, p41, p51,      p71, p81, p91, p101, p111,
        p12, p22,      p42, p52, p62, p72, p82, p92, p102,
        p13, p23, p33, p43,      p63, p73, p83,      p103, p113,
        p14, p24, p34, p44, p54, p64, p74, p84, p94, p104, p114,
        p15, p25, p35, p45, p55, p65, p75, p85, p95, p105, p115,
        p16, p26, p36, p46, p56, p66, p76, p86, p96, p106, p116,
        p17, p27, p37, p47, p57, p67,                p107, p117,
        p18, p28,                p68, p78,           p108, p118,
        p19, p29,                p69, 
             p210,                    p710,                p1110,
        p1A, p2A, p3A, p4A,      p6A,           p9A,       p1111,
             p2B, p3B, p4B,      p6B, p7B, p8B,  
        p1C, p2C,                p6C, p7C,
             p2D,                               p9F]
    extests = [p112, p53, p77, p87, p119, p110, p610,
        p5A, p7A, p8A, p1B, p5B, p9B, p10B, p3D, p7D, p9D, p7E]
        #Exclude 32, 3C, 48, 4C, 61, 79, 93, 9C, 109, 1010, 11A
    if full: tests = extests + tests
    start_time = time.time()
    for i, puzzle in enumerate(tests):
        if full and i == len(extests):
            print("\033[92mAll extra tests passed!\033[00m")
        print('Test', str(i+1)+'/'+str(len(tests)))
        sol = solver.solve(puzzle, print_moves=print_moves)
        if len(sol)-1 != puzzle.target_moves:
            print('\033[91m')
            solver.print_moves(sol)
            print('Solve Failed, test terminated\033[00m')
            return
    elapsed = time.time() - start_time
    print("\033[92mTest Complete in {:.2f} seconds.\033[00m".format(elapsed))

if __name__ == "__main__":
    #test(full=0, print_moves=0) #Time: ~83 sec
    #practice()

    LockpickSolver().solve(p61x, verbose=0, debug=0, showprogress=1)