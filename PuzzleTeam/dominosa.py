from solver import GridSolver, NumberGridState

class DominosaState(NumberGridState):
    def __init__(self, grid, x, y, nums, counts):
        super().__init__(grid, x, y)
        self.nums = nums
        self.counts = counts[:]
    def __repr__(self):
        string = ""
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
               string += str(chr(self.nums[y][x] - 10 + ord('A')) if self.nums[y][x] > 9 else self.nums[y][x]) if char == 0 else str(char)
            string += "\n"
        return string
    def get_count(self, x, y, x2, y2):
        if not self.on_grid(x2, y2): return -1
        if self.grid[y2][x2] != 0: return -1
        num1, num2 = self.nums[y][x], self.nums[y2][x2]
        if num2 < num1: num1, num2 = num2, num1
        return self.counts[num1][num2]
    def set_count(self, x, y, x2, y2, val):
        if not self.on_grid(x2, y2): return -1
        if self.grid[y2][x2] != 0: return
        num1, num2 = self.nums[y][x], self.nums[y2][x2]
        if num2 < num1: num1, num2 = num2, num1
        self.counts[num1] = self.counts[num1][:]
        self.counts[num1][num2] = val
    def decr_count(self, x, y, x2, y2, amount = -1):
        if not self.on_grid(x2, y2): return
        if self.grid[y2][x2] != 0: return
        num1, num2 = self.nums[y][x], self.nums[y2][x2]
        if num2 < num1: num1, num2 = num2, num1
        self.counts[num1] = self.counts[num1][:]
        self.counts[num1][num2] += amount
    def place(self, x, y, x2, y2):
        if not self.on_grid(x2, y2):
            return False
        if self.grid[y2][x2] != 0:
            return False
        if self.get_count(x, y, x2, y2) == -1:
            return False
        offsets1 = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        offsets2 = [(x2-1, y2), (x2+1, y2), (x2, y2-1), (x2, y2+1)]
        offsets1.remove((x2, y2))
        offsets2.remove((x, y))
        for x3, y3 in offsets1:
            if self.get_count(x, y, x3, y3) == 1:
                #print("Can't do", x, y, x2, y2, "(", self.nums[y][x], self.nums[y2][x2], ")",
                #    "bc", x, y, x3, y3,  "(", self.nums[y][x], self.nums[y3][x3], ")", "would be impossible")
                return False
            self.decr_count(x, y, x3, y3)
        for x3, y3 in offsets2:
            if self.get_count(x2, y2, x3, y3) == 1:
                #print("Can't do", x, y, x2, y2, "(", self.nums[y][x], self.nums[y2][x2], ")",
                #    "bc", x2, y2, x3, y3,  "(", self.nums[y2][x2], self.nums[y3][x3], ")", "would be impossible")
                return False
            self.decr_count(x2, y2, x3, y3)
        if x2 < x:
            self.set(x, y, '>')
            self.set(x2, y2, '<')
        if x2 > x:
            self.set(x, y, '<')
            self.set(x2, y2, '>')
        if y2 < y:
            self.set(x, y, 'v')
            self.set(x2, y2, '^')
        if y2 > y:
            self.set(x, y, '^')
            self.set(x2, y2, 'v')
        self.set_count(x, y, x2, y2, -1)
        return True

class DominosaSolver(GridSolver):
    def solve(self, board, debug=0, showprogress=0):
        nums = []
        i = 0
        while i < len(board):
            if board[i] == '[':
                for i2,c2 in enumerate(board[i+1:]):
                    if c2 == ']':
                        nums.append(int(board[i+1:i+1+i2]))
                        i += i2+2
                        break
            else:
                nums.append(int(board[i]))
                i += 1
        length = 0
        for i in range(4, len(nums)):
            if i*(i+1) == len(nums):
                length = i; break
        nums = [[nums[y*(length+1)+x] for x in range(length+1)] for y in range(length)]
        counts = [[0 for _ in range(len(nums[_2])-1)] for _2 in range(len(nums))]
        grid = [[0 for _ in row] for row in nums]
        starting_state = DominosaState(grid, 0, 0, nums, counts)
        for y in range(len(nums)):
            for x in range(len(nums[y])):
                starting_state.decr_count(x, y, x+1, y, 1)
                starting_state.decr_count(x, y, x, y+1, 1)
        print("Starting state: \n" + str(starting_state))
        self.solve_iterative(starting_state, debug=debug, showprogress=showprogress)
    def get_next_states(self, state):
        states = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in offsets:
            new_state = DominosaState(state.grid, state.x, state.y, state.nums, state.counts)
            if new_state.place(state.x, state.y, state.x+dx, state.y+dy):
                states.append(new_state)
        return states

