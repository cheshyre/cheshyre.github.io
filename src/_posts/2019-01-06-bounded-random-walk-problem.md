---
title: "The Bounded Random Walk"
categories: physics
layout: post
include_math: true
---

Recently, my brother and I discussed a problem which could effectively be phrased as follows:

> You have a 1-dimensional random unbiased walk that reaches a boundary at $B$ and $-B$. What is the expectation value for the number of steps $N$ it will take the walk to reach a boundary?

Fairly quickly, I came to the conclusion that this must be $B^2$, arguing that for large $N$ steps the random walk follows a Gaussian distribution with standard deviation $\sqrt{N}$ and when the width of the distribution reaches the boundary $B$ corresponds to the expected time to reach the boundary. I wrote some code to simulate many bounded random walks and the results seemed to match this result, so initially I was satisfied.

Thinking about it more, I became increasingly unsatisfied with this argument, especially when I observed that the distribution of times of a walk to the boundary was far from normal. While the previous argument can be understood to give roughly the correct order of magnitude, it can also be shown using a similar argument that based on the distribution of walks for large $N$, the *median* time to the boundary is $0.756B^2$. This argument is as follows: Once a particle reaches the boundary, how it moves from there is a new random walk, which has a symmetric distribution centered at the boundary. Thus, when $25$% of particles are outside the boundary, $50$% should have reached the boundary. This corresponds to a P-value of $1.15$, giving the equation: $1.15\sqrt{N} = B$.

The following describes how to analytically compute the mean time, which is in fact $B^2$. It also briefly discusses the full distribution of times. My only complaint is that this solution does not build off of previous knowledge on the behavior of 1-dimensional random walks at all. If you know of a better way to understand this exact solution, please let me know because I am legitimately curious. I also want to thank torchlight, whom I consulted regarding this problem. They solved it quickly and pointed me to some excellent references which allowed me to solve it as well.

# The Solution

This problem is an example of a Markov chain stopping time problem, and, as a result, my solution is based on a Markov chain formulation of the random walk. Markov chains have the property that the probability to be in a state at $t=n+1$ is given in terms of the probability distribution at $t=n$ in the transition probabilities between states. For systems with discretized states, this can be written as a transition matrix:

$$
\begin{array}{c|lcr}
 & \textbf{1} & \textbf{2} \\
 \hline
 \textbf{1} & 0.7 & 0.3 \\
 \textbf{2} & 0.2 & 0.8
\end{array}.
$$

Here the row represents the current state and the column represents the potential next state so $M_{ij} = P(j_{t+1}\|i_{t})$. I will be using the transition matrix going forward, leaving off state labels after discussing briefly what the state space looks like.

For the bounded random walk, we have states ranging from $-B$ to $B$ in integer steps, where $-B$ and $B$ are final states, so they transition to themselves with $P=1$. The resulting matrix looks as follows for $B=2$:

$$
\begin{pmatrix}
1 & 0 & 0 & 0 & 0 \\
0.5 & 0 & 0.5 & 0 & 0 \\
0 & 0.5 & 0 & 0.5 & 0 \\
0 & 0 & 0.5 & 0 & 0.5 \\
0 & 0 & 0 & 0 & 1
\end{pmatrix}.
$$

So we get a square transition matrix with dimension $2B + 1$. Now we want to compute the expected time to reach a final state from this. We can rephrase is this as how many steps is a state $x$ away from the goal on average and define that for states $-B$ and $B$ this is 0. Using notation from Rick Durrett's "Essentials of Stochastic Processes", we define $g(x)$ to be the expected time to the boundary for a state $x$. Thus, $g(-B)=0$ and $g(B)=0$. By considering the state $0$, we can see that:

$$
\begin{equation}
g(0) = 1 + 0.5 g(1) + 0.5 g(-1).
\end{equation}
$$

