import os
from typing import Optional

import isaacsim.core.api.tasks as tasks
import numpy as np
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.robot.manipulators import SingleManipulator
from isaacsim.robot.manipulators.grippers import ParallelGripper
from isaacsim.storage.native import get_assets_root_path


class PickPlace(tasks.PickPlace):
    def __init__(
        self,
        name: str = "cs66_pick_place",
        cube_initial_position: Optional[np.ndarray] = None,
        cube_initial_orientation: Optional[np.ndarray] = None,
        target_position: Optional[np.ndarray] = None,
        offset: Optional[np.ndarray] = None,
    ) -> None:
        tasks.PickPlace.__init__(
            self,
            name=name,
            cube_initial_position=np.array([0.6, 0.3, 0.85]),
            cube_initial_orientation=cube_initial_orientation,
            target_position=target_position,
            cube_size=np.array([0.1330, 0.1330, 0.0715]),
            offset=offset,
        )
        return

    def set_robot(self) -> SingleManipulator:
        assets_root_path = get_assets_root_path()
        if assets_root_path is None:
            raise Exception("Could not find Isaac Sim assets folder")
        asset_path= 'Collected_World2/World0.usd'

        add_reference_to_stage(usd_path=asset_path, prim_path="/World/World0")
        gripper = ParallelGripper(
            end_effector_prim_path="/World/World0/Robotiq_2F_140_physics_edit/robotiq_base_link",
            joint_prim_names=["finger_joint", "right_outer_knuckle_joint"],
            joint_opened_positions=np.array([0, 0]),
            joint_closed_positions=np.array([0.628, -0.628]),
            action_deltas=np.array([-0.628, 0.628])
        )

        manipulator= SingleManipulator(
            prim_path="/World/World0/CS66urdf",
            name="cs_66",
            end_effector_prim_path="/World/World0/Robotiq_2F_140_physics_edit/robotiq_base_link",
            gripper=gripper,
            )

        joints_default_positions = np.zeros(14)
        joints_default_positions[1] = -1.57 -0.3
        joints_default_positions[2] =  0.3
        joints_default_positions[6] = 0.0
        joints_default_positions[7] = 0.0
        manipulator.set_joints_default_state(positions=joints_default_positions)
        return manipulator
