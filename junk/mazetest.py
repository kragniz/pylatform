import random
#http://amertune.blogspot.com/2008/12/maze-generation-in-python.html
width, height = 10, 10

# create a list of all walls 
# (all connections between squares in the maze)
# add all of the vertical walls into the list
walls = [(x,y,x+1,y)
    for x in range(width-1)
    for y in range(height)]
# add all of the horizontal walls into the list
walls.extend([(x,y,x,y+1)
    for x in range(width)
    for y in range(height-1)])

# create a set for each square in the maze
cell_sets = [set([(x,y)])
    for x in range(width)
    for y in range(height)]

cells = [[1
    for x in range(width)]
    for y in range(height)]

# in Kruskal's algorithm, the walls need to be
# visited in order of weight
# since we want a random maze, we will shuffle 
# it and pretend that they are sorted by weight
walls_copy = walls[:]
random.shuffle(walls_copy)

for wall in walls_copy:
    set_a = None
    set_b = None

    # find the sets that contain the squares
    # that are connected by the wall
    for s in cell_sets:
        if (wall[0], wall[1]) in s:
            set_a = s
        if (wall[2], wall[3]) in s:
            set_b = s

    # if the two squares are in separate sets,
    # then combine the sets and remove the 
    # wall that connected them
    if set_a is not set_b:
        cell_sets.remove(set_a)
        cell_sets.remove(set_b)
        cell_sets.append(set_a.union(set_b))
        walls.remove(wall)
        print set_a, set_b
        cells
print cells