#Pentru majoritatea laboratorelor am inceput prin a face varianta hard-coded apoi am facut o alta varianta cu citirea din fisier
#Varianta cu citire din fisier e cea relevanta, pe cealalta am pastrat-o desi e irelevanta
#In orice caz am pus in arhiva doar fisierele de input pentru variantele relevante

#%%
#citirea si afisarea unei matrici
fin = open("input.in", "r")
fout = open('output.out', "w")
linia1 = fin.readline()
n, m = map(int, linia1.split())
lines = fin.readlines()
a = [[int(x) for x in lines[i].split()] for i in range(n)]
for row in a:
    fout.write(" ".join(map(str, row)) + "\n")

fin.close()
fout.close()
#%%
#DFA hard-coded
fin = open("asdf.in", "r")
okk=0
a = []
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if not all(c in "01" for c in line):  
        print("Invalid input")
        okk=1
        break
    a.extend(map(int, line))  

fin.close()
states={0,1}
alphabet={0,1} 
state=0
startstate=state
if(okk==0):
    for i in range(len(a)):
        ok=0
        if(state==0 and ok==0):
            if(a[i]==0):
                state=0
                ok=1
            if(a[i]==1):
                state=1
                ok=1
        if(state==1 and ok==0):
            if(a[i]==0):
                state=0
                ok=1
            if(a[i]==1):
                state=1
                ok=1
    print(state)
with open("asdf.out", "w") as fout:
    fout.write(f"States: {states}\n")
    fout.write(f"Alphabet: {alphabet}\n")
    fout.write(f"Initial State: q{startstate}\n")
    fout.write(f"Final State: q{state}\n")
    fout.write("Accepting State: q1\n")
    if(state==0):
        fout.write("Rejected")
    else:
        fout.write("Accepted")
#%%
#DFA cu input din fisier
#Aparent nu il facusem chiar bine la laborator asa ca l-am mai schimbat putin si am adaugat comentarii la cod
fin = open("dfa.in", "r")

# Citire:
states = set()
alphabet = set()
startstate = None
accept_states = set()
transitions = {}  #formatul tranzitiilor: [state] [input] -> [state] de ex: 0 1 -> 1
string_ok=1
mode = None
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):#pentru a ingnora comentariile
        continue

    if line.startswith("states:"):
        states = set(map(int, line.split(":")[1].strip().split()))
    elif line.startswith("alphabet:"):
        alphabet = set(map(int, line.split(":")[1].strip().split()))
    elif line.startswith("start_state:"):
        startstate = int(line.split(":")[1].strip())
    elif line.startswith("accept_states:"):
        accept_states = set(map(int, line.split(":")[1].strip().split()))
    elif line.startswith("transitions:"):
        mode = "transitions"
    elif mode == "transitions":
        if "->" not in line: #daca linia nu are -> (si nici #) atunci e input string
            mode = "inputs"
        else:
            parts = line.split()
            #validarea formatului
            if len(parts) != 4 or parts[2] != "->":
                print(f"Invalid transition format: {line!r}")
                string_ok=0
                break

            src = int(parts[0]) #stare_curenta
            sym = int(parts[1]) #input
            nxt = int(parts[3]) #stare actualizata

            if src not in states or sym not in alphabet or nxt not in states:
                print(f"Transition has unknown state or symbol: {line!r}")
                string_ok=0
                break
            transitions[(src, sym)] = nxt
            continue

    if mode == "inputs":
        try:
            symbols = list(map(int, list(line)))
        except ValueError:
            print("Line has invalid symbols (not in the alphabet):", line)
            string_ok=0
            break
        if not all(sym in alphabet for sym in symbols):
            print("Invalid input string (symbol outside alphabet):", line)
            string_ok=0
            break
        if "inputs" not in globals():
            inputs = []
        inputs.append(symbols)

fin.close()

for q in states:
    for a in alphabet:
        if (q, a) not in transitions:
            print(f"Missing transition for state {q}, symbol {a}")
            string_ok=0
#sfarsitul validarii
results = []
for inp in inputs:
    state = startstate
    for sym in inp:
        state = transitions[(state, sym)]
    if state in accept_states:
        results.append("Accepted")
    else:
        results.append("Rejected")

