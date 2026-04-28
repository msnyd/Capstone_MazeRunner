"""
Neural Network Popup Visualizer

Displays a large popup window showing the neural network when an agent is selected.
Click outside the popup or press ESC/B to close.
"""

import pygame
import numpy as np
import math
from typing import List, Tuple, Optional
import src


class NetworkPopup:
    """
    Neural Network Popup Visualizer class for MazeRunner.
    
    Implements:
        REQ-8.1: Open popup on agent click
        REQ-8.2: Display agent stats
        REQ-8.3: Render network layers as columns
        REQ-8.4: Node activation colors (yellow/blue)
        REQ-8.5: Connection weight colors (green/red)
        REQ-8.6: Input/output labels
        REQ-8.7: Close with ESC/B/click
        REQ-8.8: Semi-transparent overlay
    """
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the popup visualizer.
        
        Args:
            screen_width, screen_height: Screen dimensions for centering
        """
        # Popup dimensions
        self.width = 500
        self.height = 400
        
        # center on screen
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # State
        self.visible = False
        self.agent = None
        
        # Colors
        self.bg_color = (35, 35, 45)
        self.border_color = (100, 100, 120)
        self.text_color = (220, 220, 220)
        self.node_outline = (100, 100, 100)
        self.close_btn_color = (180, 60, 60)
        self.close_btn_hover = (220, 80, 80)
        
        # Node settings
        self.node_radius = 18
        self.font = None
        self.font_title = None
        
        # close button
        self.close_btn_rect = pygame.Rect(self.x + self.width - 35, self.y + 8, 25, 25)
        
        # Labels for i/o
        self.input_labels_5 = ['Far L', 'Left', 'Fwd', 'Right', 'Far R', 'Goal']
        self.input_labels_7 = ['90°L', '60°L', '30°L', 'Fwd', '30°R', '60°R', '90°R', 'Goal']
        self.output_labels = ['Turn']
    
    def show(self, agent):
        """
        Show the popup for a specific agent
        
        Implements: REQ-8.1
        """
        self.visible = True
        self.agent = agent
    
    def hide(self):
        """Hide the popup
         Implements: REQ-8.7
         """
        self.visible = False
        self.agent = None
    
    def toggle(self, agent=None):
        """Toggle popup visibility
        
        Implements: REQ-8.2 through REQ-8.6, REQ-8.8
        """
        if self.visible:
            self.hide()
        elif agent:
            self.show(agent)
    
    def handle_event(self, event) -> bool:
        """
        Handle mouse/keyboard events        
        Returns True if event was consumed (popup should stay open)
        Returns False if popup should close
        """
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b):
                self.hide()
                return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                
                #check close button
                if self.close_btn_rect.collidepoint(mouse_x, mouse_y):
                    self.hide()
                    return True
                
                # Check if clicked outside popup
                popup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                if not popup_rect.collidepoint(mouse_x, mouse_y):
                    self.hide()
                    return True
        
        return True  # Consume event while popup is open
    
    def draw(self, screen, goal_x: float = 0, goal_y: float = 0):
        """Draw the popup if visible"""
        if not self.visible or not self.agent or not self.agent.brain:
            return
        
        # Initialize fonts
        if self.font is None:
            self.font = pygame.font.Font(None, 20)
            self.font_title = pygame.font.Font(None, 28)
        
        # Update close button position
        self.close_btn_rect = pygame.Rect(self.x + self.width - 35, self.y + 8, 25, 25)
        
        # Draw semi-transparent overlay behind popup
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw popup background
        popup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, popup_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, popup_rect, 3, border_radius=10)
        
        # Draw title
        title = self.font_title.render("Agent Neural Network", True, self.text_color)
        screen.blit(title, (self.x + 15, self.y + 12))
        
        # Draw close button
        mouse_pos = pygame.mouse.get_pos()
        btn_color = self.close_btn_hover if self.close_btn_rect.collidepoint(mouse_pos) else self.close_btn_color
        pygame.draw.rect(screen, btn_color, self.close_btn_rect, border_radius=5)
        x_text = self.font.render("✕", True, (255, 255, 255))
        screen.blit(x_text, (self.close_btn_rect.x + 7, self.close_btn_rect.y + 4))
        
        # Draw agent stats
        stats_y = self.y + 45
        stats = [
            f"Fitness: {self.agent.fitness:.1f}",
            f"Steps: {self.agent.steps_taken}",
            f"Position: ({int(self.agent.x)}, {int(self.agent.y)})",
            f"Alive: {self.agent.alive}",
        ]
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (180, 180, 180))
            screen.blit(text, (self.x + 15 + (i % 2) * 150, stats_y + (i // 2) * 20))
        
        # Draw separator line
        pygame.draw.line(screen, self.border_color, 
                        (self.x + 10, self.y + 90), 
                        (self.x + self.width - 10, self.y + 90), 1)
        
        # Draw neural network
        network = self.agent.brain
        layer_sizes = network.layer_sizes
        
        # Get current inputs
        inputs = self._get_inputs(goal_x, goal_y)
        activations = self._get_activations(network, inputs)
        
        # Calculate node positions (within popup)
        node_positions = self._calculate_node_positions(layer_sizes)
        
        # Draw connections
        self._draw_connections(screen, network, node_positions, activations)
        
        # Draw nodes
        self._draw_nodes(screen, node_positions, activations, layer_sizes)
        
        # Draw legend
        self._draw_legend(screen)
    
    def _get_inputs(self, goal_x: float, goal_y: float) -> Optional[np.ndarray]:
        """Get current input values from the agent"""
        if not hasattr(self.agent, 'sensor_distances') or not self.agent.sensor_distances:
            return None
        
        inputs = self.agent.sensor_distances.copy()
        goal_angle = self.agent._angle_to_point(goal_x, goal_y)
        inputs.append(goal_angle)
        return np.array(inputs)
    
    def _get_activations(self, network, inputs: Optional[np.ndarray]) -> List[np.ndarray]:
        """Get activation values for each layer."""
        if inputs is None:
            return [np.zeros(size) for size in network.layer_sizes]
        
        activations = [inputs]
        x = np.array(inputs, dtype=np.float32)
        
        for i in range(len(network.weights)):
            x = x @ network.weights[i] + network.biases[i]
            x = np.tanh(x)
            activations.append(x)
        
        return activations
    
    def _calculate_node_positions(self, layer_sizes: Tuple[int, ...]) -> List[List[Tuple[int, int]]]:
        """Calculate (x, y) positions for each node within popup."""
        positions = []
        num_layers = len(layer_sizes)
        
        # Drawing area within popup
        draw_x = self.x + 80
        draw_y = self.y + 110
        draw_width = self.width - 120
        draw_height = self.height - 160
        
        # Horizontal spacing
        layer_spacing = draw_width // (num_layers - 1) if num_layers > 1 else 0
        
        for layer_idx, layer_size in enumerate(layer_sizes):
            layer_positions = []
            
            # X position for this layer
            layer_x = draw_x + layer_idx * layer_spacing
            
            # Vertical spacing
            if layer_size > 1:
                node_spacing = min(40, draw_height // (layer_size - 1))
            else:
                node_spacing = 0
            
            # Starting Y (centered)
            total_height = (layer_size - 1) * node_spacing
            start_y = draw_y + (draw_height - total_height) // 2
            
            for node_idx in range(layer_size):
                node_y = start_y + node_idx * node_spacing
                layer_positions.append((layer_x, node_y))
            
            positions.append(layer_positions)
        
        return positions
    
    def _draw_connections(self, screen, network, positions: List[List[Tuple[int, int]]], 
                          activations: List[np.ndarray]):
        """Draw connections between nodes."""
        for layer_idx in range(len(network.weights)):
            weights = network.weights[layer_idx]
            
            for from_idx, from_pos in enumerate(positions[layer_idx]):
                for to_idx, to_pos in enumerate(positions[layer_idx + 1]):
                    weight = weights[from_idx, to_idx]
                    
                    # Color based on weight
                    intensity = min(200, int(abs(weight) * 120))
                    if weight > 0:
                        color = (50, 50 + intensity, 50)
                    else:
                        color = (50 + intensity, 50, 50)
                    
                    # Line thickness based on weight magnitude
                    thickness = max(1, min(4, int(abs(weight) * 2.5)))
                    
                    pygame.draw.line(screen, color, from_pos, to_pos, thickness)
    
    def _draw_nodes(self, screen, positions: List[List[Tuple[int, int]]], 
                    activations: List[np.ndarray], layer_sizes: Tuple[int, ...]):
        """Draw nodes with activation colors and labels."""
        # Choose labels based on input size
        num_inputs = layer_sizes[0]
        if num_inputs <= 6:
            input_labels = self.input_labels_5
        else:
            input_labels = self.input_labels_7
        
        for layer_idx, layer_positions in enumerate(positions):
            for node_idx, (x, y) in enumerate(layer_positions):
                # Get activation value
                if layer_idx < len(activations) and node_idx < len(activations[layer_idx]):
                    activation = float(activations[layer_idx][node_idx])
                else:
                    activation = 0.0
                
                # Color based on activtion (-1 to 1)
                if activation > 0:
                    r = 255
                    g = 255
                    b = int(255 * (1 - min(1, activation)))
                else:
                    r = int(255 * (1 + max(-1, activation)))
                    g = int(255 * (1 + max(-1, activation)))
                    b = 255
                
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                
                # Draw node
                pygame.draw.circle(screen, color, (x, y), self.node_radius)
                pygame.draw.circle(screen, self.node_outline, (x, y), self.node_radius, 2)
                
                # Draw activation value inside node
                val_text = self.font.render(f"{activation:.1f}", True, (0, 0, 0))
                text_rect = val_text.get_rect(center=(x, y))
                screen.blit(val_text, text_rect)
                
                # Draw labels for input layer
                if layer_idx == 0 and node_idx < len(input_labels):
                    label = self.font.render(input_labels[node_idx], True, self.text_color)
                    screen.blit(label, (x - 55, y - 8))
                
                # Draw labels for output layer
                elif layer_idx == len(positions) - 1 and node_idx < len(self.output_labels):
                    label = self.font.render(self.output_labels[node_idx], True, self.text_color)
                    screen.blit(label, (x + 25, y - 8))
        
        # Draw layer labels
        layer_names = ['Input', 'Hidden', 'Output']
        for layer_idx, layer_positions in enumerate(positions):
            if layer_positions:
                x = layer_positions[0][0]
                name = layer_names[min(layer_idx, len(layer_names)-1)]
                if layer_idx > 0 and layer_idx < len(positions) - 1:
                    name = f"Hidden {layer_idx}"
                label = self.font.render(name, True, (150, 150, 150))
                label_rect = label.get_rect(center=(x, self.y + self.height - 25))
                screen.blit(label, label_rect)
    
    def _draw_legend(self, screen):
        """Draw color legend."""
        legend_x = self.x + 15
        legend_y = self.y + self.height - 50
        
        # Activation legend
        pygame.draw.circle(screen, (255, 255, 100), (legend_x + 8, legend_y), 6)
        text = self.font.render("= Positive", True, (150, 150, 150))
        screen.blit(text, (legend_x + 20, legend_y - 8))
        
        pygame.draw.circle(screen, (100, 100, 255), (legend_x + 100, legend_y), 6)
        text = self.font.render("= Negative", True, (150, 150, 150))
        screen.blit(text, (legend_x + 112, legend_y - 8))
        
        # Instructions
        hint = self.font.render("Press B or ESC to close", True, (120, 120, 120))
        screen.blit(hint, (self.x + self.width - 160, self.y + self.height - 25))