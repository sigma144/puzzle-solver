def from_strs(strs, extra={}):
    map = {'P':'P-', 'p':'P.', 'X':'X-', 'x':'X.', 'O':'O-', 'o':'O.'}
    map.update(extra)
    return [[map.get(c) or c for c in s] for s in strs]

puzzle1 = from_strs([
'p..x..o',
'O--X--P',])
'''
< < < < < S > > > > >
Solved with score 10!
Moves: 11
382 iterations, 0.01 seconds.
'''

puzzle2 = from_strs([
'----X-O',
'o.x.p..',
'----P--',])
'''
S < < ^ ^ > > > S < < <
Solved with score 10!
Moves: 12
455 iterations, 0.01 seconds.
'''

puzzle3 = from_strs([
'....',
'.px-',
'..--',
'o-P-',
'----',])
'''
S ^ > v S > ^ < S < v S v <
Solved with score 10!
Moves: 14
905 iterations, 0.01 seconds.
'''

puzzle4 = from_strs([
'----',
'-P-.',
'--x.',
'o-p.',
'....',])
'''
S v v S > ^ < S ^ < ^ ^ > > v < ^ < v v
Solved with score 17!
Moves: 20
2625 iterations, 0.04 seconds.
'''

puzzle5 = from_strs([
'  ---..',
'o.--X..',
'.-P-.p.',
'.---...',
'  --...',])
'''
> ^ ^ > v v < v S < < S ^ < ^ ^ > > v < ^ < v > v < S < v S < S ^
Solved with score 28!
Moves: 33
11347 iterations, 0.20 seconds.
'''

puzzle6= from_strs([
'  -----',
'-------',
'-.-X-s-',
'---P---',
'  -----',], {'s':'OP.'})
'''
S ^ < ^ > > S ^ S ^ > > v < < < < S v S v v < < ^ ^ > > > > ^ > v
Solved with score 28!
Moves: 33
4202 iterations, 0.06 seconds.
'''

puzzle7 = from_strs([
' ..  -- ',
'..o.----',
'.p.X-XP-',
'..o.----',
' ..  -- ',])
'''
v < < ^ < > v > > ^ < < S v > ^ > ^ S < S < v < < ^ >
Solved with score 24! 
Moves: 27
151468 iterations, 2.42 seconds.
'''

puzzle8 = from_strs([
' --  .. ',
'--X-....',
'-P-o.op.',
'--X-....',
' --  .. ',])
'''
S v v > ^ S < < < < ^ S < ^ > < ^ ^ > v S > > S < v >
Solved with score 22! 
Moves: 27
67345 iterations, 1.10 seconds.
'''

puzzle9 = from_strs([
'  --- ',
' .X-X.',
'..OSOp',
' .-X-.',
'  --- ',], {'S':'OP-'})
'''
^ ^ > v S < S v S < S < < v v > ^ ^ > ^ ^ < v ^ < v S < < < S > v < v v > ^ v > ^ S >
Solved with score 36! 
Moves: 43
366978 iterations, 5.57 seconds.
'''

puzzle10 = from_strs([
'   .. ',
'--...-',
'-XossP',
'--...-',
'  .p  ',], {'s':'OX.'})
'''
S < < S ^ > ^ < ^ ^ > v < < v < S < < ^ ^ > v S > v S < v > S ^ v > ^
Solved with score 29! 
Moves: 35
204994 iterations, 3.24 seconds.
'''

puzzle11 = from_strs([
'-----',
'-XPX-',
'..-..',
'..p..',
'.o-o.',])
'''
S > S ^ < < v > ^ > v v ^ ^ > v S > ^ < < v > S < v v S < v < < ^ ^ > v S >
Solved with score 32!
Moves: 38
73811 iterations, 1.02 seconds.
'''

puzzle12 = from_strs([
'..o..',
'.xpX.',
'--P--',
'--.--',
'--o--',])
'''
S > ^ ^ S ^ < < v > > > > S v v v > v < S ^ <
Solved with score 19!
Moves: 23
14810 iterations, 0.21 seconds.
'''

