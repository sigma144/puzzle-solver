from solver import Solver, Catalog, parse_edges
from lockpicklevels import *
import re, time
import pickle

class LockpickState:
    def __init__(self, access, stock, edges):
        self.access = access
        self.stock = stock
        self.edges = edges[:]
        self.last_move = None
        self.last_access = None
        self.master = []
        self.win = False
        self.terminate = False
        self.solver = None
        self.iview = False
        self.iviewmoves = []
        self.salvage = {}
        self.gates = []
        self.gates_passed = 0
        self.multiplicity = 1
        self.level_num = None
    def __eq__(self, state):
        if self.stock != state.stock or self.salvage != state.salvage or self.gates != state.gates or self.access != state.access or self.win != state.win:
            return False
        return self.edges == state.edges
    def __hash__(self):
        return hash(pickle.dumps((self.stock, self.edges, sorted([(k, v) for k, v in self.salvage.items()]), sorted(list(self.access)), self.gates), -1))
    def __repr__(self) -> str:
        s = 'Access:' + str(self.access) + '\n'
        s += 'Stock:' + str(Catalog.get(self.stock)) + '\n'
        s += 'Master:' + str(self.master) + '\n'
        s += 'I-View:' + str(self.iviewmoves) + '\n'
        s += 'Salvage: ' + str({k: Catalog.get(v) for k, v in self.salvage.items()}) + '\n'
        if self.previous:
            s += 'Last move:' + str(self.last_move) + ' ' + str(self.last_access) + '\n'
        for e, (start, end) in enumerate(self.solver.edges):
            s += str(start) + ' -> ' + ' '.join([str(Catalog.get(lock)[0])+str(Catalog.get(lock)[1])+str(Catalog.get(lock)[2]) for lock in self.edge(e)]) + ' -> ' + str(end) + '\n'
        return s
    def copy(self, i, back):
        s = LockpickState(self.access, self.stock, self.edges)
        s.last_move = i
        s.last_access = back
        s.master = self.master
        s.iviewmoves = self.iviewmoves
        s.previous = self.previous
        s.solver = self.solver
        s.salvage = self.salvage
        s.gates = self.gates
        s.level_num = self.level_num
        s.multiplicity = self.multiplicity
        return s
    def edge(self, i):
        return Catalog.get(self.edges[i])
    def can_open(self, color, num):
        stock = Catalog.get(self.stock)
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
        stock = Catalog.get(self.stock)
        req = color[-1].lower()
        if num[-1] == 'i':
            return 0, int(num[:-1])
        if num == '0': return 0, 0
        elif num[-1] == 'x': return stock[req], 0
        elif num[-1] == '+': return 0, stock[req+'i']
        elif num == '=': return stock.get(req, 0), stock.get(req+'i', 0)
        else: return int(num), 0
    def collect_keys(self, color, num):
        stock = dict(Catalog.get(self.stock))
        if color + '*' in stock:
            if num == '-*':
                del stock[color + '*']
                del stock[color + 'i*']
            self.stock = Catalog.kadd(stock, '{'+str(sorted([(k,v) for k,v in stock.items()])))
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
            return
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
        self.stock = Catalog.kadd(stock, '{'+str(sorted([(k,v) for k,v in stock.items()])))
    def spend_keys(self, key, amount):
        stock = dict(Catalog.get(self.stock))
        if key + '*' not in stock:
            if key not in stock: stock[key] = 0
            stock[key] -= amount
            if stock[key] == 0: del stock[key]
            self.stock = Catalog.kadd(stock, '{'+str(sorted([(k,v) for k,v in stock.items()])))
    def mimic_color(self, mimic):
        for i, e in enumerate(self.edges):
            edge = Catalog.get(e)[:]
            for i2, l in enumerate(edge):
                l = Catalog.get(l)
                if l[0] and l[0][-1].isalpha() and '~' not in l[0]:
                    edge[i2] = Catalog.sadd((l[0][:-1]+mimic, l[1], l[2]))
            self.edges[i] = Catalog.sadd(edge)
    def open(self, i, si, aura, sign=1):
        seq = self.edge(i)[:]
        sid = Catalog.get(self.stock).get('s', None)
        _, color, num = Catalog.get(seq[si])
        if color[0] in '-∞':
            self.gates = [seq[si]] + self.gates
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
            if max(abs(imag), abs(real)) > self.solver.max_stacks - 1:
                if max(abs(imag), abs(real)) > self.solver.max_stacks:
                    return False
                self.win = 'Open copy'
            if real == 1 and imag == 0:
                seq[si] = Catalog.sadd((aura, color, num))
                self.edges[i] = Catalog.sadd(seq)
                self.terminate = True
                return True
            imag_part = 0
            if imag < 0: imag_part = str(imag) + 'i'
            elif imag > 0: imag_part = '+' + str(imag) + 'i'
            if real != 0 or imag != 0:
                seq[si] = Catalog.sadd((aura, color, num + 'X' + str(real) + (imag_part or '')))
                self.edges[i] = Catalog.sadd(seq)
                self.terminate = True
                return True
        elif sign == -1:
            if not self.iview and self.solver.max_stacks == 1: return False
            if self.solver.max_stacks == 2: self.win = 'Open copy'
            seq[si] = Catalog.sadd((aura, color, num + 'X' + ('1+1i' if self.iview else '2')))
            self.edges[i] = Catalog.sadd(seq)
            self.terminate = True
            return True
        elif self.iview:
            seq[si] = Catalog.sadd((aura, color, num + 'X1-1i'))
            self.edges[i] = Catalog.sadd(seq)
            self.terminate = True
            return True
        if (isinstance(color, list) and color[0] not in '∞-' or isinstance(color, str) and color.isupper()) and sid:
            self.terminate = True
            self.salvage = {k:v for k,v in self.salvage.items()}
            if color == 'S':
                id = int(num.split('X')[0])
                aura, color, num = Catalog.get(self.salvage[id])
            aura = aura.replace('!', '').replace('@', '').replace('#', '').replace('~', '')
            if aura and aura[-1].isalpha(): aura = aura[:-1] + 'Z'
            self.salvage[sid] = Catalog.sadd((aura, color, num))
            if -sid in self.salvage: self.salvage.pop(-sid)
            if self.solver.salvage is None:
                self.win = 'Salvage'
                seq.pop(si)
                self.edges[i] = Catalog.sadd(seq)
                return True
            if (color, num) != self.solver.salvage: return False
            if self.solver.salvage_id is not None and sid != self.solver.salvage_id: return False
            for e in self.edges:
                if Catalog.sadd(('', '^', '')) in Catalog.get(e):
                    return False
            self.win = True
        seq.pop(si)
        if len(seq) > 0 and seq[si] == Catalog.sadd(('', '^', '')):
            seq.pop(si)
        if len(seq) == 0:
            new_access = self.solver.edges[i][0] if si == -1 else self.solver.edges[i][1]
            self.add_access(new_access)
        self.edges[i] = Catalog.sadd(seq)
        return True
    def add_access(self, room):
        if room is None or room in self.access: return
        self.access = set(self.access)
        self.access.add(room)
        for i, (start, end) in enumerate(self.solver.edges):
            if self.edges[i]: continue
            if start == room: self.add_access(end)
            if end == room: self.add_access(start)
    def apply_effects(self, aura, color):
        stock = Catalog.get(self.stock)
        if stock.get('r', 0) >= 1 and '!' in aura:
            aura = aura.replace('!', '')
        if stock.get('g', 0) >= 5 and '@' in aura:
            aura = aura.replace('@', '')
        if stock.get('b', 0) >= 3 and '#' in aura:
            aura = aura.replace('#', '')
        if stock.get('n', 0) > 0 and color[0].isupper() and \
            'U' not in color and '-' not in color and color != 'N' and '~' not in aura and \
                not ('Z' in color and aura[-1] in 'MU'):
            aura = '~'+aura
        elif stock.get('n', 0) < 0 and '~' in aura:
            aura = aura.replace('~', '')
        return aura
    def adjust_num(self, num, stacks, iview):
        if iview and '-' in stacks[1:] or not iview and stacks[0] == '-':
            if num == '=': return '='
            if num[0] == '-': num = num[1:]
            else: num = '-'+num
        if not iview: return num
        if num == 'x': return '+'
        if num == '+': return '-x'
        if num == '-x': return '-+'
        if num == '-+': return 'x'
        if num == '=': return '='
        if num[-1] == 'i':
            if num[0] == '-': return num[1:-1]
            return '-'+num[:-1]
        return num+'i'
    def unlock(self, i, back=False, iview=False, door=None):
        state = self.copy(i, back)
        state.iview = iview
        if self.last_move != i or self.last_access != back or self.terminate:
            state.master = []
            state.iviewmoves = []
        next_states = []
        stock = Catalog.get(state.stock)
        seq = state.edge(i)
        si = -1 if back else 0
        if len(seq) == 0:
            return []
        lock = Catalog.get(seq[si])
        aura, color, num = lock
        if door is not None:
            id = int(num.split('X')[0])
            state.salvage = dict(state.salvage)
            state.salvage[-id] = Catalog.sadd(door)
            aura, color, num = door
        #Salvaged doors
        if color == 'S':
            id = int(num.split('X')[0])
            if -id in self.salvage:
                aura, color, num = Catalog.get(self.salvage[-id])
            else:
                aura, color, num = Catalog.get(self.salvage[id])
                for door in self.get_painted_doors(aura, color, num):
                    next_states += self.unlock(i, back, door=door)
                return next_states
        #Auras
        aura = state.apply_effects(aura, color)
        if not iview and aura != lock[0] and not (aura.replace('~', '') == lock[0] and num != '0' \
            and 'M' not in color and 'Z' not in color and 'i' not in num):
            s = state.copy(i, back)
            seq = seq[:]
            seq[si] = Catalog.sadd((aura, color, num))
            s.edges[i] = Catalog.sadd(seq)
            next_states.append(s)
        if '!' in aura or '@' in aura or '#' in aura:
            return next_states
        if '~' in aura:
            if type(color) is list:
                color = ['N', [(l[0], 'N', l[2]) for l in color[1]]]
            else: color = 'N'
        elif self.solver.mimic and aura and aura[-1].isalpha():
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
        #Infinite Keys
        if type(color) is list and color[0] == '∞':
            seq = color[1]
            for mult in range(1, self.solver.mult_max+1):
                state = state.copy(i, back)
                state.collect_keys(aura[-1].lower() if seq[0][1] == 'z' else seq[0][1], seq[0][2] or '1')
                state.terminate = True
                state.multiplicity = mult
                next_states.append(state)
                state2 = state.copy(i, back)
                state2.open(i, si, '', None)
                state2.multiplicity = mult
                next_states.append(state2)
            return next_states
        #Passing Effect
        if self.solver.passing_effect is not None and i-1 in self.solver.passing_effect:
            if len(state.edge(i-1)) == self.solver.passing_effect[i-1]:
                seq2 = state.edge(i-1)[:]
                aura1, color1, num1 = Catalog.get(seq2[0])
                aura2 = state.apply_effects(aura1, color1)
                if aura1 != aura2:
                    seq2[0] = Catalog.sadd((aura2, color1, num1))
                    state.edges[i-1] = Catalog.sadd(seq2)
        #Specials
        if color == '$':
            if state.level_num is not None or isinstance(self.solver.salvage, tuple):
                return []
            for e in state.edges:
                if ('', '^', '') in Catalog.get(e):
                    return []
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
        #Master Key
        master = stock.get('mi' if iview else 'm', 0)
        if master: master = 1 if master > 0 else -1
        if master and 'U' not in color and 'M' not in color and '-' not in color and not ('Z' in color and aura[-1] in 'MU'):
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
            if not num: num = '1'
            elif num == 'i': num = '1i'
            elif num == '-i': num = '-1i'
            num = state.adjust_num(num, stacks, iview)
        #I-View
        if not iview and (stacks[-1] == 'i' or stock.get('mi', 0) != 0):
            s = state.copy(i, back)
            s.iviewmoves = state.iviewmoves[:] + [len(seq)-1]
            next_states += s.unlock(i, back, True, door)
        if iview and 'i' not in stacks or not iview and stacks[0] == '0':
            return next_states
        #Combo Doors
        if type(color) is list:
            spend = color[0]
            seq = color[1]
            amountr = 0
            amounti = 0
            for lock in seq:
                _, color, num = lock
                if not num: num = '1'
                elif num == 'i': num = '1i'
                elif num == '-i': num = '-1i'
                num = state.adjust_num(num, stacks, iview)
                if not state.can_open(color, num):
                    return next_states
                amount = state.spend_amount(color, num)
                amountr += amount[0]; amounti += amount[1]
            if spend != '-':
                if amountr: state.spend_keys(spend.lower(), amountr)
                if amounti: state.spend_keys(spend.lower()+'i', amounti)
                if self.solver.mimic:
                    state.mimic_color(spend)
                    if aura and aura[0].isalpha():
                        aura = aura[:-1] + spend
        #Regular Doors
        else:
            if not state.can_open(color, num):
                return next_states
            amountr, amounti = state.spend_amount(color, num)
            if amountr: state.spend_keys(color[0].lower(), amountr)
            if amounti: state.spend_keys(color[0].lower()+'i', amounti)
            if self.solver.mimic:
                state.mimic_color(color[0])
                if aura and aura[0].isalpha():
                    aura = aura[:-1] + color[0]
        if state.open(i, si, aura, None):
            next_states.append(state)
        return next_states
    def get_painted_doors(self, aura, color, num):
        if str((aura, color, num)) in self.solver.paint_results:
            return self.solver.paint_results[str((aura, color, num))]
        if isinstance(color, list):
            matching_locks = []
            for i1 in range(len(color[1])-1):
                for i2 in range(i1+1, len(color[1])):
                    if i1 == i2: continue
                    if color[1][i1] == color[1][i2]:
                        matching_locks.append((i1, i2))
            used = {str(color[1])}
            combos = [color[1][:]]
            for c in self.solver.omega:
                for i in range(len(color[1])):
                    for combo in combos[:]:
                        if combo[1] == c: continue
                        locks = combo[:]
                        locks[i] = (locks[i][0], c, locks[i][2])
                        if str(locks) not in used:
                            for i1, i2 in matching_locks:
                                if i1 > i or i2 > i: continue
                                if locks[i2][1] < locks[i1][1]:
                                    break
                            else:
                                used.add(str(locks))
                                combos.append(locks)
            doors = []
            for combo in combos:
                for i1, i2 in matching_locks:
                    if combo[i2][1] < combo[i1][1]:
                        break
                else:
                    specials = []
                    for cl in 'MUZ':
                        if any([cl in l[1] for l in combo]):
                            specials.append(cl)
                    doors.append([color[0], combo] + specials)
                    for c in self.solver.omega:
                        if color[0] == c: continue
                        doors.append([c, combo] + specials)
            #doors = doors
            result = [('Z' if 'Z' in str(d) else aura, d, num) for d in doors]
            self.solver.paint_results[str((aura, color, num))] = result 
            return result
        doors = {color}
        for c in self.solver.omega:
            for door in set(doors):
                if door[0] != c and door[-1] != c:
                    doors.add(c+"/"+door[-1])
                    doors.add(door[0]+"/"+c)
            doors.add(c)
        #doors = doors
        result = [('Z' if 'Z' in str(d) else aura, d, num) for d in doors] 
        self.solver.paint_results[str((aura, color, num))] = result 
        return result
    def score_state(self):
        return None #TODO

