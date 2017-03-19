import tkinter
from random import randint
from tkinter import *
from clustering import *


class GUI:
    def __init__(self, width=700, height=600):
        """
        GUI constructor
        :param width: (int) window width
        :param height: (int) window height
        """
        self.window = tkinter.Tk()
        self.window.configure(background="white")
        self.width = width
        self.height = height
        self.window.geometry(str(self.width) + "x" + str(self.height + 100))

        self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=10)

        self.update_period = 50

        # step-by-step stuff

        self.clusters_num = 3
        self.clusters = []
        self.points = []
        self.global_potential = []
        self.alpha = 0.1
        self.pot_p = []
        self.steps = []
        self.current_step = 0
        self.dist_fn = euclid_distance

        

        # buttons

        self.b_clean = Button(self.window, text="Очистить", command=self.clean)
        self.b_clean.grid(row=1, column=0)

        self.b_show_points = Button(self.window, text="Добавить точки", command=self.show_points)
        self.b_show_points.grid(row=1, column=1)

        self.b_show_pots = Button(self.window, text="Показать потенциалы", command=self.show_potentials)
        self.b_show_pots.config(state=DISABLED)
        self.b_show_pots.grid(row=1, column=2)

        self.b_next_spike = Button(self.window, text="Следующая итерация", command=self.next)
        self.b_next_spike.config(state=DISABLED)
        self.b_next_spike.grid(row=1, column=3)

        self.b_prev_spike = Button(self.window, text="Предыдущая итерация", command=self.prev)
        self.b_prev_spike.config(state=DISABLED)
        self.b_prev_spike.grid(row=1, column=4)
        self.l_step_var = StringVar()
        self.l_step_var.set(self.current_step)
        self.l_step = Label(self.window, textvariable=self.l_step_var)
        self.l_step.grid(row=2, column=1)


        self.clusters_label = Label(self.window, text="Шаг: ")
        self.clusters_label.grid(row=2, column=0)
        self.b_clusterize = Button(self.window, text="Кластеризовать", command=self.clusterize)
        self.b_clusterize.config(state=DISABLED)
        self.b_clusterize.grid(row=1, column=5)

        self.l_alpha = Label(self.window, text="Альфа:")
        self.l_alpha.grid(row=2, column=2)


        self.alpha_var = StringVar()
        self.alpha_var.set("0.1")
        self.t_alpha = Entry(self.window, textvariable=self.alpha_var)
        self.t_alpha.grid(row=2, column=3)

        self.b_alpha = Button(self.window, text="Задать", command=self.set_alpha)
        self.b_alpha.grid(row=2, column=4)

        self.l_alpha = Label(self.window, text="Альфа:")
        self.l_alpha.grid(row=2, column=2)

        self.c = 3
        self.c_var = StringVar()
        self.c_var.set("3")
        self.t_c = Entry(self.window, textvariable=self.c_var)
        self.t_c.grid(row=3, column=3)

        self.b_c = Button(self.window, text="Задать число кластеров", command=self.set_c)
        self.b_c.grid(row=3, column=4)

        self.window.mainloop()

    def set_alpha(self):
        self.alpha = float(self.alpha_var.get())

    def set_c(self):
        self.c = int(self.c_var.get())

    def clean(self):
        self.canvas.delete(self.canvas, ALL)
        self.alpha = 0.1
        self.clusters = []
        self.clusters_num = 3
        self.global_potential = []
        self.points = []
        self.pot_p = []
        self.steps = []
        self.current_step = 0

        self.b_show_points.config(state=NORMAL)
        self.b_show_pots.config(state=DISABLED)
        self.b_next_spike.config(state=DISABLED)
        self.b_prev_spike.config(state=DISABLED)
        self.b_clusterize.config(state=DISABLED)


    def show_points(self):

        self.canvas.delete(self.canvas, ALL)

        for i in range(3):
            self.clusters.append(get_cluster(50, 50, randint(-200, 200), randint(-200, 200)))

        for c in self.clusters:
            self.draw_arc(c)

        self.b_show_pots.config(state=NORMAL)

    def show_potentials(self):
        self.canvas.delete(self.canvas, ALL)

        for c in self.clusters:
            for p in c:
                self.points.append(p)

        # self.alpha = calc_avg_dist(self.points, euclid_distance)

        print("alpha: {0}".format(self.alpha))

        self.pot_p = calc_potential(self.points, self.dist_fn, self.alpha)

        # assign colors

        colored_points = self.colorize(self.pot_p)

        self.draw_colored_dots(colored_points)
        self.prepare_steps()

    def colorize(self, points):
        max_p = max(points, key=lambda x: x[1])[1]
        min_p = min(points, key=lambda x: x[1])[1]
        # print("max_p {0}".format(max_p))
        # print("min_p {0}".format(min_p))

        colored_points = []
        for coords, pot in points:
            color = int(pot / (max_p - min_p) * 255)
            if color > 255:
                color = 255
            # print("color: {0}".format(color))

            hex_color = "#00" + hex(color)[2:].zfill(2) + "00"
            # print("hex color: {0}".format(hex_color))
            colored_points.append((coords, hex_color))
        return colored_points

    def prepare_steps(self):
        sorted_pot_p = sort_by_potential(self.pot_p)
        print(sorted_pot_p)
        self.steps.append(self.colorize(sorted_pot_p))
        for i in range(self.c - 1):
            iter_pot_p = sub_cluster_potential(sorted_pot_p, self.alpha, self.dist_fn)
            sorted_pot_p = sort_by_potential(iter_pot_p)
            print(len(sorted_pot_p))
            print(sorted_pot_p)

            colored = self.colorize(sorted_pot_p)
            print("len: {0}".format(len(colored)))
            self.steps.append(colored)

        self.b_next_spike.config(state=NORMAL)
        self.b_prev_spike.config(state=NORMAL)
        self.b_clusterize.config(state=NORMAL)


    def next(self):
        self.draw_colored_dots(self.steps[self.current_step])

        (x, y), color = self.steps[self.current_step][0]
        print(x, y)
        self.canvas.create_oval(self.get_screen_coords(x - 4, y - 4, x + 4, y + 4), fill="red")
        self.l_step_var.set(self.current_step)
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1

    def prev(self):
        if self.current_step > 0:
                self.current_step -= 1
        self.draw_colored_dots(self.steps[self.current_step])
        (x, y), color = self.steps[self.current_step][0]
        print(x, y)
        self.canvas.create_oval(self.get_screen_coords(x - 4, y - 4, x + 4, y + 4), fill="red")
        self.l_step_var.set(self.current_step)

    def clusterize(self):
        clusters = []
        for step in self.steps:
            clusters.append(step[0][0])

        clustered = clusterize(clusters, self.points, self.dist_fn)
        print(len(clustered.keys()))
        for (x, y), ps in clustered.items():
            color = "#" + hex(randint(0, 255*255*255))[2:].zfill(6)
            for xp, yp in ps:
                self.canvas.create_oval(self.get_screen_coords(xp - 2, yp - 2, xp + 2, yp + 2), fill=color)
            self.canvas.create_oval(self.get_screen_coords(x - 4, y - 4, x + 4, y + 4), fill="red")


    def draw_colored_dots(self, points):
        self.canvas.delete(self.canvas, ALL)

        for (x, y), color in points:
            # print("Draw dots: {0}".format(color))
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill=color)

    def draw_arc(self, arc):
        """
        Draw given arc
        :param arc: (x, y) Tuples list
        :return: None
        """
        for x, y in arc:
            # self.canvas.create_line(self.get_point_coords(x, y), fill="black")
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="black")

    def get_point_coords(self, x, y):
        """
        Get oval coordinates representing point for given coordinates
        :param x:
        :param y:
        :return: [x1, y1, x2, y2] Oval coordinates
        """
        return x + int(self.width / 2), \
               y + int(self.height / 2), \
               x + int(self.width / 2) + 1, \
               y + int(self.height / 2) + 1

    def get_screen_coords(self, x1, y1, x2, y2):
        """
        Get screen coordiantes for given coordinates
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return: [x1, y1, x2, y2] Coordinates list
        """
        return x1 + int(self.width / 2), \
               y1 + int(self.height / 2), \
               x2 + int(self.width / 2), \
               y2 + int(self.height / 2)


if __name__ == "__main__":
    gui = GUI()

