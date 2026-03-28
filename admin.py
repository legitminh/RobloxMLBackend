# admin.py
import requests
from pathlib import Path
import re
import subprocess

BACKEND_PATH = "http://localhost:8000/admin"
PATH_HOME = Path(__file__).resolve()

def input_string(): return input().rstrip()
def input_interable(sep = " "): return input_string().split(sep)

def str_is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def commander():
    previous_exec = None
    state = None
    is_running = True
    params = []
    

    def output(*l):
        print(">>",*l)
    
    def repeat(l):
        output("repeating...", *previous_exec)
        exec(previous_exec[0], *previous_exec[1])
    
    exec_no_record = (repeat, ) #commands that aren't recorded when executed

    def end(l):
        nonlocal is_running
        output("Terminated")
        is_running = False

    def exec(f, *params):
        output(f, *params)
        nonlocal previous_exec
        if f not in exec_no_record:
            previous_exec = (f, params)
        f(*params)
    
    def get_path_from_token(token):
        return Path(re.findall(r"[a-zA-Z/0-9_\-\.]+", token)[0]) #select all characters possible in a file path description

    def run_python(path_main):
        # path_in = Path.joinpath(path, PATH_REL_IN)
        # with open(path_in, "r") as f:
        print("testing", path_main)
        result = subprocess.run(
            ["python3", path_main],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    
    def start_backend(l):
        run_python(Path.joinpath(PATH_HOME, "backend.py"))
    
    def send_command(*raw):
        requests.post(
            BACKEND_PATH,
            json={
                "usr": "admin",
                "cmd" : raw
            }
        )


    def update(l):send_command("update")
    def reset(l):send_command("reset")
    def reset_save(l):send_command("reset_save")
    def reset_save(l):send_command("reset_save", l[0])
    

    cmd_list = {
        "repeat" : (0, repeat),
        "end" : (0, end),
        "update" : (0, update),
        "reset" : (0, reset),
        "reset_save" : (0, reset_save),
        "reset_save_1" : (1, reset_save),
    }
    def is_terminate(token): return isinstance(token, tuple)

    def is_valid(token): return len(token.strip()) != 0
   
    def reset_state():
        nonlocal state, cmd_list, params
        state = cmd_list
        params = []

    def input_token(token):
        nonlocal state, params

        def confusion(previous_state, candidates):
            def resolution(l):
                if str_is_int(l[0]):
                    return previous_state[candidates[int(l[0])]]
                raise TypeError
                # return previous_state[l[0]]
            return resolution
        
        #read sequence
        if is_terminate(state):
            #if is in functional parameter state
            if state[0] >=0:
                state = (state[0]-1, state[1])
                params.append(token)
        else:
            #if in function selection state
            if token in state:
                state = state[token]
            else:
                #recommend options
                candidates = []
                
                for i, key in enumerate(state.keys()):
                    if key.startswith(token):
                        candidates.append(key)
                lc = len(candidates)
                if lc == 0:
                    output("no valid command, options:", state.keys())
                elif lc == 1:
                    output("autocompleting option:",candidates[0])
                    state = state[candidates[0]]
                else:
                    for i, v in enumerate(candidates):
                        output(i,v)
                    output("options available, choose with int: ")
                    state = (1, confusion(state, candidates))
                
        
        #function execution sequence
        if is_terminate(state):
            if state[0] == 0:
                exec(state[1],params)
                reset_state()
        

    def main():
        reset_state()
        while is_running:
            for token in input_interable():
                if is_valid(token):
                    input_token(token)
    return main
commander()()



# while True:
#     raw = input(">> ").rstrip()
#     if raw == "exit":
#         break
#     raw = raw.split(" ")
#     result = requests.post(
#         BACKEND_PATH,
#         json={
#             "usr": "admin",
#             "cmd" : raw
#         }
#     )
#     # print(result.text)
