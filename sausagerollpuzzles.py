from sausageroll import SSRState

#World 1

pBabysNeck = SSRState.build_puzzle( #48 moves
    ['..#.',
     ' . .',
     '^#FS',
     'v.. '])
pBurningWharf = SSRState.build_puzzle( #34 moves
    ['SF<>..',
     '.^## .',
     ' d## .'])
pComelyHearth = SSRState.build_puzzle( #51 moves
    ['  ...',
     '.FS. ',
     '<>#<r',
     '.##. ',
     '...  '])
pEastreach = SSRState.build_puzzle( #26 moves
    ['^..# ',
     'v<>##',
     'FS.  ',
     '.##  ',
     ' ##  '])
pFieryJut = SSRState.build_puzzle( #25 moves
    ['###  .',
     '###^^.',
     '###vvS',
     '###  F'])
pHappyPool = SSRState.build_puzzle( #54 moves
    [' .<>..',
     '..   .',
     '.  # .',
     '. #  .',
     'S   ..',
     'F.... '])
pInfantsBreak = SSRState.build_puzzle( #30 moves
    ['  ...  ',
     '  <>^  ',
     '##FSv# ',
     '##   ##'])
pInletShore = SSRState.build_puzzle( #44 moves, takes a while
    ['F.^.',
     'S.v#',
     '#^..',
     '.v..'])
pLachrymoseHead = SSRState.build_puzzle( #68 moves, takes a while
    ['.###.',
     '<>^..',
     'F.v<>',
     'S###.'])
pLittleFire = SSRState.build_puzzle( #34 moves
    ['....',
     '<>#^',
     '.#.v',
     '.SF.'])
pMaidensWalk = SSRState.build_puzzle( #30 moves
    ['#^.#',
     '#vF.',
     ' .S.',
     '..  '])
pMerchantsElegy = SSRState.build_puzzle( #46 moves, takes a long time (need pruning)
    ['.....',
     'F#^^#',
     'S#vv#',
     '.....'])
pSeafinger = SSRState.build_puzzle( #18 moves
    ['.##u ',
     '.##v.',
     '.## f',
     '   ^S',
     '   v.'])
pSouthjaunt = SSRState.build_puzzle( #34 moves
    [' SF ',
     '....',
     '^##^',
     'v##v',
     '....'])
pTheAnchorage = SSRState.build_puzzle( #112 moves!
    ['   .......',
     '   . .   .',
     ' ####uuu F',
     ' ####vvv.S',
     '          ',
     '..##      '])
pTheClover = SSRState.build_puzzle( #62 moves, takes a long time
    [' <>....',
     ' ##   .',
     ' ## ##^',
     'SF..##v',
     ' ##....',
     ' ##.   ',
     ' <>.   '])

# World 2