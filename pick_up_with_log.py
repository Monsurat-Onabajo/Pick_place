# from isaacsim import SimulationApp
# simulation_app = SimulationApp({"headless": False})

# import argparse
# import numpy as np
# import os
# import pandas as pd  # For saving CSV
# from PIL import Image  # For saving images

# from controllers.pick_place import PickPlaceController
# from isaacsim.core.api import World
# from tasks.pick_place import PickPlace
# from isaacsim.sensors.camera import Camera

# # Argument parser
# parser = argparse.ArgumentParser()
# parser.add_argument("--test", default=False, action="store_true", help="Run in test mode")
# args, unknown = parser.parse_known_args()

# # Create world and task
# my_world = World(stage_units_in_meters=1.0)
# target_position = np.array([0.8, 0.7, 1.0])  # Target cube placement position
# my_task = PickPlace(name="cs66_pick_place", target_position=target_position)

# my_world.add_task(my_task)
# my_world.reset()

# # Get robot
# my_cs66 = my_world.scene.get_object("cs_66")

# # Initialize the controller
# my_controller = PickPlaceController(name="controller", robot_articulation=my_cs66, gripper=my_cs66.gripper)
# task_params = my_world.get_task("cs66_pick_place").get_params()
# articulation_controller = my_cs66.get_articulation_controller()

# # --- Initialize Camera from USD ---
# camera_prim_path = "/World/World0/Camera_side"
# camera = Camera(prim_path=camera_prim_path,
#                 resolution=(1920, 1920)
#                 )  
# camera.initialize()


# # --- Create Image Save Directory ---
# image_save_dir = "images"
# if not os.path.exists(image_save_dir):
#     os.makedirs(image_save_dir)
#     print(f"Created directory: {image_save_dir}")

# # --- Logging Setup ---
# log_data = {
#     "time": [],
#     "joint_positions": [],
#     "gripper_state": [],
#     "cube_position": [],
#     "target_position": [],
#     "actions": [],
#     "image_paths": []
# }

# # Simulation loop
# reset_needed = False
# step_counter = 0

# while simulation_app.is_running():
#     my_world.step(render=True)

#     if my_world.is_stopped() and not reset_needed:
#         reset_needed = True

#     if my_world.is_playing():
#         if reset_needed:
#             my_world.reset()
#             my_controller.reset()
#             reset_needed = False

#         # Get observations
#         observations = my_world.get_observations()

#         # Extract relevant data
#         joint_positions = observations[task_params["robot_name"]["value"]]["joint_positions"]
#         gripper_state = my_cs66.gripper.get_joint_positions()  # Assuming gripper state is last joint
#         cube_position = observations[task_params["cube_name"]["value"]]["position"]

#         # Get actions from controller
#         actions = my_controller.forward(
#             picking_position=cube_position,
#             placing_position=observations[task_params["cube_name"]["value"]]["target_position"],
#             current_joint_positions=joint_positions,
#             end_effector_offset=np.array([0, 0, 0]),
#         )

#         if step_counter % 10 == 0:
#             rgb_image = camera.get_rgb()  # Get raw image

#             # Save the raw NumPy array directly
#             image_path = f"{image_save_dir}/frame_{step_counter}.npy"
#             np.save(image_path, rgb_image)

#             print(f"✅ Image saved as raw NumPy array: {image_path}")

       

#         # --- Log Data ---
#         log_data["time"].append(step_counter)
#         log_data["joint_positions"].append(joint_positions.tolist())  # Convert to list for safe storage
#         log_data["gripper_state"].append(gripper_state.tolist())  # Convert to list
#         log_data["cube_position"].append(cube_position.tolist())  # Convert to list
#         log_data["target_position"].append(target_position.tolist())  # Convert to list
#         log_data["actions"].append(vars(actions))  # Convert ArticulationAction to a dictionary
#         log_data["image_paths"].append(image_path)  # Store image path if captured

#         step_counter += 1  # Increment step count

#         if my_controller.is_done():
#             print("Done picking and placing")
#             break  # Stop when task is completed

#         articulation_controller.apply_action(actions)

#     if args.test is True:
#         break

# # --- Save Logs ---
# save_path_npy = "simulation_logs.npy"
# save_path_csv = "simulation_logs.csv"

# # Save as NumPy file
# np.save(save_path_npy, log_data)
# print(f"Simulation logs saved to {save_path_npy}")

# # Convert to DataFrame and save as CSV
# df = pd.DataFrame({
#     "time": log_data["time"],
#     "joint_positions": [str(jp) for jp in log_data["joint_positions"]],  # Convert list to string for CSV
#     "gripper_state": [str(gs) for gs in log_data["gripper_state"]],
#     "cube_position": [str(cp) for cp in log_data["cube_position"]],
#     "target_position": [str(tp) for tp in log_data["target_position"]],
#     "actions": [str(ac) for ac in log_data["actions"]],
#     "image_paths": [str(ip) for ip in log_data["image_paths"]]  # Save image paths
# })
# df.to_csv(save_path_csv, index=False)
# print(f"Simulation logs also saved to {save_path_csv}")

# simulation_app.close()