#Afisare
with open("dfa.out", "w") as fout:
    if(string_ok==1):
        fout.write(f"States: {sorted(states)}\n")
        fout.write(f"Alphabet: {sorted(alphabet)}\n")
        fout.write(f"Initial State: q{startstate}\n")
        fout.write(f"Accepting State(s): {sorted(accept_states)}\n\n")
        for idx, inp in enumerate(inputs):
            fout.write(f"Input {idx+1}: {''.join(str(c) for c in inp)}\n")
            fout.write("Result: " + results[idx] + "\n\n")


#%%
#minigame hard-coded
fin = open("asdf3.in", "r")
okk=0
a = []
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    
    if line.startswith("rooms:"):
        states = set(map(int, line.split(":")[1].strip().split()))
    elif line.startswith("alphabet:"):
        alphabet = set(map(int, line.split(":")[1].strip().split()))
    elif line.startswith("start_state:"):
        startstate = int(line.split(":")[1].strip())
    elif line.startswith("accept_states:"):
        accept_states = set(map(int, line.split(":")[1].strip().split()))
    else:
        if not all(int(c) in alphabet for c in line):  
            print("Invalid input")
            okk=1
            break
        a.extend(map(int, line)) 
fin.close()
if(okk==0): #ENTRANCE=0 HALLWAY=1 KITCHEN=2 SECRET ROOM=3 LIBRARY=4 EXIT=5
    transition = {#UP=0 DOWN=1 LEFT=2 RIGHT=3
    0: {0:1, 1:0, 2:0, 3:0},
    1: {0:3, 1:0, 2:2, 3:4},
    2: {0:2, 1:2, 2:2, 3:1},
    3: {0:3, 1:1, 2:3,3:3},
    4: {0: 4, 1: 5, 2: 4,3:4},
    5:{0:4,1:5,2:5,3:5}
}
for inp in a:
    state=transition[state][inp]
with open("asdf3.out", "w") as fout:
    fout.write(f"States: {states}\n")
    fout.write(f"Alphabet: {alphabet}\n")
    fout.write(f"Initial State: q{startstate}\n")
    fout.write(f"Final State: q{state}\n")
    fout.write(f"Accepting State(s):{accept_states} \n")
#%%
#minigame cu citire din fisier
fin = open("minigame.in", "r")
okk = 0 #okk e opusul lui ok adica daca e 0 e de bine, verifica daca e valid inputul
a = []

states = set() #states==rooms de mai devereme
#ENTRANCE=0 HALLWAY=1 KITCHEN=2 SECRET ROOM=3 LIBRARY=4 EXIT=5
#UP=0 DOWN=1 LEFT=2 RIGHT=3
alphabet = set()
startstate = None
accept_states = set()
transition = {}

mode = None
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue

    if line.startswith("states:"):
        states = set(map(int, line.split(":", 1)[1].strip().split()))
    elif line.startswith("alphabet:"):
        alphabet = set(map(int, line.split(":", 1)[1].strip().split()))
    elif line.startswith("start_state:"):
        startstate = int(line.split(":", 1)[1].strip())
    elif line.startswith("accept_states:"):
        accept_states = set(map(int, line.split(":", 1)[1].strip().split()))
    elif line.startswith("transitions:"):
        mode = "transitions"
    elif mode == "transitions":
        if "," not in line:
            mode = "inputs"
        else:
            entries = line.split(";")
            for ent in entries:
                ent = ent.strip()
                if not ent:
                    continue
                parts = ent.split(",")
                if len(parts) != 3:
                    print(f"Invalid transition format: {ent!r}")
                    okk = 1
                    break
                state_from, symbol, state_to = map(int, parts)
                if state_from not in transition:
                    transition[state_from] = {}
                transition[state_from][symbol] = state_to
            if okk:
                break
            continue

    if mode == "inputs":
        if "," in line:
            print("Invalid input")
            okk = 1
            break
        if not all(ch.isdigit() and int(ch) in alphabet for ch in line):
            print("Invalid input")
            okk = 1
            break
        symbols = [int(ch) for ch in line]
        a.extend(symbols)

fin.close()

if okk == 0:
    state = startstate
    for inp in a:
        if state in transition and inp in transition[state]:
            state = transition[state][inp]
        else:
            print(f"No transition found for state {state} with input {inp}")
            okk = 1
            break

