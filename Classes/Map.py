
''' Defining a network of Vertices and Edges, where vertices are chambers, and edges are the connections/components existing between chambers'''


class Map: 
    def __init__(self): 
        ''' key is id assigned to vertex: Chamber instance'''
        self.graph = {} 
    

    def print_graph_info(self): 
        for chamber in self.graph.values(): 
            print(chamber)                       # chamber id and adjacent vertices
            for adj in chamber.connections.keys(): 
                edge = chamber.connections[adj]  
                print(edge)                      # edge id and vertices it connects
                print(edge.headval)              # all components on edge
            

    def new_chamber(self, id): 
        ''' new Chamber instantiated and added to graph'''
        self.graph[id] = self.Chamber(id)

    
    def new_shared_edge(self, id, v1, v2, components=None):
        ''' single Edge object that is shared by both vertices. Ordering of linked list will require checking the vertex indices ''' 
        if not all(v in self.graph.keys() for v in [v1, v2]): raise Exception(f'Could Not Create Edge: one or both of the chambers has not been created yet, so could not add edge between them.')
        newEdge = self.Edge(id, v1, v2,'shared')
        self.graph[v2].connections[v1] = newEdge 
        self.graph[v1].connections[v2] = newEdge
        return newEdge
        

    def new_unidirectional_edges(self, id, v1, v2, components=None): 
        ''' creates 2 new Edges for connecting 2 chambers -- each has a different Edge instance tho, so components may differ '''
        if not all(v in self.graph.keys() for v in [v1, v2]): raise Exception(f'Could Not Create Edge: one or both of the chambers has not been created yet, so could not add edge between them.')
        self.graph[v1].connections[v2] = self.Edge(id,v1,v2) # add edges to vertices' adjacency dict 
        rev_id = int(str(id)[::-1]) # reverse the id for the edge going the reverse direction 
        self.graph[v2].connections[v1] = self.Edge(rev_id,v2,v1)

    
    def get_edge(self, edgeid): 
        # sort thru chamber edges and locate edge with <id> 
        for cid in self.graph.keys(): # for all chambers stored in graph
            chamber = self.graph[cid] # get Chamber object
            for adj_id in chamber.connections.keys(): # for all of its adjacent vertices 
                if chamber.connections[adj_id].id == edgeid: # check if vertex has edge w/ that id 
                    return chamber.connections[adj_id]

        raise Exception(f'Edge {edgeid} Not Found')

    

    # 
    # Chamber -- vertices in the graph
    #  
    class Chamber: 
        def __init__(self,id): 
            self.id = id 
            self.connections = {} # adjacent chamber: a single Edge object which points to linked list of components
        
        def __str__(self): 
            return 'Chamber: ' + str(self.id) + ', adjacent: ' + str([x for x in self.connections])

    #
    # Edges -- linked list for storing Components
    # 
    class Edge:    
        def __init__(self, id, chamber1, chamber2, type=None): 
            
            # Identifying Edge w/ id val and the chambers it connects 
            self.id = id 
            self.v1 = chamber1 
            self.v2 = chamber2
            self.type = type 

            # Component Makeup of the Edge 
            self.headval = None # will point to first instance of Component
        
        def __str__(self): 
            if self.type=='shared': 
                return 'Edge ' + str(self.id) + f', connects: {self.v1} <-> {self.v2}'

            return 'Edge ' + str(self.id) + f', connects: {self.v1} -> {self.v2}'


        def find_component(self, interactable): 
            # beginning at headval, traverses linked list to find component. Returns None if it does not exist
            
            if (self.headval.interactable == interactable): 
                return self.headval 

            c = self.headval
            while(c.nextval): 
                c = c.nextval 
                if c.interactable == interactable: 
                    return c 
            return None # c does not exist in linked list 

        def new_component(self, newinteractable): 
            # instantiates new Component and adds to end of linked list
            newComp = self.Component(newinteractable)

            if self.headval is None: 
                self.headval = newComp
                return newComp
            
            component = self.headval 
            while(component.nextval):
                component = component.nextval # list traversal to get last component in linked list 
                if component.interactable == newComp.interactable:                 
                    # check that component is not a repeat 
                    del newComp
                    raise Exception(f'component not added because this component has already been added to the edge')
            
            
            component.nextval = newComp # update list w/ new Component
            newComp.prevval = component # set new Component's previous component to allow for backwards traversal     
            return newComp
                

        def add_component_after(self, newinteractable, previnteractable): 
            # instantiates and adds new component directly after the specified interactable (so can be in middle of linked list if desired) 

            if (self.find_component(newinteractable)) is not None: raise Exception(f'{newinteractable} already exists on this edge')
            
            # if previous component set to None, then make new component the new head of Linked List
            if previnteractable is None: 
                if self.headval is None: 
                    return self.new_component(newinteractable)
                else: 
                    prevhead = self.headval 
                    self.headval = self.Component(newinteractable)
                    self.headval.nextval = prevhead
                    return self.headval
            
            else: 
                prevComp = self.find_component(previnteractable) # retrieve prevComp and check that it exists 
                if prevComp is None: 
                    raise Exception(f'{previnteractable} must already exist on this edge to add a component that follows it, so could not add {newinteractable}')

                # once prevcomponent is located, instantiate new component and update the vals of the previous component, current component, and next component
                newComp = self.Component(newinteractable)
                newComp.prevval = prevComp 
                newComp.nextval = prevComp.nextval

                # update the components on either side of newComp to reflect changes
                prevComp.nextval = newComp 
                newComp.nextval.prevval = newComp 
                return newComp


        
        '''
        def add_component_at_idx(self, newcomponent, idx) # adds new component at position <idx> in the linked list
        '''    

            

        class Component: 
            def __init__(self, interactable): 
                self.interactable = interactable # dataval 
                self.nextval = None
                self.prevval = None
            
            def __str__(self): 
                return str(self.interactable) + f', {self.nextval}'

                ''' add any attributes here that are for tracking status of component but are only relevant to the Simulation '''
                '''
                Attributes 
                self.prob_success # probability that vole successfully interacts (meets threshold) w/ the component
                '''
                