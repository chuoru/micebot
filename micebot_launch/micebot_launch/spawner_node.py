#!/usr/bin/env python3
##
# @file spawner.py
#
# @brief Provide a method to spawn models in gazebo
#
# @section author_doxygen_example Author(s)
# - Created by Tran Viet Thanh on 2024/10/16.
#
# Copyright (c) 2024 System Engineering Laboratory.  All rights reserved.

# Standard library
import os
import yaml

# External library
import rospy
import rospkg
from geometry_msgs.msg import Pose, PoseStamped
from gazebo_msgs.srv import SpawnModel, DeleteModel


class SpawnerNode(object):
    """! Class to spawn models in gazebo

    This class provides a method to spawn models in gazebo
    """
    # ==========================================================================
    # PUBLIC METHOD
    # ==========================================================================

    def __init__(self):
        """! Constructor for SpawnerNode class
        @return an instance of SpawnerNode class
        """
        super(SpawnerNode, self).__init__()

        rospy.init_node('spawner_node')

        self._load_parameters()

        self._register_clients()

    def run(self):
        """! Constructor for SpawnerNode class
        @return an instance of SpawnerNode class
        """
        for key, value in self._config.items():
            pose = Pose()

            pose.position.x = value["position"]["x"]

            pose.position.y = value["position"]["y"]

            pose.position.z = value["position"]["z"]

            self._spawn(key, value["model_name"], pose, "_spawn")

            rospy.loginfo(f"Spawned {key} at position {value['position']}")

    # ==========================================================================
    # PRIVATE METHOD
    # ==========================================================================
    def _register_clients(self):
        """! Register clients for this node
        """
        try:
            rospy.loginfo(
                "Waiting for service '/gazebo/spawn_sdf_model' to appear..")

            rospy.wait_for_service('/gazebo/spawn_sdf_model', timeout=5.0)

            self._spawn_model_client = rospy.ServiceProxy(
                '/gazebo/spawn_sdf_model', SpawnModel)

        except Exception as exception:
            rospy.logerr(exception)

        try:
            rospy.loginfo(
                "Waiting for service '/gazebo/delete_model' to appear..")

            rospy.wait_for_service('/gazebo/delete_model', timeout=5.0)

            self._delete_model_client = rospy.ServiceProxy(
                '/gazebo/delete_model', DeleteModel)

        except Exception as exception:
            rospy.logerr(exception)

    def _apply_table(self):
        """! Apply table to the scene
        """
        pose = PoseStamped()

        pose.pose.position.x = self._config["table"]["position"]["x"]

        pose.pose.position.y = self._config["table"]["position"]["y"]

        pose.pose.position.z = self._config["table"]["position"]["z"]

        pose.pose.orientation.w = 1.0

        pose.header.stamp = rospy.Time.now()

        pose.header.frame_id = "base_link"

        table_size = (self._config["table"]["size"]["x"], self._config["table"]
                      ["size"]["y"], self._config["table"]["size"]["z"])

        status = self._planner.add_objects_in_planning_scene(
            "table", pose, table_size)

        return status

    def _spawn(self, name, model_name, position, frame="world"):
        """! Constructor for SpawnerNode class
        @param name<string>: The name of model
        @param model_name<string>: The name of model
        @param position<Pose>: The position of model
        @param frame<string>: The frame of model
        @return an instance of SpawnerNode class
        """
        file_path = os.path.join(
            self._micebot_launch_path, "models", model_name, "model.sdf")

        model_xml = open(file_path, 'r').read()

        request = {
            "model_name": name,
            "model_xml": model_xml,
            "robot_namespace": '/foo',
            "initial_pose": position,
            "reference_frame": frame
        }

        self._spawn_model_client(**request)

    def _load_parameters(self):
        """! Load paramters for this node
        """
        self._config_file_path = rospy.get_param("~config")

        self._config = self._read_yaml_file(self._config_file_path)

        self._micebot_launch_path = rospkg.RosPack().get_path("micebot_launch")

        rospy.loginfo(f"Spawner configuration: {self._config}")

        rospy.loginfo("Successfully loaded parameters for node")

    # ==========================================================================
    # STATIC METHOD
    # ==========================================================================
    @staticmethod
    def _read_yaml_file(path):
        """! Read yaml file
        @param path<string>: The path to yaml file
        @return The data of yaml file
        """
        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)

            except yaml.YAMLError as e:
                rospy.logerr(e)

                return {}
