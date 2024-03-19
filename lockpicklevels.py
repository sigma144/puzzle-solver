from lockpick import parse, add_edge

p11 = parse('w|Wo|Op|P$', 4)
p12 = parse('w|Wo|WwO$', 4)
p13 = parse('w|Wo|Pk|Wp|Oc|K$', 4)
p14 = parse('OO$|WWoo|(wW|gG)(Gww|Go)', 5)
p15 = parse('w|WwBbOw|OwBoo|WoOw|OoWb|WW$', 11)
p16 = parse('o|(OoOOcCO|OcCocCC|OoOoCoC)$', 6)
p17 = parse('wp|(CoPkCoP|OoCkPwOwW|WcKcPwKcWoO|) |KP$', 10)
p18 = parse('w2(O3w4|W2ow3|W6$|O2w2|W2o2w)', 5)
p19 = parse('w16((W2W3W2W3W|WW6WW|W4WW2W3)(W3W2W3|W2W3W2)$', 4)
p110 = parse('p16o8g4c2(W6$|O4w|G2C2w|(|WP4wGP2O2|GP2wGO2) |P6O2c2|C3Gw|P6w|G2C2w|CCw', 9) #Takes a bit (0.5 min)
p1A = parse('k|PwWcPc|(KkOpP|OpWwC|KoPkK)(p|PpOw|OoWp|CoKoWwK$', 20)
p1B = parse('w5o2p3g4k2((PPcGG|WKcWW|WKcGP|GWcKO|WWcWG|OOcKO|GPcPW|GOcOW|) )|C8$', 10, special='1-B')
p1C = parse('w2|WkKoOcCw|WpPcCkKw|WgGkKpPw|WoOpPgGw|WcCgGoOw|P2p2K2k2C2c2O2$', 16)

p21 = parse('m|W(mw|WP(W2w2|Wm|m|W2W$', 8)
p22 = parse('m|W2w3|W2mO2m|Wo2O4K4(PmCmW6m|mR8w6P$', 10)
p23 = parse('m|(OgGmW|WoPmRgP|PgGoOpWpP|GwOoPwWmGoO)mRwCgKpN$', 16)
p24 = parse('m3w11(W3W2W3|W3W8)(W2W6|W12W|WW3W)(W5W6|W3W3W3W3)W3$', 5)
p25 = parse('W0w(W2w|wW|W0WwW0$', 8)
p26 = parse('mo4(O2p2WWp2|O2w2WWp2|WWp2PPPPo4|PPO0(O2O2$|OOw4', 7)
p27 = parse('w15o15c15(C2W8C4|CO6C12|W2O2C2|O4|W0O0C0$|(C6|W2O12C2)(C3OW3W|W6O)', 7)
p28 = parse('o3p3c3(C3P3O3m|O12o3p3O3c3P3o3P3o3|O3p3O3p3P6o3o3O6o3c3|C3c3P6o3c3C3p3O3p3C3p3|C6c6O6o6P3P3C3$', 10)
p29 = parse('o24(O24W3w5|O2o2O4(W8o2|Ow2|O4o4w4|W2oO2W0o4W2(O0WW0$|O8|O6W2w2|O0w4|O2W6o2w8|W0w4o6|O8', 15)
p210 = parse('o(O0o|OoP2c|OoC2p2|Oc|Po4|O0(P2p2C2O0P0$|Oc2Po2|PCpO2c2', 12, special='2-10') #Demo only
p210f = parse('o(O0o|OoP3c2|OoC2p2|Oc|Po4|O0(P2p2C2O0P0$|Oc2Po2|PCpO2c2', 16, special='2-10') #Full game only
p2A = parse('m3w2k2o2c3p4(RW|KO)(CC|OK)(OK|WP)(CC|WO)(OR|OW)(PP|KO)(OR|RW)(CC$|PP$)', 9)
p2B = parse('m(O4mK2mp4|W2k24w3|K24(C2k2W8wc|W3mWCR$|P4m', 10)
p2C = parse('m3p16o3((O2(|(O2P4|O2o6|O2P2))O4P2|O4(|(P4o|P0P0P0P0$))O2)(O2p2o6|OOOOO3P3P6)', 12)
p2D = parse('o4p6(P3O2|P6o4|O4(P3o2O2p3|PP0$|o6(O2O0p3|OO0p2|P6O6p12|P0Oo2O(O2o4p3|P3P0P3o2O6p5', 17)

p31 = parse('o|Oxo2Ox(pp|Px(Pxo|Pxo2|Ox(p|OO$', 10)
p32 = parse('c4(P8$|CkKp|CkKp|CkKp|CkK0p|KKxc4|CkK0p|CkK0p|CkKp|CkK0p', 15) #Takes a while (2.9 min)
p33 = parse('c6w20o40(C6Wx|C6Ox|(O24W5|WO5O|O5W5)(W5O2W|W4OO5|W5W5)O5O2W5W2O0W0$', 8)
p34 = parse('c5m(C6c18|C3c12|C6Cx(CC4C0C0$|C6c12|C0C6|C12C3', 6) #Full game only
p35 = parse('w3w=1Ww3(Ww=3|Ww=2|WW3W2$', 7)
p36 = parse('Oo3c4|O4c4|O3o3c4|C24$|O2o4c4|O6o=3c4|O5o5c4|o3OOOo3', 9)
p37 = parse('w2(WW0w=8WW0w=5W2W0w=50WW0$|W0w4W2w4|W2w4W2w8|(W6|W2w=2)(W2W|W2W0w8|W0(W24w|<>W2w8|W8w=1', 16)
p38 = parse('p=6p=4p=5p=8p=6p=2p=3p=2c|P6P0(P3P0P2P0Pxc|(P4P0|P5P0)(P8P0c|P2P0C3P0$', 14)
p3A = parse('w(Kwc3|C2w|WkWkWkCc|KwWkOww|WkKw|WWW$|CxKwKwKkWwCo', 16)
p3B = parse('p4((Pp=0WwPp=0Oo=0Pp=0PoO|) |PoPp=0o|OoOp|PpWow|Ow=0Www|WW$', 15)
p3C = parse('c15(O2C4c=27C2C2|O2c4c4c4|O2c4O0c8C4|O2c4C4c12C8|O2C4C4|O2O0O2O0c4O6|o4O0o4O0o16O0o8O0C|O2C4C4c4Ox|C0C0$', 18) #Takes a long time (8.2 min)
p3D = parse('m3o24(W3w6W3O5|WRKm=0O0W0K0$|W3k15O4K4w2|m=0K3W3O|m=0K3O3k6|K4m=0O3K3(WK3O2|WO6|W4w8', 12) #Takes a bit (0.5 min)

p41 = parse('mw6(!O0O2w2|OOp4!P4o2w2|W2W2o2P2P2r|!W3!W3R$', 8)
p42 = parse('g5p3(@G0@G0$|@P3g|P3G3|@P0(G@P2p6G5|G2p2P3g5', 13)
p43 = parse('b2(B4b4|#Bm|Bb2|#B3b2#B0mB2(bB2|bB2|bB2|#B0#B0$', 14)
p44 = parse('m3M3(o4O0c2C3m3|O2O2c2C2m2M3m5|M5M0$', 6)
p45 = parse('w(Kw!Orw|W4r|WoKo!CkR0O0!Oow|Oc2Cw3Ro|OcKoWo2Ow|OkCk!W0o|Wo!Co!Rc|!O2!W2$', 18) #Demo only
p45f = parse('rw4o4c3(!W!W|OO)(CW|OR)(!W!O|CC)(!W!O|WC)(CW|OR)(OC|WC)$', 8) #Full game only
p46 = parse('b3(WoWow|#KwKc|BkWoWb|BkWc|R$|OwOw|Ko#Kc|BkWwOw|BkOc|#C2CCm', 22)
p47 = parse('m2(Rx|Gx|Bx|!R0r2B0g2!B2g2G0b#B0m2|B2r2B0g2#G0b2G2b2G0m2|G2g2G0b@R2g2G0r2R0m2|R2bG2g2!B0r2#R0b2R2m2|M8B6$', 25)
p48 = parse('c25p20k15m10(P4C3b3@K8G2P5K4|C3Bg5G3P0#C6G0K2P5|@G5C3K8C3rR!P6C6|!R@G8#B3R0G0B0!WKPC|M0K0P0C0$', 8) #Takes a very long time (10.1 min)
p4A = parse('mr(Rr|R|!R0!R0R|!R0!R0(!R0r!R0r!R0R|!R0!R0mrrm!R0R2|!R0(rR!R0!R0Rr|!R0!R0!R0!R0!R0!R0$', 41)
p4B = parse('#R0g=4|b2B3R|g4G2m|!G2B2!M0b3@R0#B0b2@B2#G0m4|m2@B3Gx|r5R4|!R0@G0#B0M0(G3b2#G0m|#M4r|!@#W0$', 20)
p4C = parse('m10k15p20c25(M4m2|C8KP4P4KC|K12C3KP6K4C3P5|P5C4K12P8K5C12|M0M0K0K0P0P0C0C0$', 8) #Takes a long time (6 min)

