class DFA:
    def __init__(self, states, sigma, start_state, accepting_states, transition_functions):
        self.states = set(states)                               #trạng thái
        self.sigma = set(sigma)                                 #bảng chữ cái
        self.start_state = start_state                          #trạng thái bắt đầu
        self.accepting_states = set(accepting_states)           #trạng thái kết
        self.transition_functions = transition_functions        #hàm chuyển trạng thái
        self.extra_state = "exS"                                #đỉnh thêm mới (nếu có)
        
        self.fill_otomat()
        self.NFA2DFA()
        self.minization_DFA()
    
    #Trạng thái từ state nhận epsilon
    def e_closure(self, state):
        res = set()
        for s in state:
            res.add(s)
            if not s in self.transition_functions:
                continue
            if not '-' in self.transition_functions[s]:
                continue
            new_state = self.transition_functions[s]['-']
            res = res.union(self.e_closure(new_state))
        return res

    #Trạng thái tiếp theo nếu state nhận symbol
    def move(self, state, symbol):
        res = set()
        for s in state:
            if not s in self.transition_functions:
                continue
            if not symbol in self.transition_functions[s]:
                continue
            new_state = self.transition_functions[s][symbol]
            res = res.union(self.e_closure(new_state))
        return res
    
    #Làm đầy đủ otomat
    def fill_otomat(self):
        create_extra_state = False #có tạo đỉnh mới hay ko?
        for s in self.states:
            if not s in self.transition_functions:
                create_extra_state = True
                self.transition_functions[s] = {}
            for symbol in self.sigma:
                if not symbol in self.transition_functions[s]:
                    create_extra_state = True
                    self.transition_functions[s][symbol] = [self.extra_state]
    
        if create_extra_state:
            self.states.add(self.extra_state)
            self.transition_functions[self.extra_state] = {}
            for symbol in self.sigma:
                self.transition_functions[self.extra_state][symbol] = [self.extra_state]


    #Chuyển otomat không đơn định sang đơn định
    def NFA2DFA(self):
        res_states = set()
        res_sigma = [x for x in sigma if x != '-']
        res_start_state = self.e_closure([start_state])
        res_accepting_states = set()
        res_transition_functions = {}

        res_start_state = sorted(res_start_state)

        res_states.add('_'.join(str(v) for v in res_start_state))
        queue = []
        queue.append(res_start_state)
        while queue:
            current_state = queue.pop(0)
            cs = '_'.join(str(v) for v in current_state)
            res_states.add('_'.join(str(v) for v in current_state))
            
            #check trạng thái hiện tại là trạng thái kết
            for acs in self.accepting_states:
                if acs in cs:
                    res_accepting_states.add(cs)

            #thử đi theo các sigma
            for symbol in sigma:
                if symbol == '-':
                    continue
                new_state = self.move(current_state, symbol)
                if not new_state:
                    continue
                new_state = sorted(new_state)
                
                ns = '_'.join(str(v) for v in new_state)
                if not ns in res_states:
                    queue.append(new_state)
                    res_states.add(ns)
                
                if not cs in res_transition_functions:
                   res_transition_functions[cs] = {}
                res_transition_functions[cs][symbol] = ns
                
        self.states = res_states
        self.sigma = res_sigma
        self.start_state = '_'.join(str(v) for v in res_start_state)
        self.accepting_states = res_accepting_states
        self.transition_functions = res_transition_functions
    
    def minization_DFA(self):

        #draw table and mark all pair P \in F and Q not \in F
        table = {}
        for p in self.states:
            if p not in table:
                table[p] = {}
            for q in self.states:
                if q not in table:
                    table[q] = {}
                table[p][q] = 0
                if p in self.accepting_states and q not in self.accepting_states:
                    table[p][q] = 1
                if p not in self.accepting_states and q in self.accepting_states:
                    table[p][q] = 1
                table[q][p] = table[p][q]

        #marked all [P,Q] if [δ(P,symbol), δ(Q,symbol)] is marked
        flag = True
        while flag:
            flag = False
            for p in self.states:
                for q in self.states:
                    if table[p][q] == 1:
                        continue
                    for x in self.sigma:
                        tmpP = self.transition_functions[p][x]
                        tmpQ = self.transition_functions[q][x]

                        if table[tmpP][tmpQ] == 1:
                            table[p][q] = 1
                            flag = True


        #create new states
        new_state = []
        s = {}
        for p in self.states:
            for q in self.states:
                if table[p][q] == 0:
                    if p in s and q not in s:
                        new_state[s[p]].append(q)
                        s[q] = s[p]
                    elif q in s and p not in s:
                        new_state[s[q]].append(p)
                        s[p] = s[q]
                    elif p not in s and q not in s:
                        new_state.append( list(set([p, q])) )
                        s[p] = len(new_state)-1
                        s[q] = s[p]
        
        #combine states
        new_transition_functions = {}
        for ns in new_state:
            for symbol in self.sigma:
                str_ns = '_'.join(str(v) for v in ns)
                if str_ns not in new_transition_functions:
                    new_transition_functions[str_ns] = {}
                next_s = self.transition_functions[ns[0]][symbol]
                next_state = ""
                for nst in new_state:
                    if next_s in nst:
                        next_state = "_".join(str(v) for v in nst)
                        break
                new_transition_functions[str_ns][symbol] = next_state

        #make state and find accepted / start state
        new_acpt = set()
        res_states = []
        for ns in new_state:
            current_state = '_'.join(str(v) for v in ns)
            res_states.append(current_state)
            for s in ns:
                if s in self.accepting_states:
                    new_acpt.add(current_state)
                if s == self.start_state:
                    self.start_state = current_state
        
        self.states = res_states
        self.accepting_states = new_acpt
        self.transition_functions = new_transition_functions

        pass

