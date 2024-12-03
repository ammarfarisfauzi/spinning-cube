from math import sin, cos
from time import sleep

CUBE_SIZE = 10
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 33
BACKGROUND_CHAR = ' '
DISTANCE_FROM_CAMERA = 100
K1 = 40
ROTATION_SPEED = 0.6

frame_buffer = [BACKGROUND_CHAR] * (SCREEN_WIDTH * SCREEN_HEIGHT)
z_buffer = [0] * (SCREEN_WIDTH * SCREEN_HEIGHT * 4)

rotation_x = 0.0
rotation_y = 0.0
rotation_z = 0.0

def initialize_buffers():
    """Reset frame and Z buffers for each frame."""
    global frame_buffer, z_buffer
    frame_buffer = [BACKGROUND_CHAR] * (SCREEN_WIDTH * SCREEN_HEIGHT)
    z_buffer = [0] * (SCREEN_WIDTH * SCREEN_HEIGHT * 4)

def render_frame():
    """Render the current frame to the screen."""
    print("\x1b[H", end='') 
    for i in range(SCREEN_WIDTH * SCREEN_HEIGHT):
        if i % SCREEN_WIDTH != 0:
            print(frame_buffer[i], end='')
        else:
            print()

def project_cube():
    """Project a rotating cube onto the screen."""
    global rotation_x, rotation_y, rotation_z
    cube_x = -CUBE_SIZE
    while cube_x < CUBE_SIZE:
        cube_x += ROTATION_SPEED
        cube_y = -CUBE_SIZE
        while cube_y < CUBE_SIZE:
            cube_y += ROTATION_SPEED
            project_face(cube_x, cube_y, -CUBE_SIZE, '@')  
            project_face(CUBE_SIZE, cube_y, cube_x, '$')   
            project_face(-CUBE_SIZE, cube_y, -cube_x, '#')
            project_face(-cube_x, cube_y, CUBE_SIZE, '~') 
            project_face(cube_x, -CUBE_SIZE, -cube_y, ';')
            project_face(cube_x, CUBE_SIZE, cube_y, '+')   

def project_face(x, y, z, char):
    """Calculate the projection of a single face of the cube."""
    transformed_x = transform_x(x, y, z)
    transformed_y = transform_y(x, y, z)
    transformed_z = transform_z(x, y, z) + DISTANCE_FROM_CAMERA

    ooz = 1 / transformed_z
    horizontal_offset = 2 * CUBE_SIZE
    screen_x = int(SCREEN_WIDTH / 2 - horizontal_offset + K1 * ooz * transformed_x * 2)
    screen_y = int(SCREEN_HEIGHT / 2 + K1 * ooz * transformed_y)
    buffer_index = screen_x + screen_y * SCREEN_WIDTH

    if 0 <= buffer_index < SCREEN_WIDTH * SCREEN_HEIGHT and ooz > z_buffer[buffer_index]:
        z_buffer[buffer_index] = ooz
        frame_buffer[buffer_index] = char

def transform_x(i, j, k):
    """Apply rotation transformations to the x-coordinate."""
    global rotation_x, rotation_y, rotation_z
    return (j * sin(rotation_x) * sin(rotation_y) * cos(rotation_z) -
            k * cos(rotation_x) * sin(rotation_y) * cos(rotation_z) +
            j * cos(rotation_x) * sin(rotation_z) +
            k * sin(rotation_x) * sin(rotation_z) +
            i * cos(rotation_y) * cos(rotation_z))

def transform_y(i, j, k):
    """Apply rotation transformations to the y-coordinate."""
    global rotation_x, rotation_y, rotation_z
    return (j * cos(rotation_x) * cos(rotation_z) +
            k * sin(rotation_x) * cos(rotation_z) -
            j * sin(rotation_x) * sin(rotation_y) * sin(rotation_z) +
            k * cos(rotation_x) * sin(rotation_y) * sin(rotation_z) -
            i * cos(rotation_y) * sin(rotation_z))

def transform_z(i, j, k):
    """Apply rotation transformations to the z-coordinate."""
    global rotation_x, rotation_y, rotation_z
    return (k * cos(rotation_x) * cos(rotation_y) -
            j * sin(rotation_x) * cos(rotation_y) +
            i * sin(rotation_y))

def main():
    """Main loop to animate the rotating cube."""
    global rotation_x, rotation_z
    print("\x1b[2J")  

    while True:
        initialize_buffers()
        project_cube()
        render_frame()
        rotation_x += 0.1
        rotation_z += 0.1
        sleep(0.01)

if __name__ == "__main__":
    main()
