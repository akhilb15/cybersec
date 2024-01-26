# Map state
# # refines our view of the world as much as possible
#   sawnbombsat()
# # check is there is possibly a bomb there or if we were there before we learned something ew
#   canmoveto
#   movedto()

# while True
#   for x [up down left right] ordered by going closed to flag:
#     if mapstate.canmoveto(x):
#       moveto(x
from pwn import *
import z3.z3
# import cvc5.pythonic as z3
import networkx as nx

from queue import PriorityQueue
from functools import reduce

ROWS = 2034
COLS = 2034
TILE_ROW = 2034 // 3
TILE_COL = 2034 // 3

FROG_WARNINGS = ['ribbit', 'giggle', 'chirp']
NEBULA_WARNINGS = ['light', 'dust', 'dense']

def dist(x, y):
    return sum(map(lambda x, y: abs(x - y), x, y))

def in_bounds(loc):
    return loc[0] >= 0 and loc[0] < ROWS and loc[1] >= 0 and loc[1] <= COLS

def add_off(loc, off):
    return tuple(map(lambda x, y: x + y, loc, off))

def adjacent_to(loc):
    adjacent = []
    for off in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        potential = add_off(loc, off)
        if in_bounds(potential):
            adjacent += [potential]

    return adjacent

class WorldState:
    def __init__(self):
        # print("Initing WorldState")
        self.s = z3.Solver()
        # self.s = z3.Tactic('qflia').solver()
        self.s.push()
        self.constraints = set()
        self.variables = {}
        self.tiles = set()
        self.free = set()

        # print("WorldState inited")
    def get_var(self, loc, check=True):
        if check and ((loc[0] // 3, loc[1] // 3) not in self.tiles):
            row_start = (loc[0] // 3) * 3
            col_start =  (loc[1] // 3) * 3
            s = []
            for r in range(row_start, row_start + 3):
                for c in range(col_start, col_start + 3):
                    # print("Tile")
                    # print(r, c)
                    s += [(self.get_var((r, c), check=False), 1)]

            self.tiles.add((loc[0]//3, loc[1] // 3))
            # print(s == 1)
            # self.s.add(s == 1)
            self.s.add(z3.PbEq(s, 1))
        if loc in self.variables:
            return self.variables[loc]
        else:
            v = z3.Bool(str(loc))
            # self.s.add(z3.Or((v == 0), (v == 1)))
            self.variables[loc] = v
            return v

    def get_knowledge_id(self):
        return len(self.constraints)

    def add_constraint(self, loc, n):
        # we already have the info from this loc
        if (loc, n) in self.constraints:
            return

        self.constraints.add((loc, n))
        # print(self.constraints)

        adjacent = map(self.get_var, adjacent_to(loc))
        # print(list(adjacent))
        # print("Add constaint: ", loc, n)
        # c = reduce(lambda x, y: x + y, adjacent, 0) == n
        c = z3.PbEq(list(map(lambda x: (x, 1), adjacent)), n)
        # print(c)
        self.s.add(c)

    def definetly_free(self, loc):
        if loc in self.free:
            return True
        self.s.push()
        # self.s.add(self.get_var(loc) == 1)
        self.s.add(self.get_var(loc))
        # print(self.s.check())
        out = self.s.check() == z3.unsat
        if out:
            self.free.add(loc)
        # print("Check: {}".format(loc),  out)
        self.s.pop()
        return out

r = remote("chall.pwnoh.io", 13387)
# r = process(["python", "./maze.py"])


class Navigator:
    def __init__(self):
        self.traversal_nodes = {}
        self.traversal_nodes_rev = {}
        self.traversal_graph = nx.Graph()


        self.nodes = 0
        self.state = WorldState()

        t = r.recvline()[1:-2].split(b' ')
        self.loc = int(t[0]), int(t[-1])
        self.get_node(self.loc)
        self.state.add_constraint(self.loc, 0)

    def get_node(self, loc):
        if loc in self.traversal_nodes:
            return self.traversal_nodes[loc]
        else:
            self.nodes += 1
            self.traversal_nodes[loc] = self.nodes
            self.traversal_nodes_rev[self.nodes] = loc
            self.traversal_graph.add_node(self.nodes)
            for x in adjacent_to(loc):
                if x in self.traversal_nodes:
                    self.traversal_graph.add_edge(self.nodes, self.traversal_nodes[x])
            return self.nodes

    def get_move_to(self, fr, to):
        diff = fr[0] - to[0], fr[1] - to[1]

        if diff == (1, 0):
            return 'w'
        elif diff == (-1, 0):
            return 's'
        elif diff == (0, -1):
            return 'd'
        elif diff == (0, 1):
            return 'a'
        else:
            # print(diff)
            breakpoint()
            assert(False)

    def get_moves(self, loc):
        path = None
        for i, adj in enumerate([loc] + adjacent_to(loc)):
            if adj in self.traversal_nodes:
                # print(loc, adj)
                try:
                    path = nx.shortest_path(self.traversal_graph, self.get_node(self.loc), self.get_node(adj))
                except nx.exception.NetworkXNoPath:
                    continue
                if i != 0:
                    path += [self.get_node(loc)]
                # print(i, path)
                break
            
        if path == None:
            breakpoint()
            assert(False)

        moves = []
        # print("Nodes to hit: ", list(map(self.traversal_nodes_rev.get, path)))
        for i, j in zip(path, path[1:]):
            i = self.traversal_nodes_rev[i]
            j = self.traversal_nodes_rev[j]
            moves += [self.get_move_to(i, j)]

        return moves

    def move(self, loc):
        if loc is not None and loc == self.loc:
            return
        plan = (self.get_moves(loc) if loc is not None else ['w'])
        # print("Plan to get from {} to {} is {}".format(self.loc, loc, plan))
        for d in plan:
            r.sendline(d)
            t = r.recvline()[1:-2].split(b' ')
            coords = []
            for x in t:
                try:
                    coords += [int(x)]
                except ValueError:
                    continue
            assert (len(coords) == 2)
            coords = tuple(coords)
            if loc ==  None:
                self.loc = coords[0] -1, coords[1]
            # print("add edge {}={} to {}={}".format( self.loc, self.get_node(self.loc), coords, self.get_node(coords)))
            self.traversal_graph.add_edge(self.get_node(self.loc), self.get_node(coords))
            self.loc = coords
            ind = 0
            data = b''
            while r.can_recv(timeout=0.01):
                data += r.recv()
            ind = 0 if data == b'' else len(data.strip().split(b'\n'))
            # while r.recvline(timeout=0.1) != '':
            #     # line = r.readline()[:-1].decode("ascii")
            #     ind += 1
            #     try:
            #         # ind = FROG_WARNINGS.index(line)
            #         pass
            #     except:
            #         try:
            #             # ind = NEBULA_WARNINGS.index(line)
            #             pass
            #         except:
            #             try:
            #                 line.index("somet")
            #                 # print("Died")
            #                 print(self.loc)
            #                 import sys
            #                 sys.exit()
            #             except AttributeException:
            #                 # print("wtf?")
            #                 breakpoint()
            #                 r.interactive()
            print("at: ", coords, " there are ", ind)

            self.state.add_constraint(self.loc, ind)

goal = tuple(map(int, r.recvline().split(b" ")))
import os
# goal = (0, COLS - 1)
try_to_die = False

print("Goal: ", goal)
os.system("sleep 1")

nav = Navigator()

last_knowledge = {}

try:
    with context.local(log_level='debug'):
        frontier = PriorityQueue()
        for x in adjacent_to(nav.loc):
            frontier.put((dist(goal, x), -nav.state.get_knowledge_id(), x))
        while not frontier.empty():
            print(frontier.qsize())
            loc = None
            while True:
                _, _, loc = frontier.get()
                is_free = nav.state.definetly_free(loc)
                # print("is free: ", is_free)
                if try_to_die:
                    break
                if not is_free:
                    continue
                if (last_knowledge.get(loc, -1) == -1):
                    break
                for x in sorted(adjacent_to(loc), key=lambda x: dist(x, goal)):
                    if nav.state.definetly_free(x) and x not in last_knowledge:
                        loc = x
                        break
                else:
                    continue
                break
            print("Moving to: ", loc)
            nav.move(loc)
            last_knowledge[loc] = nav.state.get_knowledge_id()
            # if nav.loc == (0, 0):
            #     goal = (0, COLS - 1)
            if nav.loc == (0, COLS - 1):
                try_to_die = True
            for adj in adjacent_to(loc):
                # print("adding to frontier: ", adj)
                frontier.put((dist(goal, adj), -nav.state.get_knowledge_id(), adj))
            else:
                print("Didn't go to ", loc, " because free=" ,is_free, " last_kid=", last_knowledge.get(loc, -1))
                pass

except Exception as e:
    print(e)
    r.interactive()
