# Q-Learning

Q-learning is one model of reinforcement learning, where a function **Q(s, a)** outputs an estimate of the value of taking action **a** in state **s**.

## Elements
- Enviorment
- Agent
- State **S**
- Set of Actions **Actions(S)**
- Reward Function **R(S, a, s')**




Q(state, action) = Q(state, action) + alpha * (reward + gamma * max(Q(newState, actions)) - Q(state, action))

