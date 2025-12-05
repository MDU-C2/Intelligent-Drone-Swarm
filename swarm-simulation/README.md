# Follow the steps bellow to get started

## gym-pybullet-drones

This is a minimalist refactoring of the original `gym-pybullet-drones` repository, designed for compatibility with [`gymnasium`](https://github.com/Farama-Foundation/Gymnasium), [`stable-baselines3` 2.0](https://github.com/DLR-RM/stable-baselines3/pull/1327), and SITL [`betaflight`](https://github.com/betaflight/betaflight)/[`crazyflie-firmware`](https://github.com/bitcraze/crazyflie-firmware/).

## Intellignet Replanning Drone Swarm
An intelligent replanning drone swarm was created for this project. To run and test it, follow the instructions below.

## Installation

```sh
git clone https://github.com/utiasDSL/gym-pybullet-drones.git
cd gym-pybullet-drones/

conda create -n drones python=3.10
conda activate drones # 'drones' is the name you will call your envirnoment, but you can change it to whatever you want. 

pip3 install --upgrade pip
pip3 install -e . # if needed, `sudo apt install build-essential` to install `gcc` and build `pybullet`
pip install PyQt5
```

## Use
```sh
git clone https://github.com/MDU-C2/Intelligent-Drone-Swarm.git
cd Intelligent-Drone-Swarm/simulation/code/
# Before running the simulation, you will have to change the path to the subject.
# 1. Open the main.py file.
# 2. line 124, change the path there to the path of where you stored the .urdf file (you can find the file in the folder Object(.urdf files).

# Once that is done, you can now run the gui.py file to run the simulation.
python gui.py
```