if __name__ == "__main__":
    print("File input dạng :")
    print("trang_thai_1,trang_thai_2,...,trang_thai_n")
    print("ky_tu_1,ky_tu_2,ky_tu_3,...,ky_tu_4")
    print("trang_thai_khoi_dau")
    print("trang_thai_ket_1,trang_thai_ket_2,...,trang_thai_ket_k")
    print("trang_thai,ky_tu,trang_thai_moi_1,trang_thai_moi_2,..")
    print(".....\n.....\n.....\n")
    print("trang_thai,ky_tu,trang_thai_moi_1,trang_thai_moi_2,..")

    print("\n\n ###################################################### \n\n")
    print("Lưu ý : sử dụng \'-\' thay cho epsilon")
    print("\n\n ###################################################### \n\n")
    states = set()
    sigma = set()
    start_state = ''
    accepting_states = set()
    transition_functions = {}
    
    input_file_name = "example.txt"
    # input_file_name = input("Đường dẫn tới file input : ")
    ip_file = open(input_file_name, 'r')
    states = ip_file.readline()[:-1].split(",")
    sigma = ip_file.readline()[:-1].split(",")

    start_state = ip_file.readline()[:-1]
    if start_state not in states:
        print("File input lỗi : trạng thái bắt đầu  : ", start_state)
        exit()

    accepting_states = ip_file.readline()[:-1].split(",")
    for ac in accepting_states:
        if ac not in states:
            print("File input lỗi : trạng thái kết : ", ac)
            exit()

    # transition_functions
    for x in ip_file:
        tmp = []
        if x[-1] == '\n':
            tmp = x[:-1].split(",")
        else:
            tmp = x.split(",")
        if tmp[0] not in states:
            print("File input lỗi : hàm chuyển : ", x)
            exit()
        if tmp[1] not in sigma+['-']:
            print("File input lỗi : hàm chuyển : ", x)
            exit()
        if len(tmp) < 3:
            print("File input lỗi : hàm chuyển : ", x)
            exit()
        if tmp[0] not in transition_functions:
            transition_functions[tmp[0]] = {}
        transition_functions[tmp[0]][tmp[1]] = tmp[2:]
    ip_file.close()

    print("Otomat trước khi đơn định đơn định : ")
    print("Tập trạng thái : ", set(sorted(states)))
    print("Bảng chữ cái vào : ", set(sorted(sigma)))
    print("Trạng thái khởi đầu : ", start_state)
    print("Tập trạng thái kết : ", set(sorted(accepting_states)))
    
    print("{:<20}".format("δ"), end="")
    for symbol in sigma:
        print("{:<20}".format(symbol), end="")
    print("{:<20}".format("epsilon"), end="\n")

    for s in sorted(states):
        print("{:<20}".format(s), end="")
        for symbol in sigma:
            tmp = '-'
            if not s in transition_functions:
                print("{:<20}".format(tmp), end="")
                continue
            if symbol in transition_functions[s]:
                tmp = ','.join(transition_functions[s][symbol])
            print("{:<20}".format(tmp), end="")
        tmp = '-'
        if not s in transition_functions:
            print("{:<20}".format(tmp), end="")
            continue
        if '-' in transition_functions[s]:
            tmp = ','.join(transition_functions[s]['-'])
        print("{:<20}".format(tmp), end="")

        print()

    print("\n########################################################\n")

    otomat = DFA(states, sigma, start_state, accepting_states, transition_functions)

    print("Otomat sau đơn định + tối thiểu : ")
    print("Tập trạng thái : ", set(sorted(otomat.states)))
    print("Bảng chữ cái vào : ", set(sorted(otomat.sigma)))
    print("Trạng thái khởi đầu : ", otomat.start_state)
    print("Tập trạng thái kết : ", set(sorted(otomat.accepting_states)))

    print("{:<20}".format("δ"), end="")
    for symbol in otomat.sigma:
        print("{:<20}".format(symbol), end="")
    print()
    for s in sorted(otomat.states):
        print("{:<20}".format(s), end="")
        for symbol in otomat.sigma:
            if not s in otomat.transition_functions:
                print("{:<20}".format(tmp), end="")
                continue
            print("{:<20}".format(otomat.transition_functions[s][symbol]), end="")
        print()



