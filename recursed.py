from solver import Solver, Catalog, parse_edges
import pickle

objects = 'kbfxXypo$*_wWmMgP0123456789ABCDXYZ'

class Room:
    def __init__(self):
        self.id = -1
        self.player_pos = 0
        self.global_exit_from = None
        self.nodes = []
        self.edges = []
        self.jar_num = 0
    def copy(self):
        room = Room()
        room.id = self.id
        room.player_pos = self.player_pos
        room.global_exit_from = self.global_exit_from
        room.nodes = self.nodes
        room.edges = self.edges
        return room
    def build_from_edges(self, edges):
        self.nodes = [[] for _ in range(max([e[2] for e in edges], default=0))]
        self.edges = []
        for start, chars, end in edges:
            obj = [c for c in chars if c in objects]
            for i, o in enumerate(obj):
                if o == 'g': obj[i+1] = 'g'+obj[i+1]
            obj = [o for o in obj if o != 'g']
            edge = [c for c in chars if c not in objects]
            self.nodes[end - 1] += obj
            if 'x' in obj: self.player_pos = start
            if start > 0: self.edges.append((start-1, edge, end-1))
    def build(self, nodes, edges):
        self.nodes = [[c for c in n] for n in nodes]
        for j, obj in enumerate(self.nodes):
            for i, o in enumerate(obj):
                if o == 'g': obj[i+1] = 'g'+obj[i+1]
            self.nodes[j] = [o for o in obj if o != 'g']
        self.edges = [(start, [c for c in e], end) for start, e, end in edges]
        for i, n in enumerate(nodes):
            if 'x' in n: self.player_pos = i
    def __str__(self):
        return f'{self.id}({self.player_pos},{self.global_exit_from}) {["".join([str(it) for it in n]) for n in self.nodes]} {["".join(e[1]) for e in self.edges]}'.replace('"', '').replace("'", '')
    def __repr__(self):
        return str((self.id, self.player_pos, self.global_exit_from, self.nodes, self.edges))
    def __lt__(self, s): return repr(self) < repr(s)
    def __le__(self, s): return repr(self) <= repr(s)
    def __gt__(self, s): return repr(self) > repr(s)
    def __ge__(self, s): return repr(self) >= repr(s)
    def __eq__(self, s):
        return isinstance(s, Room) and self.id == s.id and self.player_pos == s.player_pos and self.global_exit_from == s.global_exit_from and self.nodes == s.nodes and self.edges == s.edges
    