puzzle13 = from_strs([
'...-  ',
'.px-- ',
'.xs---',
'---...',
' --. .',
'  -..o',], {'s':'PX.'})
'''
> ^ ^ S > v ^ < < v > S v v < v S > > v v < S v S > >
Solved with score 22! 
Moves: 27
153638 iterations, 2.36 seconds.
'''

puzzle14 = from_strs([
'----  ',
'-.o.. ',
'-osX.-',
'-.Xx.-',
' ...S-',
'  ---P'], {'s':'OX.', 'S':'OP.'})
'''
< < ^ ^ < ^ > v > v S < < ^ S > v < S ^ ^ S ^ ^ < > > S < ^ ^ > > > v v v < v
S ^ < > v v < < < S ^ S v > >
Solved with score 46! 
Moves: 54
4480805 iterations, 86.19 seconds.
'''

puzzle15 = from_strs([
' O.o  ',
' -p   ',
'--....',
' -PXx.',
'  --  ',])
'''
S v > > S v > ^ ^ S < S < < S < ^ S > > v v S v > > > v < S > ^ ^ S ^ < S < <
S < v S > S ^ > > S v > v > ^ S < < S < < ^ S ^ < S ^ S >
Solved with score 49!
Moves: 68
35358 iterations, 0.49 seconds.
'''

puzzle16 = from_strs([
'   -P-',
'...O-O',
'..-.x.',
' .x.p.',
'  .---',
'  .---',])
'''
S v v S > ^ < S < v S < < < v > S v > S ^ > v v < v S < < S ^ S ^ ^ > ^
S ^ < ^ ^ > v v S v v < S > ^ v < < ^ < ^ > S ^ > > S >
Solved with score 50!
Moves: 64
22834 iterations, 0.32 seconds.
'''

puzzle17 = from_strs([
' p... ',
'...X.o',
'.X.-.S',
'.-.x.-',
' .... ',], {'S':'OP-'})
'''
S > v v v > v > ^ S < S ^ v < < ^ ^ ^ S < S > > v ^ < < v < v > > > S v v S v <
S < S v < ^ ^ < ^ > < < S ^ ^ S > S > > S > > >
Solved with score 51! 
Moves: 64
256897 iterations, 3.51 seconds.
'''

puzzle18 = from_strs([
' ---- ',
'-X.-o-',
'PXs---',
'-X.-o-',
' ---- ',], {'s':'OP.'})
'''
v S > > > v v < < ^ S ^ < ^ > v < S < ^ ^ > > > v v v < < ^ ^ v v > > ^ ^ ^ ^
S > S v ^ < < v < v > > > ^ > v
Solved with score 50!
Moves: 55
631636 iterations, 9.32 seconds.
'''

puzzle19 = from_strs([
'  .O.  ',
'...S...',
'. pSx .',
'. .S. .',
'...P...',
'  ...  ',
'  ...  ',], {'S':'OX-'})
'''
S > ^ > v v S > S < < v v > > ^ ^ < < ^ ^ S < ^ v < S v v S > ^ S ^ ^ < < v v v > >
S v v S ^ ^ ^ ^ > > v v v ^ ^ > > v v v < < S ^ S v < v < ^ ^ ^ ^ v v < < ^ ^ ^ > >
Solved with score 73! 
Moves: 84
6370131 iterations, 118.84 seconds.
'''

puzzle20 = from_strs([
'-----',
'-----',
's o-o',
'-----',
' XXX ',
'--P--',
'--X--',], {'s':'OP.'})
'''
S < v > ^ > ^ ^ < < v > v v < < ^ > v > ^ ^ ^ > ^ < ^ ^ > > v < < v v v v > ^ ^ ^ <
^ < > ^ > > v < < S ^ > S ^ < < v > > ^ > v v v v S v S < v v > ^ ^ ^ < ^ >
Solved with score 75! 
Moves: 80
413611 iterations, 5.76 seconds.
'''

