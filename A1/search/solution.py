#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def dead_state(state):
  '''
  Whether the state has one or more dead boxes (boxes thath can not be moved to the storage).
  @return: True if it's a dead state; False otherwise
  '''
  for box in state.boxes:
    # Check if the box reaches the storage location.
    if box in state.storage:
      continue

    upper = box[1] == 0
    lower = box[1] == (state.height - 1)
    left = box[0] == 0
    right = box[0] == (state.width - 1)
    blocks = state.obstacles|state.boxes

    # Check whether the box is in the corner.
    # upper_wall = box[1] == 0 or (box[0], box[1] - 1) in state.obstacles
    # lower_wall  = box[1] == (state.height - 1) or (box[0], box[1] + 1) in state.obstacles
    # left_wall  = box[0] == 0 or (box[0] - 1, box[1]) in state.obstacles
    # right_wall  = box[0] == (state.width - 1) or (box[0] + 1, box[1]) in state.obstacles
    # if (upper_wall or lower_wall) and (left_wall or right_wall):
    #   return True


    # Check whether the box is along the wall and has a box or obstacles next to it
    if upper or lower:
      if (box[0] - 1, box[1]) in blocks or (box[0] + 1, box[1]) in blocks:
        return True
    elif left or right:
      if (box[0], box[1] - 1) in blocks or (box[0], box[1] + 1) in blocks:
        return True 


    # Check whether the box is surrounded by boxes or obstacles
    upper_block = upper or (box[0], box[1] - 1) in blocks
    lower_block = lower or (box[0], box[1] + 1) in blocks
    left_block = left or (box[0] - 1, box[1]) in blocks
    right_block = right or (box[0] + 1, box[1]) in blocks
    upper_left_block = upper or left or (box[0] - 1, box[1] - 1) in blocks
    upper_right_block = upper or right or (box[0] + 1, box[1] - 1) in blocks
    lower_left_block = lower or left or (box[0] - 1, box[1] + 1) in blocks
    lower_right_block = lower or right or (box[0] + 1, box[1] + 1) in blocks
    if upper_block:
      if left_block and upper_left_block:
        return True
      elif right_block and upper_right_block:
        return True
    elif lower_block:
      if left_block and lower_left_block:
        return True
      elif right_block and lower_right_block:
        return True

    # Check if the box is beside the wall and there is a storage along the wall
    found = False
    if upper or lower:
      for storage in state.storage:
        if storage[1] == box[1]:
          found = True
          break
      if not found:
        return True
    elif left or right:
      for storage in state.storage:
        if storage[0] == box[0]:
          found = True
          break
      if not found:
        return True

  return False


def number_of_obstacles(state, obj, dest):
  '''
  Calculate the number of obstacles on the path for obj to destination.
  @obj: robot's location
  @dest: tuple of location
  @return: numbet of obstacles
  '''
  blocks = state.obstacles|state.boxes|frozenset(state.robots)
  num_obstacles = 0

  for block in blocks:
    if min(obj[0], dest[0]) < block[0] < max(obj[0], dest[0]):
      if min(obj[1], dest[1]) < block[1] < max(obj[1], dest[1]):
        num_obstacles = num_obstacles + 1
  
  return num_obstacles

def storage_remain(state):
  '''
  @return: the avaliable storage of the state
  '''
  remain = []
  for storage in state.storage:
    remain.append(storage)
  for box in state.boxes:
    if box in remain:
      remain.remove(box)
  
  return remain

    

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    distance = 0

    for box in state.boxes:
      nearest = None
      for storage in state.storage:
        distance_between = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
        if nearest is None or nearest > distance_between:
          nearest = distance_between
      distance = distance + nearest 

    return distance


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    # If the state is a dead state, h(state) = infinity
    if dead_state(state):
      return float("inf")

    cost = 0

    # Calculate the cost of robots move to the closest box
    for robot in state.robots:
      closest_distance = float("inf")
      for box in state.boxes:
        # if box in state.storage: # exclude the box in the storage 
        #   continue
        distance = abs(box[0] - robot[0]) + abs(box[1] - robot[1]) + 2 * number_of_obstacles(state, robot, box)
        if distance < closest_distance:
          closest_distance = distance
      cost = cost + closest_distance
    
    # Calculate the cost of box move to the closest storage
    for box in state.boxes:
      closest_distance = float("inf")
      for storage in state.storage:
        distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1]) + 2 * number_of_obstacles(state, box, storage)
        if distance < closest_distance:
          closest_distance = distance
      cost = cost + closest_distance

    return cost

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return sN.gval + weight * sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  initial_time = os.times()[0]
  end_time = initial_time + timebound

  wrapped_fval_function = (lambda sN : fval_function(sN,weight))
  searcher = SearchEngine('custom', 'full')
  searcher.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

  t_left = end_time - os.times()[0] #time left

  optimal = searcher.search(t_left)
  solution = optimal

  if not optimal:  # No solution, return False
    return False

  f_cost = optimal.gval + heur_fn(optimal)
  c_bound = (optimal.gval, float("inf"), f_cost)

  while t_left > 0 and not searcher.open.empty(): # continue searching
    weight = weight * 0.75 # decreasing weight by 25%
    wrapped_fval_function = (lambda sN : fval_function(sN,weight))

    solution = searcher.search(t_left, c_bound)

    if solution:
      if solution.gval < optimal.gval:
        optimal = solution
        f_cost = optimal.gval + heur_fn(optimal)
        c_bound = (optimal.gval, float("inf"), f_cost)
    else:
      return optimal

    t_left = end_time - os.times()[0]

  return optimal



def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  initial_time = os.times()[0]
  end_time = initial_time + timebound

  searcher = SearchEngine('best_first', 'full')
  searcher.init_search(initial_state, sokoban_goal_state, heur_fn)

  t_left = end_time - os.times()[0] #time left

  optimal = searcher.search(t_left)

  if not optimal:  # No solution, return False
    return False

  c_bound = (optimal.gval, float("inf"), float("inf"))

  while t_left > 0 and not searcher.open.empty(): # continue searching
    solution = searcher.search(t_left, c_bound)

    if solution: 
      if solution.gval < optimal.gval:
        optimal = solution
        c_bound = (optimal.gval, float("inf"), float("inf"))
    else:
      return optimal
    t_left = end_time - os.times()[0]

  return optimal