p51 = parse('w2(W2o3|Cn2|C2c3|O3c2|C4n13(KC6|P4|N4|W3O2|W0$', 10)
p52 = parse('w(CCCBxCCC$|WpPwPpPoWoc2|WoOwOwOoPwc2|WnWnOpOpPnc2', 14)
p53 = parse('m24(M4M2|N3MM3)(M3M2M3|MM8)(M6n10|M3M2(M3M3N3|M3M0N0|MM4M3M)(M2N2N4M2|M2M4M2M)M24M0$', 10, special='5-3')
p54 = parse('W2W2W4|W2W2W6p2|n8N0C0mM0C0OOKKPP$|c7(C5o2|C0C2k2', 10)
p55 = parse('k10(K4|N2k25|K2n10K5N6|K2N4|K3K2|K0K12(N2K4|N2n15|K6n15K6|K0K2K0K0$', 15)
p56 = parse('u4(U2m4U3n5O5O5u4|C2M2uU4m(KCm|O6c6|BxOPCu|U$|C4n2|C2n2', 13)
p57 = parse('c30|n20|u10|K24U$|U3C6C2N0C3C3Cxk8|U3C2N3C12NN0Ck8|U3C5N5CxC2N2k8|U3C0C8C6CxCk8', 13)
p5A = parse('m5(W2CPO2n2|O2o|O2o|W2w2|Wp|Wp|Wc|Wc|Mxw2(WWc2|WWp2|WWo|OOP4CC$', 9) #Takes a bit (0.5 min)
p5B = parse('m2(B3g8w4U3m2U2|W4(G2u9k12Mg2Gx|u=5(UU0gK4|RxKK6(G4U2w5|C3@U0K4m8g=2(W2G3M2u|K6G0W0u|K3W5W0@K0PG0W(G2@G0u|U2W2u2|U3U0$', 24, special='5-B') #Takes a while (1.9 min)

p61 = parse('(c-5c9c-4c-4|c-2c4c4c-2|c2c3c-8c3c4c-4|c-1c-1c-2c7c-1c-1)(C24$|c-1c-2c-3c8|c-2c3c-4c3|c-6c2c2c', 8) #Takes a while (3.8 min)
p62 = parse('O-2c4o-2|C2o5|o-4O-5$|O-3o-2C4c-4O-2o4(C-2o-5|O8|C-2o-2|C-2o3|C-2c2', 9)
p63 = parse('m(P-2p-2P-4P0p2P-3p-4P-2p3P8(P3p-2|P2p7|P2p-10)|P8p2P2P0P4p-2p-4P0p8P-8|M0p6P0p-6P0p6P0$', 14)
p64 = parse('r2(R2r2R-2r-2R2r2R2r-2|R2r-2R-2r-2R2r2R-2r2|R2r2R2r2R-2r-2R-2r2|R-2r-2R2r2R-2r-2R2$', 13)
p65 = parse('r4r-R-4m3(R12R-1|!R-4R-1R|R-4R12|R-12R4|r-34r-M0R0$', 10)
p66 = parse('n10(W3N5|K2C-4R3|N8N-4|O6G-3|B2N-3|N0n-7N0n7(C3N-4|K12R-3|W0N-3|n-9N0n8N0$', 15)
p67 = parse('g3(K12K12K12K12|K-12K-12K-12K-12|k-11k-12k10k-23k13k-2k=6G|k-15k14k24k-16k-9k43k=-6G|G2G0K0$', 6)
p68 = parse('OO0PP0CC0$|P0o2O2p-2P0o2P-2c2O-2p-2P0p-2C-2o2O|O0p2P0c-2C0o-2O0p2C2c2P-2o-2C2p2P|O2p-2C2o-2C-2o2O0c2P2p2P0c-2O-2c2C', 18)
p69 = parse('w-2w-W2(g4R-2r-2g-@R-2G3w6|wr2G2r-2|w-2g-w-2R-2w3g|wR2wr-2|w-r-!W16$', 13)
p610 = parse('m(U25$|(PxbUu4#B3|Uxu4U2bC-x|p-5P-xu5B0c-C3n3U|c9C3b#P0u-#P0u-4u-M-3u4N0|P-4p4C-xu-U3u3b=0c-U-3)u-6', 19, special='6-10')
p6A = parse('ur-1g-1b-1k(Uk=-1r=1b=1|Uk-b=1g=-1u|Ug=1r-b-u|Uk=-1r=0b=0u|Uk-r=1g=-1u|Ur=-1g=-1b=-1|Ub-g-r-u|Ub-g-r-u|>R-1G-1B-1K-1U$', 8) #Edge case (1-way drop)
p6B = parse('n2M4$|o2O2c2C2p-2P2c-2P2o-2|P2n-4m2|C-2o2C2p2P2c2O-2o2|O2p2P0o2C2o2P2o2|O2c2P-2p2O2c2O2p2N2o2O0p2C2c2C2o-2O2N-2', 23)
p6C = parse('RR0GG0BB0g2CC0$|C-2r2R2b2G-2b2R-2g-2C2r-2B2g2!R-2R|G0c-2B2g-2B-2g2G2b2C2c2#R0c-2!C-2G|C0r-2G-2b-2B0c2R2g2@C0b2B2r2G0B|!R-2b2B0r2G0b-2#G2c2C2r-2!B0c2G2C', 29)

p71 = parse('w6(O/W6(Ox|O-x|W2o6|W2o-4)|W/O6(O2O0o12o-4W/O-4|W0$', 11)
p72 = parse('o2O/P0c4(C2O0P0$|C4O2)|p2P/O0c4(C4P2|C2P/O2', 6)
p73 = parse('o5c7C/OxO/Cx(C/Ox(c-|C/Oxc)|O0C0$|O/Cx(o-|O/Cxo)', 8) #Demo only
p73f = parse('o5c7C/OxO/Cx(r-1|r-2|r-4|r-8|r-16|r-32|o=2>(OC/R-xC/R-xO|OC/R-xC/R-xC/R-xO|OC/R-xC/R-xC/R-xC/R-xO|OC/R-xC/R-xC/R-xC/R-xC/R-xO)L/CxL-97L0$', 7) #Full game only
p74 = parse('W/C-xW/C-xW/C-x|W24W24W0$|c-1|c-8|c-3|c4|c-3|c-3', 7)
p75 = parse('w4w*Wxw2(mP/W4M0P0pP0$|P6W5p*|W/P2w5P4p-6|W/P-4p-|P-4W/P-2p-p4', 7)
p76 = parse('cm5(k60C|M/C0c8(CK20KK4K|K2K3C3K20C2K|CK6C8K20)M/C0M/K0$', 7)
p77 = parse('c*c-*|c7(P/C4p*p-*p*|C4CP-1C/P-3m2|(P-2P-3C|C2P-4)P0m|p-4M2P-4C4(C8P-8$|C8C0p-*p-4', 15) #Takes a bit (0.5 min)
p78 = parse('c4(C24$|P/C8c4|C8p-8|P8c2|P/C4p4|C-4c6|P/C4c2|C-4p8|C/P4c2|P-4p4|C/P4c4|P-4c4', 14)
p79 = parse('(w-32w*w=-4w=54w=-42w-8|w=-12w-1w*w=71w=-17w-16|w-64w=-18w-2w=92w-*w*|w=-1w*w-4w=77w=-99w=-3)W0$', 10) #Takes a long time (8 min)
p710 = parse('m3b-5o8c9(M/C0M/O0M/B0$|B-3B4O/B5|B-xC-2#C3|CO4M/B-1b5B2O/B3C3|B/M4M2B-4(C/O-1|#O-4m|B/C8|Bx#B-5C3', 17)
p7A = parse('p4(P/C-xC/Px|C-4P/C-xP/C-x|P24P/C-x|P2C/Px|PC/Px|P8C/PxP/C-xC/Px|PxP/C-x|C-xC/Px|C-2P/C-x|P256$', 11) #Max possible score is 568
p7B = parse('o4(n17|N-3!N0$|N/O5u7O-4r|O/N8o-R2|O4r-2R2o=4|N!N-1|U/R-1UU0r2r=0N/O4|U/R-1U2U0r-r=0N/U7', 11)
p7C = parse('m1m*(U3@C-8$|G/PC2G/P-1G/PN3G/P2P-3P2p-u|P-4P/G2G-5G/PP2W4pu|RP/G-2G/P-4P/G-1G-4G/P-4G/P-1p-4u', 7)
p7D = parse('!W12$|C2C0O2w2|KC2Ow2|KR2w2|K12|o10k10c10(NN0K0O0C2w6|NC3KO6|OKk2|C4n13|N/K4rN8w6', 16, passing_effect=[0]) #Takes a bit (0.7 min)
p7E = parse('c-|o-|p-|cccccccc|oooooooo|pppppppp|>(W/Cx|W/C-x)(W/OxW/Ox|W/O-xW/O-x)(W/PxW/PxW/Px|W/P-xW/P-xW/P-x)W17W0' + 
    '(W/Px|W/P-x)(W/CxW/Cx|W/C-xW/C-x)(W/OxW/OxW/Ox|W/O-xW/O-xW/O-x)W2W0(W/Ox|W/O-x)(W/PxW/Px|W/P-xW/P-x)(W/CxW/CxW/Cx|W/C-xW/C-xW/C-x)W17W0$', 18, special='7-E')

