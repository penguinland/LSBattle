# Light Speed Battle

[日本語版](./README-ja.md)

This is a FPS game where you can experience special relativity.

![SS1](./play_screenshot_1.png)
![SS2](./play_screenshot_2.png)

## Usage

1. I don't have a Mac, but the original instructions involved installing extra things on it:
    ```
    brew install glfw
    brew install sdl2
    ```
2. Set up a new virtual environment
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Compile the Cython code
    ```
    python cython_setup.py
    ```
4. Let's play!
    ```
    ./LSBattle3D.py
    ```