puzzle21 = from_strs([
'o..p..',
'--X-XO',
'.x.x.o',
'O-P---',])
'''
> S > v v < > ^ ^ < < v v v S < < ^ S ^ > S ^ S > > > ^ ^ < < < S > >
Solved with score 29!
Moves: 35
145954 iterations, 1.97 seconds.
'''

puzzle22 = from_strs([
'..---o',
'..p.-.',
'---x-.',
'-.X...',
'-.-P--',
'O...--',])
'''
< S < ^ ^ ^ ^ S > > > > v v < < ^ ^ > S > > v S > S v v S v < S < ^ S < < S v
S v > S v S < <
Solved with score 35! 
Moves: 47
182623 iterations, 2.61 seconds.
'''

puzzle23 = from_strs([
' ---...',
' -.-x-.',
'.-PXx.p',
'.-- ...',
'o      ',])
'''
< ^ ^ > > v > v < ^ ^ < < v v v > ^ > > ^ S < < > > ^ ^ < < v S < ^ < < S ^ > > v v
< < < < ^ ^ S v v > ^ > < < S v v S ^ ^ > > v v < S < S > ^ ^ < < v v > v < S v
Solved with score 73!
Moves: 82
89687 iterations, 1.25 seconds.
'''

puzzle24 = from_strs([ #Unsolved
' ...---',
' .-x-.-',
'-.pxX-P',
'-.. .--',
'O   ---',])
'''
S ^ ^ < < v v v S > S ^ S < < ^ ^ > > v > S > > ^ ^ < < v S v v S v < S ^ ^ < <
S < S > ^ ^ < < v v > v < S v
Solved with score 44! 
Moves: 55
69996 iterations, 0.97 seconds.
'''

puzzle25 = from_strs([
'.......',
'...X...',
'---S---',
'.s.!.s.',
'...p...',], {'s':'OX.', 'S':'OP-', '!':'OX-'})
'''
S > > > ^ < S > v < > ^ > S v < ^ S < < v < ^ < S v < < ^ ^ S > S ^ ^ S ^ > v < <
S < v S > > ^ > v > S ^ > > v v S < S v >
Solved with score 49! 
Moves: 62
11114445 iterations, 222.88 seconds.
'''

puzzle26 = from_strs([
'.......',
'---p---',
'-.-S---',
'-OX.Xo-',
'---.---',], {'S':'OPX.'})
'''
S > S v S > > v v < < ^ < < v < < ^ > v > ^ S < S < < ^ ^ > > v S > > ^
S ^ < < v v > > > > > ^ ^ < v S < v S > v < < < S ^
Solved with score 52! 
Moves: 62
606688 iterations, 9.50 seconds.
'''

puzzle27 = from_strs([
'o.o  ',
'.p.X-',
'.oX--',
'-X.--',
'P-.  ',])
'''
> ^ ^ > < v < S v v > v S > > > S ^ ^ > S > ^ ^ < > v v < ^ S < v S > ^ <
S ^ < v < ^ S v <
Solved with score 38!
Moves: 46
92621 iterations, 1.30 seconds.
'''

puzzle28 = from_strs([
'    -  ',
' ----- ',
'--oxs- ',
'--xPx--',
' -oxo- ',
' ----- ',], {'s':'OP.'})
'''
S ^ S < S ^ S < < S < v ^ > > > > v v > S > > > v S < v v < < ^ ^ > S ^
S ^ ^ S ^ < S v < < v < < S < v v > < ^ ^ S v > S v S < ^ >
Solved with score 51! 
Moves: 66
6098059 iterations, 117.20 seconds.
'''

puzzle29 = from_strs([
'     .-..',
'.----.-x.',
'.---Ppxx.',
'o    ....',])
'''
S v > ^ v > > ^ < < S > S v < ^ > > > ^ ^ < v > S > ^ S < > v < < < > ^ < > >
S v v S v < S < < S < ^ S > < ^ < < v > > S < v S ^ > > v < < < S < ^ S < S v
Solved with score 63! 
Moves: 78
262785 iterations, 3.97 seconds.
'''

