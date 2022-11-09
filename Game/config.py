height, width  = 20, 10 # width and height of the game grid
tile_size = 35 # tile size for visualization
resolution = (width * tile_size, height * tile_size) # resolution of the visualization screen

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], # the different figures of tetris with respect to the centre of rotation point
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

anim_speed, anim_limit_relaxed, anim_limit_pressed = 100, 101, 50  #figure fall speed