Important here is the $1$ in the sum which represents the fact that we need to take a step in time to reach states $-1$ and $1$. More generally, we can write this as $1$ plus a sum over the product of the transition probability from $x$ to $y$ and the expected time to the boundary for $y$ for all states $y$.

$$
\begin{equation}
g(x) = 1 + \sum_y p(x \to y)g(y)
\end{equation}
$$

Re-expressing this linear system of equations in terms of vectors and matrices will prove useful, because we can easily use the transition matrix we know here. We will also cut off the rows and columns corresponding to the final states, so now our "reduced" transition matrix $T$ has dimension $2B - 1$. In the following equations, $g$ and $\textbf{1}$ are vectors of the correct dimension with $\textbf{1}$ being a vector of $1$s, and $I$ is the identity matrix with the correct dimension.

$$
\begin{equation}
g = \textbf{1} + Tg
\end{equation}
$$


$$
\begin{equation}
(I - T)g = \textbf{1}
\end{equation}
$$

Assuming $I - T$ is invertible, this gives us an easy way to solve for $g$, which will give us the expected distance of all states. For the $B=2$ case, $M=I-T$ is:

$$
\begin{pmatrix}
1 & -0.5 & 0 \\
-0.5 & 1 & -0.5 \\
0 & -0.5 & 1
\end{pmatrix}.
$$

This is a tri-diagonal Toeplitz matrix that is invertible and there is an analytic expression for the inverse. Computing this inverse for general $B$ is beyond me, so I won't discuss it here. The inverse is symmetric, depends on its dimension $n$, and is defined for $j \geq i$ as:

$$
\begin{equation}
(T_n)_{ij}^{-1} = 2 i \frac{n+1-j}{n+1}.
\end{equation}
$$

Note that defining the inverse for one half is sufficient because it is symmetric. We can now do the inversion and the following product into $\textbf{1}$ by hand. To make it easier, we note that state $0$ corresponds to $i=B$ in our $2B - 1$-dimensional space. Thus we can focus only on this element of $g$.

$$
\begin{align}
g(0) & = \sum_{j=1}^B\Big(2 j \frac{(2B - 1) + 1 - B}{(2B - 1) + 1}\Big) + \sum_{j=B+1}^{2B - 1}\Big(2B \frac{(2B - 1) + 1 - j}{(2B - 1) +1}\Big) \\
g(0) & = \sum_{j=1}^B (j) + \sum_{j=B+1}^{2B-1}(2B - j) \\
g(0) & = \sum_{j=1}^B (j) + \sum_{j=1}^{B-1}(B - j) \\
g(0) & = \sum_{j=1}^B (j) + \sum_{j=1}^{B-1}(B) - \sum_{j=1}^{B-1}(j) \\
g(0) & = B^2 - B + B \\
g(0) & = B^2
\end{align}
$$

And this gives us the same solution as the one incorrectly argued previously.

# The Distribution

This distribution for the number of steps it would take a walk to reach a boundary is a type of [phase-type distribution](https://en.wikipedia.org/wiki/Discrete_phase-type_distribution). I recommend looking at the previous link to read up on it some more. We define $\tau$ to be a vector that is all $0$s besides a single $1$ at the $B$-th position, which corresponds to the starting distribution of the walk.

The distribution is given by:

$$
\begin{equation}
f(N) = \tau T^{N - 1} \textbf{T}^0.
\end{equation}
$$

Here $\textbf{T}^0$ is given by $\textbf{T}^0 = (I - T)\textbf{1}$. The interpretation for this formula is that we evolve our initial state $\tau$ via the transition matrix $N - 1$ times and then evolve one more step and project on the final state with $\textbf{T}^0$.
This can be computed for fairly small systems and gives the distribution below, shown for $B=30$.

![Distribution](/assets/images/post/2019-bounded-random-walk/distribution.svg)

# Conclusion

This was a hopefully understandable explanation of how to arrive correctly at the $B^2$ value for the expectation time. I found it interesting to learn about Markov chains and stochastic processes, and I plan on looking at more complex random walks in my free time in the future.