with open("minigame.out", "w") as fout:
    fout.write(f"States: {states}\n")
    fout.write(f"Alphabet: {alphabet}\n")
    fout.write(f"Initial State: q{startstate}\n")
    fout.write(f"Final State: q{state}\n")
    fout.write(f"Accepting State(s): {accept_states}\n")
    if okk == 0 and state in accept_states:
        fout.write("Accepted\n")
       # print("Accepted")
    else:
        fout.write("Rejected\n")
      #  print("Rejected")




#%%
#NFA direct cu citire din fisier
def process_nfa(input_string, states, alphabet, transitions, start_state, accept_states):
    def epsilon_closure(state_set):
        closure = set(state_set)
        stack = list(state_set)
        while stack:
            state = stack.pop()
            if state in transitions and 'epsilon' in transitions[state]:
                for next_state in transitions[state]['epsilon']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    current_states = epsilon_closure([start_state])
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            if state in transitions and symbol in transitions[state]:
                next_states.update(transitions[state][symbol])
        current_states = epsilon_closure(next_states)

    is_accepted = bool(current_states & accept_states)
    return is_accepted, current_states

#Citire
okk = 0
states = set()
alphabet = set()
transitions = {}
start_state = None
accept_states = set()

with open("nfa_input.in", "r") as fin:
    for line in fin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("states:"):
            states = set(map(int, line.split(":", 1)[1].strip().split()))
        elif line.startswith("alphabet:"):
            alphabet = set(line.split(":", 1)[1].strip().split())
        elif line.startswith("start_state:"):
            start_state = int(line.split(":", 1)[1].strip())
        elif line.startswith("accept_states:"):
            accept_states = set(map(int, line.split(":", 1)[1].strip().split()))
        else:
            if ":" in line and "->" in line:
                state_str, rest = line.split(":", 1)
                s = int(state_str.strip())
                if s not in transitions:
                    transitions[s] = {}
                for piece in rest.split(","):
                    sym_str, nxt_str = piece.split("->")
                    sym = sym_str.strip()
                    nxt = int(nxt_str.strip())
                    transitions[s].setdefault(sym, set()).add(nxt)
            else:
                continue
            
#Validare
for state, transition_dict in transitions.items():
    for input_symbol in transition_dict:
        if input_symbol != 'epsilon' and input_symbol not in alphabet:
            print(f"Invalid input symbol: {input_symbol} in state {state}")
            okk = 1
            break
    if okk:
        break


#Citirea string-ului
input_string = None
if okk == 0:
    with open("nfa_input.in", "r") as fin2:
        for line in fin2:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if (not line.startswith(("states:", "alphabet:", "start_state:", "accept_states:"))
                and "->" not in line):
                input_string = line
                break
    if input_string is None:
        okk = 1


#Afisare
with open("nfa_output.out", "w") as fout:
    fout.write(f"States: {sorted(states)}\n")
    fout.write(f"Alphabet: {sorted(alphabet)}\n")
    fout.write(f"Start State: {start_state}\n")
    fout.write(f"Accept States: {sorted(accept_states)}\n\n")

    if okk == 0:
        fout.write(f"Input String: {input_string}\n")
        accepted, final_states = process_nfa(
            input_string, states, alphabet, transitions, start_state, accept_states
        )
        fout.write(f"Final states: {sorted(final_states)}\n")
        if accepted:
            fout.write("Accepted\n")
        else:
            fout.write("Rejected\n")
    else:
        fout.write("Result: Error in NFA definition or input parsing\n")


#%%
#PDA direct cu input din fisier

def process_pda(input_string, states, alphabet, transitions, start_state, accept_states):
    state = start_state
    stack = []
    idx = 0  #index

    def apply_transition(t):
        nonlocal state
        (_, inp_sym, pop_sym, next_q, push_str) = t
        #pop:
        if pop_sym != "epsilon":
            stack.pop()
        #push:
        if push_str != "epsilon":
            for c in reversed(push_str):
                stack.append(c)
        state = next_q

    while True:
        applied = False

        #incerc sa consum un simbol din input
        if idx < len(input_string):
            sym = input_string[idx]
            for t in transitions:
                q, inp_sym, pop_sym, next_q, push_str = t
                if q == state and inp_sym == sym:
                    if pop_sym == "epsilon" or (stack and stack[-1] == pop_sym):
                        apply_transition(t)
                        idx += 1
                        applied = True
                        break
            if applied:
                continue

        # incerc epsilon
        for t in transitions:
            q, inp_sym, pop_sym, next_q, push_str = t
            if q == state and inp_sym == "epsilon":
                if pop_sym == "epsilon" or (stack and stack[-1] == pop_sym):
                    apply_transition(t)
                    applied = True
                    break
        if not applied:
            break

    is_accepted = (state in accept_states and idx == len(input_string))
    return is_accepted, state, stack, idx



