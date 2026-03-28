requirements.txt lists the required python modules 

Backend
admin.py script will be the main user command interface 
    when running admin.py, the user can type part of the command for command suggestion/autocomplete. See cmd_list for the full list of commands
        each command is a tuple with (#number of parameters, function)
        when param count is met (if 0, automatically run function), the function is ran with the list l as the input where l is the list of parameters

backend.py is the server running on the local machine to interact with the Roblox game. The “fetch” field will be opened to send commands to the Roblox game. The “admin” field will be opened to receive commands from admin.py. 

Roblox end
The ServerScriptService.API.commander will send HTTP fetch to the backend.py server to receive a list of commands. Each command is a list starting with the command name, then parameters. The function do_command defines behavior based on the command list.

Startup
Start admin.py and backend.py as a typical Python script or in your venv.
Use different terminals. 
Use the terminal to run: cloudflared tunnel --url http://localhost:8000 
Copy the tunnel URL
Paste the URL in the Roblox game module script ServerScriptService.API.Constants

This setup is valid for local testing purposes; the game must be published for the backend to be connected live.

Expansion
Future use development should use permanent URLs which would require registering a domain you own with cloudflare. This eliminates the hassel of manually updating the tunnel URL each testing cycle and decouples backend and roblox-end development.
