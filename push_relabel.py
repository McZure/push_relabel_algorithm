import sys

# Global variables
NODE = []
EDGE = []

class Node:
    def __init__(self, id, height, excess, source, sink):
        self.id = id
        self.height = height
        self.excess = excess
        self.source = source
        self.sink = sink
        self.via = False
        self.adjacent = False
        self.selected = False
        self.relabelled = False
    
    def toGraph(self):
        color = "grey"  # Initial node
        if self.selected:
            color = "red"  # Selected to receive excess flow
        elif self.relabelled:    
            color = "blue"  # Relabel on vertex
        elif self.via:
            color = "green"  # Current node
        elif self.adjacent:
            color = "yellow"  # Adjacent node
        elif self.id == self.source:
            color = "pink"  # Source node
        elif self.id == self.sink:
            color = "orange"  # Sink node

        return {
            "id": str(self.id),
            "label": f"{self.height}:{str(self.excess)}",
            "color": color,
        }

class Edge:
    def __init__(self, u, v, capacity, flow, backward: bool = False):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow
        self.backward = backward

    def toGraph(self):
        return {
            "from": str(self.u),
            "to": str(self.v),
            "label": str(self.flow),
            "style": "dotted" if self.backward else "solid",
            "color": "black",
        }

    def __str__(self) -> str:
        return str(
            {
                "from": self.u,
                "to": self.v,
                "capacity": self.capacity,
                "flow": self.flow,
                "isBackward": self.backward,
            }
        )

def graph():
    """
    draw a graph
    """
    global GRAPH, RESIDUAL
    GRAPH = {
        "kind": {"graph": True},
        "nodes": [node.toGraph() for node in NODE],
        "edges": [edge.toGraph() for edge in EDGE if not edge.backward],
    }

    # generate residual graph based on edges
    residualEdges = []
    for edge in EDGE:
        if edge.backward:
            continue

        forwardFlow = edge.capacity - edge.flow
        if forwardFlow != 0:
            forwardEdge = Edge(edge.u, edge.v, edge.capacity, forwardFlow)
            residualEdges.append(forwardEdge)

        backwardFlow = edge.flow
        if backwardFlow != 0:
            backwardEdge = Edge(edge.v, edge.u, edge.capacity, edge.flow, True)
            residualEdges.append(backwardEdge)

    RESIDUAL = {
        "kind": {"graph": True},
        "nodes": [node.toGraph() for node in NODE],
        "edges": [edge.toGraph() for edge in residualEdges],
    }

def preFlow(source):
    """
    set the height of the source node to N, 
    where N is the number of nodes, 
    the height of all other nodes is 0, 
    and the height of the sink node is fixed to 0
    """

    # Set the height of source vertex as the number of nodes
    NODE[source].height = len(NODE)

    for edge in EDGE:
        # Find adjacent nodes of the source
        if edge.u == source:
            edge.flow = edge.capacity

            # Set excess flow of these nodes to max
            des = edge.v
            NODE[des].excess += edge.flow

            # Create an edge in the residual graph for adjacent nodes back to source
            edge_back = Edge(des, source, edge.capacity, 0, True)
            EDGE.append(edge_back)
            graph()