p81 = parse('m4w13(M0W0p12P0$|(W8W2W0C2P6|M/WW4P6W) ', 8)
p82 = parse('m-4(M0w12W0c4k=6P-5P0p-P5P0W0K/CxK4$|W8|P/W5|P/C8|C/K-4|(C3K/W6|W/K-4P-1|) ', 20)
p83 = parse('m-13M0o52O0o20O0o15O0o46O0$|O|O3|O9|O27', 36)
p84 = parse('m(U/M0U/N0U/M0U/N0$|M6n|M5mn=1|M5mm-1|n3m11n-2', 11)
p85 = parse('w16p-8(P-2W4M/P-8M-2W/P-4|W2P-4M8W6M0W|M/P-2W5P-2M/W2M0P-1P-1|W0|M/P0M/W0($)', 11, special='8-5') #Special logic for bridge
p86 = parse('b(BU4M0M/B0M/W0M/C0$|BM0mw12C12bu|BM0C4m2bCc5u|BM0W4m-2bWw5u|BM0m-1c12W12bu', 13)
p87 = parse('m-1m*c-4(P/C-1|P/C-4|K/C-1|K/C-4|C-x>m-*m=1M/KxC/PxM0C-84C0C/KxC/PxC-25C0$', 19, max_stacks=2)
p8A = parse('m-5N/M-5b|c5M/C5b|n5N/C5b|U/M-xU/M0U/M-xU/M0U/M-xU/M0U/M-x#U/N0$', 41, max_stacks=4) #Takes a bit (0.6 min)
p8B = parse('w80W-8X-2m4(W-8X-1u|W8u|M2m-6M2m-2M-2m-3M2u|M2m4M-2m5Mxm-4M-2m-u|U4M0M/W0$', 23)

p91 = parse('B/[KC0O0W]Kx|B/[WCO3K3]Wx|B/[K0W3CO2]Cx|B/[O2C2W4]Ox|cccc|oooo|kkkk|wwww|B-8B-8B-8B/[WO0C2K4]$', 11)
p92 = parse('w2r-3[R-1R-1R-1R-1R-1]([RR]|[WW])(W2r2R-1u|B-1r-1|WRwr|R2w2!W0m|m-1(M0UR-1u2|U2$', 14)
p93 = parse('(wWxw4Wxw|o2Oxo2Oxo3|pPxp3Pxp2|c3Cxc2Cxc)(wWxwWxw=1|o2Oxo2Oxo=1|p3Pxp3Pxp=1|c3Cxc2Cxc=1)B/[WxOxPxCx]B-32$', 17, special='9-3') #Takes a long time (12 min), some moves out of order
p94 = parse('m(B/[WOPC]|C/[MWOP])mw(O2wc4|Wc-|P-1p-3|Wo-2|O-1o2|Wm|C-1c-|P2mo|P/[M0W0O2]([C-8PxM0]$|C/[O-2P-1]p3|P-4p-8', 17)
p95 = parse('b-2w4p7u3(B/[RxC-xM0]B0$|UM/[PxB-1]|UM/[WxB-1]|UM/[WxPxB-2]|b=0p-(UR/P-x|UC/Wx|UR/[WxP-xM0]|UC/[WxP-xM0]', 24)
p96 = parse('n8B/[M6BN]n10c2(B/[WRGB]m-1P/[C2W0]p-Pxm-1|K/[C2P]m-1P/[C2K-1]p-c2N/[C2P]p-k|P/[C2K]N/[P-2K-2]C/[P2C2]P-2K-2U/[P0K0C0]$', 16) #Fix display
p9A = parse('w*|o*|p*|c*|w2op3c3(B-4$|W/[OP0C]C/[W0P-1C-1]P/[W0OC]b-1|C/[WOP0]P/[W0OC-1]O/[OP-1C]b-1|C/[W0OC]O/[W0OC]W/[P-1C2]b-1|P/[WOC]W/[OP-1C]C/[W0P-2]b-1|P/[W0OP0]O/[W0P-1C]W/[OPC0]b-1', 14)
p9B = parse('o|o2|o4|o8|o16|o32|o64|o128|c|c2|c4|c8|c16|c32|c64|c128|o256|c256|c512|B/[OxOxOxOxOxOxOxOxOxOxOxCxCxCxCxCxCxCxCxCxCxCxCxCxCx]B-13337B0$', 8, special='9-B') #Takes a bit (0.5 min)
p9C = parse('wo3p6k10c15b21m-9(W/Bx|B/Cx|C/Kx|K/Px|P/Ox|O/Wx|[BW0M0]|[B0K0C0W0O0P0U0]$', 27, max_stacks=2, special='9-C') #Takes a bit (1.4 min)
p9D = parse('p3u6(Uc-|Uc2|Uw|Uc-9|Up-|Up3|Uk-4|Up-4|Uk4|[BxM0][B-xM0]$|UxB/[WP0CK-x]Bxb-4|UxC6PKb-|U[MxMx]|UxB/[K4PxC-x]|Um', 12) #Takes a bit (0.5 min)
p9E = parse('#U/N0$|[KU0]n90n*[BU0]b-1|k16[KxKx]|b-2[BxBx]|m4[MxMxU0]|b-*[N-xN-xU0]|([B-xB-x][M2U0][K-xK-x]M-4W/[M0U0]|B2M6B2K17W/[M0U0])(K-9|b-*)|(B2N-8[KU0][K3U0]W/[K0U0]|B-2[NxNxNxNx][K-1U0]K4W/[K0U0])(W70|b*)', special='9-E') #Timeout
p9F = parse('o(W3$|{0}{1}{1}{0}{1}{1}{0}{0}{0}{1}{0}{0}{0}{1}w|{0}{0}{0}{1}{0}{0}{1}{0}{0}{0}{1}{1}{0}{0}w|{1}{1}{1}{1}{0}{0}{1}{1}{1}{1}{1}{1}{1}{0}w'.format('[OO]', '[O-1O-1]'), 29)

p101 = parse('W0z4oOz2(!C8$|zz8|W6R0C0|O8r|O2z2O4c4|W2w2W4c4', 9)
p102 = parse('w3c2(PPZC0$|WoWzOw|WoZpWo|WoWc*Ow|OO0C|WW0C', 10)
p103 = parse('w7o6B/[W0O0P0C0]$|C0O0P/Z16|O4O0Z|c6W/P0([ZZZZZZ]W4|OO0Z|p16P0|WP0|OC/O0)', 19, special='10-3') #Bridge special case
p104 = parse('mK0W0k6Z3Z3m2(w6|k10|b3|m-2U3[B0W0K0M0]$|WZBZBZu|WZ5K2Ku|BB5Wu', 17)
p105 = parse('B0p3n-4u|P-2n-|Cn*|Z-4|P3b-4u|P-3n-8|p-8P0b3|Z-8|U2U/[B0N0]$', 12) #Preservation
p106 = parse('w50u-7(U-2p*o*w-50|U-2o-7O-1n6|U-2o-4O-6O0P5|U-2p5P6P0O-4|U-2M-1m*n*z50|N0(Z50$|W0u-4m-1', 11, passing_effect=[7]) #Passing curse
p107 = parse('N/W6|M/W6|w6n=0|K0k51W/[M0N0U0CZ50]$|[KU0]M6c|[KxU0]c|z-m-', 12)
p108 = parse('o12O/[](W/[]O/[]C/[]|W/[](U64$|W20u20|Z4Z3u7|z24|z19|z9|Z8Z4Z3u15|O14u14|C8u8', 15)
p109 = parse('z17Z0Z0Z0$|Z/[O2P2]m|Z/[W2O2]m|w18O12Z4|p26P8Z16Z4|(K4W4|C4Z4|>)z*|(o10O4n10>|P4W8Z) ') #Timeout + one way drop issue
p1010 = parse('u4m-1m3M/[OxGxBxRxU0]$|U[Z-xZ-x]|U[ZxZxZx]|UZ/Mx|UZ/U|UZ/[OOOO]|U[NxN-x]|UO/[]R/[]G/[]B/[]|UM/[]N/[]M/[]N/[]', 30, max_stacks=3) #Takes a long time (5 min)
p10A = parse('Z|Z2|Z4|Z8|Z16|Z32|Z64|B/[M-1U]|uK[M-1U]|C/[M-1U]|m-3nn-2|u-1k43b92c5W/[B0K0C0U0]$', special='10-A', passing_effect=[0, 1, 2, 3, 4, 5], max_stacks=2) #Timeout
p10B = parse('(>m-1>|>k-1>|>c-1>)w*(m=0Z/W5[Z-5U0]$|n-|Ck*n=0Cw-*|Kc*n=0Kw-*|Mn*k4c4w5|N0|n2', 11, special='10-B') #Brown bridge special case
p10C = parse('c50b-90m-1m*(z-b-z-|[C10Zx]|[B-20Z-x]|O/[C0B0U0]$|n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10n10', 25, max_stacks=2) #Takes a while (1.6 min)

