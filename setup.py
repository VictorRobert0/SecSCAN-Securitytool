from cx_Freeze import setup, Executable

executables = [Executable("SecSCAN.py", base="Win32GUI", target_name="SecSCAN.exe", icon="favicon.ico")]

# Incluindo tkinter explicitamente
build_exe_options = {
    "packages": ["tkinter"],
    "includes": ["tkinter"],
    "excludes": ["tkinter.test"]  # Caso queira evitar incluir testes do tkinter
}

setup(
    name="SecSCAN",
    version="1.0",
    description="SecSCAN Application",
    options={"build_exe": build_exe_options},
    executables=executables
)