pattern = r'([_!#@%&]*)((?:[A-WYZ]/)?(?:[a-hj-wyzA-WYZ$ω<>^]|[\[\{][^(\[\{)}]*[\]\}]))(-?\d*i?(?:[\+-]\d*i)?X-?\d+(?:[\+-]\d*i)?|-?xi?|-?\+|=?-?\*?\d*i?(?:[\+-]\d*i)?)'

def parse(level, target_moves=0, salvage_moves=0, salvage=None, salvage_id=None, max_stacks=100, mult_max=1, special=None, passing_effect=None, salvage_from=[], salvage_start={}, omega=''):
    edges = parse_edges(level)
    state = LockpickState({0}, {}, [])
    state.target_moves = target_moves
    state.salvage_moves = salvage_moves
    state.mimic = None
    state.max_stacks = max_stacks
    state.mult_max = mult_max
    state.special = special
    state.previous = None
    state.passing_effect = passing_effect
    state.salvage = salvage
    state.salvage_id = salvage_id
    state.salvage_from = salvage_from
    state.salvage_start = {k: parse_locks(state, v)[0] for k, v in salvage_start.items()}
    state.omega = omega
    state.level = level
    for tup in edges:
        a, s, b = tup
        parse = parse_locks(state, s)
        state.edges.append((a, parse, b))
    return state
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
        if 'Z' in color or 'z' in color:
            aura = aura+'Z'
            parse[i] = (aura, color, num)
            state.mimic = True
        if '[' in color or color[0] == '{':
            if '/' in color:
                spend, color = color.split('/')
            elif color[0] == '{':
                spend = '∞' if color[1].islower() else '-'
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