def push(u):
    """
    find a node u whose excess flow is greater than 0 from all nodes, 
    and push its excess flow to its adjacent node v as much as possible.
    excess flow pushed to the adjacent node is the minimum of excess flow and the available capacity of the edge.
    """

    for i, edge in enumerate(EDGE):
        # find all edges connecting to a node
        if edge.u == u:
            # if the current edge' capacity reached its maximum, then push operation is infeasible
            if edge.flow == edge.capacity and not edge.backward:
                continue

            # make sure the height of current node is larger than the adjacent node
            source = NODE[u]
            des = NODE[edge.v]

            if source.height > des.height:
                NODE[u].via = True

                # update the graph
                for e in EDGE:
                    if e.u == u:
                        NODE[e.v].adjacent = True
                        graph()
                
                NODE[edge.v].selected = True
                graph()

                # flow should be set to the minimum of remaining available flow of the edge and excess flow of the node
                flow = min(edge.capacity - edge.flow, source.excess)

                # transfer the flow from source to destination
                source.excess -= flow
                des.excess += flow
                edge.flow += flow

                # updates the flow of an backward edge
                currentEdge = EDGE[i]
                for ee in EDGE:
                    # retrieve the backward edge
                    if ee.u == currentEdge.v and ee.v == currentEdge.u:
                        ee.flow -= flow
                        graph()
                        break
                # creates a new backward edge if it does not exist
                if ee.u != currentEdge.v and ee.v != currentEdge.u:
                    new_edge = Edge(currentEdge.v, currentEdge.u, flow, 0, True)
                    EDGE.append(new_edge)
                    graph()

                # update the graph
                NODE[edge.v].selected = False
                graph()

                NODE[u].via = False
                for eee in EDGE:
                    if eee.u == u:
                        NODE[eee.v].adjacent = False
                graph()

                return True

    # if the push is unsuccessful, update the graph
    NODE[u].via = False
    for edge in EDGE:
        if edge.u == u:
            NODE[edge.v].adjacent = False
    graph()

    return False

def relabel(u):
    """
    Initialize the height of all nodes to 0 except the source.
    When the flow storage of a node is greater than 0 but the flow does not flow out, 
    increase the height of the node by 1, 
    so that the flow storage of the node flows into the node lower than it.
    """
    # prepare the minimum height for future comparsions
    minHeight = sys.maxsize

    for edge in EDGE:
        if edge.u == u:
            # if the max capacity is reached, relabel is infeasible
            if edge.flow == edge.capacity:
                continue

            NODE[u].relabelled = not NODE[u].relabelled
            graph()

            des = NODE[edge.v]
            # update the height current node and retrieve the minimum height of all adjacent nodes
            if des.height < minHeight:
                minHeight = des.height
                currentNode = NODE[u]
                currentNode.height = minHeight + 1
                graph()
    
    if NODE[u].relabelled:
        NODE[u].relabelled = False
        graph()

def excess(source, sink) -> int:
    # test existiong excess flows in the graph, which means push or relabel operation is needed
    for i, node in enumerate(NODE):
        # sink node's excess flow is not under consideration
        if node.id == source or node.id == sink:
            continue

        if node.excess > 0:
            return i
    return -1
            
        
def push_relabel(source, sink) -> int:
    """
    use push & relabel to find the maximum flow and return it
    """
    preFlow(source)

    node = -1
    for i, n in enumerate(NODE):
        # sink node's excess flow is not under consideration
        if n.id == source or n.id == sink:
            continue

        if n.excess > 0:
            node = i

    while node >= 0:
        # Push is infeasible if the node has the same height as all adjacent vertices, and then relabel it
        if not push(node):
            relabel(node)
        node = excess(source, sink)
        

    # When it is located at the last node in the array, any excess flow is the max flow
    return NODE[sink].excess

if __name__ == "__main__":
    # editable, change the following numbers to create different graphs
    source = 0
    num = 6 # number of nodes
    sink = num - 1

    # generate nodes
    for i in range(num):
        node = Node(i, 0, 0, source, sink)
        NODE.append(node)
    graph()

    # editable, change the following data to create different graphs
    # *Edge(source, destination, capacity, backward or not), just keep the last parameter as 0
    edge = Edge(0, 1, 10, 0)
    EDGE.append(edge)
    edge = Edge(1, 2, 5, 0)
    EDGE.append(edge)
    edge = Edge(0, 3, 8, 0)
    EDGE.append(edge)
    edge = Edge(1, 3, 2, 0)
    EDGE.append(edge)
    edge = Edge(3, 4, 10, 0)
    EDGE.append(edge)
    edge = Edge(4, 2, 8, 0)
    EDGE.append(edge)
    edge = Edge(4, 5, 10, 0)
    EDGE.append(edge)
    edge = Edge(2, 5, 7, 0)
    EDGE.append(edge)
 
    graph()
    print("The maximum flow is ",push_relabel(source, sink))