import pygame
import heapq

from character import Character



class Ghost(Character):
    def __init__(self, x, y, speed=2):
        super().__init__(x, y, speed)
        self.path = []
        self.path_update_timer = 0

    def find_path(self, target_pos, walls):
        start = (int(self.position.x) // 20, int(self.position.y) // 20)
        goal = (int(target_pos.x) // 20, int(target_pos.y) // 20)

        def neighbors(pos):
            x, y = pos
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if not any(w.rect.collidepoint(nx*20+10, ny*20+10) for w in walls):
                    yield (nx, ny)

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break
            for next in neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + abs(goal[0]-next[0]) + abs(goal[1]-next[1])
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        path = []
        current = goal
        while current and current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        self.path = [pygame.Vector2(x*20+10, y*20+10) for x, y in path]

    def update(self, pacman, walls):
        self.path_update_timer += 1
        if self.path_update_timer >= 15:  
            self.find_path(pacman.position, walls)
            self.path_update_timer = 0
        if self.path:
            if self.position.distance_to(self.path[0]) < 5:
                self.path.pop(0)
            if self.path:
                direction = (self.path[0] - self.position).normalize()
                self.position += direction * self.speed