p111 = parse('c20cxi(C8|C8i)(K2iB-2iwxiW4$|k4(K2z*w4|C6ikxi|W0z*b2|C6ibxi|C6ib-', 12)
p112 = parse('bb-xi(B-ic2o-xi|B-ic2oxi|Cw2p-xi|Cw2pxi|Wbk-xi|Wbkxi|[BWC]o3p4k5(KPO-iK-ib|OiPKKib|PiOKK-ib|P-iKO-iPb|OPK-iPib|OK-iO-iP-ib|WCB$', 15) #Takes a while (1.7 min)
p113 = parse('r(rxi!C6U/[N0B0]$|rn30(C5B3R5c6|B5|K5W10i|K5b8|nxi|K5z5', 14)
p114 = parse('n7Z-100$|z50izxi(@G10iG10nxi|(g10|g-10)(@O2iz-50|Z/G0z=0|G2gxi|zxi|G2gxi', 14)
p115 = parse('o-17io-xi(m-2|O4O/W9i|O-5o-99|[W9W9i][O-9O-9i]$|([O-4O-4]|W/O-9wxi) ', 13)
p116 = parse('p12-8iP-+p99iPxp99PxP+(p1+1i|[PxPxPxP-+][P+P+P+][P-xP-xP+P+]|[P-+P-+P-+][PxPxPx][PxP-+P+P-x]|[PxP+PxP+][P-xP-xP-x][PxP+P+P+]|m-4)[P16P16i]$', 16)
p117 = parse('o3-5iO=(o-5+2i|O=o([O=O=O=]|[O=O=O=O=]|['+'O='*6+']|['+'O='*8+']|['+'O='*12+']|['+'O='*18+']|['+'O='*14+']|O2618O0$', 8)
p118 = parse('c6+4i(C4X1+1i|c-6C0m-2ir6i(R/C6i|!W0C0$|cxi|[C=C=]|C/R=|C2', 13)
p119 = parse('n-n-n-|n55+28iU/N0$|m1-2i|KN-8i|KN-32|K-4iN-16N2|K4iK-8i', 16, max_stacks=1) #Takes a bit (0.5 min)
p1110 = parse('m-1iu3+3iU0W0>M0[B-15B-7i]B0$|U(w=7i|B/WxUi)|U(w*|B/W+Ui)|Uw=20W5Ui|UW15W7iUi', 10)
p1111 = parse('m-3p18(P6|M0)(U/P0p6iU/P0p-6U/P0p-6iU/P0$|(mm-1im|m-1m1im-1i) ', 21)
p11A = parse('m-1m*o-6(O-1|W/O-x|R/O-x|G/O-x|B/O-x|>o=0-1ir-K/[WxR-x]K=K/[GxR-x]K=K/[BxR-x]K=g-K/[WxG-x]K=K/[BxG-x]K=b-K/[WxB-x]K=r-g-b-' +
    'k30K/[O-1iWx]C/[U0K+]K+K0k30K/[O-1iRx]C/[U0K+]K+K0k30K/[O-1iGx]C/[U0K+]K+K0m-*k30K/[O-1iBx]C/[U0K+]K+K0M-1C-15iC0$', max_stacks=2) #Timeout
p11B = parse('m99p5-6ic58-33i(mximximximxi|pxipxipxipxi|C/[PxP+]M/C0$', 25, max_stacks=2) #Full game only

pPt2 = parse('ow(OpBwPkCb|Wo(BWos|PkCbBB$|KcBwKc|OpKcWo|PkOpKcCb', 7, 15, salvage='W') #Demo only
pPt2f = parse('m2(C-6wK4l-3|k6(w-1#W0Kxk7B3|K2C/K6b3|L-3K8)|(K#B0W0|WsL-3)U/K0$', 7, 6, salvage='W') #Full game only
finale = parse('m2wp8((C2WPg-WOx|KWO-xK12c-12)b-u|W0C-2M0o=1(w(Wo=-1o=-1!C!Cg-5u|N-3O-xKWC8u)|mWO0O0M0(K4C2OxBP-6W!O0u|c4w2((#C2WP-1wG4B0|C2WPk17K12C3)ru|m2o=1W0C0C0O0O0O0M0c6b(p-|P6w2#O0u|m3K12BP-1w2o=-1(' +
    'P0B@O0u|k31O0O0M0m(RN-3B0g-5|(K4w2P-1@C@C|BG12Pn-99C)O0b2u|WWC4o=1M0m2(C0WOxKW0|PPC-12O0W0P-1P-1)(r-RGxWc-u|R0W0M0(o=1!W0G-xC0C0u|m5U10M0O0K0R0G0B0n92N0$', special='finale') #Put in for kicks and giggles, I highly doubt it will solve this!
graduation = parse('u(Z/[R2iO0G-6C0B4iP0W6]$|m=-1P/[]|m=-1P/[]|U(O|K|C)(O-1|K-1|C-1)(o3|o-32)(o254iu|P6i)|U(P0p-123|K0k4)(O0o10|P0p5)(K0k12|O0o3)k64iu|Ur=0g=0b=0(Cx|K+)c=2iu|U(R|G|B)(!O|@O|#O)c24u|Un3+7iN0un=1n=-1|' + 
    'U(P5|O-6)(g-k-|r-b-|o-)(p-u|n-)|U(R/K4|G/K4)(B/K4|P/R-1)(z*u|z-*)|Um=-1(m=-1|O3(m=-1|P123u))|UL/[R-1OGxCB-1PKU0]mxiL/[O0M0C0P0K0U0]u|U(K/[]|O/[]|C/[])(Zi|Z|Z-1)(Z/L6i|Z8)u|Ulxig-xib-xir-xig-xi|UW/L0u')

#Part 2
pt11 = parse('m-1(m*|r-10(c20(C/[K-xRx]|K3W/R-4K/W3|W8W/C0!M0$|r=0k8(r-R=W=K=s1|K4|R-2(C/WxW6C100', 15, 39, salvage='C100', max_stacks=2, special='T1-1'); add_edge(pt11, 2, 'R-8r-3', 5); add_edge(pt11, 3, 'C3', 5) #Salvage takes a long time ()
pt12 = parse('(oOx|o2Ox|o4Ox)(b6Bx|b12Bx|b18Bx)(c36Cx|c54Cx|c72Cx)L/[OxBxCxZx]L-63L0$', 9) #Takes a bit (0.5 min)
pt13 = parse('r*o-16|g10(O2g-R3p-2Zxg=0O-2|O/[]r3G2o5O-2p9@R0)G3s2|G0(G-xo-5!R0|R3g-@W0)(O2r-*!O0|G4p*P/[])@P-2$', 10, 7, salvage='G0')
pt13s = parse(pt13.level, 0, 9, salvage='G-x')
pt13s2 = parse(pt13.level, 0, 12, salvage='Zx')
pt14 = parse('nm10N0(N0N0N0N0m2(N0N0N0m3|N0N0N0N0(N0N0N0N0m8))|N0N0N0N0N0(N0N0N0m6N0N0N0(N0N0N0N0N0N0N0N0N0M|N0N0N0N0N0N0(N0N0N0N0N0N0N0m9|N0(N0N0(N0N0N0(N0m4|N0N0N0m4)|N0N0N0m(N0N0N0m2|N0N0N0N0m6|N0N0N0m5|'+
    'N0N0N0N0N0N0N0N0N0N0M5$', 21); add_edge(pt14, 2, 'N0', 4); add_edge(pt14, 3, 'N0N0', 5); add_edge(pt14, 5, 'N0N0N0N0N0>m5', 7) 
pt15 = parse('$|k-4|s3|K0r-12|R/K-4X1+1i|!R/K4X-1R0n4|R/Z-4R0n2i|R/K-4X-1-1i|R/K4N0n2i|m-1', 1, 13, salvage='R/K-4')
pt16 = parse('w(Wn4C|Wc-2!R|Wn2C-1)N0$', 6)
pt17 = parse('p4(wP/C-xC/Px|wC-4P/C-xP/C-x|wP24P/C-x|P2C/Px|PC/Px|wP8C/PxP/C-xC/Px|PxP/C-x|C-xC/Px|C-2P/C-x|wP400$|>(P0C0L0|P7C-7W0s4)', 12, 12, salvage='L0', special='T1-7') #Takes a while (1 min)