###########################################################################################
#Ví dụ otomat = { states, sigma, start_state, accepting_states, transition_functions }
# states = ['A', 'B', 'C']
# sigma = ['0', '1']                                 
# start_state = 'A'                                   
# accepting_states = ['C']

# transition_functions = {                            # '-' nếu biểu diễn epsilon , nếu không có đường đi thì không biểu diễn
#         'A' : {
#             '0' : ['B', 'C'],
#             '1' : ['A'],
#             '-' : ['B']
#         },
#         'B' : {
#             '1' : ['B'],
#             '-' : ['C']
#         },
#         'C' : {
#             '0' : ['C'],
#             '1' : ['C']
#         }
#     }
# ###########################################################################################

# print("Otomat trước khi đơn định đơn định : ")
# print("Tập trạng thái : ", set(sorted(states)))
# print("Bảng chữ cái vào : ", set(sorted(sigma)))
# print("Trạng thái khởi đầu : ", start_state)
# print("Tập trạng thái kết : ", set(sorted(accepting_states)))

# print("{:<20}".format("δ"), end="")
# for symbol in sigma:
#     print("{:<20}".format(symbol), end="")
# print("{:<20}".format("epsilon"), end="")

# print()
# for s in sorted(states):
#     print("{:<20}".format(s), end="")
#     for symbol in sigma:
#         tmp = '-'
#         if not s in transition_functions:
#             print("{:<20}".format(tmp), end="")
#             continue
#         if symbol in transition_functions[s]:
#             tmp = ','.join(transition_functions[s][symbol])
#         print("{:<20}".format(tmp), end="")
    
#     tmp = '-'
#     if not s in transition_functions:
#         print("{:<20}".format(tmp), end="")
#         continue
#     if '-' in transition_functions[s]:
#         tmp = ','.join(transition_functions[s]['-'])
#     print("{:<20}".format(tmp), end="")

#     print()

# print("\n########################################################\n")

# otomat = DFA(states, sigma, start_state, accepting_states, transition_functions)

# print("Otomat sau khi đơn định đơn định : ")
# print("Tập trạng thái : ", set(sorted(otomat.states)))
# print("Bảng chữ cái vào : ", set(sorted(otomat.sigma)))
# print("Trạng thái khởi đầu : ", otomat.start_state)
# print("Tập trạng thái kết : ", set(sorted(otomat.accepting_states)))

# print("{:<20}".format("δ"), end="")
# for symbol in otomat.sigma:
#     print("{:<20}".format(symbol), end="")
# print()
# for s in sorted(otomat.states):
#     print("{:<20}".format(s), end="")
#     for symbol in otomat.sigma:
#         if not s in otomat.transition_functions:
#             print("{:<20}".format(tmp), end="")
#             continue
#         print("{:<20}".format(otomat.transition_functions[s][symbol]), end="")
#     print()