from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import argparse
import numpy as np
import os
import pandas as pd  # For saving CSV
from isaacsim.sensors.camera import Camera

from controllers.pick_place import PickPlaceController
from isaacsim.core.api import World
from tasks.pick_place import PickPlace
from isaacsim.sensors.camera import Camera

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--test", default=False, action="store_true", help="Run in test mode")
args, unknown = parser.parse_known_args()

# Create world and task
my_world = World(stage_units_in_meters=1.0)
target_position = np.array([0.8, 0.7, 1.0])
my_task = PickPlace(name="cs66_pick_place", target_position=target_position)

my_world.add_task(my_task)
my_world.reset()

# Get robot
my_cs66 = my_world.scene.get_object("cs_66")

# Initialize the controller
my_controller = PickPlaceController(name="controller", robot_articulation=my_cs66, gripper=my_cs66.gripper)
task_params = my_world.get_task("cs66_pick_place").get_params()
articulation_controller = my_cs66.get_articulation_controller()

# --- Initialize Two Cameras from USD ---
camera1_prim_path = "/World/World0/Camera_side"
camera2_prim_path = "/World/World0/Camera_side_02" 

camera1 = Camera(prim_path=camera1_prim_path, resolution=(1920, 1920))
camera2 = Camera(prim_path=camera2_prim_path, resolution=(1920, 1920))

camera1.initialize()
camera2.initialize()

# --- Create Separate Image Save Directories ---
image_save_dir_1 = "images/camera1"
image_save_dir_2 = "images/camera2"

os.makedirs(image_save_dir_1, exist_ok=True)
os.makedirs(image_save_dir_2, exist_ok=True)

print(f"Created directories: {image_save_dir_1}, {image_save_dir_2}")

# --- Logging Setup ---
log_data = {
    "time": [],
    "joint_positions": [],
    "gripper_state": [],
    "cube_position": [],
    "target_position": [],
    "actions": [],
    "camera1_image_paths": [],
    "camera2_image_paths": [],
}

# Simulation loop
reset_needed = False
step_counter = 0

while simulation_app.is_running():
    my_world.step(render=True)

    if my_world.is_stopped() and not reset_needed:
        reset_needed = True

    if my_world.is_playing():
        if reset_needed:
            my_world.reset()
            my_controller.reset()
            reset_needed = False

        # Get observations
        observations = my_world.get_observations()
        joint_positions = observations[task_params["robot_name"]["value"]]["joint_positions"]
        gripper_state = my_cs66.gripper.get_joint_positions()
        cube_position = observations[task_params["cube_name"]["value"]]["position"]

        # Get actions from controller
        actions = my_controller.forward(
            picking_position=cube_position,
            placing_position=observations[task_params["cube_name"]["value"]]["target_position"],
            current_joint_positions=joint_positions,
            end_effector_offset=np.array([0, 0, 0]),
        )

        # --- Capture from Both Cameras Every 10 Steps ---
        if step_counter % 10 == 0:
            # Capture from Camera 1
            rgb_image_1 = camera1.get_rgb()
            image_path_1 = f"{image_save_dir_1}/frame_{step_counter}.npy"
            np.save(image_path_1, rgb_image_1)

            # Capture from Camera 2
            rgb_image_2 = camera2.get_rgb()
            image_path_2 = f"{image_save_dir_2}/frame_{step_counter}.npy"
            np.save(image_path_2, rgb_image_2)
        if step_counter % 50 == 0:
            print(f"✅ Images saved up to: {image_path_1}, {image_path_2}")

        # --- Log Data ---
        log_data["time"].append(step_counter)
        log_data["joint_positions"].append(joint_positions.tolist())
        log_data["gripper_state"].append(gripper_state.tolist())
        log_data["cube_position"].append(cube_position.tolist())
        log_data["target_position"].append(target_position.tolist())
        log_data["actions"].append(vars(actions))
        log_data["camera1_image_paths"].append(image_path_1)
        log_data["camera2_image_paths"].append(image_path_2)

        step_counter += 1  # Increment step count

        if my_controller.is_done():
            print("Done picking and placing")
            break

        articulation_controller.apply_action(actions)

    if args.test is True:
        break

# --- Save Logs ---
save_path_npy = "simulation_logs.npy"
save_path_csv = "simulation_logs.csv"

np.save(save_path_npy, log_data)
print(f"Simulation logs saved to {save_path_npy}")

df = pd.DataFrame({
    "time": log_data["time"],
    "joint_positions": [str(jp) for jp in log_data["joint_positions"]],
    "gripper_state": [str(gs) for gs in log_data["gripper_state"]],
    "cube_position": [str(cp) for cp in log_data["cube_position"]],
    "target_position": [str(tp) for tp in log_data["target_position"]],
    "actions": [str(ac) for ac in log_data["actions"]],
    "camera1_image_paths": [str(ip) for ip in log_data["camera1_image_paths"]],
    "camera2_image_paths": [str(ip) for ip in log_data["camera2_image_paths"]],
})
df.to_csv(save_path_csv, index=False)
print(f"Simulation logs also saved to {save_path_csv}")

simulation_app.close()
