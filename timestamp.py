
class Timestamp:
    
    def __init__(self,N = 10) -> None:
        
        self.arr = []
        
        for i in range(N):
            
            self.arr.append(0)
            
    def __gt__(self, t1:object):
       
        if len(self.arr) != len(t1.arr):
            raise NotImplementedError("Length of the 2 timestamps do not match")
        for i in range (len(self.arr)):
            
            if self.arr[i] < t1.arr[i]:
                return False
            
        return True
    
    def _change(self, arr: list):
        
        if len(self.arr) == len(arr):
            
            self.arr = arr
    
    

# t1 = Timestamp(N = 3)
# t2 = Timestamp(N = 4)
# t1._change([1,0,1])

# print(t1>t2)
        
            
        