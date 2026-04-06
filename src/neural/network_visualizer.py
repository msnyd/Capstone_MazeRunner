"""
Neural Network Visualizer
 
Displays the neural network structure with:
- Nodes colored by activation strength
- Connections colored by weight (green = positive, red = negative)
- Real-time updates as agent thinks
"""
 
import pygame
import numpy as np
import math
from typing import List, Tuple, Optional
 
 
class NetworkVisualizer:
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize the visualizer.
        
        Args:
            x, y: Top-left position on screen
            width, height: Size of visualization area
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # colors
        self.bg_color = (30, 30, 30) 
        self.text_color = (200, 200, 200)
        self.node_outline = (100, 100, 100)
        
        # Node settings
        self.node_radius = 15
        self.font = None  # init in draw (pygame must be init first)
        
        # Labels for inputs/outputs
        self.input_labels = ['90°L', '60°L', '30°L', 'Fwd', '30°R', '60°R', '90°R', 'Goal']
        self.output_labels = ['Turn']
    
    def draw(self, screen, network, inputs: Optional[np.ndarray] = None):
        """
        Draw the neural network.
        
        Args:
            screen: Pygame screen
            network: NeuralNetwork object
            inputs: Current input values (for showing activations)
        """
        if self.font is None:
            self.font = pygame.font.Font(None, 18)
        
        # Draw background panel
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, panel_rect)
        pygame.draw.rect(screen, (80, 80, 80), panel_rect, 2)
        
        # title
        title = self.font.render("Neural Network", True, self.text_color)
        screen.blit(title, (self.x + 10, self.y + 5))
        
        # get layer sizes
        layer_sizes = network.layer_sizes
        num_layers = len(layer_sizes)
        
        # calculate node positions
        node_positions = self._calculate_node_positions(layer_sizes)
        
        # get activations if inputs provided
        activations = self._get_activations(network, inputs)
        
        # draw connections first (behind nodes)
        self._draw_connections(screen, network, node_positions, activations)
        
        # draw nodes
        self._draw_nodes(screen, node_positions, activations, layer_sizes)
    
    def _calculate_node_positions(self, layer_sizes: Tuple[int, ...]) -> List[List[Tuple[int, int]]]:
        """Calculate (x, y) positions for each node."""
        positions = []
        num_layers = len(layer_sizes)
        
        # Horizontal spacing
        usable_width = self.width - 80
        layer_spacing = usable_width // (num_layers - 1) if num_layers > 1 else 0
        
        for layer_idx, layer_size in enumerate(layer_sizes):
            layer_positions = []
            
            # x position for this layer
            layer_x = self.x + 40 + layer_idx * layer_spacing
            
            # vrtical spacing
            usable_height = self.height - 60
            if layer_size > 1:
                node_spacing = usable_height // (layer_size - 1)
            else:
                node_spacing = 0
            
            # Starting Y (centered)
            start_y = self.y + 30 + (usable_height - (layer_size - 1) * node_spacing) // 2
            
            for node_idx in range(layer_size):
                node_y = start_y + node_idx * node_spacing
                layer_positions.append((layer_x, node_y))
            
            positions.append(layer_positions)
        
        return positions
    
    def _get_activations(self, network, inputs: Optional[np.ndarray]) -> List[np.ndarray]:
        """Get activation values for each layer."""
        if inputs is None:
            # Return zeros if no input
            return [np.zeros(size) for size in network.layer_sizes]
        
        activations = [inputs]
        x = np.array(inputs, dtype=np.float32)
        
        for i in range(len(network.weights)):
            x = x @ network.weights[i] + network.biases[i]
            x = np.tanh(x)
            activations.append(x)
        
        return activations
    
    def _draw_connections(self, screen, network, positions: List[List[Tuple[int, int]]], 
                          activations: List[np.ndarray]):
        """Draw connections between nodes."""
        for layer_idx in range(len(network.weights)):
            weights = network.weights[layer_idx]
            
            for from_idx, from_pos in enumerate(positions[layer_idx]):
                for to_idx, to_pos in enumerate(positions[layer_idx + 1]):
                    weight = weights[from_idx, to_idx]
                    
                    # Color based on weight
                    # Green = positive, red = negative
                    intensity = min(255, int(abs(weight) * 150))
                    if weight > 0:
                        color = (0, intensity, 0)
                    else:
                        color = (intensity, 0, 0)
                    
                    # Line thickness based on weight magnitude
                    thickness = max(1, min(3, int(abs(weight) * 2)))
                    
                    # Draw connection
                    pygame.draw.line(screen, color, from_pos, to_pos, thickness)
    
    def _draw_nodes(self, screen, positions: List[List[Tuple[int, int]]], 
                    activations: List[np.ndarray], layer_sizes: Tuple[int, ...]):
        """Draw nodes with activation colors."""
        for layer_idx, layer_positions in enumerate(positions):
            for node_idx, (x, y) in enumerate(layer_positions):
                # Get activation value
                if layer_idx < len(activations) and node_idx < len(activations[layer_idx]):
                    activation = activations[layer_idx][node_idx]
                else:
                    activation = 0
                
                # Color based on activation (-1 to 1)
                # Blue = negative, White = zero, Yellow = positive
                if activation > 0:
                    r = 255
                    g = 255
                    b = int(255 * (1 - activation))
                else:
                    r = int(255 * (1 + activation))
                    g = int(255 * (1 + activation))
                    b = 255
                
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                
                # Draw node
                pygame.draw.circle(screen, color, (x, y), self.node_radius)
                pygame.draw.circle(screen, self.node_outline, (x, y), self.node_radius, 2)
                
                # Draw labels for input/output layers
                if layer_idx == 0 and node_idx < len(self.input_labels):
                    label = self.font.render(self.input_labels[node_idx], True, self.text_color)
                    screen.blit(label, (x - 35, y - 6))
                elif layer_idx == len(positions) - 1 and node_idx < len(self.output_labels):
                    label = self.font.render(self.output_labels[node_idx], True, self.text_color)
                    screen.blit(label, (x + 20, y - 6))
                
                # Draw activation value
                val_text = self.font.render(f"{activation:.1f}", True, (0, 0, 0))
                screen.blit(val_text, (x - 12, y - 6))
 
 
class CompactNetworkVisualizer(NetworkVisualizer):
    """Smaller version for corner of screen."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, width=250, height=200)
        self.node_radius = 10
        self.input_labels = ['L', 'L', 'L', 'F', 'R', 'R', 'R', 'G']  # Shortened
        self.output_labels = ['T']