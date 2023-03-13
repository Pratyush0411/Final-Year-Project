


class Graph:
    
    '''
    connection has 3 possible values: "fully_connected", "hard_code"
    '''
    
    def __create_fully_connected(self,num_nodes):
        
        adj_list = {}
        
        for i in num_nodes:
            adj_list[i] = []
            for j in range(num_nodes):
                
                if j != i:
                    adj_list[i].append(j)
                    
        self.graph = adj_list
    
    def __create_hardcoded(self, num_nodes):
        
        
        if num_nodes == 6:
            
            self.graph = {
            1: [0,2,4],
            0: [1,5,4],
            4: [0,1,3],
            5: [0,3,2],
            2: [1,3,5],
            3: [2,4,5]
            }
        
        elif num_nodes == 10:
            
            self.graph = {
            1: [0,2,4,5],
            8: [4,5,7,9],
            4: [0,1,3,5,7,8],
            5: [1,2,6,8,9,4],
            0: [1,3,4],
            2: [1,6,5],
            3: [0,4,7],
            6: [2,5,9],
            7: [3,4,8],
            9: [8,5,6]
            }
            
            
    
    def __init__(self,num_nodes = 10, connection:str = "fully connected"):
        
        self.graph = {}
        
        if connection == "fully connected":
            self.__create_fully_connected(num_nodes)
            
        elif connection == "hard_coded":
            if num_nodes in [6,10]:
                self.__create_hardcoded(num_nodes)
            else:
                self.__create_fully_connected(num_nodes)
                
        else: 
            self.graph = None
        
        
    