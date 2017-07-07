Do a `pip install win10toast` to install dependencies [win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications)

- Make sure you have [python launcher](https://docs.python.org/3/using/windows.html#launcher) installed and default choice for running python files

- Add a shortcut to this script on windows startup folder to make it run on startup
Find startup folder by running `shell:startup` in run [Win + R]
It is usually found in `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

If it shows in `Task Manager` -> `Startup` Tab, It will auto start on boot

- How to stop it
Look for 2 python processes, End them using Task Manager