pt21 = parse('s5|u(O/UC/UP/UK/U|C/UK/UP/UO/U|C/UP/UO/UK/U|O/UP/UC/UK/U|cU/C0cU/C0cU/C0cC0cu|kU/K0pU/P0oU/C0kU/O0cu|pU/P0oU/O0cU/C0ku|oU/O0kU/K0cU/C0pu|U4U/[O0P0K0C0]$', 10, 10, salvage='C0')
pt21s = parse(pt21.level, 10, 10, salvage='U4') #Takes a long time (6.5 min)
pt22 = parse('rm(R0R0U/RR0R0|B0B0B0B0B0|G0G0G0G0G0)(z5+1iZxMxRw5|ZxG5Zxm3|b3#B0W0b3#B0W0b3#B0W0W/MW/MW/MW/MW/M@M/W0U-1M/W0$', 18)
pt23 = parse('$|s6|k8n8m-8(#N0n=0#B3X8+2i|[M-2M-x]X1+99i|N/K8b|mxib|N/M-8b|M/K8', 1, 0, salvage='B3') #Timeout
pt24 = parse('e11(E5n5P5mE-5w12|E/W5n24m-1U/N0w3|[E0E0MM]w5ExE12w4|[W24U0E0]$', 12)
pt25 = parse('$|m-1l-1((L-1s=7k3|L-1p-3Kx)(K-xp6P-2|P0k-K-2)L0s=8(L/P6|L-6)|(K2k-2K0|P-2k2s=7l-4K/P2)(K-2L-1s=7L-1K2|P4k6Px)(R2X-1K=|L-1P/K-3P/K-3', 1, 12, salvage='K=', salvage_id=7)
pt25s = parse(pt25.level, 1, 19, salvage='L-6', salvage_id=8)
pt25s2 = parse(pt25.level, 1, 13, salvage='K=', salvage_id=8)
pt26 = parse('wo-1m-1m*(O/Wx|W/O-x|m-*(M-1W872O-383L/[W0O0]$', 0, max_stacks=2) #Takes a bit (0.5 min)
pt27 = parse('u-63P-6s=9[RxRxP0]|u-42P-3s=10[GxGxP0]|u-25P-3s=11[BxBxP0]|L/[M8M-8]$|p-1P/U-1(P/Cu|P/Cu2|P/Cu4|P/Cu8|P/Cu16|P/Cu32|cC>[U0P0C0](m64U-67n', 14, 14, salvage='[RxRxP0]', salvage_id=9); add_edge(pt27, 0, 'M63', 2)
pt27s = parse(pt27.level, 0, 11, salvage='[GxGxP0]', salvage_id=10); add_edge(pt27s, 0, 'M63', 2)
pt27ss = parse(pt27.level, 0, 11, salvage='[BxBxP0]', salvage_id=11); add_edge(pt27ss, 0, 'M63', 2)
pt27sss = parse(pt27.level, 0, 18, salvage='L/[M8M-8]', salvage_id=9); add_edge(pt27sss, 0, 'M63', 2)

pt31 = parse('U>(wo10p100|%S12|P-314P0$)|U(Wc|%S12(Cc-2|wo-4(C-6$|O0(c-|[C-xC-xC-xC-x]))))|u(U(%S12wO/Wx)|U%S12(oOxo-1|cO-4|C-1w3|%[CxCxCxCxCxCxCxCxCx])|s12', 24, special='T3-1')
pt32 = parse('s13|w5L/W3K3[W0M0]k=0|[W0K0L0]l-1W/L-xl-[K-xK-x]|k1i(L-xk-*[WxWx]|W2k*K/Wx)|%W0k1i%K0>k1iw=-1m(%S13|M0S13$', 16)
pt34 = parse('u36(U2s=15|[GGG]m[G-1G-1G-1]|g|[GG-1]U12|[GG-1]s=16|>(UU12|S16S15U0$)', 18)
pt35 = parse('<m99$|s=17s=18s=19s=20|m-1w99&W19o37&O12S17P0(mp-32o-c-3&W30&O-4&S18K/Wxw11&O-12G/C-3(m&W15o-C-3&S19&O6z=0&[WxK-xK-x]m(&W44w-26O3S20C-xO0O0O0&P-8@W/[]&U/[M0W0C0P0]s=21W0', 1, 0, salvage='W0', salvage_id=21, special='T3-5') #Timeout
pt36 = parse('c-10|c-10i|[C-10C=]|m-1im1im-1mc-M0mm-1u-1c=10(c=-10+10i(M-1($', 20, special="T3-6")

pt4W = parse('e11w80l-1i(W2|W3|[W=W=W=][W=W=W=]|[W=W=W=][W=W=W=]|W10|W30|W1000W0$', 6)
pt41 = parse('w10o10p10k10([O=O=]|m-1C/[W=O=P=K=]L/[W0O0P0K0]U4C$|K2O2W8P5u|PK2O4K2u|P4KOu|K3O2OW2u', 13) #Takes a bit (1.5 min)
pt4R = parse(pt4W.level[:-1]+'|s22|w-35k5r10W0(w2n-|(WR6W|WK4W)(N/W|(WK4W|WnKW)(WR2K2W|WR8W)(WR2K2W|WR4W)R3N/[K0R0W0U0]$', 17, salvage='N/W')
pt42 = parse('e11(S22|s24|B20$|O/B-1|[Z=P=]|B/Z0|B/Z8|[Z=P=]|O/B-5|OC/[B-2O2]|B-3P/Zx[O-xO-x]P/Zx|Zx[OxOxOxOx]|L-1$', 14, 8, salvage='[OxOxOxOx]', salvage_start={22:'E'})
pt42s = parse(pt42.level, 0, 8, salvage='[Z=P=]')
pt43 = parse('L-1i|m-5iM0(m|s25(C/[WRGB])|[W=W=]m[P=P=]X0-1il3U/L0$|[O=O=]m1i[R=R=]X0+1im-1[G=G=]X-1m-1i|[B=B=]X0+1im1i[K=K=]X-1m2w-1', 15, 11, salvage='[B=B=]')
pt43s = parse(pt43.level.replace('L-1i', 'N/W'), 0, 17, salvage='C/[WRGB]', special='T4-3')
pt4B = parse('[B=B=]|[OxOxOxOx]|o10b-10(BxO/B-7B-x|[O=O=]O30O/B-2)(O/B2O-8B2B/O3|B/O2B4B/O-7|o-b-o-|o*b*o-*b-*|O/B6O-5O/B2B3B/O20|B/O4B-2B/O-6O/B6|O/B-12O-2O5O/B-8|B-50O40$') #Takes a very long time (20 min)
pt44 = parse('p-10m-20(K/P-1|K/P-10|k*m=0G/K33P/G=m-1m*p=10P/[K=G=U0]Pxg-P/[K=G=U0]P-10p7P0P/[K=G=U0]p80Pxp30P/[G=U0]P-xP/[G=U0]P-5p3P0P/[K=U0](P-2|P-4|P-8|P0$', 43, max_stacks=2)
pt4L = parse(pt4W.level[:-1]+'|L-1i|[E=P=]|C/[WRGB]|P/L-12|L0L0L0(rgb[C-4U0]l-12W256wxiW0p-|[E12U0]$', 16)
pt45 = parse('p-Z3|u1+1iS22|l6(L0s27|p-5Z3|l274iL137iL0$|[PPPPP](Ul-6|U0$', 5, 6, salvage='[PPPPP]', salvage_start={22:'L0'})

p02 = parse('w8(O8w8|W8w8(W8o8|W8p8(P8w8O8w8W8o8p8|P8o8W8p8W8o8O8w8O8P8$', 11)
p05 = parse('w500r30b10l=140o=65p=-15m-1m*k1iL/[RxP-xK1i]lxim-*m=2M/Lxl-xi[L-+U0]([O0U0]o=-1|([L0U0]|[L-xU0])(O/[BxU0]|[O-xU0])(W/Ox|[M0W]$', max_stacks=2)
p06 = parse('m-1l-1m*(C/L-x|>(K/Cx|>(P/K-x|>(O/Px|>(W/O-x|W1000000$', max_stacks=2) #TImeout

pomegaO = parse('c100C0|S1|z*|g3G0|S2|k-4|!K-4|S3|Z-8|l-1l-1l-1l-1l-1l-1l-1l-1|W4$|K-50K0|[WOPCKRGB]', 3,
    salvage_from=[pt11, pt13, pt15, pt17], salvage_start={1:'C100', 2:'G0', 3:'R/K-4', 4:'L0'}, omega='w')
pt21m = parse('s5|u(O/U|C/U|K/U|P/U)') #Timeout v
pomegaP = parse('m-1U/M0|S5|(<|#U/B0|[C-8U0])(b18u4[U0B0]|S6S6S6S6S6)|r5|g5|b1+1i|S9|S10|S11|k50U/K0k-50(u-4|U/K0l-6U/L0)|S7|S8|U/OU/O-1U/OU/O-1U/O$|U/C-999999999|L/[R-xG-xB-xO-xU0]',
    salvage_from=[], salvage_start={5:'O/U', 6:'B3', 7:'K=', 8:'K=', 9:'[RxRxP0]', 10:'[GxGxP0]', 11:'[BxBxP0]'}, omega='wo', max_stacks=2)