def test(full=False, print_moves=False, salvages=True):
    solver = LockpickSolver()
    tests = [
        p11, p21, p31, p41, p51,      p71, p81, p91, p101, p111,                   p121,
        p12, p22,      p42, p52, p62, p72, p82, p92, p102,                   pt42, p122,
        p13, p23, p33, p43,      p63, p73, p83,      p103, p113, pt13,       pt43, 
        p14, p24, p34, p44, p54, p64, p74, p84, p94, p104, p114,       pt24, 
        p15, p25, p35, p45, p55, p65, p75, p85, p95, p105, p115, pt15, pt25, 
        p16, p26, p36, p46, p56, p66, p76, p86, p96, p106, p116, pt16,       pt36,
        p17, p27, p37, p47, p57, p67,                p107, p117,       pt27,
        p18, p28, p38,           p68, p78,           p108, p118,             pt4W,
        p19, p29,                p69,                                        pt4L,
             p210,                    p710,                p1110,
        p1A, p2A, p3A, p4A,      p6A,           p9A,       p1111,
             p2B, p3B, p4B,      p6B, p7B, p8B,            p11B,
        p1C, p2C,                p6C, p7C,
             p2D,                               p9F]
    extests = [p112, p53, p77, p87, p119, p110, p610,
        p5A, p7A, p8A, p1B, p5B, p9B, p10B, p3D, p7D, p9D, p7E]
        #Exclude 32, 3C, 48, 4C, 61, 79, 93, 9C, 109, 1010, 11A
    salvagetests = [pt13, pt15, pt17, pt25, pt27, pt32, pt34, pt42, pt43, #pt31, 
        #pomegaO, pomegaK, pomegaL, pomegaG, pomegaB,
        ]
    if full: tests = extests + tests
    if salvages: tests = salvagetests
    start_time = time.time()
    for i, puzzle in enumerate(tests):
        if full and i == len(extests):
            print("\033[92mAll extra tests passed!\033[00m")
        print('Test', str(i+1)+'/'+str(len(tests)))
        if salvages and puzzle.salvage_moves: puzzle.target_moves = puzzle.salvage_moves
        sol = solver.solve(puzzle, print_moves=print_moves, showprogress=0, salvage=salvages)
        if len(sol)-1 != puzzle.target_moves:
            print('\033[91m')
            solver.print_moves(sol)
            print('Solve Failed, test terminated\033[00m')
            return
    elapsed = time.time() - start_time
    print("\033[92mAll Tests Passed in {:.2f} seconds.\033[00m".format(elapsed))

