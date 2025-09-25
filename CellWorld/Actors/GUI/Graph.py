import pygame
from pygame import Vector2
import CellWorld.Constants.Constants as const
from CellWorld.Actors.GUI.ActiveObject import ActiveObject
import numpy as np

class Graph(ActiveObject):
    def __init__(self, id, data, pos=(0, 0), size=(400, 300), color=const.TEMPLATE_COL, form_id=None, offset=10):
        super().__init__(id, pos, size, color, form_id, offset)
        
        self.target_data = np.array(data, dtype=np.float64)

        self.initial_data = self.target_data.copy()
        self.initial_data[:, 1:] = 0  
        
        self.current_data = self.initial_data.copy()  
        self.animation_speed = 2.0
        
         
        self.axis_color = (100, 100, 100)
        self.line_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255)]   
        self.line_width = 2
        self.point_radius = 3
        
         
        self.padding = 20
        self._update_bounds()
        
         
        self.animation_progress = 0.0   
        self.animation_complete = False
        
         
        self.animation_type = 1

    def _update_bounds(self):
        """Обновляет границы графика"""
        self.x_min = np.min(self.target_data[:, 0])
        self.x_max = np.max(self.target_data[:, 0])
        self.y_min = 0   
        self.y_max = np.max(self.target_data[:, 1:])
        
         
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        self.x_min -= x_range * 0.05
        self.x_max += x_range * 0.05
        self.y_max += y_range * 0.05   

    def draw(self, screen):
        if not self.is_visible:
            return
            
         
        pygame.draw.rect(screen, self._bg_color, self.rectangle, border_radius=5)
        
         
        pygame.draw.line(
            screen,
            self.axis_color,
            (self.rectangle.left + self.padding, self.rectangle.bottom - self.padding),
            (self.rectangle.right - self.padding, self.rectangle.bottom - self.padding),
            2
        )
        pygame.draw.line(
            screen,
            self.axis_color,
            (self.rectangle.left + self.padding, self.rectangle.top + self.padding),
            (self.rectangle.left + self.padding, self.rectangle.bottom - self.padding),
            2
        )
        
         
        for line_idx in range(1, self.current_data.shape[1]):
            points = []
            for point in self.current_data:
                x = self._map_value(point[0], self.x_min, self.x_max, 
                                self.rectangle.left + self.padding, 
                                self.rectangle.right - self.padding)
                y = self._map_value(point[line_idx], self.y_min, self.y_max,
                                self.rectangle.bottom - self.padding,
                                self.rectangle.top + self.padding)
                points.append((x, y))
            
            # Сортируем точки по X-координате перед отрисовкой
            points.sort(key=lambda p: p[0])
            
            if len(points) > 1:
                pygame.draw.lines(screen, self.line_colors[line_idx-1], False, points, self.line_width)
            
            # Рисуем точки после сортировки
            for x, y in points:
                pygame.draw.circle(screen, self.line_colors[line_idx-1], (int(x), int(y)), self.point_radius)

    def update(self, dt):
        super().update(dt)
        
        if not self.animation_complete:
             
            self.animation_progress += self.animation_speed * dt
            
             
            self.animation_progress = min(1.0, self.animation_progress)
            
             
            if self.animation_type == 1:
                 
                smoothed_progress = self._parabolic_ease(self.animation_progress)
            else:
                 
                smoothed_progress = self.animation_progress
            
             
            self.current_data = self.initial_data + (self.target_data - self.initial_data) * smoothed_progress
            
             
            if self.animation_progress >= 1.0:
                self.animation_complete = True

    def _parabolic_ease(self, t):
        """Параболическая функция для плавной анимации"""
         
        if t < 0.5:
            return 2 * t * t
        else:
            t = t - 0.5
            return 2 * t * (1 - t) + 0.5

    def _map_value(self, value, in_min, in_max, out_min, out_max):
        """Преобразует значение из одного диапазона в другой"""
        if in_max - in_min == 0:   
            return out_min
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def set_data(self, new_data):
        """Обновляет данные графика с сохранением анимации"""
        self.target_data = np.array(new_data, dtype=np.float64)
        
        self.initial_data = self.target_data.copy()
        self.initial_data[:, 1:] = 0
        
         
        self.current_data = self.initial_data.copy()
        self._update_bounds()
        self.animation_complete = False
        self.animation_progress = 0.0

    def set_animation_speed(self, speed):
        """Устанавливает скорость анимации (единиц в секунду)"""
        self.animation_speed = max(0.1, speed)
    
    def set_animation_type(self, anim_type):
        """Устанавливает тип анимации (0 - линейная, 1 - параболическая)"""
        self.animation_type = anim_type
        
    def reset_animation(self):
        """Сбрасывает анимацию к начальному состоянию"""
        self.current_data = self.initial_data.copy()
        self.animation_complete = False
        self.animation_progress = 0.0

    def set_pos(self, x, y):
        """Переопределяем метод для обновления позиции с учетом локальных координат"""
        super().set_pos(x, y)
        self.reset_animation()