import cx_Freeze
from cx_Freeze import *

setup(
    name= "game",
    options = {'build_exe' :{'packages': ['pygame']}},
    executables=[
        Executable(
            "game.py", base = "Win32GUI"

            )

        ]
    
    )