class RecursedState:
    def __init__(self):
        self.context = 'A'
        self.item = None
        self.state = None
        self.stack = None
        self.room = None
        self.node = 0
        self.jars = 0
        self.globals = []
        self.name = 'Start'
        self.starting_rooms = None
    def copy(self):
        state = RecursedState()
        state.context = self.context
        state.item = self.item
        state.state = {k: v for k, v in self.state.items()}
        state.stack = self.stack[:]
        state.state[state.context] = state.stack
        state.room = self.room.copy()
        state.state[state.context][-1] = state.room
        state.node = self.node
        state.jars = self.jars
        state.globals = self.globals
        state.starting_rooms = self.starting_rooms
        return state
    def current_node(self):
        return self.room.nodes[self.node]
    def current_item(self):
        if isinstance(self.item, int):
            item = self.globals[self.item][2]
            if isinstance(item, Room):  return 'g jar '+str(item.jar_num)
            return item
        if isinstance(self.item, Room): return 'jar '+str(self.item.jar_num)
        return self.item
    def drop_item(self, dest=None):
        if dest is None: dest = self.node
        if isinstance(self.item, int):
            if 'M' in self.room.nodes[dest]:
                self.item = self.globals[self.item][2].replace('g', '')
            else: return self.drop_global_item(dest)
        self.room.nodes = self.room.nodes[:]
        self.room.nodes[dest] = self.room.nodes[dest][:]
        node = self.room.nodes[dest]
        if '_' not in node: node.append(self.item)
        node.sort()
        self.item = None
    def drop_global_item(self, dest=None):
        node = self.node
        if dest is not None:
            node = dest
        if '_' not in self.room.nodes[node]:
            self.globals = self.globals[:]
            self.globals[self.item] = (self.room.id, node, self.globals[self.item][2])
        self.item = None
    def grab_item(self, i, transform=True):
        self.room.nodes = self.room.nodes[:]
        self.room.nodes[self.node] = self.room.nodes[self.node][:]
        node = self.room.nodes[self.node]
        self.item = node[i]
        node.pop(i)
        if transform: self.transform_oobleck()
    def grab_global_item(self, i):
        self.item = i
        self.globals = self.globals[:]
        self.globals[i] = (None, None, self.globals[i][2])
        self.transform_oobleck()
    def transform_oobleck(self, copy_room = False):
        copy = self.globals[self.item][2] if isinstance(self.item, int) else self.item
        if copy == 'y': return
        if isinstance(self.item, int) and not isinstance(copy, Room): copy = copy.replace('g', '')
        if copy == 'o': return
        transformed = False
        new_nodes = self.room.nodes[:]
        for ni, node in enumerate(new_nodes):
            for ii, item in enumerate(node):
                if item == 'o':
                    new_nodes[ni] = new_nodes[ni][:]
                    new_nodes[ni][ii] = copy
                    transformed = True
        if transformed:
            if copy_room:
                self.stack[-1] = self.room.copy()
            self.room = self.stack[-1]
            self.room.nodes = new_nodes
            self.room.oobleck = False
        for i, (r, n, c) in enumerate(self.globals):
            if r == self.room.id and c == 'go':
                self.globals = self.globals[:]
                self.globals[i] = (r, n, 'g'+copy if isinstance(copy, str) else copy)
    def unlock_door(self, x, back):
        for i, (r, n, c) in enumerate(self.globals):
            if r == self.room.id and n == x and len(self.room.edges[x][1]) == c:
                self.globals = self.globals[:]
                self.globals[i] = (None, None, None)
                self.item = None
                return
        self.room.edges = self.room.edges[:]
        edge = self.room.edges[x]
        self.room.edges[x] = (edge[0], edge[1][:], edge[2])
        edge = self.room.edges[x][1]
        r = range(0, len(edge))
        if back: r = range(len(edge)-1, -1, -1)
        for i in r:
            if edge[i] == 'l':
                edge.pop(i)
                self.item = None
                return
    def push_room(self, room, global_exit_from):
        self.room.player_pos = self.node
        self.room.global_exit_from = global_exit_from
        self.room = room.copy()
        self.stack.append(self.room)
        self.node = self.room.player_pos
        for i, (r, n, c) in enumerate(self.globals):
            if r == self.room.id and 'M' in self.room.nodes[n]:
                self.room.nodes = self.room.nodes[:]
                self.room.nodes[n] = self.room.nodes[n][:]
                self.room.nodes[n].append(c.replace('g', ''))
                self.globals = self.globals[:]
                self.globals[i] = (None, None, c)
        if self.item is not None: self.transform_oobleck()
    def pop_room(self):
        prev_room = self.stack.pop(-1)
        room = self.stack[-1]
        if room.global_exit_from is None or room.global_exit_from == self.item:
            self.node = room.player_pos
        else:
            r, n, item = self.globals[room.global_exit_from]
            if r != self.stack[-1].id or 'X' in room.nodes[n]:
                self.to_paradox()
            else: self.node = n
        self.room = self.stack[-1]
        return prev_room
    def to_paradox(self, context='P'):
        if len(self.state) == 1: self.state['A'] = []
        self.state[context] = []
        self.context = context
        self.stack = self.state[context]
        if context in self.starting_rooms:
            self.push_room(self.starting_rooms[context], None)
        else: self.push_room(self.starting_rooms['A'], None)
        self.name = 'Exit (Paradox)'
        if self.context == 'X':
            self.name = 'Exit (Invalid)'
    def can_move_to(self, edge_i):
        start, edge, end = self.room.edges[edge_i]
        height = -1
        if self.item is not None: height += 1
        if 'f' in self.current_node(): height = -100
        boxes = self.current_node().count('b')
        for r, n, c in self.globals:
            if r == self.room.id and n == self.node and c == 'gb':
                boxes += 1
            if r == self.room.id and n == self.node and c == 'gf':
                height = -100
            if r == self.room.id and n == edge_i and start == self.node and c == len(edge):
                return 'l'
        result = True
        if start == self.node:
            if edge and edge[0] == '-': return 't'
            if edge and edge[0] == '=':
                if 'f' in self.room.nodes[end]: return False
                for (r, n, c) in self.globals:
                    if r == self.room.id and n == end and c == 'gf':
                        return False
            for c in edge:
                if c == 'l': result = 'l'
                if c == 't': result = 't'
                if c == '<': height += 1
            if boxes >= height: return result
        elif end == self.node:
            if edge and edge[-1] == '-': return 't'
            if edge and edge[-1] == '=':
                if 'f' in self.room.nodes[start]: return False
                for (r, n, c) in self.globals:
                    if r == self.room.id and n == start and c == 'gf':
                        return False
            for c in edge[::-1]:
                if c == 'l': result = 'l'
                if c == 't': result = 't'
                if c == '>': height += 1
            if boxes >= height: return result
        return False
    def __str__(self):
        s = str((self.context, self.node, self.item)) + "G:" + str(self.globals) + "\n"
        for ct, c in self.state.items():
            s += '-------<'+ct+'>-------\n'
            for r in c:
                s += str(r) + '\n'
        return s
    def __repr__(self):
        return repr((self.context, self.node, self.item, self.globals, self.state))
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, s):
        return self.context == s.context and self.node == s.node and self.item == s.item and self.globals == s.globals and self.state == s.state

