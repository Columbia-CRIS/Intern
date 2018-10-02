# Genetic Algorithm for Network Topology

## Usage

```
usage: main.py [-h] [--n N] [--e E] [--p P] [--a A] [--c C] [--w W]

A genetic algorithm that generates network topologies based on user input

optional arguments:
  -h, --help  show this help message and exit
  --n N       The number of nodes in the network [2, inf)
  --e E       The number of edges in the network [1, inf)
  --p P       Parent pool size for the GA [2, inf)
  --s S       Number of Generations Without Improvement Before Stopping
  --a A       Alpha value for evaluation: [0, 1]
  --c C       Whether the graph should be connected (default: true)
  --w W       Whether the graph should be weighted (default: false)
  --d D       Whether the graph should be directed (default: false)
```

### Dependencies

To run this program, install the [SciPy Pack](https://www.scipy.org/install.html), a group of essential Python plugins for scientific and data analysis work. Also, install [NetworkX](https://networkx.github.io/) using `pip3 install networkx`.

## Pipeline

This GA will be split into the following components, with each interaction described:

`main.py`
  - Purpose: To initiate and to end the entire process
  - Input: User execution or kill notification, any custom parameters (such as alpha)
  - Output: Best networks and their scores

`generator.py`
  - Purpose: Generate an initial generation of seed networks
  - Input: Custom parameters for network constraints (if any)
  - Output: A network described in an object

`iterator.py`
  - Purpose: Begin and maintain a loop of evaluating and mutating networks
  - Input: Seed network generation from `generator`
  - Output: A best network given certain specified stopping mechanisms

`evaluator.py`
  - Purpose: Runs fitness simulations on networks to evaluate them
  - Input: A network
  - Output: A score

`mutator.py`
  - Purpose: Mutate the networks that performed the best
  - Input: A set of networks (or a network)
  - Output: A new generation of mutated networks

## Changing Evaluation Mechanism
This GA can run on SECON metrics or on the custom metrics. Make these changes in `evaluator.py`.
Uncomment/comment lines 52, 54 for efficiency. Or lines 79, 82-86, 89, 92 for robustness.

### Seeing results
If you run the GA and see images for each generation populating the `img/` folder,
then you can run the following command to convert all of the images into a video:
```
convert -quality 100 -delay 10x100  *.png gen.mpeg
```

### TODO
There are still a couple of things that need to be worked on. For example, a multi-starting point needs to be added as an additional way to overcome local optima. In terms of extensibility, the directedness and weightedness have not been tested since all of the research results have been done on unweighted, undirected graphs. However, the options are there and should be able to be quickly debugged should any issues arise.