class LockpickSolver(Solver):
    def get_next_states(self, state):
        next_states = []
        if state.win == 'Salvage':
            if state.level_num is not None:
                for i in range(state.level_num + 1, len(self.salvage_from)):
                    s = self.init_level(self.salvage_from[i], state.salvage)
                    s.level_num = i
                    s.win = 'Enter'
                    next_states.append(s)
            state = self.init_level(self.parent_level, state.salvage)
            state.level_num = None
        for i, (start, end) in enumerate(self.edges):
            if state.win == 'Open copy' and i != state.last_move: continue
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
                    s = states[i2]
                    #s.score = s.score_state()
                    if not s.terminate:
                        next = s.unlock(i, back=a)
                        states += next
                    if s.gates:
                        if len(s.edge(i)) == 0 and s.solver.edges[i][0 if a else 1] is not None:
                            s.access = set()
                            seq = s.edge(i)[:]
                            for g in s.gates:
                                if a: seq.append(g)
                                else: seq.insert(0, g)
                            s.edges[i] = Catalog.sadd(seq)
                            s.add_access(s.solver.edges[i][0 if a else 1])
                        else:
                            for g in s.gates:
                                mimic, locks, _ = Catalog.get(g)
                                for _, color, num in locks[1]:
                                    if color.isupper() and not s.can_open(mimic if color == 'Z' else color, num or '1'):
                                        s.access = set()
                                        break
                            else:
                                seq = s.edge(i)[:]
                                for g in s.gates:
                                    if a: seq.append(g)
                                    else: seq.insert(0, g)
                                s.edges[i] = Catalog.sadd(seq)
                            s.terminate = True
                        s.gates_passed = len(s.gates)
                        s.gates = []
                    i2 += 1
                next_states += states
        #for s in next_states:
        #    s.stock = Catalog.kadd(s.stock, str(sorted([(k,v) for k,v in s.stock.items()])))
        return next_states
    def check_finish(self, state):
        return state.win is True
    def print_moves(self, moves, verbose=False, pause=False):
        if not moves: return
        red, yellow, green, blue, black = '\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[00m'
        if verbose: print(moves[0])
        for i, m in enumerate(moves):
            if i == 0: continue
            print(str(i)+': ', end='')
            pm = moves[i-1]
            if m.win == 'Enter':
                print(green + 'Enter Sublevel', m.level_num, black)
                continue
            if pm.win == 'Salvage':
                pm = self.init_level(self.parent_level if m.level_num is None or m.level_num < 0
                    else self.salvage_from[m.level_num], m.salvage)
            locks = [Catalog.get(l) for l in Catalog.get(pm.edges[m.last_move])]
            next = [Catalog.get(l) for l in Catalog.get(m.edges[m.last_move])]
            for i in range(m.gates_passed):
                lock = next[i]
                if isinstance(lock[1], list) and lock[1][0] in '-∞':
                    next = next[:i] if m.last_access else next[i+1:]
                    break
            for i2, lock in enumerate(locks):
                if lock[1] == 'S':
                    id = int(lock[2].split('X')[0])
                    if -id in m.salvage and m.salvage[id] != m.salvage[-id]:
                        lock = Catalog.get(m.salvage[-id])
                        print(blue + "ω" + black, end='')
                    elif id in m.salvage:
                        lock = Catalog.get(m.salvage[id])
                    else: continue
                if isinstance(lock[1], list):
                    if lock[1][0] in '-∞':
                        lock = ('', '{'+''.join([l[0] + l[1] + l[2] for l in lock[1][1]])*m.multiplicity+'}', lock[2])
                    elif lock[1][1] and lock[1][0] == lock[1][1][0][1]:
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
                    if masterloc in m.iviewmoves:
                        print(blue + "I-View" + black, end=' ')
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
                    if masterloc in m.iviewmoves:
                        print(blue + "I-View" + black, end=' ')
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
            if m.win == 'Salvage' or isinstance(self.salvage, tuple) and i == len(moves) - 1:
                print(green + 'Salvage', end=' ')
            print(black, end='')
            if verbose: print(m)
            if pause: input()
            else: print()
    def solve(self, state, salvage=False, debug=False, print_moves=True, verbose=False, showprogress=True, use_ids=False, use_score=0):
        Catalog.init()
        self.salvage = None
        if state.salvage and salvage:
            self.salvage = parse_locks(state, state.salvage)[0]
            self.salvage = (self.salvage[1], self.salvage[2])
            self.salvage_id = state.salvage_id
        target = state.target_moves
        if self.salvage: target = state.salvage_moves
        self.parent_level = state
        self.salvage_from = state.salvage_from
        self.mult_max = state.mult_max
        self.omega = state.omega.upper()
        self.edges = [(start, end) for start, _, end in state.edges]
        state = self.init_level(state, {k: Catalog.sadd(v) for k, v in state.salvage_start.items()})
        #state.score = None
        #if use_score: state.score = 0
        if self.salvage_from:
            state.win = "Salvage"
            state.level_num = -1
        self.paint_results = {}
        moves = self.solve_optimal(state, debug=debug, prnt=False, showprogress=showprogress, use_ids=use_ids)
        red, green, black = '\033[91m', '\033[92m', '\033[00m'
        if moves and target and len(moves)-1 > target:
            print(red, moves[0], 'Len', len(moves)-1, 'exceeded target of ', target, black)
        if moves and target and len(moves)-1 < target:
            print(green, moves[0], 'Target beaten! New target:', len(moves)-1, black)
        if print_moves:
            self.print_moves(moves, verbose)
        return moves
    def init_level(self, state, salvage):
        self.special = None
        if state.special:
            self.special = state.special
        self.starting_edges = state.edges
        self.start = 0
        self.mimic = state.mimic
        self.max_stacks = state.max_stacks
        self.passing_effect = state.passing_effect
        if self.passing_effect is not None:
            self.passing_effect = {i: len(state.edges[i][1]) for i in self.passing_effect}
        state = state.copy(0, 0)
        state.solver = self
        state.access = {0}
        state.stock = Catalog.kadd({}, '{[]')
        state.last_move = None
        state.last_access = None
        state.salvage = {abs(k): v for k, v in salvage.items() if k > 0 or -k not in salvage}
        state.edges = [(e[0], e[1][:], e[2]) for e in state.edges]
        new_edges = []
        for e in state.edges:
            for li, (aura, color, num) in enumerate(e[1]):
                if color == 'S':
                    id = int(num.split('X')[0])
                    if id not in salvage:
                        e[1][li] = None
                        continue
                    sl = Catalog.get(salvage[id])
                    xspace = aura.count('&') - sl[0].count('&')
                    yspace = aura.count('%') - sl[0].count('%')
                    if yspace < 0 or xspace < 0:
                        e[1][li] = None
                        continue
                    #if yspace > 0:
                        #1/0 #Need to fix door spacing with memory update
                        #e[1][li] = None
                        #continue
                        #new_edges.append(Catalog.sadd([('', color, num)]))
                        #continue
        state.edges = [(e[0], [l for l in e[1] if l is not None], e[2]) for e in state.edges] + new_edges
        state.edges = [(e[0], [('', '<', '') if e[2] is None else ('', 's', '0')], e[2]) if not e[1] else e for e in state.edges]
        state.edges = [Catalog.sadd([Catalog.sadd(l) for l in e[1]]) for e in state.edges]
        return state
    #def score_state(self, state):
    #    return state.score
    def check_state(self, state): #Place to add some extra logic
        prev = state.previous
        stock = Catalog.get(state.stock)
        prev_stock = Catalog.get(prev.stock)
        if not self.special:
            return True
        if self.special == '1-B':
            if state.last_move >= 1 and state.last_move <= 8 and len(state.edge(state.last_move)) != 2:
                return False
        elif self.special == '2-10':
            prev = state.previous
            if state.last_move in [4, 5] and prev.last_move not in [4, 5]:
                if len(prev.edge(1)) < 2 or prev_stock.get('o', 0) == 0:
                    return False
            elif prev.last_move in [4, 5] and state.last_move not in [4, 5, 1]:
                if prev_stock.get('o', 0) == 0:
                    return False
        elif self.special == '5-3':
            for edge in state.edges:
                for lock in Catalog.get(edge):
                    if '~' in Catalog.get(lock):
                        return False
        elif self.special == '5-B':
            if state.last_move == 4 and stock.get('u', 0) == 0:
                return False
        elif self.special == '6-10':
            if len(state.edge(1)) <= 1:
                return True
            total = abs(stock.get('u', 0)) + sum([sum([abs(int(Catalog.get(lock)[2])) for lock in Catalog.get(edge) if Catalog.get(lock)[1] == 'u' and Catalog.get(lock)[2] != '-']) for edge in state.edges])
            return total >= 25
        elif self.special == '7-E':
            if state.last_move == 0 and stock.get('c', 0) == 0: return False
            if state.last_move == 1 and stock.get('o', 0) == 0: return False
            if state.last_move == 2 and stock.get('p', 0) == 0: return False
            if state.last_move == 3 and prev_stock.get('c', 0) != 0: return False
            if state.last_move == 4 and prev_stock.get('o', 0) != 0: return False
            if state.last_move == 5 and prev_stock.get('p', 0) != 0: return False
        elif self.special == '8-5':
            if not state.edge(5) and stock.get('w', 0) == 0 and (not state.edge(4) or Catalog.sadd(('', 'W', '0')) in state.edge(4)):
                return False
        elif self.special == '9-3':
            if state.last_move == 8:
                return False
            if state.last_move == 2 and len(state.edge(1)) == 5 and len(state.edge(5)) == 5:
                return False
            if state.last_move == 3 and len(state.edge(2)) == 5 and len(state.edge(6)) == 5:
                return False
            total = sum(stock.values())
            for e in state.edges:
                count_blast = 0
                for l in Catalog.get(e):
                    if type(l[1]) is str and l[-1] == 'x':
                        count_blast += 1
                    if type(l[1]) is str and l[1].islower():
                        total += int(l[2][-1]) if l[2] else 1
                if count_blast >= 2: total -= 1
            if total < 32:
                return False
        elif self.special == '9-B':
            if state.last_move == 19:
                return False
            if state.last_move < 8 and stock.get('c', 0) != 0:
                return False
        elif self.special == '9-C':
            for k, v in stock.items():
                if v < 0 and k != 'm':
                    return False
        elif self.special == '9-E':
            for i, i2 in ((6, 7), (7, 6), (10, 11), (11, 10)):
                if state.last_move == i and len(state.edge(i)) == 0 and len(state.edge(i)) > 0:
                    state.open(i2, -1, '')
                    return True
        elif self.special == '10-3':
            if state.last_move in [7, 8] and prev.last_move not in [7, 8]:
                if len(prev.edge(4)) < 2 or prev_stock.get(Catalog.get(prev.edge(4)[0])[0][-1].lower(), 0) > 0:
                    return False
            elif prev.last_move in [7, 8] and state.last_move not in [7, 8, 4]:
                if prev_stock.get(Catalog.get(prev.edge(4)[0])[0][-1].lower(), 0) > 0:
                    return False
        elif self.special == '10-B':
            if state.last_move == 10 and prev.edge(9) and Catalog.get(prev.edge(9)[0])[2] == '0':
                return False
        elif self.special == 'T1-1':
            if self.salvage is None and 'm*' in stock: return False
            if self.salvage is not None:
                if stock.get('c', 20) < 9: return False
                if stock.get('w', 0) > 8: return False
        elif self.special == 'T1-7':
            if self.salvage is not None and 'w' in stock: return False
        elif self.special == 'T3-1':
            if state.last_move == 15 and not state.salvage:
                return False
        elif self.special == 'T3-5':
            if 17 in state.salvage and '&' in Catalog.get(state.salvage[17])[0]:
                return False
            if 20 in state.salvage and '&' in Catalog.get(state.salvage[20])[0]:
                return False
        elif self.special == 'T3-6':
            if prev.last_move is None: return True
            if state.last_move <= 3 and prev.last_move >= 4 or prev.last_move <= 3 and state.last_move >= 4:
                if prev_stock.get('c', 0) >= 10: return False
            if state.last_move <= 4 and prev.last_move >= 5 or prev.last_move <= 4 and state.last_move >= 5:
                if prev_stock.get('ci', 0) >= 10 or prev_stock.get('c', 0) <= -10: return False
            if stock.get('u', 0) < 0 and not state.edge(2) and prev.edge(2): return False
        elif self.special == 'T4-3':
            if state.last_move == 4:
                if prev_stock.get('m', 0) != 0 or prev_stock.get('mi', 0) != 0:
                    return False
        elif self.special == '12-3':
            if stock.get('p', 0) < 0:
                return False
        elif self.special == '12-6':
            for c in 'plwz':
                if stock.get(c+'*', 0) > 0:
                    return False
            for c in 'olwz':
                if stock.get(c+'i', 0) > 0:
                    return False
        elif self.special == '12-9':
            if len(state.edge(3)) == 0 or Catalog.get(state.edge(3)[-1])[1][0] != 'C':
                return False
            if state.last_move == 5 and Catalog.get(state.edge(3)[-1])[0] != '~':
                return False
            return True
        elif self.special == '12-10': #14
            if state.last_move == 14 and Catalog.get(prev.edge(14)[0])[0] != 'P':
                return False
        elif self.special == '12-11':
            if stock.get('gi', 0) > 0:
                return False
        elif self.special == '12-D':
            for i in range(4, 9):
                if len(state.edge(i)) == 0: return False
                if i != 8 and Catalog.get(state.edge(i)[0])[0] and Catalog.get(state.edge(i)[0])[0][0] == '~':
                    return False
            if Catalog.get(state.edge(8)[0])[0][-1] != 'Z': return False
        elif self.special == 'omegaE':
            if 51 in state.salvage and 52 in state.salvage and state.salvage[51] > state.salvage[52]:
                return False
            if stock.get('e', 0) > 12 or stock.get('w', 0) < 0:
                return False
            if 's' in stock and stock['s'] in state.salvage and state.win != 'Salvage':
                return False
        elif self.special == 'O-5':
            if stock.get('r', 0) > 5000: return False
            if state.last_move == 4:
                stock = dict(stock)
                if stock.get('b', 0) <= 0 or stock.get('r', 0) <= 0: return False
                if (stock.get('r', 0) + stock.get('b', 0)) % 2 == 1: return False
                avg = (stock.get('r', 0) + stock.get('b', 0)) // 2
                stock['r'] = avg
                stock['b'] = avg
                stock['c'] = avg % 10
                state.stock = Catalog.kadd(stock, '{'+str(sorted([(k,v) for k,v in stock.items()])))
            if stock.get('c', 0) > 0 and state.last_move not in [4, 5]:
                return False
        elif self.special == 'O-12':
            if abs(stock.get('o', 0)) > 33 or abs(stock.get('p', 0)) > 33 or abs(stock.get('c', 0)) > 33:
                return False
        elif self.special == 'O-13':
            if stock.get('r', 0) < -3 or stock.get('ri', 0) < -3 or stock.get('r', 0) > 0 or stock.get('ri', 0) > 0:
                return False
            if state.last_move >= 2 and state.last_move <= 9 and (prev_stock.get('k', 0) != 0 or prev_stock.get('ki', 0) != 0):
                return False
            if 'w' in stock or 'wi' in stock:
                return False
            if prev.last_move == 12 and (Catalog.get(prev.previous.stock).get('k', 0) != 0 or Catalog.get(prev.previous.stock).get('ki', 0) != 0) and not (state.last_move >= 13 and state.last_move <= 21):
                return False
            if state.last_move >= 13 and state.last_move <= 21 and len(state.edge(state.last_move)) != 0:
                return False
        elif self.special == 'O-18':
            if len(state.edge(state.last_move)) > 0:
                return False
        return True

if __name__ == "__main__":
    #test(full=0, print_moves=0, salvages=0) #Time: ~113 sec
    LockpickSolver().solve(p11, salvage=1, verbose=0, debug=0, use_ids=1)