class RecursedSolver(Solver):
    def setup(self, rooms):
        Catalog.init()
        state = RecursedState()
        self.rooms = rooms
        has_water = False
        self.steal_item = False
        self.glitch = Room()
        self.glitch.nodes = [['x']]
        for r in self.rooms:
            for n in r.nodes:
                if 'w' in n or 'W' in n or 'm' in n or 'M' in n:
                    has_water = True
        for i, r in enumerate(self.rooms):
            r.id = i
            if has_water and i >= len(self.rooms)//2:
                r.id -= len(self.rooms)//2
            for j, n in enumerate(r.nodes):
                for c in n:
                    if c[0] == 'g':
                        state.globals.append((i, j, c))
                r.nodes[j] = sorted([c for c in n if c[0] != 'g'])
            for j, e in enumerate(r.edges):
                for k, c in enumerate(e[1]):
                    if c == 'L':
                        state.globals.append((i, j, len(e[1]) - k - 1))
                r.edges[j] = (e[0], [c for c in e[1] if c != 'L'], e[2])
        state.starting_rooms = {'A': rooms[0]}
        for r in rooms:
            for n in r.nodes:
                if 'p' in n:
                    state.starting_rooms['P'] = r
                    n.remove('p')
                    if 'p' in n:
                        self.steal_item = True
                        n.remove('p')
        state.state = {'A': []}
        state.stack = state.state['A']
        state.room = rooms[0].copy()
        state.stack.append(state.room)
        state.node = state.room.player_pos
        self.entered_paradox = 0
        return state
    def get_next_states(self, state):
        states = []
        node = state.current_node()
        if state.item is None:
            for i, item in enumerate(node):
                if item == self.kwargs.get('goal', '$'):
                    #Win the level
                    new_state = state.copy()
                    new_state.item = item
                    new_state.name = 'Win'
                    return [new_state]
                elif item == 'x':
                    if len(state.stack) > 1:
                        #Exit
                        new_state = state.copy()
                        new_state.name = 'Exit'
                        new_state.pop_room()
                        if new_state.name == 'Exit (Paradox)':
                            if not self.steal_item or self.entered_paradox and self._depth > self.entered_paradox + 1:
                                new_state.globals = [(gr, gn, gi) for gr, gn, gi in new_state.globals if gr is not None and gr >= new_state.room.id]
                                states.append(new_state)
                        else: states.append(new_state)
                elif item == 'y':
                    if len(state.stack) > 1 and state.item == None and state.jars < JAR_LIMIT:
                        #Jar Exit
                        new_state = state.copy()
                        new_state.name = 'Yield ' + str(state.jars + 1)
                        new_state.grab_item(i, False)
                        jar = new_state.pop_room()
                        jar.player_pos = state.node
                        new_state.item = jar
                        new_state.jars += 1
                        jar.jar_num = new_state.jars
                        new_state.transform_oobleck(True)
                        if new_state.name == 'Exit (Paradox)':
                            new_state.name = 'Yield ' + str(state.jars + 1) + ' (Paradox)'
                            if self.steal_item or self.entered_paradox and self._depth > self.entered_paradox + 1:
                                states.append(new_state)
                        else: states.append(new_state)
                elif isinstance(item, Room):
                    #Pick up jar
                    new_state = state.copy()
                    new_state.grab_item(i)
                    new_state.name = 'Grab jar '+str(new_state.item.jar_num)
                    states.append(new_state)
                elif item not in '_wWmMLX':
                    #Pick up item
                    new_state = state.copy()
                    new_state.grab_item(i)
                    new_state.name = 'Grab '+new_state.item
                    states.append(new_state)
            for i, (r, n, c) in enumerate(state.globals):
                if r == state.room.id and n == state.node and not isinstance(c, int):
                    #Pick up global item
                    new_state = state.copy()
                    new_state.grab_global_item(i)
                    new_state.name = 'Grab '+new_state.current_item()
                    states.append(new_state)
        else:
            if len(node) < ITEM_LIMIT:
                #Drop held item
                new_state = state.copy()
                new_state.name = 'Drop '+new_state.current_item()
                new_state.drop_item()
                states.append(new_state)
            if 'x' in node:
                if len(state.stack) > 1:
                    #Exit with item
                    new_state = state.copy()
                    new_state.name = 'Exit'
                    new_state.pop_room()
                    new_state.transform_oobleck(True)
                    if new_state.name == 'Exit (Paradox)':
                        if self.steal_item or self.entered_paradox and self._depth > self.entered_paradox + 1:
                            states.append(new_state)
                    else: states.append(new_state)
        for i, edge in enumerate(state.room.edges):
            result = state.can_move_to(i)
            if result is True:
                #Move
                new_state = state.copy()
                dest = edge[0]
                if state.node == edge[0]: dest = edge[2]
                new_state.name = 'Move '+str(new_state.node) + '->' + str(dest)
                new_state.node = dest
                if isinstance(new_state.item, int) and 'M' in new_state.room.nodes[dest]:
                    new_state.item = new_state.globals[new_state.item][2].replace('g', '')
                states.append(new_state)
                #Drop item off ledge
                if state.item != None and '=' not in edge[1]:
                    new_state = state.copy()
                    dest = edge[0]
                    if state.node == edge[0]: dest = edge[2]
                    if len(state.room.nodes[dest]) < ITEM_LIMIT:
                        new_state.name = 'Throw '+state.current_item() + '->' + str(dest)
                        new_state.drop_item(dest)
                        states.append(new_state)
            elif result == 'l':
                if state.current_item() in ['k', 'gk']:
                    #Unlock door
                    new_state = state.copy()
                    new_state.unlock_door(i, back = state.node == edge[2])
                    new_state.name = 'Unlock door'
                    states.append(new_state)
            elif result == 't':
                if state.item != None:
                    #Throw item
                    new_state = state.copy()
                    dest = edge[0]
                    if state.node == edge[0]: dest = edge[2]
                    if len(state.room.nodes[dest]) < ITEM_LIMIT:
                        new_state.drop_item(dest)
                        new_state.name = 'Throw '+state.current_item() + '->' + str(dest)
                        states.append(new_state)
        if len(state.stack) < STACK_LIMIT:
            for i, item in enumerate(node):
                if isinstance(item, Room):
                    #Enter jar
                    new_state = state.copy()
                    new_state.grab_item(i, False)
                    jar = new_state.item
                    new_state.item = state.item
                    #if jar.jar_num == -1:
                    #    new_state.push_room(self.glitch, None)
                    #else:
                    new_state.push_room(jar, None)
                    new_state.name = 'Enter jar '+str(jar.jar_num)
                    #new_state.room.jar_num = -1
                    states.append(new_state)
                elif item.isdigit():
                    #Enter chest
                    if 'W' not in node and 'M' not in node:
                        #Dry
                        new_state = state.copy()
                        new_state.push_room(self.rooms[int(item)], None)
                        new_state.name = 'Enter '+item
                        states.append(new_state)
                    if 'w' in node or 'W' in node or 'm' in node or 'M' in node:
                        #Wet
                        new_state = state.copy()
                        new_state.push_room(self.rooms[int(item)+len(self.rooms)//2], None)
                        new_state.name = 'Enter '+item+' wet'
                        states.append(new_state)
            for i, (r, n, item) in enumerate(state.globals):
                if r == state.room.id and n == state.node:
                    if isinstance(item, str) and item[-1].isdigit():
                        #Enter global chest
                        if 'W' not in node and 'M' not in node:
                            #Dry
                            new_state = state.copy()
                            new_state.push_room(self.rooms[int(item[-1])], i)
                            new_state.name = 'Enter g'+item[-1]
                            states.append(new_state)
                        if 'w' in node or 'W' in node or 'm' in node or 'M' in node:
                            #Wet
                            new_state = state.copy()
                            new_state.push_room(self.rooms[int(item[-1])+len(self.rooms)//2], i)
                            new_state.name = 'Enter g'+item[-1]+' wet'
                            states.append(new_state)
                    elif isinstance(item, Room):
                        #Enter global jar
                        new_state = state.copy()
                        jar = state.globals[i][2]
                        new_state.globals = state.globals[:]
                        new_state.globals.pop(i)
                        #if jar.jar_num == -1:
                        #    new_state.push_room(self.glitch, None)
                        #else:
                        new_state.push_room(jar, None)
                        new_state.name = 'Enter g jar '+str(jar.jar_num)
                        #new_state.room.jar_num = -1
                        states.append(new_state)
        return states
    def check_state(self, state):
        if self.kwargs.get('goal', '$') == '$' and state.context == 'P':
            return False
        if self.kwargs.get('goal', '$') != '$' and state.item == '$':
            return False
        if self.entered_paradox:
            if self.steal_item:
                return state.context == 'P' or self._depth <= self.entered_paradox + STEAL_ITEM_THRESHOLD
            else:
                if self._depth > self.entered_paradox + 1: self.steal_item = True
                return state.context == 'P'
        elif state.context == 'P':
            self.entered_paradox = self._depth
        return True
    def check_finish(self, state):
        return state.item == self.kwargs.get('goal', '$')

pJourney = ['x123', (['x', 'b'], [(0, 'l', 1), (0, '>>', 1)]), 'xk', 'x(<<$)'] #9 moves
pReset = ['xb(<<1|<<<<$)', 'xb'] #12 moves
pLedges = [(['xb1', '_', '', '$'], [(0, '', 1), (0, '<<<', 2), (2, '', 3)]),
           (['x', '_', '2'], [(0, '>', 1), (1, '<', 2), (0, 't', 2)]), 'xb'] #15 moves
pTrap = ['x1b(l$)', (['x', '', '2'], [(0, '>', 1), (1, '<', 2), (0, 't', 2)]), 'x(<<k)'] #16 moves
pSecure = ['x1', 'xk(ll$)'] #9 moves
pPits = ['x12', 'x(>>>>k)', 'x(l$)'] #9 moves
pAwkward = [(['x1', '', 'k'], [(0, '<', 1), (1, '>>>>', 2)]),
            (['x', 'b', '', '$'], [(0, '', 1), (1, '<<', 2), (0, '<t', 2), (2, 'l', 3)])] #27 moves
pSituation = ['x12', 'xbbb', 'x(<<<$)'] #13 moves
pLoop = [(['x', 'k', 'b', '0', '', '$'], [(0, '>>', 1), (0, '>>', 2), (1, '>>>', 3), (2, '>>>', 3), (3, 'l', 4), (4, '<<<', 5)])] #20 moves
pKnot = ['x1', 'x2(llb)', 'xk(<<<$)'] #35 moves
pPerspective = ['x12bk', (['x', '_', '0'], [(0, '>>', 1), (1, '>', 2)]), 'x(<l$)'] #18 moves
pMoreSecure = ['x1', 'x2', 'xk(lll$)'] #18 moves
##########################################################################
pFlood = ['xw1', 'xw(<<$)', '', 'xW($)'] #3 moves
pDrain = ['xw1', 'x(<<bk|<<<l$)', '', 'xW(bW|l$)'] #15 moves
pBasin = [(['xw1', '_', 'k'], [(0, '', 1), (1, '<<', 2)]), (['x', '0'], [(0, '<<', 1)]), 'xW1k', 'xWb(l$)'] #16 moves
pRepeat = ['xwk0(ll<<<$)', 'xw0(ll$)'] #9 moves
pLatch = ['x1(>>>W)', 'x2', 'x(l$)', '', 'xw(<>>W2)', 'xkW'] #17 moves
pGyre = [(['xb', '$', '', '1'], [(0, '<l', 1), (0, '>>>', 2), (2, '<<', 3)]), (['x', '_', 'k2'], [(0, '>>', 1), (1, '', 2)]),
         (['xw', 'w', '0'], [(0, 'l', 1), (1, '>', 2)]), 'xWb1', 'xW2k', 'xW(l0)'] #28 moves
pPermute = ['x1k(ll$|<<2)', 'x(lb)', (['x', 'w3'], [(0, 'l', 1), (0, '<<>>', 1)]), 'xw(<<<<k)', '', 'xWb', 'xW3', 'xWk'] #56 moves
pIntrospect = ['x(>>W12)', 'x0', 'x$', 'xW12', 'xW', 'xw'] #14 moves
##########################################################################
pGreen = ['x1(<<k|l$)', 'xgb'] #10 moves
pStore = ['gkx1k', 'x(ll$)'] #11 moves
pPile = [(['gb', '', 'x', '1'], [(0, '<', 1), (1, '>', 2), (2, '>', 3)]), 'xb(<<<<$)'] #23 moves
pReach = [(['xg0', '', '$'], [(0, 't', 1), (1, 't', 2), (0, '<<', 1), (1, '<<', 2)])] #10 moves
pGaol = ['x123', 'x(<<<gk)', 'xb', (['x', '', '$'], [(0, 'l', 1), (1, '<<', 2)])] #32 moves
pEmpty = ['x1', (['xgkgb', '', '2', '', '$'], [(0, '<', 1), (1, '<', 2), (2, 'l', 3), (3, '<<', 4)]), 'x'] #30 moves
pMostSecure = ['x1', 'xkgk(lLll$)'] #19 moves
pSluice = [(['xwg0','','$', 'X'], [(0, '<<<', 1), (1, 't', 2)]), (['px', '2', '2'], [(0, '>>', 1), (0, '>>', 2)]), (['x', 'f', 'k', '*'], [(0, '<', 1), (1, 'l', 3), (1, '<<=', 2)]),
           (['xW', 'W', '$', ''], [(0, '', 1), (0, '', 3)]), '', ''] #10/? moves
pAttic = ['xg1k', 'x2', (['x', '', '', '$'], [(0, 'l', 1), (1, 't', 2), (0, '<<', 2), (2, 't', 3)]),
          'px4', (['xf', '', '5'], [(0, '<<', 1), (1, '>', 2)]), (['x', '', '*'], [(0, '<<', 1), (1, '<<', 2)])] #27/39 moves
pObstruction = ['xw1', 'xg2(l3)', 'x(<<k)', (['x', '', 'X'], [(0, '>>', 1)]), 'px5', 'x(>>6)', (['xgf', '', '', '*'], [(0, '<', 1), (1, '<<', 2), (2, '<<', 3)]),
                '', 'xW(lW3)', 'xW(k)', (['xW', 'W', 'W$'], [(1, '', 2)]), '', '', ''] #35/68 moves
#########################################################################
pSinkhole = ['x1', 'x2(>>>W)', (['x', 'k', '', '', '$'], [(0, '<<', 1), (0, '', 2), (2, 'L', 3), (3, '<<', 4)]),
             '', 'x2W', (['x', 'k', '', 'W', '$'], [(0, '', 1), (1, '<', 2), (2, '', 3), (3, '', 4)])] #20 moves
pBridge = ['x(>1|>2)', (['x3gk', '', '$'], [(0, '<', 1), (1, 'l', 2)]), 'x3(<<k|lgb)', 'x'] #49 moves
pAcid = ['xkgk(M1)', 'x(ll2)', 'x(<<$)', '', 'xM(llM2)', 'xM($)'] #20 moves
pBlock = ['x(>1|>2)', 'x1(<<<$)', 'xM(gbgb)', '', 'xM1', 'xM(M)'] #42 moves (takes a while)
pFeedback = [(['xg1', '', '$'], [(0, '<<<<', 1), (1, '<<', 2)]), (['x0w', '', 'b'], [(0, 't', 1), (0, '<<', 1), (1, 'l', 2)]), 'px3', (['x', '_', 'fk', '', '', '*'], [(0, '', 1), (1, '<', 2), (2, '<<', 3), (3, '<', 4), (4, 'l', 5), (0, 't<<<', 4)]),
             (['xk', '', '$'], [(0, '', 1)]), (['x0W', 'W', 'Wb'], []), '', ''] #27/29 moves (crystal takes a while)
pBath = ['x1a(<<<<gb)', 'xb(<<<<$)', '', 'x'] #23 moves
pEmbed = ['x1', (['x2', 'M', 'g3'], [(0, '', 1), (1, 'l', 2)]), 'x', (['x', '$'], [(0, 't', 1)]), 'px5', 'x(<>6)', (['x', 'f', '', 'k', '*'], [(0, '<', 1), (1, '<<', 2), (2, '<<', 3), (2, 'l', 4)]),
          '', '', 'xkM', (['xM', '$M'], []), '', '', ''] #32/71 moves
pPillar = ['x12', (['xM', '', 'gbgk'], [(0, '', 1), (1, '<>>>', 2), (0, '<<<', 2)]), 'x(<<3)', (['x', '', '$'], [(0, '<', 1), (1, 'l', 2)]),
           '', '', 'xM(<<<3)', (['xM', 'X', '$'], []),] #39 moves
pMire = ['x12', (['xb3', '', 'gk'], [(0, '>>>', 1), (1, '', 2)]), (['x', '', '', '$'], [(0, '<<', 1)]), 'xw',
         '', (['xb3W', 'W', 'W'], [(0, '', 1)]), (['x', '', '', '$'], [(0, '<', 2), (1, '', 2), (2, 'l', 3)]), 'xW'] #50 moves (takes a long time)
pInterlock = ['x1', 'xg23g4', (['x', 'gk'], [(0, '<<>>', 1), (0, 't', 1)]), 'x', (['x', '', '$'], [(0, 't', 1), (1, 'l', 2)]), 'px*'] #53/17 moves
##########################################################################
pFissure = ['xbb1', (['x', 'y', '$'], [(0, '<<>>>>', 1), (1, '<<', 2)])] #11 moves
pResume = ['x1', (['k', 'x', 'y', '$'], [(0, '<', 1), (1, '<', 2), (2, 'l', 3)])] #11 moves
pPermanence = ['xkgb1', (['x', 'y', '', '$'], [(0, '<', 1), (1, 'l', 2), (2, '<<', 3)])] #17 moves
pRestructure = ['xk12', 'x(<y|<<<$)', 'x(lbby)'] #21 moves
#pJar = ['1k', (['x', 'y', '', '$'], [(0, '>', 1), (1, '<>>>', 2), (0, 'T', 2), (2, 'l', 3)])]
pBuild = ['x1(l$)', 'xb(<<<y|<<<<<k)'] #27 moves
pInternal = ['xbk1', (['xy', '', 'W'], [(0, '<', 1), (1, 'L', 2)]), '', 'xW$'] #23 moves
pEntwine = ['x12', (['x', 'y', '', '$'], [(0, '<', 1), (1, 't', 2), (0, '<<', 2), (2, 'l', 3)]),
            (['x', 'k', 'b', 'y'], [(0, '>>', 1), (0, '>>', 2), (1, '>>>', 3), (2, '>>>', 3)])] #25 moves (takes a long time)
pClasp = ['xkkg1', (['xy', 'b', '', '$'], [(0, 'll', 1), (0, '<', 2), (2, '<t', 3)]), 'xp'] #31/? moves (takes a while)
pTraversal = ['x1', 'xy(>b|<<<$)'] #19 moves
pHydrophobic = ['x1(>>W)', 'xy(lb|<<<<$)', '', 'xWyk(lW|<<<$)'] #35 moves (takes a long time)
pBlister = [(['xwg0', 'y', '', '$', ''], [(0, '<<', 1), (0, '<', 2), (1, 't', 2), (2, '<<', 3), (0, '', 4)]), (['px', '', '2'], [(0, '<', 1), (1, '<-', 2)]), (['xgf', '1', '', '*'], [(0, '<<', 1), (0, '<<', 2), (2, '<<', 3)]),
            (['xW', 'yW', 'W', 'W$', 'X'], [(0, '', 1), (2, '', 3)]), (['x', '', '2'], [(0, '<', 1), (1, '<-', 2)]), (['x', '1', '', '*'], [(0, '<<', 1), (0, '<<', 2), (2, '<<', 3)])] #19/70 moves (takes a while)
#################################################################################
#pClutch
pSojourn = [(['x1', '2', 'W'], [(0, '<>', 1), (0, 't>>', 2), (1, '>>', 2)]), (['x', 'gky'], [(0, '>', 1)]), (['x', 'y', '', '$'], [(0, '>>>', 1), (1, '<>', 2), (2, 'l', 3)]),
            '', (['xW', 'yW'], []), (['xw', 'yW', 'W', 'W$'], [(0, '<>>', 2), (1, '', 2)])] #37 moves (takes a while)
pPayload = [(['xbbk1', '_', '2'], [(0, '>>', 1), (1, '', 2)]), 'xyy', 'x(lyy|<<<$)'] #41 moves (takes a long time)
#pAltar
pEscalate = ['xg1', (['xy', '', '2'], [(0, 't', 1), (1, '>>', 0), (1, 't', 2), (2, '>>', 0)]), (['x', '', '$'], [(0, 't', 1), (1, '>>', 0), (1, 't', 2), (2, '>>', 0)]),
             'xpkg4(<<ll*)', 'x(>gf5)', 'x'] #51/59? moves (S8+J2, takes a very long time)
pTrilemma = ['x1', 'xg1(l2|->>k)', 'x(<3$)', 'x', (['px', 'b56'], [(0, '<>', 1)]), (['x', 'gf', '', '', 'k'], [(0, '<<<', 1), (0, '<<', 2), (1, 't', 2), (0, '=>>', 3), (3, '>', 4)]), 'xm(Ll*)',
             '', (['xM', 'M2', 'Mk'], [(0, 'l', 1)]), 'xM(<M3$)', 'xM', '', (['xM', '', '', 'M', 'Mk'], [(0, '', 1), (0, '<<', 2), (1, 't', 2)]), 'xM(Ml*)'] #12/91 moves
#################################################################################
pOobleck = [(['x', 'k', 'o', '$'], [(0, '<>', 1), (1, 'l', 2), (2, 'l', 3)])] #8 moves
pCopy = ['x1(<>k)', 'xo(ll$)'] #15 moves
pScale = ['x12', 'xb(<<<<3)', 'xo', 'x(<<<$)'] #30 moves
pSplit = ['x1', (['xo', 'bk', '$'], [(0, '>>>>', 1), (1, '<<ll', 2)])] #24 moves
pEnchant = ['xb1', (['xgo', 'k', '$'], [(0, '<<', 1), (0, 't', 1), (0, '<tll', 2)]), 'xp*'] #33/? moves
pOubliette = ['xog0(t>>k|tll$)'] #20/? moves (takes a while)
pWash = ['x1b(<<2)', 'xw(<<<$)', 'x(<<>>o)', '', 'xW(W$)', 'xW(Wo)'] #18 moves
pCombine = ['xoo1(<l$)', 'x(>k|>b)'] #16 moves
pIntangible = ['x12(ll$)', 'x(b|<<o)', (['x', '', 'gk'], [(0, '>', 1), (1, '>', 2)])] #40 moves
pTransient = ['xbbb1', (['x', 'yo', '$'], [(0, '<', 1), (1, '<<<<', 2)])] #25 moves
pHanoi = ['xkgo12', 'x(<<3)', 'x(lb)', (['xk', '', '$'], [(0, '<<', 1), (1, 't', 2)]),
          'xpg56*', 'x(<>k)', ''] #60/? moves (takes a long time)
pDual = [(['x', 'w1k', 'o'], [(0, '>>>', 1), (1, 'l', 2)]), (['x', '0', 'b', '$'], [(0, '>>>', 1), (1, '<>', 2), (1, '<<', 3)]), 'xW1ko', 'xW'] #28 moves
pJetsam = ['xW12', 'x(<<o)', 'x(<<<<|<<$)', 'xgb', '', (['xW3', ''], []), (['xW', '', '$'], [(0, '', 1)]), 'xW'] #51 moves
pJaunt = ['x123', (['x', 'y', '$'], [(0, '<<>>>', 1), (1, 'l', 2)]), 'xwgo', (['x', '', 'k'], [(0, '<', 1), (1, '>>', 2)]), 
          '', (['x', 'y', '$'], [(0, '', 1), (1, 'l', 2)]), 'xW', (['x', '', 'k'], [(0, '', 1)])] #33/? moves
pTransfer = [(['1', 'k', 'x', 'o', '2'], [(0, '<', 1), (1, '<', 2), (2, '>', 3), (3, '>', 4)]), 'xy(<l$)', 'x(<>by)'] #50 moves
pDump = [(['xg1', 'gk', '_', '2'], [(0, '<<', 1), (0, '>', 2), (2, '<', 3)]), (['x_', 'y', 'b'], [(0, '<>', 1), (1, 't', 2), (1, 't>>', 0), (2, '>>>', 0)]), (['xo', '', '$'], [(0, '>>>>', 1), (1, 'lll', 2)])]

ITEM_LIMIT = 5
STACK_LIMIT = 5
JAR_LIMIT = 2
STEAL_ITEM_THRESHOLD = 3
if __name__ == '__main__':
    puzzle = pDump
    rooms = []
    for edges in puzzle:
        room = Room()
        if isinstance(edges, str):
            edges = parse_edges(edges, place_endpoints=True)
            room.build_from_edges(edges)
        else:
            room.build(edges[0], edges[1])
        rooms.append(room)
    print(rooms)
    solver = RecursedSolver()
    solver.solve_optimal(rooms, debug=0, diff=0, use_names=1, showprogress=1, goal='$')