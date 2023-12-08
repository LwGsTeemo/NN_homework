import math as m
import random as r
from simple_geometry import *
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import pandas as pd
import RBFmodel
import draw
import tkinter as tk
import UIhw2_support #tkinter的UI檔案
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #tkinter導入matplotlib
from matplotlib.figure import Figure

class Car():
    def __init__(self) -> None:
        self.radius = 6
        self.angle_min = -90
        self.angle_max = 270
        self.wheel_min = -40
        self.wheel_max = 40
        self.xini_max = 4.5
        self.xini_min = -4.5

        self.reset()

    @property
    def diameter(self):
        return self.radius/2

    def reset(self):
        self.angle = 90
        self.wheel_angle = 0

        xini_range = (self.xini_max - self.xini_min - self.radius)
        left_xpos = self.xini_min + self.radius//2
        self.xpos = r.random()*xini_range + left_xpos  # random x pos [-3, 3]
        self.ypos = 0

    def setWheelAngle(self, angle):
        self.wheel_angle = angle if self.wheel_min <= angle <= self.wheel_max else (
            self.wheel_min if angle <= self.wheel_min else self.wheel_max)

    def setPosition(self, newPosition: Point2D):
        self.xpos = newPosition.x
        self.ypos = newPosition.y

    def getPosition(self, point='center') -> Point2D:
        if point == 'right':
            right_angle = self.angle - 45
            right_point = Point2D(self.radius/2, 0).rorate(right_angle)
            return Point2D(self.xpos, self.ypos) + right_point

        elif point == 'left':
            left_angle = self.angle + 45
            left_point = Point2D(self.radius/2, 0).rorate(left_angle)
            return Point2D(self.xpos, self.ypos) + left_point

        elif point == 'front':
            fx = m.cos(self.angle/180*m.pi)*self.radius/2+self.xpos
            fy = m.sin(self.angle/180*m.pi)*self.radius/2+self.ypos
            return Point2D(fx, fy)
        else:
            return Point2D(self.xpos, self.ypos)

    def getWheelPosPoint(self):
        wx = m.cos((-self.wheel_angle+self.angle)/180*m.pi) * \
            self.radius/2+self.xpos
        wy = m.sin((-self.wheel_angle+self.angle)/180*m.pi) * \
            self.radius/2+self.ypos
        return Point2D(wx, wy)

    def setAngle(self, new_angle):
        new_angle %= 360
        if new_angle > self.angle_max:
            new_angle -= self.angle_max - self.angle_min
        self.angle = new_angle

    def tick(self):
        '''
        set the car state from t to t+1
        '''
        car_angle = self.angle/180*m.pi
        wheel_angle = self.wheel_angle/180*m.pi
        new_x = self.xpos + m.cos(car_angle+wheel_angle) + \
            m.sin(wheel_angle)*m.sin(car_angle)

        new_y = self.ypos + m.sin(car_angle+wheel_angle) - \
            m.sin(wheel_angle)*m.cos(car_angle)
        new_angle = (car_angle - m.asin(2*m.sin(wheel_angle) / (self.radius*1.5))) / m.pi * 180

        new_angle %= 360
        if new_angle > self.angle_max:
            new_angle -= self.angle_max - self.angle_min

        self.xpos = new_x
        self.ypos = new_y
        self.setAngle(new_angle)


