from constants import TILE
from entities.wall import Wall
from entities.coin import Coin, PowerPellet
from entities.portal import Portal

def load_level(path):
    walls, coins, power, portals = [], [], [], []
    player_start, ghost_starts = (0,0), []
    with open(path) as f:
        for r,line in enumerate(f):
            for c,ch in enumerate(line.rstrip("\n")):
                x,y = c*TILE, r*TILE
                if ch=='#':
                    walls.append(Wall(x,y))
                elif ch=='.':
                    coins.append(Coin(x+TILE//2,y+TILE//2))
                elif ch=='*':
                    power.append(PowerPellet(x+TILE//2,y+TILE//2))
                elif ch=='P':
                    player_start = (x+TILE//2,y+TILE//2)
                elif ch=='G':
                    ghost_starts.append((x+TILE//2,y+TILE//2))
                elif ch=='=':
                    portals.append(Portal(x,y))
    return walls, coins, power, portals, player_start, ghost_starts