#citire
okk = 0
states = set()
alphabet = set()
transitions = []
start_state = None
accept_states = set()
idx=-1

with open("pda_input.in", "r") as fin:
    for line in fin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("states:"):
            states = set(map(int, line.split(":", 1)[1].split()))
        elif line.startswith("alphabet:"):
            alphabet = set(line.split(":", 1)[1].split())
        elif line.startswith("start_state:"):
            start_state = int(line.split(":", 1)[1])
        elif line.startswith("accept_states:"):
            accept_states = set(map(int, line.split(":", 1)[1].split()))
        else:
            # linie de tranzitie: 1: 0,epsilon -> 0,1
            if ":" in line and "->" in line:
                state_str, rest = line.split(":", 1)
                q = int(state_str.strip())
                left, right = rest.split("->", 1)
                inp_sym, pop_sym = map(str.strip, left.split(",", 1))
                push_sym, nxt_str = map(str.strip, right.split(",", 1))
                p = int(nxt_str)
                transitions.append((q, inp_sym, pop_sym, p, push_sym))
            else:
                continue

#Validare 1
for (q, inp_sym, pop_sym, p, push_sym) in transitions:
    if inp_sym != "epsilon" and inp_sym not in alphabet:
        print(f"Invalid input symbol: {inp_sym} in {q}")
        okk = 1
        break

#Citire
input_string = None
if okk == 0:
    with open("pda_input.in", "r") as fin2:
        for line in fin2:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if (not line.startswith(("states:", "alphabet:", "start_state:", "accept_states:"))
                and ":" not in line and "->" not in line):
                input_string = line
                break
    if input_string is None:
        okk = 1
#Validare 2   
if okk == 0:
    for c in input_string:
        if c not in alphabet:
            print(f"Invalid input symbol in string: '{c}'")
            okk = 1
            break
#Afisare
with open("pda_output.out", "w", encoding="utf-8") as fout:
    fout.write(f"States: {sorted(states)}\n")
    fout.write(f"Alphabet: {sorted(alphabet)}\n")
    fout.write(f"Start State: {start_state}\n")
    fout.write(f"Accept States: {sorted(accept_states)}\n\n")

    if okk == 0:
        fout.write(f"Input String: {input_string}\n")
        accepted, final_state, final_stack, idx = process_pda(
            input_string, states, alphabet, transitions, start_state, accept_states
        )
        fout.write(f"Final State: {final_state}\n")
        fout.write(f"Final Stack: {final_stack}\n")
        fout.write("Result: " + ("Accepted\n" if accepted else "Rejected\n"))
        if not accepted:
            if idx != len(input_string):
                reason = f"Unconsumed input: {len(input_string) - idx} input(s) left"
            elif final_state not in accept_states:
                reason = f"Final state ({final_state}) is not in accept_states "
            else:
                reason = f"Stack is not empty: {final_stack}"
            fout.write(f"Reason: {reason}\n")
    else:
        fout.write("Result: Error in PDA definition or input parsing\n")




#%%
#masina turing hard-coded
transitions = {
    ('q0', '□'): ('1', 'R', 'q1'),
    ('q1', '□'): ('□', 'R', 'q0'),
}
blank      = '□'
start_state= 'q0'
accept_states = {'q_accept'}

def turing(tape_str):
    tape = list(tape_str) + [blank]*500
    #print(tape)
    head  = 0
    state = start_state
    steps = 0
    while (steps<=100):
        symbol = tape[head]
        key = (state, symbol)
        if key not in transitions:
            state = 'q_reject'
            break

        write, move, nxt = transitions[key]
        tape[head] = write

        if move == 'R':
            head += 1
        elif move == 'L':
            head -= 1

        state = nxt
        steps += 1
    result = ''.join(tape).rstrip(blank)
    return state, result, steps

initial = ''
st, out, steps = turing(initial)
print(st, out, steps)


        
        
    
#%%
#masina turing cu input din fisier

# Citire 
fin = open("turing.in", "r", encoding="utf-8")#e nevoie de acel encoding pentru caracterul pentru blank

