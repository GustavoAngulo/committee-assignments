# Committee Assignments
Code for assigning committees based on people's preferences

### Algorithm
This committee assignment uses [SciPy's linear sum assignment](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html), which solves for the minimum weight matching in a bipartite graph

### Approach: 
In a bipartite graph (P,C), nodes in P are people, and nodes in C are
spots in a committee (i.e X committee may have N spots, so there are N
nodes for committee X in C). The weights on the edges represent a person's 
preference for those committee's spots. First choice gives weight of 0,
second choice weight of 1, and so on. 


### Notes:
* Requires equal number of people and committee spots
* Idea taken from [Anish Athalye's post](http://www.anishathalye.com/2016/10/07/algorithms-in-the-real-world-committee-assignment/)