#3x3 Dominosa Normal Puzzle ID: 3,643,185
puzzle_easy = '10230132201332310021'
#7x7 Dominosa Normal Puzzle ID: 1,561,500
puzzle_medium = '174002272575767666033155047420327642570653403572265014133443611265301411'
#15x15 Dominosa Normal Puzzle ID: 6,160,683
puzzle_hard = '9965[15][10]0[14][15]83284[11]334[13][11][15][15]10[12]587273[14]5[13][11]4[11][13]54573[14][14][10][13][10]65[10]60[14]4[14][14]824094[15]8[12]6[14][15][15]340[13][10]114365[14]1[10]42126[11][12]9[10]04[10]2552[12][12]140[15]6863501[13]37[13][13]996[10]5781326[13][12][12]70[13]87971[15]0[10]614[13][12]02[14]6036[15][15]342383281[12]18127[10]5[14]5[12]9[15]4[13]7[11]7[11][15]0[12][15]99[14]2[14][10]99[14]760[14]9[11][13][14]4[12][10][15][10]120758[13]86[11][12]789[12][11][11]775818656[11]02[12][14][11]2[11][15]4[11][11]7[10]30[13][13]1[11][13]2[10][10]99533[12]18[12]9[15]'
#Special Daily Dominosa - Mar 03, 2022
puzzle_ultra = '[22][21]7[19][11][17][18][16][24]03[23]0[17][11]50[14][17]3[10][22][21]07[15][22][18][12]1[21][25][10][15]6[17]927[11][24][24][12][10]8[23]39[23]18[17]8[22]57[20]9[14]654[12]3[12][13][20]02[20][24][25][20][19][19][15][16]442[12]8[23][12][21]0[20][21]3[16][17][15]7[23]42[18][21][11][14][17]62[21][14][23][13][16]9[25][24]0[18][25][19][10][24]6[21]5[20]853[22][24][20]9[12]5[19][12][25][25][22][12][15][15][16]3[20]78[24][15]1[16]2[23]0[13]1211[19][15][10][25][10]8[25][24][10][23][24]88[13]8[22][13][24]7[16][20]6[13]1[20][13][12][15][13][23][23]6[25]0[24][19]5[18][21][24][17][21][18][23]6[10][17]34[12][25][22]64[24][20]65[11]2[22][12][21]8[21][23]1[24]678[11][15][11]3[22][11][19]6[19]48[15]1[25]4[25]0[21][11][17][10]1[11][13][15][18][16]5[16][14][20][18]6[10][16][16][11][18][14][13]9[20]7[19][23]3[12]0[12][11][18][13]27[13][25][14][18][10][21]4[16][10][11][14][25][23][19]7[21]5[12][22][14]5[14][12][16]97[22]6[20][15][17]4[21][11][19]6[24]9[13]4[19]042[11]2[14][16][20][13][13][10][12]47[11]264[13][23][19]7[17]82[18]94[11][24][13][16]5[13]2[14]096[20]31[19][18]55[17]3[24]59[20][11]1865[19][13]3[23]4[15][18][12][18]0[14]9[18][19]9[10]0[13]1[24][16][14][21][19][18]6[10]86[25]2885[12]1[20]88[25]8[11][21][15][17][20]93[15][14][25][22][25][10][15]0[23][16][17][24][12][16][23]4[22]2[16][11]065[23][13][22][10][15][13][16]5[17]3[22]685728[10]14[13][19][15]9[11][21][10][22]34[21]32[10][14]41[15][18][15][10]79[14]24[19]6[18]5[23][23][25][13][14][22]9[11][12]9[18][19][24][18][25][14]15[24][23][23][21]183[15][13][18][22]04[10][15][25]1[25][25][21][20][20][11]9[16][17][17]9[15][22][22][17][11][17][16][10]3[17][19]678[21]6[24][17][21][16][19]72[20][17][14][11][16]00[14][19][17]203[12][24]2[24]30697[21][25]9949[20]2[22][20][14][16][25][22]55[20]08[12]771[20][18]142[16][24][21][15][16]73[12]67[23]45[21]2293[22]9[10][10][10][18][24][14][14][11]80[17][13][20][17][23][19]3[19]71[18][10]10[22]1[11]2[14][22]003[15]5[18][12]71[25][12]1[25]53[22]1[14][17][19]64[14]3[18][13]97[15]7[23]4[23][12]'
#Special Monthly Dominosa - Mar 01, 2022
puzzle_ultra2 = '[24][25][25][25][34]8[18]5[13]6[21][13]9[25]7[40][13][11][25][14][21][22][29][15][23][13]9[12][39][31]5[36][31][24][19][34]2[10][34][22][21][13][20][31]1[39]1[30][31][18][40][38][35][35]2[39][39][29]4[24]3[16][36][18][33][26][27]994[27]2[20][26][38][38][30]6[37][14][19]3[10]1[13][14][40]4[27][39][25][31][13]5[36][32]86[40][29]06[17]20[40][32][15][36]2[19][32][20][36]11[16]46[36][17][10][15]17[26][23]6[40][10][31][22]7[22][16][40][26][28][29][37][15][19][20]0[25]66[17][40][33][12][22][13]73[12][19][15][14][26][21]4[29][32][27]19[31][10][33]2[19][27][35][30]7[24][10]9[26][10][24][39][36][26][37][34][26]2[38][13]6[34][40][31][26][23][17]15[31][23][35][30][29]77[13]5[15][18]0[10][28][31][17][29]4[23][38]6[15][33][17][14][25]3[34][29][19][10][25]5[32]15[26][25][40][36]097[18]82[23]14[28][22][21]2[28]68[37]5[26][13][16][18][38][24][34][18][28]3[18]6[15][26][36][32]8[10][14][16][21][19][32]7[28][35][21][13][39][10][40][17][15][38][27][22][21][17]802[40][39][35]94[16][34]6[17]0[20][26][23][18][30]2[23]4[32]367[35][13][29][18][18][36]3[19][22][26][31]4[11][10]9[16][37][33][24][13][24][35]03[23][27][19]63[35][11]534[40][13][39]2[26][15]13[15][39][20][27][26][23][25][23][28]92[15][22][26][11][11][20]90[18]4[36]6[21][37]3[29]4[33]0[12]4[12][26][35][25][37][27][40][12][20][24][36][32]0[16][35][23]41[32][36][36][29][39][33]4[23]1[11][34][35][20]38[25]2[29][29][35][38]2[12][14]0[33][37]2[30]5[29][38][22][39]2[32][23][39][35][36][34][30]1[40][36][40]9[33][24][20][21][39][29][26]6[25][22][29][28][29][15][40][26][30][30][34][40]0[38][19][36]552[23][25][15][27]45[39]9[29][36][19][14][19][25][39][13][17][31][24][34][20][15][11][33][19][20][13][29][21]8[12][16][22][20][32][22][36][11][16][29]5[31][18][10][39][16][17][33][40][35]642[31]99[38][16][17][29][12][31]3[40][30][24][22][33][21][33][17]28[10][40][40][12][38][18][26]3[28][11]9[21][10][29][23][34][28][11][36][28][25]9[14][16][18]139[12][26][30]2[27][27]2[38]0[26]7[38][20][20][35]28[33][17]8[12][19]1[40][34][14]8[20][18][22][22][14][18][25][21][21][14][26]7060[12]0[26]4[14][40]8[15]1[30][34][28][34][23]6[25][24][25][20][33][31][24][34]5[28][25][24][28][20]66[14][23]6[28][38][23]4[24][19][24]0[14]33[19][36][20][33][30][32][12]7[39][10][16][37]65[35][16][38][20][32][38][27][23]1[15][24][14][27]1[24]7[17][17][27][20][28][32][28][17][37]1[31][10][24][30][31][19][35]6[28][15][21][27][29][11]9[24][34][26][26][20][30][37][13][39]19[18][17]82[38][15][28]5[16]1[22]8[33][36][27][34][14][31][22][39]7[17][26][28]4[13][23][25][39][24][18]7[19][37]5[27][25]93[33][12][21]9[33][22][34][11]0[13][24][40]9[35]3[39][16]4[21][10]1[25][32][11][10][19][38][15][15][34][19][24]8[11][13][32][23][20][27]7[39][38]2[14][19][11]8[24][35][23]0[26]0[22][17][11]30[36][18][29][17]5[22][23]50[19][11][20][39]74[32]9[36][31]0[33][14][13][28]0[11][19][35][10]97[10][10][29][11]1[34][33][32][28][37][34][31][23][39]0[40][33][19][14][12][12][11][19]4[37][38][28]0[13][11]294[32][12]6[37][37][35][23][22][31][36][10][27][15]7[15][39][31][15][30][37][31][11]0[23]89[17][22][25][17][25]5[13]78[21][14][31][29][29][14][36]3[15]6[25][20][33][16]7[36][11]1[33][34][21][14][18]39[19][35]6[15]4[14][10][28]3[24][23]88[34][36][39][28][13][32][39][40][12][24][24][40]9[20][39][17][33][31][27][18][24][27][16][20]3[32][29][26][32][22][27][35][28][35]4[34][32][16]1[34][34][36][23][37][19][19][12][18][28]2[30][23]0[11][10][25]4[29][14][13]1[37][14][12][25][34][11][23]75828[31]5[10][15][18][10][33]14[38][32][21][39][39][16][27]2[22]6[32][12][26]8[18]8[33][31]7[28][38][16][16]8[38][14][29]5[30][29]3[31][32][19]9[15]12[22]4[35][32][21][16][38][40][21][26]8[27][30][22]4[10]3[21][35][37][12][14]55[17]77[16][21][37][11][10]5[15]17[22][34]0[37][13]2[13][32][40][14][30][36][39][10][26][35][24][21]4[37][10][12][39][11][12][33][14][39][18][11]8[18][14][36]3[30][20]72[35][37]922[13][13][13]8[22]25[17][32][13]8[30][32][27][27][30]1[36][28][27][27][18]2[15][37][39]6[19][40][28][23][38][13][25][38][30][34][22][32][22]4[19][14][36][36][28][36][15]51353[23][17][23][31]7[15][16][27][25][28][30][19]73[14][12][10][28][25][40][16][16][26]5[24][19][11]343[27][24]0[10][37][10][23][23][10][33][33][27]5081[16][30][28][28][18][11][38][40][18][18][12][20]4[21][34][17]0[12]3[16][27]0[34][31]40[19][27][36][25][21][16][24][22][11][21][35][33][30][28][36][37][39]7[35][13]5[22]8[31][28][38]7[26][29][38]6[16][34][38][26][24][19]885[35][39][11][38][29][21]2[21][14][22][14][26][15][34]0[34][18]3[35][19][12]9[38]64[31][11][11][21][21][25][12][22]9[20][15][10][17][35][13]7[18][24][34][15][40]5[11][30][35][32][12][29]5[28][19][18][30][33][35]5[22][33][13][12]2[18]3[27]10[22][16][31][21][36][20][17][37][25][35][40][14][18][24][20][37][12][17][32][10][25]5[30][24][29][11][25]7[30]3[20][25]6[21][19]8[21][34]4[16][11][30]3[17][22][24]5[12][17][34][17][36][20][13][30][12][29]5[33]40[17]9[27]9[34]9[35][16][37][31]840[21][30][30][29][20][34][20]7[29][22][23][16][21]70[39][38]7[31][37][40]4[12][18][37][33][16][37][40]8[27][15][33][13][29][33][33][19]7[17][17]9[32]6[11]1[18][30][38][27][37][17][15][31][12][28]2[35][29][21][21][31][35][38][20][32][24][24][27][17][18][38]1[39][16][10][18][32][36][19][17]38[33][40]1[40][37][31][10][39][38]111[37][13][26][16]630[16][10][18][15][20][38][20][21]9[21]58747[20]76[11][25][10][13][23][23]6[35][24]2[39]8[14]7[36][39][23]9[16][32][40]690[12][37][11][26]92[10][37][30][14][13][37][37][26][36]6[37]3[15][38][26]2[16][28]6[11][23]1[11]6[20][17]5[29][31][23][12]69[30][24][35][14][14][31]13[25][37][27][34][28][13][22][33][30][38][17][30][14][32][38][15][25][29][32][30][15][30][40][32][15][22][19][12][12][12][33][20]8[25][40][22][27][26][14][33][18][32]8[31][27][28]'

DominosaSolver().solve(puzzle_hard, debug=0, showprogress=0)