pomegaK = parse(pt31.level, 10, special='T3-1', salvage_start={12:'O-4'}, omega='wop') #Takes a while (2 min)
pomegaC = parse('c100C0|S1|z*|g3G0|S2|k-4|!K-4|S3|Z-8|l-1l-1l-1l-1l-1l-1l-1l-1|W4|K-50K0$|[WOPCKRGB]',
    salvage_from=[pt11, pt13, pt15], salvage_start={1:'C100', 2:'G-x', 3:'W/K-4', 4:'L0'}, omega='k') #Takes a long time (3.4 min)
pomegaN = parse('m-1U/M0|S5|(>|#U/B0|[C-8U0])(b18u4[U0B0]|S6S6S6S6S6)|r5|g5|b1+1i|S9|S10|S11|k50U/K0k-50(u-4|U/K0l-6U/L0)|S7|S8|U/OU/O-1U/OU/O-1U/O|U/C-999999999$|L/[R-xG-xB-xO-xU0]',
    salvage_from=[pt21m, pt23, pt25, pt27], salvage_start={5:'O/U', 6:'B3', 7:'O/W=', 8:'O/W=', 9:'W/[RxRxP0]', 10:'[OxGxP0]', 11:'[OxBxP0]'}, omega='okc', max_stacks=2)
pomegaL = parse('c100C0|S1|z*|g3G0|S2|k-4|!K-4|S3|Z-8|l-1l-1l-1l-1l-1l-1l-1l-1|W4|K-50K0|[WOPCKRGB]$', 3,
    salvage_from=[pt11, pt13, pt15, pt17], salvage_start={1:'K/C100', 2:'K-x', 3:'W/K-4', 4:'L0'}, omega='wopkcn')
pomegaG = parse(pt42.level, 3, salvage_start={22:'E'}, omega='wopkcnl')
pomegaB = parse(pt45.level[:-1], 7, salvage_start={22:'B-3'}, omega='wpnl')
#pomegaR = parse()

salvageSources = [pPt2f,pt11,pt13,pt15,pt17,pt21s,pt23,pt25,pt25s,pt27,pt27s,pt27ss,
    pt31,pt32,None,pt34,pt34,pt35,pt35,pt35,pt35]

#Unused levels
x11 = parse('p|Pw|Op|Oo|Wo|OpWwOpc|PoPoPc|CC$')
x12 = parse('o|O(COW$|WOco|wOoWc)|Oo(Wo|WoOwCwoCwc)')
x13 = parse('w15|(W3W4W6W2|W3W4W3W6|W4O2W4W2|W6W4W6)$')
x14 = parse('k311|(K70K84K62|K65K54K65|K38K96K97|K75K45K92|K52K82K42)(K28K61K99|K57K41K52|K82K62K84|K35K48K52|K36K57K69)$')
x15 = parse('W6o2w3W6o2w3O6o2o2w3C3$|w12W6o2w3W6o2w3W6c|O6o2w3W6o2w3w3O6w3c|W6o2w3O6o2o2w3W6o2w3c')
x16 = parse('o|WWW$|Oppp|OoPkPcKkCw|OcCoKcPcCw|OpCoPkPpKw')
x21 = parse('W2O3N$|Om|m|W2m|W2w2Nm2|O4o4|O4m')
x22 = parse('w9m2(W4|W3W2)(W2W2|W6W|WW3W)(W4W2|W6W)W2W2$')
x2A = parse('c2m3(>C3C3C3C3C3C3C3C3C3C3C3C3$|C4c5|C8c4|C2c4|C3c2|Cc5|C8c8|C3c4|C2c6|C4c6|C4c5|C5c7') #Takes too long
x23 = parse('w3|w6(W6WW0$|O2w2|W3w3W0W3ow3|W3w3W0W3ow3|(OW0WW2WW0O|) ')
x24 = parse('o6|O6c6C3o6|P3p3C3o3|P3o3P6o3|O3c3C3O3p3|O6c3O3p6|O3o3C6c3p3|P6O3$|O3P3C3m')
x25 = parse('w2(O2W3o|W2w4o2|W2O2w4o2|W4w2W4(O8O0WW0$|W2o4W2|O0o2w10|O6o8W4W2')
x31 = parse('w23o25(W12Ox|O12Wx|(W5OO6|W8WO5|O5W5O5|O5W8)W0O0$') #Cheese
x32 = parse('WW0w=1W2W0WW0w=1W2W0$|w2(W0w2W2W2|(w2w=1w2|W2W)(W6w=6|w4|W2w2W')
x3C = parse('w3k7(WxW0k6|W2K12|K6|K12k24K3m|K3k=7K6w|K2k6|W2k6|W0W0K3K|K0K0K3K3$') #Cheese
x3Ci = parse('w3k7(WxW0k6^|W2K12^|K6^|K12k24K3m^|K3k=7K6w^|K2k6^|W2k6^|W0W0K3K^|K0K0K3K3$')
x3D = parse('m3((m=0Oo2CcOm=0|m=0k4m=0|) |W2m=0o|Cw2|CcWNKW0O0K0$|m=0CcC0O0o3|K2wO3K') #Cheese
x41 = parse('w6m|Oow3|W2Cr|!W6R$|W8oWOc')
x42 = parse('Gpp|@Pg@P0@G0$|pg3G5|G4g5|PGg2')
x43 = parse('m|Bxb2|#B4b6|B3b3|#B0B6m|#W$|B2b3|b=0Bb2')
x44 = parse('mMm3M2(M6M0$|W3w8W2m2|W8m|c12C0Cxm|M2(C6m2|C8cm|C4mM4m7')
x45 = parse('ok(Oxo|Kxk2|K3o|W0p4|o=0Oxo2)|O3kopcm3|Kk2P2P2W2W2(M0M4$|KM0K0m|CM0C0m|OM0O0m|PM0P0m')
x4B = parse('mrb3g5(Rg=4b=2r=1|Gb=2r=0g=5|Br=0g=4b=3|Gx#BxBGxBB0#R@GxB0m2|!R0@G0#B0m2|(G5G0>|m=0R0B0G0R2B3)!@#M4$') #Takes a while
x4C = parse('m14(M0P0K0C0$|P2p18M4C3W4K2|K2k14K3C5P8K8|C2c12P4W2K4C4|pW8m|P4|P8') #Takes a bit
x61 = parse('b8|BxB-xBxB-xBxB-xBxB-x$|B2(b3(B2B-2b-4))|B4b-5B0B3(b4B4B0b-3B2b4|B-4B0(B2b3|b6(B2b3|B-4B0(B4b4B2b-9B-5b12|B4B0bB2B-3b-5'); add_edge(x61, 1, 'B2', 3); add_edge(x61, 2, 'Bx#B-x', 6) #Takes a while (3.5 min)
x62 = parse('GxG-xGxG-xGx@G-x$|G2g3@G3g-6@G0g6|g6|@G0@G0@G0@G0@G0@G0g-1|G2g3@G0g-3G3|G2g3@G0g-3G3|G3g2G-5g6|G3g2G-5g6|G3@G0G-3@G0g6G6')
x62i = parse('GxG-xGxG-xGx@G-x$|G2g3@G3g-6@G0g6^|g6|@G0@G0@G0@G0@G0@G0g-1^|G2g3@G0g-3G3^|G2g3@G0g-3G3^|G3g2G-5g6|G3g2G-5g6^|G3@G0G-3@G0g6G6^')
x63 = parse('u-5U-6$|!N-4@G0R12B6$|!W5b2G2gB3uR-2b|K3n8N0g2!Gxr-2b|M2gG0b2Rx|U-1r11G2BB0Gxu-5|G@Pn-4B2u|C8g2U-2U0b6|U-5m6@R2u-1|#R0@O0B0um')
x63i = parse('u-5U-6$|!N-4@G0R12B6$|!W5b2G2gB3uR-2b^|K3n8N0g2!Gxr-2b^|M2gG0b2Rx^|U-1r11G2BB0Gxu-5^|G@Pn-4B2u^|C8g2U-2U0b6^|U-5m6@R2u-1^|#R0@O0B0um^') #Possible intended solution, takes a very long time (20 min)
x9 = parse('g-5([N-xGxU0]m|[NxG-xU0]m|@M50@G-5U/[M0N0G0]$|[N-xN-x]|[GxGx]|G/N-5|N/G-5|[MxMx]g5|[NxNx]n5')
x10 = parse('w5W5(Z5$|n2(n-1|R(Gn|Zp(Wp5|Kw5|Pk5')
x111 = parse('w3(w2iW/C-i|WiW(w1i|C/W2i|c-|C2iW3i$')
x112 = parse('p4+3i|p-1-2i|[P4P3i]([P1P1i][P1P1]P0$|[P-2iP-2i][P-1P-1]|[P-1P1i]|[P-1P-2i]p8+1i|p')
x113 = parse('k4+7iK+k3iKxk-K-+k10+10i(K0$|(k-30+25i|k3+13i|k-2-2i)(LK+|(k10|k-50+50i|k-5i|l)(LKx|k2-30i|k-5+6i|k1+1i')
x114 = parse('w5+2iwxiwxiwxiwxi(g-5@W0$|WW/P=|P-+gxi|P-1pxi|W-+gxi|(P/W+w-xiP/Wx|) ')
x115 = parse('rrrrrrrr|rxirxirxi|>RR-ic6(Cr-xiC|CrxiC)R-1R-1(Cr-C|CrxiC)RRi(Cr-C|Cr-xiC)RR-i$')
x116 = parse('l-1M-1(L-1u|m2)|U5$|M3u|n-|M3u|nxi|[N10UL-1]u|m3([GxGxG12GxGx]n10|L/U3(M3u|nxi', passing_effect=[1, 4, 6, 12])
x117 = parse('c6+4i(C4X1+1i|c-6C0m-3ic-15(c-xi|cxiC0$|C2|C-1|C8|C-4i')
x118 = parse('nn-n-|u*(W/[K7K7i]u|[W0N0M0P0U]$|m-3M/P=u-*|p|k7+7ikikiki|pxipxipxip=0') #Cheese
x11A = parse('[N=N=]|m3+3i([C=C=]|U/MxU/M+U/M-xU/M-+U/MxU/M+U/M-xU/M-+$|(n3|c3+3i)(M/C3|M/C-3)', max_stacks=1, special='11-AX') #Takes a very long time (35 min)

