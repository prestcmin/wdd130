from disease_spread_logic import Ball, check_border_collision, handle_collision

import tkinter as tk
import random
from tkinter import Frame, Label, Button, Canvas
from number_entry import IntEntry
from random import randint

def main():
    root = tk.Tk()
    root.geometry("1200x750")
    root.resizable = False, False
    frm_main = Frame(root)
    frm_main.master.title("Disease Spread Simulation")
    frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=1)
    populate_main_window(frm_main)
    root.mainloop()

def populate_main_window(frm_main):
    #for auto pausing when complete
    simulation_running = True

    #rectangle boundaries for collision detection
    rect_left = 1.5
    rect_top = 1.5
    rect_right = 800
    rect_bottom = 600

    #create all labels, entries, and canvas for gui
    simulation_area = Canvas(frm_main, width = 800, height=600)
    simulation_outline = simulation_area.create_rectangle(rect_left, rect_top, rect_right, rect_bottom)
    lbl_healthy = Label(frm_main, text="Healthy:")
    lbl_sick = Label(frm_main, text="Sick:")
    lbl_recovered = Label(frm_main, text="Recovered:")
    lbl_progress = Label(frm_main)
    lbl_population_size = Label(frm_main, text="Pop. Size (100-250):")
    ent_population_size = IntEntry(frm_main, width=3, lower_bound=100, upper_bound=250)
    lbl_movement_speed = Label(frm_main, text="Move Speed (1-3):")
    ent_movement_speed = IntEntry(frm_main, width=3, lower_bound=1, upper_bound=3)
    btn_start = Button(frm_main, text="Start Simulation")
    btn_clear = Button(frm_main, text="Clear Simulation")

    #layout segments into frame
    simulation_area.grid(row=2, column=2)
    lbl_healthy.grid(row=0, column=0, padx=3, pady=3)
    lbl_sick.grid(row=1, column=0, padx=3, pady=3)
    lbl_recovered.grid(row=0, column=1, padx=3, pady=3)
    lbl_progress.grid(row=4, column=4, padx=3, pady=3)
    lbl_population_size.grid(row = 3, column=1, padx=3, pady=3)
    lbl_movement_speed.grid(row = 4, column=1, padx=3, pady=3)
    
    ent_population_size.grid(row=3, column=0, padx=3, pady=3)
    ent_movement_speed.grid(row=4, column=0, padx=3, pady=3)

    btn_start.grid(row=5, column=2, padx=3, pady=3)
    btn_clear.grid(row=5, column=4, padx=3, pady=3)

    class Simulation:
        def __init__(self):
            self.balls = []

        #add balls to list
        def add_population(self, ball):
            self.balls.append(ball)

        #run check on movement logic
        def movement_update(self):
            for ball in self.balls:
                ball.move()
                check_border_collision(ball, self.left, self.right, self.top, self.bottom)
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    handle_collision(self.balls[i], self.balls[j])    
    simulation = Simulation()
    
    #create the population    
    def create_population():
        simulation.balls.clear()
        simulation_area.delete("balls")
        ball_count = ent_population_size.get()
        move_speed = ent_movement_speed.get()

        for _ in range(ball_count):
            radius = 8.75
            x = randint(int(rect_left + radius), int(rect_right - radius))
            y = randint(int(rect_top + radius), int(rect_bottom - radius))
            ball = Ball(x, y, move_speed, radius)
            simulation.balls.append(ball)

            #create visual id for canvas tracking
            visual_id = simulation_area.create_oval(
                ball.center_x - ball.radius,
                ball.center_y - ball.radius,
                ball.center_x + ball.radius,
                ball.center_y + ball.radius,
                fill = "black",
                tags = "balls"
            )
            ball.visual_id = visual_id

    #update labels for gui
    def update_labels():
        nonlocal simulation_running
        healthy = sum(1 for b in simulation.balls if b.state == "healthy")
        infected = sum(1 for b in simulation.balls if b.state == "infected")
        recovered = sum(1 for b in simulation.balls if b.state == "recovered")

        lbl_healthy.config(text=f"Healthy: {healthy}")
        lbl_sick.config(text=f"Sick: {infected}")
        lbl_recovered.config(text=f"Recovered: {recovered}")

        #pause when no sick are left
        if simulation_running and infected <= 0 and recovered >1:
            simulation_running = False
            lbl_progress.config(text="Simulation Complete")
        
        #update every 10ms
        if simulation_running:
            simulation_area.after(10, update_labels)

    #run updates so that the logic code matches what is shown on canvas
    def update_visuals():
        for ball in simulation.balls:
            simulation_area.coords(
                ball.visual_id,
                ball.center_x - ball.radius,
                ball.center_y - ball.radius,
                ball.center_x + ball.radius,
                ball.center_y + ball.radius
            )
            color_map = {
                "healthy":"black",
                "infected":"red",
                "recovered":"green"
            }
            simulation_area.itemconfig(ball.visual_id, fill=color_map[ball.state], outline=color_map[ball.state])

    #run logic checks for balls
    def population_updates():
        nonlocal simulation_running
        move_speed = ent_movement_speed.get()
        for ball in simulation.balls:
            ball.move()
            check_border_collision(
                ball,
                rect_left,
                rect_right,
                rect_top,
                rect_bottom
            )
            ball.healing()
        for i in range(len(simulation.balls)):
            for j in range(i + 1, len(simulation.balls)):
                handle_collision(simulation.balls[i], simulation.balls[j], move_speed)
        update_visuals()
        if simulation_running:
            simulation_area.after(10, population_updates)

    #start the infection on a random ball out of the population
    def start_infection():
        if simulation.balls:
            patient_zero= random.choice(simulation.balls)
            patient_zero.infect()

    #what start button does
    def start_simulation():
        nonlocal simulation_running
        simulation_running = True
        create_population()
        population_updates()
        simulation_area.after(2500, start_infection)
        update_labels()
    
    #what clear button does
    def clear_simulation():
        nonlocal simulation_running
        simulation_running = False

        #clear list and canvas
        simulation.balls.clear()
        simulation_area.delete("balls")

        #clear labels
        lbl_population_size.config(text=f"Pop. Size (100-250): ")
        lbl_movement_speed.config(text=f"Move Speed (2-4): ")
        lbl_healthy.config(text=f"Healthy: ")
        lbl_sick.config(text=f"Sick: ")
        lbl_recovered.config(text=f"Recovered: ")
        lbl_progress.config(text="")

        #clear entries
        ent_population_size.delete(0, tk.END)
        ent_movement_speed.delete(0, tk.END)

    #controls for start button
    btn_start.config(command=start_simulation)

    #controls for clear button
    btn_clear.config(command=clear_simulation)

if __name__ == "__main__":
    main()