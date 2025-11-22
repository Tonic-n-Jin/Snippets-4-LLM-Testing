# Reinforcement Learning Notebooks

A comprehensive collection of Jupyter notebooks implementing fundamental reinforcement learning algorithms. These notebooks are designed for educational purposes, providing clear explanations, implementations, and visualizations of key RL concepts.

## 📚 Overview

This collection covers 10 essential RL algorithms across four main categories:

### 🎯 Value-Based Methods
Learn optimal value functions to derive policies:
- **Q-Learning** (`reinforcement__value_based__q_learning.ipynb`) - Classic tabular RL for discrete spaces
- **SARSA** (`reinforcement__value_based__sarsa.ipynb`) - On-policy temporal difference learning
- **Deep Q-Network (DQN)** (`reinforcement__value_based__dqn.ipynb`) - Neural network Q-learning with experience replay

### 🎲 Policy-Based Methods
Directly optimize policy parameters:
- **REINFORCE** (`reinforcement__policy_based__reinforce.ipynb`) - Monte Carlo policy gradient
- **PPO** (`reinforcement__policy_based__ppo.ipynb`) - Proximal Policy Optimization with clipped objective
- **TRPO** (`reinforcement__policy_based__trpo.ipynb`) - Trust Region Policy Optimization

### 🎭 Actor-Critic Methods
Combine value and policy learning:
- **A2C** (`reinforcement__actor_critic__a2c.ipynb`) - Advantage Actor-Critic (synchronous)
- **A3C-Style** (`reinforcement__actor_critic__a3c.ipynb`) - Multi-worker synchronous variant

### 🧠 Model-Based Methods
Learn environment dynamics for planning:
- **Dyna-Q** (`reinforcement__model_based__dyna_q.ipynb`) - Integrated planning and learning
- **MPC** (`reinforcement__model_based__mpc.ipynb`) - Model Predictive Control with optimization

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-enabled GPU for faster deep RL training

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd Data-World/notebooks
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv rl_env
   source rl_env/bin/activate  # On Windows: rl_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

5. **Open any notebook** and run cells sequentially from top to bottom.

## 📖 Usage Guide

### Notebook Structure

Each notebook follows a consistent structure:

1. **Introduction** - Algorithm principle, definition, and use cases
2. **Import Libraries** - Required packages and setup
3. **Algorithm Implementation** - Core agent class with detailed comments
4. **Training** - Training loop with progress tracking
5. **Visualization** - Performance plots and analysis

### Running Notebooks

**For Quick Testing:**
- Reduce `n_episodes` parameter in training cells (e.g., from 500 to 100)
- This speeds up execution for experimentation

**For Full Training:**
- Use default parameters for best results
- Deep RL notebooks (DQN, A2C, PPO) may take 10-20 minutes on CPU
- Consider using GPU for faster training (notebooks are GPU-compatible)

**Example:**
```python
# Original (full training)
episode_rewards = train_agent(env, agent, n_episodes=500)

# Quick test (faster)
episode_rewards = train_agent(env, agent, n_episodes=100)
```

## 🎓 Learning Path

### Beginner Track
Start with simpler algorithms to build foundations:
1. **Q-Learning** - Understand value-based RL basics
2. **SARSA** - Compare on-policy vs off-policy learning
3. **REINFORCE** - Learn policy gradient methods

### Intermediate Track
Progress to more advanced techniques:
4. **DQN** - Deep reinforcement learning fundamentals
5. **A2C** - Combine value and policy approaches
6. **PPO** - Modern policy optimization

### Advanced Track
Explore specialized methods:
7. **A3C-Style** - Parallel training strategies
8. **TRPO** - Constrained optimization
9. **Dyna-Q** - Model-based learning
10. **MPC** - Control theory integration

## ⚙️ Configuration

### Hyperparameter Tuning

Each notebook includes configurable hyperparameters in the agent initialization:

```python
agent = DQNAgent(
    state_dim=state_dim,
    action_dim=action_dim,
    learning_rate=0.001,      # Adjust for faster/slower learning
    gamma=0.99,               # Discount factor
    epsilon=1.0,              # Initial exploration rate
    epsilon_decay=0.995,      # Exploration decay
    epsilon_min=0.01          # Minimum exploration
)
```

### Environment Changes

All notebooks default to Gymnasium environments:
- Value-based: `FrozenLake-v1` (Q-Learning, SARSA) or `CartPole-v1` (DQN)
- Policy/Actor-Critic: `CartPole-v1`

To try different environments, modify the environment creation:
```python
# Original
env = gym.make('CartPole-v1')

# Alternative environments
env = gym.make('LunarLander-v2')
env = gym.make('Acrobot-v1')
```

**Note:** Ensure state/action dimensions match the new environment.

## 📊 Expected Results

### Performance Benchmarks

Approximate expected performance after full training:

| Algorithm | Environment | Success Rate | Training Time (CPU) |
|-----------|-------------|--------------|---------------------|
| Q-Learning | FrozenLake | 70-80% | 2-3 min |
| SARSA | FrozenLake | 65-75% | 2-3 min |
| DQN | CartPole | 95%+ | 15-20 min |
| REINFORCE | CartPole | 90%+ | 10-15 min |
| PPO | CartPole | 95%+ | 10-15 min |
| A2C | CartPole | 95%+ | 10-15 min |
| A3C-Style | CartPole | 95%+ | 8-12 min |
| TRPO | CartPole | 95%+ | 12-18 min |
| Dyna-Q | FrozenLake | 75-85% | 3-5 min |
| MPC | CartPole | Variable | 5-10 min |

**Success Criteria:**
- FrozenLake: Reaching goal (reward > 0)
- CartPole: Episode length ≥ 195 for 100 consecutive episodes

## 🔧 Troubleshooting

### Common Issues

**1. Import Errors**
```
ModuleNotFoundError: No module named 'gymnasium'
```
**Solution:** Install requirements: `pip install -r requirements.txt`

**2. Slow Training**
- Reduce `n_episodes` for faster testing
- Use GPU by ensuring PyTorch CUDA is installed
- Close other resource-intensive applications

**3. Poor Performance**
- Check hyperparameters match notebook defaults
- Ensure reproducibility by setting seeds
- Verify environment version matches (Gymnasium vs Gym)

**4. Notebook Kernel Crashes**
- Reduce batch size or buffer size in deep RL algorithms
- Restart kernel and clear outputs: `Kernel > Restart & Clear Output`

### Version Compatibility

These notebooks are tested with:
- Python 3.8 - 3.11
- Gymnasium 0.29.x
- PyTorch 2.0.x - 2.1.x
- NumPy 1.24.x

If you encounter issues with newer versions, consider using the specified versions.

## 🤝 Contributing

Found a bug or want to improve a notebook? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

These notebooks are part of the Data World documentation project. See the main repository for license information.

## 📚 Additional Resources

### Learning Resources
- [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [OpenAI Spinning Up](https://spinningup.openai.com/)
- [DeepMind x UCL RL Lecture Series](https://www.deepmind.com/learning-resources/reinforcement-learning-lecture-series-2021)

### Gymnasium Documentation
- [Gymnasium Main Docs](https://gymnasium.farama.org/)
- [Environment List](https://gymnasium.farama.org/environments/classic_control/)

### PyTorch Resources
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [PyTorch RL Tutorial](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)

## 📧 Support

For questions or issues:
- Open an issue in the main repository
- Check existing issues for solutions
- Refer to inline comments in notebooks for algorithm-specific questions

---

**Happy Learning! 🎉**

Master reinforcement learning one algorithm at a time.
