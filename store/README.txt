Store - optimize the placement of products in the store
        to maximize daily revenue
-------------------------------------------------------(05-Jan-2020)

item_counts.npy  -  total counts for each of the 169 items
item_names.npy   -  names for each item (same order as counts)

Goal:
    Decide how to arrange the items in the store to maximize daily profit

Store:
    The store is one dimensional, agents pass from the left to the right
    looking at each product.

Agents:
    Each agent is after a randomly selected item and will stop shopping when
    it reaches that product, which it will buy.  Additionally, each agent
    has a random set of products assigned that it will buy with a certain
    probability if it encounters the product before reaching the target
    product.

Process:
    - Generate a set of random product placements
    - For each iteration:
        - Generate a collection of N randomly generated agents
        - Pass the agents through each of the "stores"
        - Calculate the total revenue from the agents, seek to maximize this
        - Update the product placement according to the particular optimization
          algorithm

