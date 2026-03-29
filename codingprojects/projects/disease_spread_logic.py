import random
import time
from math import sqrt

class Ball:
    #initial code that runs whenever a ball class object is created
    def __init__(self, x, y, move_speed, radius = 8.75):
        self.radius = radius
        self.center_x = x
        self.center_y = y
        self.deltax = random.choice([-move_speed, move_speed])
        self.deltay = random.choice([-move_speed, move_speed])
        self.state = "healthy"
        self.infection_time= None
        #5 second recovery time
        self.recovery_time = 5
        #dont stand still
        if self.deltax == 0 and self.deltay ==0:
            self.deltax = move_speed
    
    def move(self):
        self.center_x += self.deltax
        self.center_y += self.deltay
    
    def reverse_x(self):
        self.deltax *= -1

    def reverse_y(self):
        self.deltay *= -1
    
    def distance_to(self, other):
        dx = self.center_x - other.center_x
        dy = self.center_y - other.center_y
        return sqrt(dx ** 2 + dy ** 2)
    
    def overlapping(self, other):
        return self.distance_to(other) < (self.radius + other.radius)
    
    def infect(self):
        if self.state == "healthy":
            self.state = "infected"
            self.infection_time = time.time()
    
    def healing(self):
        if self.state == "infected" and self.infection_time:
            if time.time() - self.infection_time >= self.recovery_time:
                self.state = "recovered"
                self.infection_time = None
            

def check_border_collision(ball, left, right, top, bottom):
    #check left wall
    if ball.center_x - ball.radius < left:
        ball.center_x = left + ball.radius
        ball.deltax = abs(ball.deltax)
    
    #check right wall
    if ball.center_x + ball.radius > right:
        ball.center_x - right - ball.radius
        ball.deltax = -abs(ball.deltax)

    #check top wall
    if ball.center_y - ball.radius < top:
        ball.center_y = top + ball.radius
        ball.deltay = abs(ball.deltay)

    #check bottom wall
    if ball.center_y + ball.radius > bottom:
        ball.center_y = bottom - ball.radius
        ball.deltay = -abs(ball.deltay)

def handle_collision(self, other, move_speed):
    if self.overlapping(other):
        #random bounce after hit
        self.deltax = (random.choice([-move_speed, move_speed]))
        self.deltay = (random.choice([-move_speed, move_speed]))
        other.deltax = (random.choice([-move_speed, move_speed]))
        other.deltay = (random.choice([-move_speed, move_speed]))

        #spread infection
        if self.state == "infected":
            other.infect()
        elif other.state == "infected":
            self.infect()
        return True
    return False