class Playground():
    def __init__(self):
        # read path lines
        self.path_line_filename = "軌道座標點.txt"
        self._setDefaultLine()
        self.decorate_lines = [
            Line2D(-6, 0, 6, 0),  # start line
            Line2D(0, 0, 0, -3),  # middle line
        ]

        self.car = Car()
        self.reset()

    def _setDefaultLine(self):
        # default lines
        self.destination_line = Line2D(18, 40, 30, 37)

        self.lines = [
            Line2D(-6, -3, 6, -3),
            Line2D(6, -3, 6, 10),
            Line2D(6, 10, 30, 10),
            Line2D(30, 10, 30, 50),
            Line2D(18, 50, 30, 50),
            Line2D(18, 22, 18, 50),
            Line2D(-6, 22, 18, 22),
            Line2D(-6, -3, -6, 22),
        ]

        self.car_init_pos = None
        self.car_init_angle = None

    def _readPathLines(self):
        try:
            with open(self.path_line_filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # get init pos and angle
                pos_angle = [float(v) for v in lines[0].split(',')]
                self.car_init_pos = Point2D(*pos_angle[:2])
                self.car_init_angle = pos_angle[-1]

                # get destination line
                dp1 = Point2D(*[float(v) for v in lines[1].split(',')])
                dp2 = Point2D(*[float(v) for v in lines[2].split(',')])
                self.destination_line = Line2D(dp1, dp2)

                # get wall lines
                self.lines = []
                inip = Point2D(*[float(v) for v in lines[3].split(',')])
                for strp in lines[4:]:
                    p = Point2D(*[float(v) for v in strp.split(',')])
                    line = Line2D(inip, p)
                    inip = p
                    self.lines.append(line)
        except Exception:
            self._setDefaultLine()

    def predictAction(self, state,):
        '''
        此function為模擬時，給予車子隨機數字讓其走動。
        不需使用此function。
        '''
        return 0

    @property
    def n_actions(self):  # action = [0~num_angles-1]
        return (self.car.wheel_max - self.car.wheel_min + 1)

    @property
    def observation_shape(self):
        return (len(self.state),)

    @ property
    def state(self):
        front_dist = - 1 if len(self.front_intersects) == 0 else self.car.getPosition(
            ).distToPoint2D(self.front_intersects[0])
        right_dist = - 1 if len(self.right_intersects) == 0 else self.car.getPosition(
            ).distToPoint2D(self.right_intersects[0])
        left_dist = - 1 if len(self.left_intersects) == 0 else self.car.getPosition(
            ).distToPoint2D(self.left_intersects[0])

        return [front_dist, right_dist, left_dist]

    def _checkDoneIntersects(self):
        if self.done:
            return self.done

        cpos = self.car.getPosition('center')     # center point of the car
        cfront_pos = self.car.getPosition('front')
        cright_pos = self.car.getPosition('right')
        cleft_pos = self.car.getPosition('left')
        diameter = self.car.diameter

        isAtDestination = cpos.isInRect(
            self.destination_line.p1, self.destination_line.p2
        )
        done = False if not isAtDestination else True

        front_intersections, find_front_inter = [], True
        right_intersections, find_right_inter = [], True
        left_intersections, find_left_inter = [], True
        for wall in self.lines:  # chack every line in play ground
            dToLine = cpos.distToLine2D(wall)
            p1, p2 = wall.p1, wall.p2
            dp1, dp2 = (cpos-p1).length, (cpos-p2).length
            wall_len = wall.length

            # touch conditions
            p1_touch = (dp1 < diameter)
            p2_touch = (dp2 < diameter)
            body_touch = (
                dToLine < diameter and (dp1 < wall_len and dp2 < wall_len)
            )
            front_touch, front_t, front_u = Line2D(
                cpos, cfront_pos).lineOverlap(wall)
            right_touch, right_t, right_u = Line2D(
                cpos, cright_pos).lineOverlap(wall)
            left_touch, left_t, left_u = Line2D(
                cpos, cleft_pos).lineOverlap(wall)

            if p1_touch or p2_touch or body_touch or front_touch:
                if not done:
                    done = True

            # find all intersections
            if find_front_inter and front_u and 0 <= front_u <= 1:
                front_inter_point = (p2 - p1)*front_u+p1
                if front_t:
                    if front_t > 1:  # select only point in front of the car
                        front_intersections.append(front_inter_point)
                    elif front_touch:  # if overlapped, don't select any point
                        front_intersections = []
                        find_front_inter = False

            if find_right_inter and right_u and 0 <= right_u <= 1:
                right_inter_point = (p2 - p1)*right_u+p1
                if right_t:
                    if right_t > 1:  # select only point in front of the car
                        right_intersections.append(right_inter_point)
                    elif right_touch:  # if overlapped, don't select any point
                        right_intersections = []
                        find_right_inter = False

            if find_left_inter and left_u and 0 <= left_u <= 1:
                left_inter_point = (p2 - p1)*left_u+p1
                if left_t:
                    if left_t > 1:  # select only point in front of the car
                        left_intersections.append(left_inter_point)
                    elif left_touch:  # if overlapped, don't select any point
                        left_intersections = []
                        find_left_inter = False

        self._setIntersections(front_intersections,
                               left_intersections,
                               right_intersections)

        # results
        self.done = done
        return done

    def _setIntersections(self, front_inters, left_inters, right_inters):
        self.front_intersects = sorted(front_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('front')))
        self.right_intersects = sorted(right_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('right')))
        self.left_intersects = sorted(left_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('left')))

    def reset(self):
        self.done = False
        self.car.reset()

        if self.car_init_angle and self.car_init_pos:
            self.setCarPosAndAngle(self.car_init_pos, self.car_init_angle)

        self._checkDoneIntersects()
        return self.state

    def setCarPosAndAngle(self, position: Point2D = None, angle=None):
        if position:
            self.car.setPosition(position)
        if angle:
            self.car.setAngle(angle)

        self._checkDoneIntersects()

    def calWheelAngleFromAction(self, action):
        angle = self.car.wheel_min + \
            action*(self.car.wheel_max-self.car.wheel_min) / \
            (self.n_actions-1)
        return angle

    def step(self, action=None):
        if action:
            angle = self.calWheelAngleFromAction(action=action)
            self.car.setWheelAngle(angle)

        if not self.done:
            self.car.tick()

            self._checkDoneIntersects()
            return self.state
        else:
            return self.state


