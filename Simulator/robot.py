import numpy
import pygame as pg
from map import Map
from sensor import Sensor
from configurations import *
from vec2D import swap_coordinates


class Robot(pg.sprite.Sprite):
    def __init__(self, comm=None):
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2(0, -1)
        self.velocity = 35

        self.spawn_point = 17 * Map.cell_length

        self.rect = self.image.get_rect()
        self.rect.x = Map.cell_gap
        self.rect.y = self.spawn_point + Map.cell_gap  # position of the robot

        self.sensors = pg.sprite.Group()
        #self.initialize_sensors()
        self.location = pg.math.Vector2(18, 1)
        self.comm = comm if not comm else 0
        self.initialize_sensors()

        # (ADDED)Set Up Communication Socket With RPI ###############################
        # self.comm = commMgr.CommMgr()

    def add_sensor(
        self,
        width,
        height,
        center_x_offset,
        center_y_offset,
        direction,
        location_offset,
        range=2
    ):
        self.sensors.add(
            Sensor(
                width,
                height,
                center_x_offset,
                center_y_offset,
                direction,
                self,
                location_offset,
                self.comm,
                range
            )
        )

    def initialize_sensors(self):
        """
        Robot Sensor placement
                         ^   ^   ^
                      SR  SR  SR
         << SR [X] [X] [X]
            < LR [X] [X] [X] SR >
                       [X] [X] [X]

        # up sensors
        """
        self.add_sensor(
            20,
            Map.cell_length * 8,
            0,
            -Map.cell_length * 5.5,
            Direction.UP.value,
            pg.Vector2(-1, 0),
        )
        self.add_sensor(
            20,
            Map.cell_length * 8,
            30,
            -Map.cell_length * 5.5,
            Direction.UP.value,
            pg.Vector2(-1, 1),
        )
        self.add_sensor(
            20,
            Map.cell_length * 8,
            -30,
            -Map.cell_length * 5.5,
            Direction.UP.value,
            pg.Vector2(-1, -1),
        )
        # left sensors
        self.add_sensor(
            Map.cell_length * 8,
            20,
            -Map.cell_length * 5.5,
            -Map.cell_length * 1,
            Direction.RIGHT.value,
            pg.Vector2(1, 0),
        )
        self.add_sensor(
            Map.cell_length * 15,
            20,
            -Map.cell_length * 9,
            0,
            Direction.LEFT.value,
            pg.Vector2(-1, -1),
            7
        )  # long-range sensor
        # right sensors
        self.add_sensor(
            Map.cell_length * 8,
            20,
            Map.cell_length * 5.5,
            -Map.cell_length * 1,
            Direction.RIGHT.value,
            pg.Vector2(1, -1),
        )
        """
        self.add_sensor(20, Map.cell_length* 8, 30, -Map.cell_length* 5.5, Direction.UP.value, pg.Vector2(-1,1))
        self.add_sensor(20, Map.cell_length* 8, -30, -Map.cell_length* 5.5, Direction.UP.value, pg.Vector2(-1,-1))
        # left sensors
        self.add_sensor(Map.cell_length * 8, 20, -Map.cell_length * 5.5, - Map.cell_length * 1, Direction.RIGHT.value, pg.Vector2(1,0), 7)
        self.add_sensor(Map.cell_length * 15, 20, -Map.cell_length * 9, 0, Direction.LEFT.value, pg.Vector2(-1,-1)) # long-range sensor
        # right sensors
        self.add_sensor(Map.cell_length * 8, 20, Map.cell_length * 5.5, - Map.cell_length * 1, Direction.RIGHT.value, pg.Vector2(1,-1))

        """
    def is_in_arena(self, rect):
        if (
            rect.x >= Map.arena_border_left
            and rect.x <= Map.arena_border_right
            and rect.y >= Map.arena_border_up
            and rect.y <= Map.arena_border_down
        ):
            return True
        else:
            return False

    def move_forward(self):
        # if the robot is within the arena
        # comm.send_movement(Movement.FORWARD.value,False)
        _rect = pg.Rect(self.rect)
        _rect.x += self.direction[0] * self.velocity
        _rect.y += self.direction[1] * self.velocity

        if self.is_in_arena(_rect):
            self.location += swap_coordinates(self.direction)
            self.rect.x += self.direction[0] * self.velocity
            self.rect.y += self.direction[1] * self.velocity
            # update center
            self.rect.center = pg.math.Vector2(self.rect.x + 50, self.rect.y + 50)
            for sensor in self.sensors:
                sensor.position_update(self)

    def rotate(self, degree):
        """
        if(degree<0):
            self.comm.send_movement(Movement.LEFT.value,False)
        elif(degree>0):
            self.comm.send_movement(Movement.RIGHT.value,False)
        """
        self.image = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()

        # update sensors
        for sensor in self.sensors:
            sensor.rotation_update(self, degree)

    def canCalibrateOnTheSpot(self):
        sensorVal = self.comm.get_sensor_value()
        counter = 0

        # Check can calibrate using front 3 sensors
        for front in range(1,4,1):
            if(sensorVal[front]=="1"):
                counter += 1
        if(counter == 3):
            return True

        # Check can calibrate using right 2 sensors
        counter = 0
        for right in range(4,6,1):
            if(sensorVal[right]=="1"):
                counter += 1
        if(counter == 2):
            return True
        return False

    def rotateBackDefault(self):
        counter = rotateBackDefault(self.direction)

        if(counter == 1):
            self.rotate(90)
            #self.comm.send_movement(Movement.RIGHT,Movement.RIGHT.value,0)
        else:
            self.rotate(90)
            self.rotate(90)
            #self.comm.send_movement(Movement.RIGHT,Movement.RIGHT.value,0)
            #self.comm.send_movement(Movement.RIGHT,Movement.RIGHT.value,0)


    def real_sense(self,arena_map,comm):
        try:
            sensor_val = comm.get_sensor_value()
            print(sensor_val)

            FRONT_LEFT = 0
            FRONT = 1
            FRONT_RIGHT = 2
            RIGHT_UP = 3
            RIGHT = 4
            LEFT = 5
            dct = {(0,-1):[(-1,-1),(0,-1),(1,-1),(1,-1),(1,0),(-1,-1)],(1,0):[(1,-1),(1,0),(1,1),(1,1),(0,1),(1,-1)],(0,1):[(1,1),(0,1),(-1,1),(-1,1),(-1,0),(1,1)],(-1,0):[(-1,1),(-1,0),(-1,-1),(-1,-1),(0,-1),(-1,1)]}
        except Exception as j:
            print("Assignment error in real sense:",j )
        try:
            print(self.direction)
            lst = dct[self.direction]
        except Exception as i:
            print("Error getting offset in real sense:",i)
        try:
            obstacles = []
            for i in range(6):
                if sensor_val[i] == -1:
                    continue
                if i == FRONT_LEFT or i == FRONT or i == FRONT_RIGHT:
                    obstacles.append((self.location.x + lst[i][1]-(sensor_val[i]+1), self.location.y + lst[i][0]))
                elif i == RIGHT_UP or i == RIGHT:
                    obstacles.append((self.location.x + lst[i][1], self.location.y + lst[i][0]+sensor_val[i]+1))
                elif i == LEFT:
                    obstacles.append((self.location.x + lst[i][1], self.location.y + lst[i][0]-(sensor_val[i]+1))
        except Exception as e:
            print("Error computing obstacle location in real sense:",e)

        try:
            for obstacle_loc in obstacles:
                arena_map.map_cells[obstacle_loc[0]][obstacle_loc[1]].is_obstacle=True
        except Exception as inst:
            print("Error updating obstacle location to map in real sense", inst)

            # for i in range(3):
            #     sensor = self.sensors.sprites()[i]
            #     print(sensor)
            #     sensorpos = sensor.location_offset
            #     robotpos =
            #     obstacle_loc = (sensor_loc[0], sensor_loc[1]+sensor_val[i]+1)
            #     #if(sensor_val[i]>-1):
            #     arena_map.map_cells[obstacle_loc[0]][obstacle_loc[1]].is_obstacle=True
            #         #comm.take_picture()
            # for i in range(3,5,1):
            #     sensor = self.sensors.sprites()[i]
            #     sensor_loc = sensor.location
            #     obstacle_loc = (sensor_loc[0]+sensor_val[i]+1, sensor_loc[1])
            #     #if(sensor_val[i]>-1):
            #     arena_map.map_cells[obstacle_loc[0]][obstacle_loc[1]].is_obstacle=True
            # sensor = self.sensors.sprites()[5]
            # sensor_loc = sensor.location
            # obstacle_loc = (sensor_loc[0]+sensor_val[5]+1, sensor_loc[1])
            # #if(sensor_val[i]>-1):


        finally:
            #arena = ""
            string = ""
            for row in range(20):
                for col in range(15):
                    if(arena_map.map_cells[row][col].is_obstacle):
                        string += "1"
                    else:
                        string += "0"
                print(string)
                #arena += string
                string = ""
            #print(arena)

    def get_sensor_readings(self,arena_map,comm):
        try:
            sensor_value = comm.get_sensor_value()
            index = 0
            for sensor in self.sensors:
                sensor.update_map(map, sensor_value[index])
                #index = index + 1
        except Exception as err:
            print("Error in getting sensor reading:",err)
        finally:
            string = ""
            for row in range(20):
                for col in range(15):
                    if(arena_map.map_cells[row][col].is_obstacle):
                        string += "1"
                    else:
                        string += "0"
                print(string)
                #arena += string
                string = ""
