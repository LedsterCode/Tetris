# Tetris - kind of
import random 
import time
import math
import pygame

settling = False
settling_start_time = 0

pygame.init()

width = 10   #normal: 10    huge: 64
height = 15  #normal: 15    huge: 35

pixel_size = 30
display = pygame.display.set_mode((width*pixel_size + 100,height*pixel_size),pygame.RESIZABLE)

black = (0,0,0)
textFont = pygame.font.Font(None, 30)
score = 0

shape1col = (45,255,45)
shape2col = (120,120,255)
shape3col = (255,0,0)
shape4col = (255,255,0)
shape5col = (0,0,255)
shape6col = (255,127,80)
shape7col = (255,0,255)

shape1 = [[[0,-1,-1,0],[0,-1,0,1]],[[0,1,-1,0],[0,0,1,1]]] ## S

shape2 = [[[0,-1,1,2],[0,0,0,0]],[[0,0,0,0],[0,-1,1,2]]] ## Line
shape3 = [[[0,-1,-1,0],[0,0,1,-1]],[[0,-1,0,1],[0,0,1,1]]] ## Backwards S
shape4 = [[[0,1,0,1],[0,0,1,1]]] ## square
shape5 = [[[0,-1,-1,1],[0,0,-1,0]],[[0,0,0,1],[0,-1,1,-1]],[[0,-1,1,1],[0,0,0,1]],[[0,-1,0,0],[0,1,1,-1]]] ## Backwards L
shape6 = [[[0,-1,1,1],[0,0,0,-1]],[[0,0,0,1],[0,-1,1,1]],[[0,-1,-1,1],[0,0,1,0]],[[0,0,-1,0],[0,-1,-1,1]]] ## L
shape7 = [[[0,-1,0,1],[0,0,-1,0]],[[0,0,0,1],[0,-1,1,0]],[[0,-1,1,0],[0,0,0,1]],[[0,-1,0,0],[0,0,1,-1]]] ## T

shapes = [shape1,shape2,shape3,shape4,shape5,shape6,shape7]
shape_counters = [1,0,1,0,0,0,0] 
shape_rotations = [1,1,1,0,1,1,1]
shape_rotation_requirement = [2,2,2,1,4,4,4] 
shape_colours = [shape1col,shape2col,shape3col,shape4col,shape5col,shape6col,shape7col]


picked_shape = shapes[1]
shape_number = 1
key_coord_x = picked_shape[0][0][0]+4
key_coord_y = picked_shape[0][1][0]+1
shape_rotations[shape_number] = shape_counters[shape_number] % shape_rotation_requirement[shape_number]

empty = []
area = []
for i in range(height):
    area.append([2.2]*width)
    empty.append([2.2]*width)

def spawn_shape():
    global run
    global picked_shape
    global shape_number
    shape_number = random.randint(0,6)
    picked_shape = shapes[shape_number]
    ##################                                 isinstance(area[i][j], int)


    for i in range(4):
        if not isinstance(area[picked_shape[0][1][i]+1][picked_shape[0][0][i]+4],int):
            area[picked_shape[0][1][i]+1][picked_shape[0][0][i]+4] = "X"
        else:
            run = False
            return
    
def print_area(grid):
    for i in range(height):
        for j in range(width):
            print(grid[i][j],end="")
        print()
    print()

def copy_grid(grid):
    return [row[:] for row in grid]

def move_piece_down():
    global key_coord_x
    global key_coord_y
    global piece_coords
    piece_coords = []
    global area
    empty = copy_grid(area)
    if settling:
        return
    if True:
        for i in range(height):
            for j in range(width):
              if i != height-1:  
                if isinstance(area[i][j], str) and isinstance(area[i-1][j], str):
                    empty[i+1][j] = "X"
                if isinstance(area[i][j],str) and not isinstance(area[i-1][j],str):
                    empty[i][j] = 2.2
                    empty[i+1][j] = "X"
                piece_coords.append([i+1,j])
    area = copy_grid(empty)           
    key_coord_y += 1
    
