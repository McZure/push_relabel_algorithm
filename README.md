# push_relabel_algorithm
**Push-Relabel algorithm idea：**
For a network flow graph: the algorithm can be intuitively understood in this way, first add sufficient flow at the source node(The sum of the capacities of all edges connected to the source node).
Then start to transfer the flow to the sink side by side until it can no longer transfer more flow(Similar to the Ford-Fulkerson algorithm, the augmentation path cannot be found).
Then some remaining flows can be recycled to the source node s at this time, mainly two steps: push and relabel.
Push means to find a node u whose water storage is greater than 0 from all nodes, and push its stored water to its adjacent node v as much as possible.
To implement the push operation, the following conditions must be met: the flow storage at this point e(u)>0, and the height of node u is greater than the height of node v.
The flow value of this push (u,v).f=min((u),(u,v).capacity), while (u,v).capacity is the current capacity of edge(u,v), this value will keep changing during the process.
Relabel indicates that when the flow storage of a node is greater than 0 but the flow does not flow out, we increase the height of the node by 1, so that the flow storage of the node flows into the node lower than it.
At the beginning, we set the height of the source node to N, where N is the number of nodes, the height of all other nodes is 0, and the height of the sink node is fixed to 0, and the height of other nodes will change during the execution of the algorithm.

**Compare with Ford-Fulkerson Algorithm:**
The Push-Relabel method is more efficient than the Ford-Fulkerson algorithm. Like Ford-Fulkerson, Push-Relabel also works on residual graphs (a residual graph of a flow network is a graph that indicates other possible flows. If there is a path from a source to a sink in the residual graph, the flow can be added). In Ford-Fulkerson, the net difference between the total outflow and total inflow for each vertex (except sources and sinks) remains 0. The Push-Relabel algorithm allows the inflow to exceed the outflow before the final outflow. In the final flow, all but the source and sink have a net difference of 0.The Push-Relabel algorithm works in more restricted places. The Push-Relabel algorithm does not work on one vertex at a time, instead of checking the entire residual network to find an augmenting path.

**Core Functions:**
There are three main operations in the Push-Relabel algorithm:
I. PreFlow(): 1) Initialize height and flow of every vertex as 0.
              2) Initialize height of source vertex equal to total number of vertices in graph.
              3) Initialize flow of every edge as 0.
              4) For all vertices adjacent to source s, flow and  excess flow is equal to capacity initially.
II. Push():  is used to generate traffic from nodes with excessive traffic. If a vertex has excess flow, and there is an adjacent lower height (in the residual graph),              we push the flow from the vertex to the adjacent lower height. The push flow through the pipe (edge) is equal to the minimum of excess flow and edge                    capacity. 
III. Relabel(): is used when a vertex has excess flow and none of its adjacent vertices are at lower heights. We basically increase the height of the vertex so that                push() can be performed. To increase the height, we choose the adjacent minimum height (in the residual plot, the adjacent height where the flow can be                added) and add 1 to it.

**Time Complexity:**
The maximum growth of the vertex i in the Push-Relabel algorithm is 2V-1, (mathematically confirmable), so in the end, a point i that may be adjacent to the source will be in the form of height h(i)>V. The excess is returned to the source (the height value of the source is always V); The complexity of Push-Relabel algorithm is O(V^2 *E)

**About Code:**
The input are vertices and edges which can form a graph. The output is the maximum flow of the giving graph.
To creat different graphs, you can change data under MAIN method in editable areas (which have comments on it)
The main purpose is to show the process of the Push-Relabel algorithm.


During the process, you can see the transformation of the graph and the color changes on the nodes/vertices. I use RED to indicate that the node/vertex is selected to receive the excess flow; BLUE to indicate that the relabel operation is going on the node/vertex; GREEN to illustrate that it is the current node/vertex where the flow is passing; YELLOW to show all nodes/vertices adjacent to the current node/vertex. The source node will be marked with PINK color, while the sink node will be marked with ORANGE color. I also wrote comments in the python file to explain the meaning of each used color.
To realize the visualization of the push-relabel process, I add some breakpoints to pause the process. 
•	On line 153, the breakpoint serves the step that is selecting the node where the flow is going to; 
•	on line 157, the breakpoint serves the step that is showing the selected node and its adjacent nodes; 
•	on line 226, the breakpoint serves the step that is showing the node where the relabel operation performed to increase its height; 
•	on line 246, the breakpoint serves the step which reflects the changes of the graphs till none of the nodes have excess flow; 
•	on line 259, the breakpoint serves to illustrate the node selected for relabeling; 
•	on line 260, the breakpoint serves to give a view of the graph before the relabel operation; 
•	on the last line, there is also a breakpoint serves to see the final max-flow graph and its residual graph as well. 
When the graph changes, you can focus on the current node and observe the changes on the adjacent nodes and edges to know how the flow transfers between nodes.

To show the graph, need to have Debug Visualizer in VScode
Ctrl + Shift + P -> Debug Visualizer: New View
Enter *GRAPH* into input box
Ctrl + Shift + P -> Debug Visualizer: New View
Enter *RESIDUAL* into input box
Shift + F10 to reflect changes in the graph
