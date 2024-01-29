

class parser:
    
    def __init__(self, table:dict, code:list, rules:dict) -> None:
        self.table = table
        self.code = code 
        self.code.append('$')
        self.stack = [0]
        self.state = 0
        self.index = 1
        self.next = code[0]
        self.rules = rules
        self.valid = True


    def run(self):
        for _ in range(len(self.code)):
            if self.state == -1:
                break    
            self.action()

        if self.valid:
            print('Accepted')

    

    def get_next_token(self):
        self.next = self.code[self.index]
        self.index += 1


    def pop(self):
        if self.stack != []:
            x = self.stack.pop()
            return x
    

    def push(self, value):
        self.stack.append(value)


    def error(self):
        print('Syntax Error!')
        self.valid = False


    def shift(self):
        value = self.next
        self.push(value)
        self.push(self.state)
        self.get_next_token()


    def reducee(self, rule):
        pop_size = 2 * self.rules[rule][1]
        for _ in range(pop_size):
            self.pop()

        self.state = self.pop()
        self.push(self.state)
        a = self.rules[rule][0]
        self.push(a)
        self.state = self.go_to(a)
        self.push(self.state)


    def action(self):
        x = self.table[self.state].keys()
        if self.next in x:
            action = self.table[self.state][self.next][:1]
            if action == 's':
                self.state = int(self.table[self.state][self.next][1:])
                self.shift()
            else:
                rule = int(self.table[self.state][self.next][1:])
                self.reducee(rule)
        else:
            self.error()


    def go_to(self, variable):
        x = self.table[self.state][variable]
        return x
        
            


x = { 0: {'int':'s1', '(':'s9', 'S':3, 'E':4, 'T':2},
1: {'+':'r6', '*':'r6', '$':'r6'},
2: {'+':'r4', '*':'r4', '$':'r4'},
3: {'+':'s8', '$':'-1'},
4: {'+':'r2', '$':'r2', '*':'s5'},
5: {'(':'s9', 'int':'s1', 'T':7},
7: {'+': 'r3', '*':'r3', '$':'r3'},
8: {'(':'s9', 'int':'s1', 'E':17, 'T':2},
9: {'(':'s16', 'int': 's15', 'S':10, 'E':13, 'T':14},
10:{'+':'s12', ')':'s11'},
11:{'+':'r5', '*':'r5', '$': 'r5'},
12:{'(':'s16', 'int':'s15', 'E':18, 'T':14},
13:{')':'r2', '+':'r2', '*':'s19'},
14:{'+':'r4', '*':'r4', ')':'r4'},
15:{'+':'r6', '*':'r6', ')':'r6'},
16:{'(':'s16', 'int':'s15', 'S':23, 'E':13, 'T':14},
17:{'+':'r1', '$':'r1', '*':'s21'},
18:{'+':'r1', ')':'r1', '*':'s19'},
19:{'(':'s16', 'int':'s15', 'T':14},
21:{'(':'s9', 'int':'s1', 'T':22},
22:{'+':'r3', '*':'r3', '$':'r3'},
23:{'+':'s12', ')':'s24'},
24:{'+':'r5', '*':'r5', ')':'r5'}
}


rules = {
    1: ['S', 3],
    2: ['S', 1],
    3: ['E', 3],
    4: ['E', 1],
    5: ['T', 3],
    6: ['T', 1]
}