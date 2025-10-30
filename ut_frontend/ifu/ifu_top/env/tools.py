from typing import TypeVar, Generic, Optional
T=TypeVar("T")

class FakeReg(Generic[T]):
    def __init__(self, init_val: T=0, default_ret_cur=True):
        self.cur:T = init_val
        self.next:T = init_val
        self.default_ret_cur = default_ret_cur

    def fresh(self):
        self.cur = self.next

    def get_cur(self) -> T:
        return self.cur
    
    def get_next(self) -> T:
        return self.next
    
    def set(self, val):
        self.next = val

    def get(self) -> T:
        if self.default_ret_cur:
            return self.get_cur()
        return self.get_next()

    
# class StagesReg():
#     def __init__(self, start=0, end=4, init_val=0):
#         self.regs : dict[int, FakeReg] = {}
#         self.start = start
#         self.end = end
#         for i in range(start, end+1):
#             self.regs[i] = FakeReg(init_val=init_val)
    
#     def set(self, val):
#         self.regs[self.start].set(val)
    
#     def fresh(self, fires: dict[int, bool]):
#         for i in range(self.end+1, self.start-1, -1):
#             if (i > self.start) and fires[i]:
#                 self.regs[i].set(self.regs[i-1].get_cur())
#             # self.regs[i].fresh()
    
#     def get(self, idx):
#         if idx not in self.regs.keys():
#             print("key err! please check!")
#             return None
        
#         return self.regs[idx].get()


class StagesWire(Generic[T]):
    

    def __init__(self, start: int = 0, end: int = 4, init_val: T = None):
        self.wires: dict[int, T] = {}
        self.start: int = start
        self.end: int = end
        for i in range(start, end+1):
            self.wires[i] = init_val
        

    def set(self, val: T) -> None:
        self.wires[self.start] = val

    def fresh(self, fires: dict[int, bool]) -> None:
        # 从高到低搬运（i <- i-1），只在该级 fire 时搬
        for i in range(self.end, self.start, -1):
            if fires.get(i, False):
                self.wires[i] = self.wires[i - 1]

    def get(self, idx: int) -> T:
        if idx not in self.wires:
            raise KeyError(f"idx {idx} not in [{self.start}, {self.end}]")
        return self.wires[idx]      
    

class StagesWireManager(Generic[T]):
    def __init__(self):
        self.wires: list[StagesWire] = []

    def create(self, start: int = 0, end: int = 4, init_val: Optional[T] = None) -> StagesWire[T]:
        new_wire = StagesWire(start=start, end=end, init_val=init_val)
        self.wires.append(new_wire)
        return new_wire

    def fresh_all(self, fires: dict[int, bool]):
        for wire in self.wires:
            wire.fresh(fires)

class StagesReg(Generic[T]):
    def __init__(self, start: int = 0, end: int = 4, init_val: T = None):  # type: ignore[assignment]
        self.regs: dict[int, FakeReg[T]] = {}
        self.start: int = start
        self.end: int = end
        for i in range(start, end + 1):
            self.regs[i] = FakeReg[T](init_val) 
    
    def set(self, val: T) -> None:
        self.regs[self.start].set(val)
    
    def fresh(self, fires: dict[int, bool]) -> None:
        # 从高到低搬运（i <- i-1），只在该级 fire 时搬
        for i in range(self.end, self.start, -1):
            if fires.get(i, False):
                self.regs[i].set(self.regs[i - 1].get_cur())
        # 统一提交
        # for r in self.regs.values():
        #     r.fresh()
    
    def get(self, idx: int) -> T:
        if idx not in self.regs:
            raise KeyError(f"idx {idx} not in [{self.start}, {self.end}]")
        return self.regs[idx].get()       