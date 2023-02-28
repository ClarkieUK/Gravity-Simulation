import numpy as np

# get initial acceleration

# get velocity at half timestep

# get position using halftimestepped velocity

# -----------------



def leapfrog_kickdrif(pos_i,vel_i,timestep,acceleration_i) :
    v_i_half = vel_i + acceleration_i * timestep * 0.5

    position_1 = pos_i + v_i_half * timestep

    velocity_1 = v_i_half + acceleration_i_1 * timestep * 0.5# acceleration_i_1 = gmm/r^2 where r^2 is between new position (pos_1) and other object

def leapfrog_move() :
    pass