#Keypick 100
k13 = parse('wwOOU5$|Wou|Wwu|Wou|Ww(Owu|Wou') #Bonus
k14 = parse('w(P$|Ow|Wo|Op|Wc|Ol|Ww')
k15 = parse('w(WW$|WwOw|WoWww')
k16 = parse('w|WwwOww|WpwWoc|WWW$')
k19 = parse('ww(WwOp|WoOw|WwPo|WpPw|PP$')
k20 = parse('w|Wo|Wp|Op|O(o|W$|Ol|Pw|Po')
k21 = parse('ww|(WwWWwOOwO|WoWoOOoW|WWwWwwOO)$')
k22 = parse('w(WpPoOU6$|OwPpWou|WwOoPpu|WwPoOpu|OpWoPwu|PpOwWou|WoPpOwu') #Bonus
k23 = parse('wog(WOOoog|WWGwww|WGGwwg|OGGwwo|OOGggg|WOGogg|WWOwgg|WWWwoo|GGG$')
k24 = parse('w(P$|Wo|Ow|Ooo|Ooo|WOWp|WwOw')
k25 = parse('OOwwWg|w|WWgoWg|w|OOwwGo|GG$|WWgoGo')
k27 = parse('OpPpGoGgPP$|o2w|GGp2OGo2Wp2|OOg2|OPo2PPg2OOp2') #Bonus white door skip
k30 = parse('w|Ow2|O4w6|Wo2|O3w4|W2o4|W6$')
k32 = parse('w4(W3oW3$|W2wO3w5|W2w2W2w3|W2wW2o2|W2w2O2o3|W2w2W2o|W2w2O3w3')
k33 = parse('wWw2W2w4W4W2w7|Ww3W3w5W2W3W2w8|Ww2W2w6W6W2w9|WW2W3W4W6$')
k34 = parse('w4w4w4w4|(WW3W2WW3W2WW3W|W2WW4W4W3W4|WW2W3WW3W2W4|W4WW3W2W4W3)$')
k35 = parse('w4|W2O2o4O2O3w5W6o3w3O6$|W4o4W2O2w5W2W3o3w2|W4o2w2W2W3o5O3W3o6|W4w4O4w4O2O3w6')
k36 = parse('w6w6w6w6w6w6(W6W4W8W6W4W8|W8W6W8W4W8W6|W4W8W6W8W4W8|W6W8W6W6W8W6)$')
k37 = parse('o9o9o9o9(O8w8|O3O4w6|O6w6|O2O3w4|Ow|O2w2|O3w3|O4w4|O12W24$')
k38 = parse('w2|OGCw2OGCkW$|W2g2W2o2G2w2|G2w2O2ogcO2g2Kw|W2g2W2o2G2ogc')
k39 = parse('w2|G2g2K2k2P2p2C2$|WkKoOpPw|WcCkKoOw|WgGcCkKw|WpPgGcCw|WoOpPgGw')
k40 = parse('w6W6cC6cO6cC6$|W6cw6o2O6co2C6cw6o2O6w6o2|W6cc6o2C6co2O6cw6o2C6w6o2|W6co6o2O6co2W6cc6o2W6c6o2')
k41 = parse('w(W2w3|Ww2|W3m|K$')
k42 = parse('m|GKRNB$|Wm2|Om2|Pm2|Cm2')
k43 = parse('o8m|(O6|O3O3)(O2O2|O6)(O4|O3O3)$')
k44 = parse('Cc2|Cm|cCCc(Cc2|Cm|C2c(Cc2|Cm|CC6C$')
k46 = parse('m|W2P2m|W2O2m|O3o4|C2m|P2g2o|G2o4w4|W4O4c2w2(W3O3$|W2K2w3|C2p2|G2k2o')
k47 = parse('o6|O6mW6mO6mW8O8$|W8mO4w6O6w6O6w8|O4o4O6o6O8o8W6o8|O12w6W6o6W8mW6o8')
k48 = parse('m(RoWpOgWgOmK|OgPwWoPwG|GwGpWmC|PmRmG|BwCmW)(m|BwKoCpKgBwR$)')
k49 = parse('w7w7m3((W4W2W2|W24W3)(W4|WW)(W2W2|W6)W4W2W2|W3W3W3W2W2W2W2W2|W24W3W3W3W3W3W3)(W2W2W2W2|WWWWW)$')
k51 = parse('w2(W0OCwW0$|Wo|Ww2|Wc')
k53 = parse('w4(WW6|WW2(W2W0w4W0w4|W2W0w4W0w4|W2W0w4W2W0w4W0W8W0W3W0W6W6W0W2W0W8(w4|WW0$'); add_edge(k53, 1, 'W0', 3)
k54 = parse('w2o2(W2W0o2|W2O2w4|W6w3|W2O2o4|O8o|O2O0w2|W0w2|WW0o6|OO0$')
k55 = parse('w2m(O4w2|W0w4W4o4O0w2W0(o2(O6w4W0w2O0w2W0$'); add_edge(k55, 1, 'W6', 4); add_edge(k55, 2, 'O0w2W6w2W0o2', 4); add_edge(k55, 3, 'W4o2W0w2O0w2W6', 4)
k56 = parse('wocm(W0wCwOw|W0oOoCw|O0wCoOw|O0cWoOcCw|C0oWoCwCw|C0cOcOcOw|W6W3>W0O0C0$') #Takes a bit
k57 = parse('W0cO0wC0wW3k|O0oC0oW0cO3k|C0cW0oO0wC3k|K3$')
k58 = parse('PPPPPPPPP$|cwom4(C0W0cO2mW0oO0wC2mO0cW0Wp2|O0C0oW2mC0wW0cO2mW0oC0Op2|W0O0wC2mO0cC0oW2mC0wO0Cp2')
k59 = parse('o3(O0O3o3OO0$|O3o3O12o5|O0o3O0o3|O0O3o3O0o3|O3o3O6o3|O6o3O0o6|O6o3O3o6|O12o6O3o5|O0o3O12o6')
k60 = parse('w4o4c4m(WO|C2)(WCO|W4)(WW2O2C2|O2C4|W24C)(WOC|W2C2)(OC|W4)W0O0C0$')
k61 = parse('o|!O$|Oo2|O2o3|O3or')
k62 = parse('m|!O$|OOor|Wo2')
k64 = parse('r|Wg|Pk|Rw|Gp|Ro|Gl|!K$')
k65 = parse('c(!P0cRc|CoP2r|!O0o!O3r|!C0oRc|!C0pRc|CpOr|C0o!C3$')
k66 = parse('R|r|R0R0R!R0R0R$|!R0r!R0R0r')
k67 = parse('Rm!R0!R0!R0!R0!R0!R0!R0!R0$|m(!R0m!R0r!R0mRm|!R0m!R0rR|RrRrRm')
k68 = parse('g|@W0$|G0g|W0w|Gg2|Wg2')
k69 = parse('m|!C@W$|Wc2|Rg5|Cw2|Cr')
k70 = parse('C0R0g|!C0@C0(g|!@C0$)|@C0(C0r|!C0g|G0(!C0Rg|!@C0()|C0C0(!C0g'); add_edge(k70, 0, 'C0', 4); add_edge(k70, 1, '!G2', 4); add_edge(k70, 4, 'C0', 5); add_edge(k70, 1, 'C0!G0', 5)
k71 = parse('g3(G3gG0g2@G0g2|@G0@G0@G0$|G0gG0g2|G0gG0g2@G3g|@G0g2|G3g2@G0g2G6|G3g2G0gG6')
k72 = parse('G0g2G2mG3g5@G0mG3g3G2mG6|mG0g2G3mG2g5G3mG2g3@G0mG6|G0g2@G0mG3g5G2mG3g3G2mG6|@G0@G0@G0@G0@G0@G0@G0@G0@G0$') #Takes a long time (3 min)
k73 = parse('b|#G0g|B3g|Bb2|B2b3|G2$')
k74 = parse('#W3G3$|m(B2w2|W2g2G0g2|B0g2|@W0w2G6m|@G0b3|G2b2B2g2|G2b2')
k75 = parse('G3r@R0g2@G3b#G0g2!B2bRg2@B2b@G0B0$|R0bG0g2!G3rR0b#G0bR0g2G3g2|B0g2Rg2!G3b#G0bB2g2!G3bB2g2|G0b!B2g2RbB2g2R0bG0rG3g2')
k76 = parse('B0mB3b3#B0mB3b3|B3b3#B0mBb3|B3b3#B0mBb3|#B0#B0#B0#B0#B0#B0BB0$')
k77 = parse('m4|@M4m4#M6g!M8$|!M8m6B3m2Rm4|#M4m6|G6m6G6m2|M4m2b3|M4g5|G6m4r')
k78 = parse('m2(W4m2!W6m2!W0m2|M4m2!W0m2W6m2|W4m2M6m2!M6$|W2W2rRm4')
k79 = parse('m4|m5|m3|M0WW4W6W3W2M0$') #Bonus
k80 = parse('M2M8$|m4|M2gB0r@M0b#G2m2!B2bG2gRm3|M2gB0bM0r#G2m2!R0b@B2gRm3|M2gB0rM0m2!G2b@R0g!B2bRm3|M2gB0b!M0m2#G2r!R0bB2gRm3')
k81 = parse('c9c9c9c9((c-5c-7c2|c-3c-8c|c-5c-6)(c-7c|c-3c-4|c-6)C24$|(c-3c-7c2|c-3c-4|c-9c|c-8)(c-4c-6c|c-1c-3c-4|c-3c-82|c-9) '); add_edge(k81, 5, 'c-3', 3) #Takes too long
k82 = parse('c-4|O8o8C-8c-8O8$|C-4o4O0o2C-8o8|C-4o4O0o2C-4o4|O4c-4C0c-2O4c-2|O4c-4C0c-2O4c-2')
k83 = parse('c4|C8c8C-8c-8C8c8C-8$|C4c-4C0c2C4c-4|C4c-8C-4c2C0c4|C-4c4C0c-2C-4c4|C-4c8C4c-2C0c-4')
k84 = parse('m|P8p8C-8c-8C8c8P-8$|C-4p-4P0c4P8p-8|C-4p4P4p-4P0c-8|P-4c-4C0p4C4c8|P-4c4C4c-4C0p8')
k85 = parse('r-4(R-8r-8P8p8R8r-8P-8$|R-4r-4!P-4p-4P4r8|R-4p8P4r-6P4r8|R-4p4R0r-6!R-4p8|R-4p-8P-4p4P8p-8')
k86 = parse('m(M8!R0$|R6r-6|!R0m3|RRm3|R-6r-6|M4r6m6|R-4m|M2r2|R-2m')
k87 = parse('b-6|B-8b8B-8b-8#B-8$|B-6b-4B-4b6B-8b-4|B-4b-6B-6b4B-6b-8|B6b6B4b-4B4b-6|B4b4B6b-6B4b-6')
k88 = parse('m@G0@G0@G0@G0@G0@G0@G0M2$|@G0g6@G0m2M4m5|G-8g-4G-4g4G4m2|G-6g6G6g-6G-6m2|G-4g-8G-8g8G8m2')
k89 = parse('m|M3mM3$|B-2c-3R-2m|G-2r-3B-2m|G-2r-3C-2m|C-2g-3R-2m|R-2b-3G-2m|B-2c-3G-2m|C-2g-3B-2m|R-2b-3C-2m') #Takes a bit (20 sec)
k90 = parse('mK2(g-8r-4rWm2)|P-8m2(Mc4|W24g8w3|G0R8mG-6(C2G-2o-3m|G3B-2g2m2|m3B3O0C2M0o3m3(!G3l|O12r|C0NKmW2R-4G-2mO0GM0!WP0b-2Cm2R(G6m3|B@W0LR0m4|M12$') #Takes a very long time (15 min)
k91 = parse('p4|P-8c-4P-8c-4P8$|P/C4p2C-4c4P0p2|P/C4p-2C4p-2P/C4p|P4c4C4p2C0p|P4c4C0p2C0p2')
k92 = parse('c4(P/C4p4|C-4c8|P/C4c4|C-4p8|C/P4p4|P-4c8|C/P4c4|P-4p8|C24$')
k93 = parse('c-4(P/C-4c4C8p-4P4c2|C/P4p4P-8c4C/P4c-4|P8p-4C-8c-4C-8c2|C-8c4C-4p4C8c-4|P/C4C/P4C/P-4P/C-4P/C4$')
k94 = parse('w4|R/W6R6R/W8R0W4$|R-8r-6W/R-8r4!W8r2|R/W4r4R0r-2R-4r4|W/R-4r-2!W6r6W/R-6r2|W4r4R8r-6R-6r4')
k95 = parse('RR0BB0CC0g2GG0$|B-2c2R-2r2C0b-2G-2c2!B2g2R2c-2@R-2R|G0c-2C-2g2R-2c2!R0c2#G0b2B2r-2R0B|C0b-2B-2g-2C2b2!C-2g2@B0b2C2r2#G2G|C2r-2R0r-2R2b2G2g-2B2g-2G-2r2B0C')
k96 = parse('wwww|oooo|cccc|kkkk|L/[OCK0W3]cw-3|L/[W0CKO3]wo-3|L/[C3KO0W2]oc-3|L/[K2C2O2W2]kk-3|L-8L-8L-8L/[W2O2C2K5]$')
k97 = parse('m(L/[O0W2KC3U0]mL/[W0CKO3U0]mL/[W2O2C2K5U0]|Wk2Ok|Oc3Ww2Ck-1Wo2Ww-3Kc2|CwKc2Ok2WoO0cKw2|Ko2W0o2Wc-2C0o-1Ok2|Lw4Kk2O0kW0c-1Cw2|L-2L-2L-2L-2L-2L-2L-2L-2$') #Takes a bit (22 sec)
k98 = parse('m|[B-2R-2G-4U0][G2R2B4U0][B2R2G4U0][G-2R-2B-4U0]M8$|L-8b2G0r-8G4g-2G6m5|G-4g4B-4r-4G-4g6#R-4m5|G4g-8R0b-6B4r6!G-6g4')
k99 = parse('w3(CkPgGbGcRpBG|OpBgCgGoGrB|G0cKbOrGgBk|C0oPgGbGcB|O0gBgBgGo|GbKgRgGr|!Wb#Wg@Wb|[L0R0P0B0K0O0G0C0W0]$')
kex1 = parse('g(OoGoGgOgOoGggOGoo|GGo|OgGoOg|OoGo|GoOg|GGG$|GGogOOggOo(OgOoOg|Og|GoGoGoo|OgOgGoo|OoOgOg')
kex2 = parse('p(GpGOggPPoGGpOO$|PgGpGp|OgPgPpGgPOo(GpOpg|PgOgPo|PoGgo)|PpGp|GpGgPpGpGgPpGoPg|PgPg|GgPpGgPpGoPgPpOpp|OgPo|OgPpGpGoPgPoGpOpo')
kex3 = parse('Go(PgOgGpGo|OcCCpPPoGGcPPpOO$)|cGpGcPgPcOgPcO(PgOcGpc|pPoGpCpp)|CoPgGcCgGpGpGo|CgPgOpGpGgOoPc|PgCoCpGpOgCoCgOg(PcCoo|PoCpp|PcOgg)')
kex4 = parse('(OcCgGoCkK|KoPpPoCpG)(CgOoGgPpKgk|PpGgOoCo|(CoP|gGcO)(KkGOcc|gPCGO$))|(kOpGcOpGcO|KkPgCpGgO)(KcPcGpKgCpo|pKpGoKgPgCpc)|OoCpPcGoOgPgGgPcOoPGkk')
kex5 = parse('W(oGpOgPoOcPw|OgPoGkKpCgG(OoGWco|pKKK$))|(wCkOkCgPgCcKwO|WcKwGpCcGgPpK)oCkWkCcc|(KcGcKoOpOoCk|CkCwOpGoPcK)PpOoGgWgo'); add_edge(kex5, 3, 'WkCkCgOpPgGkP', 4)