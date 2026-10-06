import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import CellWorld.Actors.GlobalEntities.SimulationManager as simuc
import pygame

class GameScene(simuc.Simulation):
    
    def __init__(self):
        super().__init__()
        
    def initialize_game(self, path):
        super().initialize_game(path)
        bitmap_cursor2 = pygame.cursors.diamond
        pygame.mouse.set_cursor(bitmap_cursor2)
    
    def initialize_spawn(self):
        try:
            cells_types = self.game_manager.get_cell_types_names_list()
            for cell_type in cells_types:
                for i in range(30):
                    self.spawn_to_world(cell_type)
            
            cell_group = self.game_manager.get_group_prototype_with_name("namevd")
            self.spawn_to_world(cell_group)
        except Exception as e:
            print(f"Error while spawning initial cells: {e}")

sim = GameScene()
sim.initialize_game(r"CellWorld/Scene1.json")
sim.initialize_spawn()
sim.initialize_gui()
sim.main()
