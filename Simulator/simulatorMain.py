from settings import *

import pygame as pg
import map_generator
import robot
import configurations
import map
import exploration
import fastestPath

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("MDP Arena Simulator")




player_robot = robot.Robot()
robot_group = pg.sprite.Group(player_robot)
arena_map = map_generator.Map()
arena_map.generate_map('map_config_1.txt')
running = True


#Testing##############################################################
test_robot = robot.RobotAlgo(configurations.START_ROW,configurations.START_COL,False,player_robot)
exploredMap = map.Map(test_robot)
realMap = map.Map(test_robot)
exploredMap.setAllUnexplored()
explorer = exploration.Exploration(exploredMap,realMap,test_robot,300,5/100000)
#path = fastestPath.astar(explorer.exploredMap, (explorer.bot.posRow,explorer.bot.posCol), (configurations.START_ROW,configurations.START_COL))
#######################################################################


while running:
    screen.fill((0,0,0))

    # generate the map
    arena_map.tiles_group.draw(screen)
    robot_group.draw(screen)
    player_robot.censors.draw(screen)
    #censors update
    for censor in player_robot.censors:
        censor.collision_update(arena_map)
    # map update
    arena_map.map_update()

    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                explorer.runExploration()
            if event.key == pg.K_a:
                path = fastestPath.astar(explorer.exploredMap, (explorer.bot.posRow,explorer.bot.posCol), (configurations.GOAL_ROW,configurations.GOAL_COL))
                fastestPath.runAStar(path,explorer.exploredMap)
                #player_robot.rotate(-90)
            if event.key == pg.K_d:
                player_robot.rotate(90)

    pg.display.update()