def move_piece_right():
    global key_coord_x
    global key_coord_y
    global continuing
    global area
    global settling  
    settling = False
    continuing = False
    empty = copy_grid(area)
    if max(picked_shape[shape_rotations[shape_number]][0])+key_coord_x < width-1:
        continuing = True
        for i in range(4):
            try:
                if isinstance(area[picked_shape[shape_rotations[shape_number]][1][i]+key_coord_y][picked_shape[shape_rotations[shape_number]][0][i]+key_coord_x+1],int):
                    continuing = False
                    return
            except:
                continuing  = True
    if continuing:
        for i in range(height):
            for j in range(width):
              if j > 0:  
                if isinstance(area[i][j],str) and isinstance(area[i][j-1],str):
                    empty[i][j+1] = "X"
                if isinstance(area[i][j],str) and not isinstance(area[i][j-1],str):
                    empty[i][j] = 2.2
                    empty[i][j+1] = "X"
              elif j == 0:
                if isinstance(area[i][j],str):
                    empty[i][j] = 2.2
                    empty[i][j+1] = "X"

        key_coord_x += 1
    area = copy_grid(empty)
    
def move_piece_left():
    global settling  
    settling = False
    global key_coord_x
    global key_coord_y
    global continuing
    global area
    continuing = False
    empty = copy_grid(area)
    if min(picked_shape[shape_rotations[shape_number]][0])+key_coord_x > 0:
        continuing = True
        for i in range(4):
            try:
                if isinstance(area[picked_shape[shape_rotations[shape_number]][1][i]+key_coord_y][picked_shape[shape_rotations[shape_number]][0][i]+key_coord_x-1],int):
                    continuing = False
                    return
            except:
                continuing = True
    if not min(picked_shape[shape_rotations[shape_number]][0])+key_coord_x > 0:
        continuing = False
    if continuing:
        for i in range(height):
            for j in range(width):
              if j != width-1:  
                if isinstance(area[i][j],str) and isinstance(area[i][j+1],str):
                    empty[i][j-1] = "X"
                if isinstance(area[i][j],str) and not isinstance(area[i][j+1],str):
                    empty[i][j] = 2.2
                    empty[i][j-1] = "X"
              elif j == width-1:
                if isinstance(area[i][j],str):
                    empty[i][j] = 2.2
                    empty[i][j-1] = "X"
        key_coord_x -= 1
    area = copy_grid(empty)           

def rotate_piece():
    global settling  
    settling = False
    continuing = False
    global key_coord_x
    global key_coord_y
    if max(picked_shape[(shape_counters[shape_number] + 1) % shape_rotation_requirement[shape_number]][0])+key_coord_x < width and min(picked_shape[(shape_counters[shape_number] + 1) % shape_rotation_requirement[shape_number]][0])+key_coord_x >= 0:
        continuing = True
        for i in range(4):
            try:
                if isinstance(area[key_coord_y+(picked_shape[(shape_counters[shape_number]+1) % shape_rotation_requirement[shape_number]][1][i])][key_coord_x+(picked_shape[(shape_counters[shape_number]+1) % shape_rotation_requirement[shape_number]][0][i])],int):
                    continuing = False  
                    return

            except:
                continuing = True
    if continuing:
        shape_counters[shape_number] += 1
        shape_rotations[shape_number] = shape_counters[shape_number] % shape_rotation_requirement[shape_number]
        
        for i in range(height):
            for j in range(width):
                if isinstance(area[i][j],str):
                    area[i][j] = 2.2
        key_coord_x += picked_shape[shape_rotations[shape_number]][0][0]
        key_coord_y += picked_shape[shape_rotations[shape_number]][1][0]
        for i in range(4):
            area[key_coord_y+(picked_shape[shape_rotations[shape_number]][1][i])][key_coord_x+(picked_shape[shape_rotations[shape_number]][0][i])] = "X"
            
        
        

def stop_falling_pieces():
    global settling
    settling = False
    for i in range(height):
        for j in range(width):
            if isinstance(area[i][j],str):
                area[i][j] = shape_number
                key_coord_x = picked_shape[0][0][0]+4
                key_coord_y = picked_shape[0][1][0]+1
            
                
