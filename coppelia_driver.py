try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')
import numpy as np

clientID = 0
cuboid_handle = 0
err_code = 0


def coppelia_connect():
    print('Program started')
    sim.simxFinish(-1)  # just in case, close all opened connections
    clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to CoppeliaSim
    return clientID


def coppelia_set_position(x, y, z):
    err_code, cuboid_handle = sim.simxGetObjectHandle(clientID, "Cuboid", sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(clientID, cuboid_handle, -1, (x, y, z), sim.simx_opmode_oneshot_wait)


def coppelia_get_position():
    err_code, cuboid_handle = sim.simxGetObjectHandle(clientID, "Cuboid", sim.simx_opmode_blocking)
    err_code, cuboid_position = sim.simxGetObjectPosition(clientID, cuboid_handle, -1, sim.simx_opmode_oneshot_wait)
    return cuboid_position


def coppelia_get_joint1_position():
    err_code, joint = sim.simxGetObjectHandle(clientID, "MTB_axis1", sim.simx_opmode_blocking)
    err_code, joint_position = sim.simxGetJointPosition(clientID, joint, sim.simx_opmode_oneshot_wait)
    return joint_position


def coppelia_get_joint2_position():
    err_code, joint = sim.simxGetObjectHandle(clientID, "MTB_axis2", sim.simx_opmode_blocking)
    err_code, joint_position = sim.simxGetJointPosition(clientID, joint, sim.simx_opmode_oneshot_wait)
    return joint_position


def coppelia_set_joint1_position(position_deg):
    err_code, joint = sim.simxGetObjectHandle(clientID, "MTB_axis1", sim.simx_opmode_blocking)
    sim.simxSetJointPosition(clientID, joint, np.deg2rad(position_deg), sim.simx_opmode_oneshot_wait)
    return err_code


def coppelia_set_joint2_position(position_deg):
    err_code, joint = sim.simxGetObjectHandle(clientID, "MTB_axis2", sim.simx_opmode_blocking)
    sim.simxSetJointPosition(clientID, joint, np.deg2rad(position_deg), sim.simx_opmode_oneshot_wait)
    return err_code


def coppelia_get_xy_position(theta1, theta2):
    x = 0.47 * np.cos(np.deg2rad(theta1)) + 0.4 * np.cos(np.deg2rad(theta1+theta2))
    y = 0.47 * np.sin(np.deg2rad(theta1)) + 0.4 * np.sin(np.deg2rad(theta1+theta2))
    return np.format_float_positional(x, precision=2), np.format_float_positional(y, precision=2)


