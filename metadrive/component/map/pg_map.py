from typing import List
import copy

from metadrive.component.algorithm.BIG import BigGenerateMethod, BIG
from metadrive.component.algorithm.blocks_prob_dist import PGBlockDistConfig
from metadrive.component.map.base_map import BaseMap
from metadrive.component.pgblock.first_block import FirstPGBlock
from metadrive.component.road_network.node_road_network import NodeRoadNetwork
from metadrive.engine.core.physics_world import PhysicsWorld
from metadrive.utils import Config
from panda3d.core import NodePath


def parse_map_config(easy_map_config, new_map_config, default_config):
    assert isinstance(new_map_config, Config)
    assert isinstance(default_config, Config)

    # Return the user specified config if overwritten
    if not default_config["map_config"].is_identical(new_map_config):
        new_map_config = default_config["map_config"].copy(unchangeable=False).update(new_map_config)
        assert default_config["map"] == easy_map_config
        return new_map_config

    if isinstance(easy_map_config, int):
        new_map_config[BaseMap.GENERATE_TYPE] = BigGenerateMethod.BLOCK_NUM
    elif isinstance(easy_map_config, str):
        new_map_config[BaseMap.GENERATE_TYPE] = BigGenerateMethod.BLOCK_SEQUENCE
    else:
        raise ValueError(
            "Unkown easy map config: {} and original map config: {}".format(easy_map_config, new_map_config)
        )
    new_map_config[BaseMap.GENERATE_CONFIG] = easy_map_config
    return new_map_config


class MapGenerateMethod:
    BIG_BLOCK_NUM = BigGenerateMethod.BLOCK_NUM
    BIG_BLOCK_SEQUENCE = BigGenerateMethod.BLOCK_SEQUENCE
    BIG_SINGLE_BLOCK = BigGenerateMethod.SINGLE_BLOCK
    PG_MAP_FILE = "pg_map_file"


class PGMap(BaseMap):
    def _generate(self):
        """
        We can override this function to introduce other methods!
        """
        parent_node_path, physics_world = self.engine.worldNP, self.engine.physics_world
        generate_type = self._config[self.GENERATE_TYPE]
        if generate_type == BigGenerateMethod.BLOCK_NUM or generate_type == BigGenerateMethod.BLOCK_SEQUENCE:
            self._big_generate(parent_node_path, physics_world)

        elif generate_type == MapGenerateMethod.PG_MAP_FILE:
            # other config such as lane width, num and seed will be valid, since they will be read from file
            blocks_config = self._config[self.GENERATE_CONFIG]
            self._config_generate(blocks_config, parent_node_path, physics_world)
        else:
            raise ValueError("Map can not be created by {}".format(generate_type))
        self.road_network.after_init()

    def _big_generate(self, parent_node_path: NodePath, physics_world: PhysicsWorld):
        big_map = BIG(
            self._config[self.LANE_NUM],
            self._config[self.LANE_WIDTH],
            self.road_network,
            parent_node_path,
            physics_world,
            # self._config["block_type_version"],
            exit_length=self._config["exit_length"],
            random_seed=self.engine.global_random_seed,
            block_dist_config=self.engine.global_config["block_dist_config"]
        )
        big_map.generate(self._config[self.GENERATE_TYPE], self._config[self.GENERATE_CONFIG])
        self.blocks = big_map.blocks

    def _config_generate(self, blocks_config: List, parent_node_path: NodePath, physics_world: PhysicsWorld):
        assert len(self.road_network.graph) == 0, "These Map is not empty, please create a new map to read config"
        last_block = FirstPGBlock(
            global_network=self.road_network,
            lane_width=self._config[self.LANE_WIDTH],
            lane_num=self._config[self.LANE_NUM],
            render_root_np=parent_node_path,
            physics_world=physics_world,
            length=self._config["exit_length"],
            ignore_intersection_checking=True
        )
        self.blocks.append(last_block)
        for block_index, b in enumerate(blocks_config[1:], 1):
            block_type = self.engine.global_config["block_dist_config"].get_block(b.pop(self.BLOCK_ID))
            pre_block_socket_index = b.pop(self.PRE_BLOCK_SOCKET_INDEX)
            last_block = block_type(
                block_index,
                last_block.get_socket(pre_block_socket_index),
                self.road_network,
                random_seed=self.engine.global_random_seed,
                ignore_intersection_checking=True
            )
            last_block.construct_from_config(b, parent_node_path, physics_world)
            self.blocks.append(last_block)

    @property
    def road_network_type(self):
        return NodeRoadNetwork

    def get_meta_data(self):
        assert self.blocks is not None and len(self.blocks) > 0, "Please generate Map before saving it"
        map_config = []
        for b in self.blocks:
            b_config = b.get_config()
            json_config = b_config.get_serializable_dict()
            json_config[self.BLOCK_ID] = b.ID
            json_config[self.PRE_BLOCK_SOCKET_INDEX] = b.pre_block_socket_index
            map_config.append(json_config)

        saved_data = copy.deepcopy({self.BLOCK_SEQUENCE: map_config, "map_config": self.config.copy()})
        return saved_data