hit_bottom_indicator = False                
def piece_hit_bottom_check():
    global settling
    global settling_start_time
    global bottom_time_check
    global key_coord_y
    global key_coord_x
    global hit_bottom_indicator
    hit_bottom_indicator = False
    for i in range(height-1,-1,-1):
        for j in range(width):
            if isinstance(area[i][j],str): ## starts from bottom
                if i == height - 1 or isinstance(area[i+1][j],int):
                  if not settling:
                    settling = True
                    settling_start_time = time.time()
                  else:
                    if time.time() - settling_start_time >= 1 or constant_downwards:
                        bottom_time_check = time.time()
                        stop_falling_pieces()
                        full_line_check()
                        spawn_shape()
                        key_coord_x = picked_shape[0][0][0] +4
                        key_coord_y = picked_shape[0][1][0] +1
                        shape_counters[shape_number] = 0
                        hit_bottom_indicator = True
                        settling = False

                  return
    settling = False
            
def full_line_check():
    global line_count
    global score
    to_clear = []
    for row in range(height):
        var = 0
        for place in range(width):
            if isinstance(area[row][place],int):
                var += 1
        if var == width:
            to_clear.append(row)

    
    ## clear line time
    for i in range(len(to_clear)):
        for k in range(row):
            for place in range(width):
                area[row-k][place] = area[(row-k)-1][place]
        line_count += 1
        score += 10

constant_right = False
constant_left = False
constant_downwards = False
spawn_shape()
time_passed = 0
start_time = time.time()
line_count = 0
move_interval = 0.15  
last_move_time = time.time()
last_move_time_left = time.time()
last_move_time_right = time.time()
run = True
while run:
  try:
    pygame.display.set_caption(f"Lines: {line_count}")
    display.fill((255,255,255))
    for i in range(width+1):
        pygame.draw.line(display, black, (pixel_size*i,0),(pixel_size*i,height*pixel_size))
    for i in range(height):
        pygame.draw.line(display, black, (0,pixel_size*i),(width*pixel_size,pixel_size*i))
        
    current_time = time.time()
    other_time = time.time()
    if math.floor(current_time-start_time) != time_passed and not constant_downwards: #if a new second has started (since time_passed is recorded at end of while loop)
        move_piece_down()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
              #  move_piece_right()
              True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
             #   move_piece_left()
             True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                rotate_piece()
            if event.key == pygame.K_q:
                pygame.quit()
        elif event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        constant_downwards = True
    else:
        constant_downwards = False

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        constant_left = True
    else:
        constant_left = False

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        constant_right = True
    else:
        constant_right = False
    
    if constant_downwards == True:
        if current_time - last_move_time >= move_interval:
            move_piece_down()
            score += 1
            last_move_time = current_time

    if constant_right == True:
        if current_time - last_move_time_right >= move_interval:
            move_piece_right()
            last_move_time_right = current_time

    if constant_left == True:
        if current_time - last_move_time_left >= move_interval:
            move_piece_left()
            last_move_time_left = current_time
            
    piece_hit_bottom_check()
    full_line_check()

    time_passed = math.floor(current_time-start_time)

    for i in range(height):
        for j in range(width):
            if isinstance(area[i][j],str):
                pygame.draw.rect(display, shape_colours[shape_number], (pixel_size*j,pixel_size*i,pixel_size,pixel_size))
            elif isinstance(area[i][j],int):
                pygame.draw.rect(display, shape_colours[area[i][j]], (pixel_size*j,pixel_size*i,pixel_size,pixel_size))

    text = textFont.render(f"Lines: {line_count}", True, (0,0,0))
    display.blit(text, (width*pixel_size +10, 10))
    text = textFont.render(f"Score: {score}", True, (0,0,0))
    display.blit(text, (width*pixel_size +10, 50))
    text = textFont.render("Press 'q'", True, (0,0,0))
    display.blit(text, (width*pixel_size +10, 90))
    text = textFont.render("to exit.", True, (0,0,0))
    display.blit(text, (width*pixel_size +10, 110))

    pygame.display.flip()
  except:
      True
print("HI")
loss_time = time.time()
current_time = time.time()
while current_time - loss_time < 5:
    current_time = time.time()
    display.blit(pygame.font.Font(None, 80).render("Game Over", True, (0,0,0)), ((width*pixel_size)//2 -100, (height*pixel_size)//2 -50))
    pygame.display.flip()

pygame.quit()













