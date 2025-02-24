from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import argparse

import numpy as np
from controllers.pick_place import PickPlaceController
from isaacsim.core.api import World
from tasks.pick_place import PickPlace

parser = argparse.ArgumentParser()
parser.add_argument("--test", default=False, action="store_true", help="Run in test mode")
args, unknown = parser.parse_known_args()

my_world = World(stage_units_in_meters=1.0)


# target_position = np.array([-0.3, 0.6, 0.7])
target_position = np.array([0.8, 0.7, 1.0])
my_task = PickPlace(name="cs66_pick_place", target_position=target_position)

my_world.add_task(my_task)
my_world.reset()
my_cs66 = my_world.scene.get_object("cs_66")
# initialize the controller
my_controller = PickPlaceController(name="controller", robot_articulation=my_cs66, gripper=my_cs66.gripper)
task_params = my_world.get_task("cs66_pick_place").get_params()
articulation_controller = my_cs66.get_articulation_controller()
i = 0
reset_needed = False
while simulation_app.is_running():
    my_world.step(render=True)
    if my_world.is_stopped() and not reset_needed:
        reset_needed = True
    if my_world.is_playing():
        if reset_needed:
            my_world.reset()
            my_controller.reset()
            reset_needed = False
        observations = my_world.get_observations()
        # forward the observation values to the controller to get the actions
        actions = my_controller.forward(
            picking_position=observations[task_params["cube_name"]["value"]]["position"],
            placing_position=observations[task_params["cube_name"]["value"]]["target_position"],
            current_joint_positions=observations[task_params["robot_name"]["value"]]["joint_positions"],
            end_effector_offset=np.array([0, 0, 0]),
       
        )
        if my_controller.is_done():
            print("done picking and placing")
        articulation_controller.apply_action(actions)
    if args.test is True:
        break
simulation_app.close()
