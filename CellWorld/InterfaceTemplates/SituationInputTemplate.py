import pygame
from pygame import Vector2
import CellWorld.Tools.Logger.loggers as lg
from CellWorld.Actors.GUI.Button import Button
from CellWorld.Actors.GUI.Icon import Icon
from CellWorld.Actors.GUI.Checkbox import Checkbox
from CellWorld.Actors.GUI.Frame import Frame
from CellWorld.Actors.GUI.Graph import Graph
from CellWorld.Actors.GUI.TextInput import TextInput
import CellWorld.Tools.StaticLib as static

_logger = lg.get_module_logger("GUI")

def create_cell_window(gui_manager, saver_manager=None, sim_manager=None):
    sim_manager.pointer_is_busy = True
    create_cell_frame = Frame("login_frame", (300, 200), (300, 400), (47,41,75), "create_cell")
    name_input = TextInput("name", (0, 0), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Название клетки", "create_cell")
    create_cell_frame.add(name_input)
    
    mass = TextInput("cell_mass", (0, -40), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Вес клетки (float)", "create_cell", type_name=float)
    create_cell_frame.add(mass)
    
    strength = TextInput("strength", (0, -80), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Сила клетки (float)", "create_cell", type_name=float)
    create_cell_frame.add(strength)
    
    hunger_border = TextInput("hunger_border", (0, -120), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Когда голодает (float)", "create_cell", type_name=float)
    create_cell_frame.add(hunger_border)
    
    food_names = TextInput("food", (0, -160), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Кого ест (перечислить через запятую)", "create_cell")
    create_cell_frame.add(food_names)
    
    relationship = TextInput("relationship", (0, -200), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Отношения (клетка:отношение)", "create_cell")
    create_cell_frame.add(relationship)
    
    friendship = TextInput("friendship", (0, -240), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Друзья (клетка:отношение)", "create_cell")
    create_cell_frame.add(friendship)
    
    can_move = Checkbox("can_move", "Может двигаться?", (0, -280), (20, 20), 
                             (255, 255, 255), (240, 240, 240), True, "create_cell")
    create_cell_frame.add(can_move)
    can_die = Checkbox("is_mortal", "Может умереть?", (0, -320), (20, 20), 
                             (255, 255, 255), (240, 240, 240), True, "create_cell")
    create_cell_frame.add(can_die)
    
    def submit_login():
        form_data = gui_manager.get_form_data("create_cell")
        saver_manager.save_cell(form_data)
        create_cell_frame.status = "killed"
        
    submit_btn = Button("submit", "Создать клетку", (0, -370), (100, 40), (109, 118, 224), 
                       (255, 255, 255), "create_cell")
    submit_btn.set_handler(submit_login)
    create_cell_frame.add(submit_btn)
    
    def kill_window():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        
    kill_btn = Button("kill", "Закрыть окно", (0, -420), (100, 40), (224, 121, 109), 
                       (255, 255, 255), "create_cell")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    
    gui_manager.add(create_cell_frame)
    return gui_manager

def del_cell_window(gui_manager, saver_manager=None, sim_manager=None):
    sim_manager.pointer_is_busy = True
    create_cell_frame = Frame("del_form", (300, 200), (300, 140), (47,41,75), "del_cell")
    name_input = TextInput("name", (0, 0), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Название клетки", "del_cell")
    create_cell_frame.add(name_input)
    
    def submit_login():
        form_data = gui_manager.get_form_data("del_cell")
        saver_manager.del_cell(form_data.get("name"))
        create_cell_frame.status = "killed"
        
    submit_btn = Button("submit", "Удалить клетку", (0, -40), (100, 40), (109, 118, 224), 
                       (255, 255, 255), "del_cell")
    submit_btn.set_handler(submit_login)
    create_cell_frame.add(submit_btn)
    
    def kill_window():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        
    kill_btn = Button("kill", "Закрыть окно", (0, -90), (100, 40), (224, 121, 109), 
                       (255, 255, 255), "del_cell")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    gui_manager.add(create_cell_frame)
    return gui_manager

def change_cell_to_control(gui_manager, sim_manager):
    sim_manager.open_control_cell_tab()
    sim_manager.pointer_is_busy = True
    change_cell_frame = Frame("control_form", (300, 200), (300, 130), (47,41,75), "control", padding = 10, offset = 10, board_pad =2)
    
    select = Icon("submit", "Выбрать клетку", (0, -10), (40, 40), (109, 118, 224), 
                       (255, 255, 255), "control")
    def select_cell_here():
        sim_manager.select_current_cell()
        change_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        
    select.set_handler(select_cell_here)
    change_cell_frame.add(select)
    
    next = Icon("submit", "Следующая клетка", (0, -40), (40, 30), (55,51,86), 
                       (255, 255, 255), "control")
    def next_cell():
        sim_manager.change_control_cell(1)
    next.set_handler(next_cell)
    change_cell_frame.add(next)
    
    prev = Icon("submit", "Предыдущая клетка", (0, -80), (40, 30), (55,51,86), 
                       (255, 255, 255), "control")
    def prev_cell():
        sim_manager.change_control_cell(-1)
    prev.set_handler(prev_cell)
    change_cell_frame.add(prev)
    
    gui_manager.add(change_cell_frame)
    return gui_manager

def spawner_window(gui_manager, game_manager, sim_manager, console_manager):
    if console_manager:
        console_manager.console_print("Info - Interface - Spawner opened")
    
    sim_manager.pointer_is_busy = True
    sim_manager.is_window_spawn = True
    create_cell_frame = Frame("del_form", (300, 200), (300, 100), (47,41,75), "create_cell_to_world")
    name_input = TextInput("name", (0, 0), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Название клетки", "create_cell_to_world")
    create_cell_frame.add(name_input)
    
    def submit_login():
        form_data:dict = gui_manager.get_form_data("create_cell_to_world")
        sim_manager.cell_type_name = form_data.get("name", "")

    name_input.set_handler(submit_login)
    
    def kill_window():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        sim_manager.is_window_spawn = False
        sim_manager.cell_type_name = None
        
    kill_btn = Button("kill", "Закрыть окно", (0, -90), (100, 40), (235, 128, 114), 
                       (255, 255, 255), "create_cell_to_world")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    gui_manager.add(create_cell_frame)
    return gui_manager

def game_rules_change(gui_manager, game_manager, sim_manager, console_manager):
    if console_manager:
        console_manager.console_print("Info - Interface - Admin panel opened")
        
    sim_manager.pointer_is_busy = True
    create_cell_frame = Frame("admin_panel", (300, 100), (300, 170), (47,41,75), "admin_pan")
    
    name_input = TextInput("g", (0, 0), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Глобальная константа G (float)", "admin_pan", float)
    create_cell_frame.add(name_input)
    
    def submit_g():
        form_data:dict = gui_manager.get_form_data("admin_pan")
        if g := float(form_data.get("g")):
            if g >= 0:
                game_manager.set_special_attribute("g", g)
                if console_manager:
                    console_manager.console_print(f"Info - Admin - Changed G const - {g}")
    name_input.set_handler(submit_g)
    
    debug_draw = Checkbox("is_debug", "Отладочная информация", (0, 0), (20, 20), 
                             (255, 255, 255), (240, 240, 240), game_manager.get_option("debug_draw"), "admin_pan")
    
    def debug_draw_func():
        form_data:dict = gui_manager.get_form_data("admin_pan")
        game_manager.set_attribute("debug_draw", form_data.get("is_debug", False))
        if console_manager:
                console_manager.console_print(f"Info - Admin - Changed draw debug - {form_data.get("is_debug", False)}")
    debug_draw.set_handler(debug_draw_func)
    create_cell_frame.add(debug_draw)
    
    
    debug_draw_cell = Checkbox("is_debug_cell", "Информация о клетках", (0, 20), (20, 20), 
                             (255, 255, 255), (240, 240, 240), sim_manager._actual_entities_on_board[0]._draw_text_table, "admin_pan")
    
    def debug_draw_сel_func():
        form_data:dict = gui_manager.get_form_data("admin_pan")
        status = form_data.get("is_debug_cell", False)
        for cell in sim_manager._actual_entities_on_board:
            cell._draw_text_table = status
        if console_manager:
                console_manager.console_print(f"Info - Admin - Changed cell draw debug - {form_data.get("is_debug", False)}")
    debug_draw_cell.set_handler(debug_draw_сel_func)
    create_cell_frame.add(debug_draw_cell)
    
    
    debug_draw_cell = Checkbox("is_debug_line_cell", "Информация о клетках", (0, 20), (20, 20), 
                             (255, 255, 255), (240, 240, 240), sim_manager._actual_entities_on_board[0]._draw_lines, "admin_pan")
    
    def debug_draw_lines_func():
        form_data:dict = gui_manager.get_form_data("admin_pan")
        status = form_data.get("is_debug_line_cell", False)
        for cell in sim_manager._actual_entities_on_board:
            cell._draw_lines = status
        if console_manager:
                console_manager.console_print(f"Info - Admin - Changed cell draw debug - {form_data.get("is_debug", False)}")
    debug_draw_cell.set_handler(debug_draw_lines_func)
    create_cell_frame.add(debug_draw_cell)
    
    
    def kill_window():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        
    kill_btn = Button("kill", "Закрыть окно", (0, -90), (100, 40), (235, 128, 114), 
                       (255, 255, 255), "create_cell_to_world")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    gui_manager.add(create_cell_frame)
    
    gui_manager.add(create_cell_frame)
    return gui_manager
    

def main_interface(gui_manager, saver_manager, game_manager, sim_manager, console_manager=None):
    if console_manager:
        console_manager.console_print("Info - Interface - Main Window opened")
    windows_size = game_manager.get_option("window_size")
    create_cell_frame = Frame("del_form", (windows_size[0]-71, 200), (71, 400), (47,41,75), "del_cell", padding = 10, offset = 10, board_pad =2)
    
    admin_panel = Icon("submit", "", (0, -40), (40, 50), (90, 120, 200), 
                       (255, 255, 255), "no_it", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\admin_ico.png")
    def submit_login():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        game_rules_change(gui_manager, game_manager, sim_manager, console_manager)
    admin_panel.set_handler(submit_login)
    create_cell_frame.add(admin_panel)
    
    botton_create_window = Icon("cell", "", (0, -80), (40, 50), (90, 120, 200), 
                       (255, 255, 255), "no_it", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\cell_add_ico.png")
    def create_add_windows():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        spawner_window(gui_manager, game_manager, sim_manager, console_manager)
    botton_create_window.set_handler(create_add_windows)
    create_cell_frame.add(botton_create_window)
    
    botton_cell_control = Icon("screen", "", (0, -80), (40, 50), (90, 120, 200), 
                       (255, 255, 255), "screen", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\cell_control_ico.png")
    def control_cell():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        console_manager.console_print("Info - Interface - Open window. (name: control_cell)")
        change_cell_to_control(gui_manager, sim_manager)
    botton_cell_control.set_handler(control_cell)
    create_cell_frame.add(botton_cell_control)
    
    botton_cell_graph = Icon("screen", "", (0, -80), (40, 50), (90, 120, 200), 
                       (255, 255, 255), "screen", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\diagram_ico.png")
    def graph_cell():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        statistic_screen(gui_manager, sim_manager, console_manager)
    botton_cell_graph.set_handler(graph_cell)
    create_cell_frame.add(botton_cell_graph)
    
    botton_cell_plus = Icon("screen", "", (0, -120), (40, 50), (235, 128, 114), 
                       (255, 255, 255), "screen", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\cell_plus_ico.png")
    def create_cell():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        console_manager.console_print("Info - Interface - Open window. (name: create_cell)")
        create_cell_window(gui_manager, saver_manager, sim_manager)
    botton_cell_plus.set_handler(create_cell)
    create_cell_frame.add(botton_cell_plus)
    
    botton_cell_minus = Icon("screen", "", (0, -120), (40, 50), (235, 128, 114), 
                       (255, 255, 255), "screen", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\cell_minus_ico.png" )
    def delete_cell():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        console_manager.console_print("Info - Interface - Open window. (name: delete_cell)")
        del_cell_window(gui_manager, saver_manager, sim_manager)
    botton_cell_minus.set_handler(delete_cell)
    create_cell_frame.add(botton_cell_minus)
    
    
    botton_exit = Icon("exit", "", (0, -120), (40, 50), (235, 128, 114), 
                       (255, 255, 255), "screen", image_path= r"E:\Python\Fun\CellsWorld\CellWorld\Source\exit_ico.png" )
    def delete_window():
        if sim_manager.pointer_is_busy:
            if console_manager:
                console_manager.console_print("Error - Pointer is busy for now, cant operate")
            _logger.warning("Pointer is busy for now, cant operate")
            return
        console_manager.console_print("Info - Interface - Open window. (name: exit window)")
        exit_screen(gui_manager, sim_manager, console_manager)
    botton_exit.set_handler(delete_window)
    create_cell_frame.add(botton_exit)
    
    
    gui_manager.add(create_cell_frame)
    return gui_manager

def exit_screen(gui_manager, sim_manager, console_manager):
    if console_manager:
        console_manager.console_print("Info - Interface - Exit window opened")
        
    if sim_manager.pointer_is_busy:
        if console_manager:
            console_manager.console_print("Error - Pointer is busy for now, cant operate")
        _logger.warning("Pointer is busy for now, cant operate")
        return
    else:
        sim_manager.pointer_is_busy = True
        
    create_cell_frame = Frame("admin_panel", (500, 200), (300, 107), (47,41,75), "kill_pan")
    
    def kill_window():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        sim_manager._quit = False
        
    kill_btn = Button("kill", "Закрыть игру", (0, -90), (100, 40), (235, 128, 114), 
                       (255, 255, 255), "kill_pan")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    
    def kill_window1():
        create_cell_frame.status = "killed"
        sim_manager.pointer_is_busy = False
        
    kill_btn1 = Button("kill", "Закрыть окно", (0, -90), (100, 40), (235, 128, 114), 
                       (255, 255, 255), "kill_pan")
    kill_btn1.set_handler(kill_window1)
    create_cell_frame.add(kill_btn1)
    
    gui_manager.add(create_cell_frame)
    return gui_manager
    

def statistic_screen(gui_manager, sim_manager, console_manager):
    if console_manager:
        console_manager.console_print("Info - Interface - Statistic opened")
        
        
    cell_stat = sim_manager._cell_statistic
    world_stat = sim_manager._world_statistic
    
    if len(cell_stat) <= 1 or len(world_stat) <= 1:
        world_stat = [[0,0],[1,0]]
        cell_stat = [[0,0],[1,0]]
        console_manager.console_print("Error - We have not enough information for open. Statistic Closed")
    
    
    create_cell_frame = Frame("admin_panel_graph1", (200, 100), (500, 530), (47,41,75), "statistic")
    
    kill2_btn = Button("kill", "Изменение соотношения клеток", (0, -90), (100, 25), (55,51,86), 
                       (255, 255, 255), "statistic")
    kill2_btn.is_clickable = False
    kill2_btn.is_enabled = False
    create_cell_frame.add(kill2_btn)
    
    
    graph = Graph("graph1", cell_stat, pos=(100, 100), size=(200, 200), color=(67,61,95))
    graph.set_animation_speed(0.7)
    create_cell_frame.add(graph)
    
    kill1_btn = Button("kill", "Изменение средней скорости", (0, -90), (100, 25), (55,51,86), 
                       (255, 255, 255), "statistic")
    kill1_btn.is_clickable = False
    kill1_btn.is_enabled = False
    create_cell_frame.add(kill1_btn)
    
    graph1 = Graph("graph1", world_stat, pos=(100, 100), size=(200, 200), color=(67,61,95))
    graph1.set_animation_speed(0.7)
    create_cell_frame.add(graph1)
    
    
    def kill_window():
        create_cell_frame.status = "killed"
        
    kill_btn = Button("kill", "Закрыть окно", (0, -90), (100, 40), (235, 128, 114), 
                       (255, 255, 255), "statistic")
    kill_btn.set_handler(kill_window)
    create_cell_frame.add(kill_btn)
    
    gui_manager.add(create_cell_frame)
    return gui_manager
    
    