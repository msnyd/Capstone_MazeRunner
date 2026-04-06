"""
Raycaster for agent sensors.

Casts rays from agent position to detect walls.
Returns distances to nearest wall for each ray.
"""

import math
import pygame
from typing import List, Tuple, Optional

class Raycaster:
    def __init__(self, num_rays: int = 5, fov: float = math.pi, max_range: float = 150.0):
        """
        initialize raycaster
        
        Args:
            num_rays: number of sensor rays
            fov: field of view in radians
            max_range: max ray distance
        """

        self.num_rays = num_rays
        self.fov = fov
        self.max_range = max_range
        #pre calc ray angle offsets
        self.ray_angles = self._calculate_ray_angles()

    def _calculate_ray_angles(self) -> List[float]:
        """Calculates angle offsets for each array centered on the way in which the agent is facing."""
        if self.num_rays == 1:
            return [0,0]
        
        angles = []
        half_fov = self.fov / 2
        
        for i in range(self.num_rays):
            t = i / (self.num_rays - 1)
            angle = -half_fov + t * self.fov
            angles.append(angle)
        
        return angles
    
    def cast_rays(self, x: float, y: float, direction: float, 
                  walls: List[pygame.Rect]) -> List[float]:
        """
        Cast all sensor rays and returns distances
        
        args:
            x: Agent x position
            y: Agent y position
            direction: Agent facing direction (radians)
            walls: list of pygame.Rect walls

        Returns:
            List of distances (one per ray)
        """
        distances = []

        for angle_offset in self.ray_angles:
            ray_angle = direction + angle_offset
            distance = self._cast_single_ray(x, y, ray_angle, walls)
            distances.append(distance)
        
        return distances
    
    def cast_rays_with_endpoints(self, x:float, y:float, direction: float,
                                 walls: List[pygame.Rect]) -> List[Tuple[float, float, float]]:
        """
        Cast rays and return distances with hit coordinates (for drawing).

        returns:
            List of (distance, hit_x, hit_y) tuples
        """
        results = []

        for angle_offset in self.ray_angles:
            ray_angle = direction + angle_offset
            dist, hx, hy, = self._cast_single_ray_with_endpoints(x, y, ray_angle, walls)
            results.append((dist, hx, hy))
        
        return results
    
    def _cast_single_ray(self, x: float, y: float, angle: float,
                         walls: List[pygame.Rect]) -> float:
        
        end_x = x + math.cos(angle) * self.max_range
        end_y = y + math.sin(angle) * self.max_range
        
        closest = self.max_range

        for wall in walls:
            edges = self._rect_to_edges(wall)
            for edge in edges:
                hit = self._line_intersection(x, y, end_x, end_y, *edge)
                if hit:
                    dist = math.sqrt((hit[0] - x)**2 + (hit[1] -y)**2)
                    if dist < closest:
                        closest = dist
        
        return closest
    
    def _cast_single_ray_with_endpoints(self, x: float, y: float, angle: float,
                                       walls: List[pygame.Rect]) -> Tuple[float, float, float]:
        """Cast one ray, return distance and hit point"""
        end_x = x + math.cos(angle) * self.max_range
        end_y = y + math.sin(angle) * self.max_range

        closest = self.max_range
        hit_x, hit_y = end_x, end_y


        for wall in walls:
            edges = self._rect_to_edges(wall)
            for edge in edges:
                hit = self._line_intersection(x, y, end_x, end_y, *edge)
                if hit:
                    dist = math.sqrt((hit[0] - x)**2 + (hit[1] - y)**2)
                    if dist < closest:
                        closest = dist
                        hit_x, hit_y = hit
        
        return (closest, hit_x, hit_y)
    
    def _rect_to_edges(self, rect:pygame.Rect) -> List[Tuple[float, float, float, float]]:
        """Convert a pygame.Rect to 4 line segments (edges)."""
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        return [
            (x, y, x + w, y), #top
            (x, y + h, x + w, y + h), #bottom
            (x, y, x, y + h), #left
            (x + w, y, x + w, y + h) #right
        ]

    def _line_intersection(self, x1: float, y1: float, x2: float, y2: float,
                           x3: float, y3: float, x4: float, y4: float) -> Optional[Tuple[float, float]]:
        """
        find intersection of two line segments

        line 1: (x1, y1) to (x2, y2) - the ray
        line 2: (x3, y3,) to (x4, y4) - the wall edge

        Returns:
            (x,y) intersection point, or None if no intersection
        """
        #directional vectors
        dx1 = x2 - x1
        dy1 = y2 - y1
        dx2 = x4 - x3
        dy2 = y4 - y3

        denom = dx1 * dy2 - dy1 * dx2

        if abs(denom) < 1e-10:
            return None
        
        t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / denom
        u = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / denom

        if 0 <= t <= 1 and 0 <= u <= 1:
            ix = x1 + t * dx1
            iy = y1 + t * dy1
            return (ix, iy)
        
        return None
    
    def draw(self, screen, x: float, y: float, direction: float,
             walls: List[pygame.Rect], color = (255, 255, 0)):
        """
        draw sensor rays on pygame

        args:
            Screen: pygame
            x, y: agent position
            direction: agent facing direction
            walls: list of walls
            color: ray color(yellow)
        """

        results = self.cast_rays_with_endpoints(x, y, direction, walls)

        for dist, hit_x, hit_y in results:
            #draw line
            pygame.draw.line(screen, color, (int(x), int(y)), (int(hit_x), int(hit_y)), 1)

            #draw hit
            pygame.draw.circle(screen, (255, 0, 0), (int(hit_x), int(hit_y)), 3)
class SimpleRaycaster(Raycaster):
    """3-ray raycaster: left, forward, right."""
    
    def __init__(self, max_range: float = 150.0, spread: float = math.pi/4):
        super().__init__(num_rays=3, fov=spread * 2, max_range=max_range)
        # Override with exact angles
        self.ray_angles = [-spread, 0.0, spread]


class WideRaycaster(Raycaster):
    """5-ray raycaster spanning 180 degrees."""
    
    def __init__(self, max_range: float = 150.0):
        super().__init__(num_rays=5, fov=math.pi, max_range=max_range)

class CornerRaycaster(Raycaster):
    """7-ray raycaster for better corner detection."""
    
    def __init__(self, max_range: float = 200.0):
        super().__init__(num_rays=7, fov=math.pi, max_range=max_range)
        # Angles: -90°, -60°, -30°, 0°, 30°, 60°, 90°
        self.ray_angles = [
            -math.pi/2,      # Far left (90° left)
            -math.pi/3,      # Left (60° left)
            -math.pi/6,      # Slight left (30° left)
            0.0,             # Forward
            math.pi/6,       # Slight right (30° right)
            math.pi/3,       # Right (60° right)
            math.pi/2,       # Far right (90° right)
        ]