puzzle30 = from_strs([
'  .. ---',
'  .x----',
'OO.pPx..',
' ..x----',
' ... ---',])
'''
< v > < ^ ^ ^ > v S < S v S > S < v v > ^ < ^ > > > v S > S ^ > S v > ^ ^
S < S < ^ S < < < < > > > > > S > ^ > v v S < S < < S < < < S < >
S ^ < v > v v < < ^ > S > S v > ^ ^ > S ^ S < ^ < v > v < 
Solved with score 79!
Moves: 99
883166 iterations, 16.90 seconds.
'''

puzzle31 = from_strs([
'...x...',
'.-oPo-.',
'.x.x.x.',
'..-o-..',
'...p...',])
'''
^ S ^ ^ > ^ ^ > > v v < < ^ < v > S v v v S < > ^ ^ < < v v v < < ^ > v > ^ v v
S < S > ^ ^ v v < < ^ < ^ > S ^ ^ S > < < ^ ^ > > > v v S >
Solved with score 62! 
Moves: 70
11807511 iterations, 185.27 seconds.
'''

puzzle32 = from_strs([
'------- ',
'p.-.-.-o',
'---X--- ',
'-.xX    ',
'---P    ',])
'''
S < ^ ^ ^ ^ > > v v < < v v > ^ < ^ ^ ^ > > v v < v < ^ v v S > v v >
S > ^ ^ v v < < < ^ ^ > S ^ ^ > < S > < < v v > > > ^ ^ ^ > ^ S > > > < < <
S < < v S v < S v v v S > S > ^ ^ ^ > > >
Solved with score 83! 
Moves: 94
768216 iterations, 10.25 seconds.
'''

puzzle33 = from_strs([ #Unsolved
'  .o.  ',
'  .... ',
'..-X-..',
'poXPXo.',
'..-X-..',
' ....  ',
'  .o.  '])
'''
^ < v v v S > v v > S ^ > ^ v < < S v > ^ ^ ^ S ^ > S ^ ^ S v ^ ^ > > S > v S < v S >
v < < < S < ^ S ^ S < ^ > > > S > > v S < ^ S > v < < < S < v S v S > v < < S < < ^
Solved with score 66! 
Moves: 85
15710585 iterations, 356.06 seconds.
'''

puzzle34 = from_strs([
'  -.---',
'-X-.-X-',
'--.o---',
'..opo..',
'---o.--',
'-X-.-X-',
'  -.--P'])
'''
v v v S ^ < < < S ^ S < S ^ ^ v v v S < < v > > > S ^ ^ S ^ > > > ^ < ^ < v v <
S > ^ ^ < S < < ^ > S v ^ ^ < v > ^ ^ S > > > v S v
Solved with score 54! 
Moves: 66
13859394 iterations, 296.00 seconds.
'''

puzzle35 = from_strs([ #Unsolved
' oX.X.  ',
'.XoX.X  ',
'p.X.X.XP',
'.X.XoX  ',
' .X.Xo  ',])
'''
S > > > > S < < v ^ ^ ^ < < < > v v < < S < < < v < ^ S > > v v >
Solved with score 29!
Moves: 33
3002088 iterations, 56.26 seconds.
'''

puzzle36 = from_strs([
'--.---',
'-X..S-',
'-.Os..',
'..cO.-',
'-X..X-',
'O--.--',], {'S':'PX-', 's':'OX-', 'c':'OP-'})
'''
< < S > ^ ^ ^ > v ^ S > > v > S v v v > v < > S < v v < v S < < < v < ^ ^
S ^ < < ^ S < S v > > ^ ^ ^ < < v ^ > ^ S ^ > > v v < v < S v v < v v > >
S > > v S < < ^ < S < ^ S >
Solved with score 74! 
Moves: 88
3034901 iterations, 54.69 seconds.
'''

