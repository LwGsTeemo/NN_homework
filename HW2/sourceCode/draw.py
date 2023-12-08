from matplotlib.patches import Circle

def read_coordinates_from_file(file_path):
    coordinates = []
    firstAndLast = []
    with open(file_path, 'r') as file:
        # 跳過前兩行
        for i in range(1):
            firstAndLast.append(next(file).strip())
        for i in range(2):
            x, y = map(int, next(file).strip().split(','))
            firstAndLast.append((x, y))
        # 讀取座標點
        for line in file:
            x, y = map(int, line.strip().split(','))
            coordinates.append((x, y))
    return coordinates,firstAndLast

def draw_map_and_circles(ax,coordinates,firstAndLast,posXY,mode=1):
    # fig, ax = plt.subplots()
    # Draw Map
    x_coordinates = [point[0] for point in coordinates]
    y_coordinates = [point[1] for point in coordinates]
    fx_c = [point[0] for point in firstAndLast[1:]]
    fy_c = [point[1] for point in firstAndLast[1:]]

    ax.plot(x_coordinates, y_coordinates, marker='o', linestyle='-', color='b', label='Map')
    ax.plot(fx_c,fy_c, marker='o', linestyle='-', color='r')
    
    # Draw Circles
    if mode == 1:
        for coord in posXY:
            x, y = coord
            circle = Circle((x, y), radius=3, edgecolor='r', facecolor='none')
            ax.add_patch(circle)
    elif mode == 2:
        x_coordinates = [point[0] for point in posXY]
        y_coordinates = [point[1] for point in posXY]
        ax.plot(x_coordinates, y_coordinates, marker='o', linestyle='-', color='purple')

    ax.set_aspect('equal', adjustable='box')
    # plt.grid(True)
    # plt.legend()

def draw_map(ax,coordinates,firstAndLast):
    # Draw Map
    x_coordinates = [point[0] for point in coordinates]
    y_coordinates = [point[1] for point in coordinates]
    fx_c = [point[0] for point in firstAndLast[1:]]
    fy_c = [point[1] for point in firstAndLast[1:]]

    ax.plot(x_coordinates, y_coordinates, marker='o', linestyle='-', color='b', label='Map')
    ax.plot(fx_c,fy_c, marker='o', linestyle='-', color='r')