states         = set()
alphabet       = set()
blank          = None
start_state    = None
accept_states  = set()
reject_states  = set()
transitions    = {}
in_transitions = False
initial        = None
max_steps      = None
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if in_transitions:
        if "->" not in line:
            continue
        parts = line.split()
        if len(parts) < 6:
            continue
        #format: src sym -> write move dst
        src, sym = parts[0], parts[1]
        write, move, dst = parts[3], parts[4], parts[5]
        transitions[(src, sym)] = (write, move, dst)
    else:
        if line.startswith("states:"):
            states = set(line.split(":", 1)[1].split())
        elif line.startswith("alphabet:"):
            alphabet = set(line.split(":", 1)[1].split())
        elif line.startswith("blank:"):
            blank = line.split(":", 1)[1].strip()
        elif line.startswith("start_state:"):
            start_state = line.split(":", 1)[1].strip()
        elif line.startswith("accept_states:"):
            accept_states = set(line.split(":", 1)[1].split())
        elif line.startswith("reject_states:"):
            reject_states = set(line.split(":", 1)[1].split())
        elif line.startswith("max_steps:"):
            max_steps = int(line.split(":",1)[1].strip())
        elif line.startswith("transitions:"):
            in_transitions = True


fin.seek(0)
for line in fin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if ":" not in line and "->" not in line:
        initial = line
        break
fin.close()

# Validare input tape
for c in initial:
    if c not in alphabet:
        raise ValueError(f"Invalid symbol: '{c}'")
        
        
#default max_steps 
if max_steps is None:
    max_steps = 10000



#simulare
tape = list(initial) + [blank] * 50000
head  = 0
state = start_state
steps = 0

while state not in accept_states and state not in reject_states and steps < max_steps:
    sym = tape[head]
    key = (state, sym)
    if key not in transitions:
        state = next(iter(reject_states))
        break

    write, move, nxt = transitions[key]
    tape[head] = write

    if move == 'R':
        head += 1
    elif move == 'L':
        head -= 1

    state = nxt
    steps += 1

#accepted daca max_steps e atins
if steps >= max_steps and state not in accept_states and state not in reject_states:
    state = next(iter(accept_states))
    accepted = True
else:
    accepted = state in accept_states



#Afisare
tape_str = "".join(tape).rstrip(blank)

with open("turing.out", "w", encoding="utf-8") as fout:
    fout.write(f"States: {sorted(states)}\n")
    fout.write(f"Alphabet: {sorted(alphabet)}\n")
    fout.write(f"Blank: {blank}\n")
    fout.write(f"Start State: {start_state}\n")
    fout.write(f"Accept States: {sorted(accept_states)}\n")
    fout.write(f"Reject States: {sorted(reject_states)}\n")
    fout.write(f"Max Steps: {max_steps}\n\n")

    fout.write(f"Input Tape: {initial}\n")
    fout.write(f"Final State: {state}\n")
    fout.write(f"Final Tape: {tape_str}\n")
    fout.write(f"Steps: {steps}\n")
    fout.write(f"Result: {'Accepted' if accepted else 'Rejected'}\n")

#%%
#Am facut si un mini program pentru collatz pentru ca eram curios de numarul maxim de pasi si numarul maxim atins intr-o secventa 
#Doar ca e in C++, pentru eficienta
"""
#include <iostream>
#include<chrono>
using namespace std;
int maxproven=1;
long long maxreached=0;
int collatz(long long n) {
    long long copien=n;
    int steps=0;
    static int maxsteps;
    while (n!=1) {
        if (n%2==0)
            n=n/2;
        else
            n=n*3+1;
        if (n>maxreached)
            maxreached=n;
        steps++;
    }
    if (steps>maxsteps)
        maxsteps=steps;
    maxproven++;
    cout<<copien<<" "<<steps<<endl;
    return maxsteps;

}
int main() {

    int n=2000,maxsteps=0;
    //cin>>n;
    auto t0 = chrono::high_resolution_clock::now();

for (int i=1;i<=n;i++) {
    maxsteps=collatz(i);
}
    cout<<maxreached<<endl;
    cout<<maxsteps;
    auto t1 = chrono::high_resolution_clock::now();
    auto elapsed = chrono::duration<double, milli>(t1 - t0);
    cout<<endl;
    cout << "wall-clock time: "
              << elapsed.count() << " ms\n";
    return 0;
}
"""


        


















