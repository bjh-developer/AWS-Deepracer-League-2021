import math

def reward_function(params):
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    center_variance = params["distance_from_center"] / params["track_width"]
    #racing line
    left_lane = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 43, 50, 53, 64, 69]#Fill in the waypoints
    
    center_lane = [1, 2, 3, 4, 5, 6, 7, 8, 9, 28, 37, 55]#Fill in the waypoints
    
    right_lane = []#Fill in the waypoints
    
    #Speed
    fast = [1, 2, 3, 4, 5, 6, 7, 8, 9, 28, 37, 55]#Fill in the waypoints, 2m/s
    slow = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 43, 50, 53, 64, 69]#Fill in the waypoints, 1m/s
    
    reward = 1e-3

    rabbit = [0,0]
    pointing = [0,0]
    x = params['x']
    y = params['y']

    rabbit = waypoints[closest_waypoints[1]]
    radius = math.hypot(x - rabbit [0], y - rabbit[1])

    pointing[0] = x + (radius * math.cos(heading))
    pointing[1] = y + (radius * math.sin(heading))

    vector_delta = math.hypot(pointing[0] - rabbit[0], pointing[1] - rabbit[1])

    if vector_delta == 0:
        reward += 1
    else:
        reward += (1 - (vector_delta / (radius*2)))

    if not params['all_wheels_on_track']:
        reward -= 5
    elif params['progress'] == 1:
        reward = 10

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10
    if params["closest_waypoints"][1] in fast:
        if params["speed"] >= 1.5 and params['speed'] < 2.0 :
            reward += 5
        else:
            reward -= 10
    elif params["closest_waypoints"][1] in slow:
        if params["speed"] < 1 and params['speed'] > 0.4:
            reward += 5
        else:
            reward -= 10
        
    
    return float(reward)