def run_example(trainfile,k=10,epoch=100):
    UIhw2_support._w1.Button3['state'] = tk.DISABLED
    # use example, select random actions until gameover
    p = Playground()
    #輸入資料
    df = pd.read_table(trainfile, sep=' ',header=None)
    weights,centers = RBFmodel.model(data=df,k=k,num_epochs=epoch)
    UIhw2_support._w1.progressbtn.set(40)
    df = pd.DataFrame(df)
    if df.shape[1] == 6:
        filename = "./track6D.txt"
    else:
        filename = "./track4D.txt"
    X = df.iloc[:,-4:-1].values
    state = p.reset()
    angle=[]
    posXY = [(0,0)]
    cnt=1
    coordinates,firstAndLast = draw.read_coordinates_from_file('./軌道座標點.txt')
    fig1 = plt.figure(figsize=(5, 4))
    plt.ion()
    ax1 = fig1.add_subplot(1,1,1)
    with open(filename, 'w') as f:
        while not p.done:
            ax1.clear()
            # print every state and position of the car
            a = p.car.getPosition('center')
            posXY.append((a.x , a.y))
            # you can predict your action according to the state here
            state = np.array(state)
            state = (state - np.mean(X, axis=0)) / np.std(X, axis=0)
            action = RBFmodel.predict(state,weights,centers)*4+40
            # write .txt file
            if df.shape[1] == 6:
                f.write(str(a.x)+" "+str(a.y)+" ")
            f.write(str(state[0])+" "+str(state[1])+" "+str(state[2])+" "+str(action)+"\n")
            angle.append(action)

            draw.draw_map(ax1,coordinates,firstAndLast)
            circle = Circle((a.x, a.y), radius=3, edgecolor='r', facecolor='none')
            ax1.add_patch(circle)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax1.text(0.05, 0.95,'state:\n('+str(round(state[0],3))+", "+str(round(state[1],3))+", "+str(round(state[2],3))+')',
                transform=ax1.transAxes, fontsize=12,verticalalignment='top', bbox=props)
            canvas1 = FigureCanvasTkAgg(fig1, master=UIhw2_support._w1.Frame1)
            canvas1.get_tk_widget().place(x=0,y=0)
            canvas1.flush_events() #畫面刷新
            # take action
            state = p.step(action)
            UIhw2_support._w1.progressbtn.set(40+cnt)
            cnt+=1
        f.close()
    #read file to draw picture
    UIhw2_support._w1.progressbtn.set(100)
    # fig2 = plt.figure(figsize=(5, 4))
    fig2 = Figure(figsize=(5, 4))
    ax2 = fig2.add_subplot(1,1,1)
    ax2.clear()
    draw.draw_map_and_circles(ax2,coordinates,firstAndLast,posXY,mode=2)
    canvas2 = FigureCanvasTkAgg(fig2, master=UIhw2_support._w1.Frame2)
    canvas2.get_tk_widget().place(x=0,y=0)
    canvas2.flush_events() #畫面刷新
    UIhw2_support.root.update_idletasks()
    plt.ioff()
    plt.close(fig1)
    plt.close(fig2)
        
if __name__ == "__main__":
    run_example("train4dAll.txt",k=10,epoch=100)
