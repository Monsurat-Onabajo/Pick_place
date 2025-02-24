# Copyright (c) 2022-2024, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

import os

# from isaacsim.core.utils.extensions import enable_extension
# enable_extension("isaacsim_robot_motion.motion_generation")


import isaacsim.robot_motion.motion_generation as mg
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.extensions import get_extension_path_from_name


class RMPFlowController(mg.MotionPolicyController):
    def __init__(self, name: str, robot_articulation: SingleArticulation, physics_dt: float = 1.0 / 60.0) -> None:
        self.rmpflow = mg.lula.motion_policies.RmpFlow(
            robot_description_path="rmpflow/robot_descriptor.yaml",
            rmpflow_config_path="rmpflow/cs66_rmpflow_common.yaml",
            urdf_path="/mnt/disk1/CS66urdf/urdf/CS66urdf.urdf",
            end_effector_frame_name="link6",
            # maximum_substep_size=0.00334
            maximum_substep_size=0.0334
        )

        self.articulation_rmp = mg.ArticulationMotionPolicy(robot_articulation, self.rmpflow, physics_dt)

        mg.MotionPolicyController.__init__(self, name=name, articulation_motion_policy=self.articulation_rmp)
        (
            self._default_position,
            self._default_orientation,
        ) = self._articulation_motion_policy._robot_articulation.get_world_pose()
        self._motion_policy.set_robot_base_pose(
            robot_position=self._default_position, robot_orientation=self._default_orientation
        )
        return

    def reset(self):
        mg.MotionPolicyController.reset(self)
        self._motion_policy.set_robot_base_pose(
            robot_position=self._default_position, robot_orientation=self._default_orientation
        )
