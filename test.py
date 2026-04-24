"""
Quick test script for internal functions.
Run from project root: python test_internals.py
"""

import numpy as np
from src.neural.neural_network import NeuralNetwork
from src.agent.agent import Agent
from src.agent.raycaster import CornerRaycaster

def test_passed(name):
    print(f"✓ {name}")

def test_failed(name, reason):
    print(f"✗ {name}: {reason}")


# =============================================================================
# NEURAL NETWORK TESTS
# =============================================================================

print("\n=== Neural Network Tests ===\n")

# NN-001: Forward pass produces output in [-1, 1]
nn = NeuralNetwork((8, 10, 1))
inputs = [0.5] * 8
output = nn.forward(inputs)
if len(output) == 1 and -1 <= output[0] <= 1:
    test_passed("NN-001: Forward pass output in [-1,1]")
else:
    test_failed("NN-001", f"Output was {output}")

# NN-002: Xavier initialization (weights have reasonable range)
nn = NeuralNetwork((8, 10, 1))
all_weights = np.concatenate([w.flatten() for w in nn.weights])
mean = np.mean(all_weights)
std = np.std(all_weights)
if abs(mean) < 0.5 and 0.1 < std < 2.0:
    test_passed(f"NN-002: Xavier init (mean={mean:.3f}, std={std:.3f})")
else:
    test_failed("NN-002", f"mean={mean}, std={std}")

# NN-004: Forward pass is consistent
nn = NeuralNetwork((8, 10, 1))
inputs = [0.3, 0.5, 0.7, 0.2, 0.8, 0.1, 0.9, 0.4]
out1 = nn.forward(inputs)
out2 = nn.forward(inputs)
if np.allclose(out1, out2):
    test_passed("NN-004: Forward pass consistent")
else:
    test_failed("NN-004", f"{out1} != {out2}")

# NN-005 & NN-006: get_genome and set_genome
nn = NeuralNetwork((8, 10, 1))
genome = nn.get_genome()
if isinstance(genome, np.ndarray) and len(genome.shape) == 1:
    test_passed(f"NN-005: get_genome returns 1D array (size={len(genome)})")
else:
    test_failed("NN-005", f"Type: {type(genome)}, shape: {genome.shape}")

nn2 = NeuralNetwork((8, 10, 1))
nn2.set_genome(genome)
genome2 = nn2.get_genome()
if np.allclose(genome, genome2):
    test_passed("NN-006: set_genome restores state")
else:
    test_failed("NN-006", "Genomes don't match after set")

# NN-007: Mutation changes weights
nn = NeuralNetwork((8, 10, 1))
original = nn.get_genome().copy()
nn.mutate(1.0, 0.5)  # 100% mutation rate to guarantee changes
mutated = nn.get_genome()
if not np.allclose(original, mutated):
    changes = np.sum(original != mutated)
    test_passed(f"NN-007: Mutation changed weights ({changes} values differ)")
else:
    test_failed("NN-007", "No weights changed")

# NN-008: Crossover combines two parents
parent1 = NeuralNetwork((8, 10, 1))
parent2 = NeuralNetwork((8, 10, 1))
g1 = parent1.get_genome()
g2 = parent2.get_genome()

child = NeuralNetwork.crossover(parent1, parent2)
gc = child.get_genome()

# Child should have some genes from each parent
from_p1 = np.sum(gc == g1)
from_p2 = np.sum(gc == g2)
if from_p1 > 0 and from_p2 > 0:
    test_passed(f"NN-008: Crossover combined parents ({from_p1} from p1, {from_p2} from p2)")
else:
    test_failed("NN-008", f"from_p1={from_p1}, from_p2={from_p2}")

# NN-009: Copy creates independent clone
nn = NeuralNetwork((8, 10, 1))
copy = nn.copy()
original_genome = nn.get_genome().copy()
copy.mutate(1.0, 0.5)
if np.allclose(nn.get_genome(), original_genome):
    test_passed("NN-009: Copy is independent (original unchanged after mutating copy)")
else:
    test_failed("NN-009", "Original was modified")


# =============================================================================
# AGENT TESTS
# =============================================================================

print("\n=== Agent Tests ===\n")

# AG-007: Angle to goal calculation
agent = Agent(100, 100, direction=0)  # x, y, direction
agent.set_brain(NeuralNetwork((8, 10, 1)))
# Goal directly to the right (agent facing right, direction=0)
agent.direction = 0
angle = agent._angle_to_point(200, 100)  # Goal to the right
if abs(angle) < 0.1:  # Should be ~0 (goal is straight ahead)
    test_passed(f"AG-007: Angle to goal (ahead) = {angle:.3f}")
else:
    test_failed("AG-007", f"Expected ~0, got {angle}")

# Goal directly above (90 degrees left)
angle = agent._angle_to_point(100, 0)  # Goal above
if abs(angle - (-np.pi/2)) < 0.1 or abs(angle - (np.pi/2)) < 0.1:
    test_passed(f"AG-007: Angle to goal (above) = {angle:.3f}")
else:
    test_failed("AG-007b", f"Expected ~±π/2, got {angle}")

# AG-010: Distance calculation
agent = Agent(0, 0, direction=0)
dist = agent.distance_to(3, 4)
if abs(dist - 5.0) < 0.01:
    test_passed(f"AG-010: Distance (3,4) = {dist}")
else:
    test_failed("AG-010", f"Expected 5.0, got {dist}")


# =============================================================================
# RAYCASTER TESTS
# =============================================================================

print("\n=== Raycaster Tests ===\n")

# RC-001: CornerRaycaster has 7 rays
rc = CornerRaycaster()
if rc.num_rays == 7:
    test_passed(f"RC-001: CornerRaycaster has {rc.num_rays} rays")
else:
    test_failed("RC-001", f"Expected 7 rays, got {rc.num_rays}")

# RC-005: Has side rays at ±90°
angles = rc.ray_angles
has_left = any(abs(a - (-np.pi/2)) < 0.1 for a in angles)
has_right = any(abs(a - (np.pi/2)) < 0.1 for a in angles)
if has_left and has_right:
    test_passed("RC-005: Has ±90° side rays")
else:
    test_failed("RC-005", f"Angles: {angles}")


# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*50)
print("Testing complete! Review results above.")
print("="*50 + "\n")