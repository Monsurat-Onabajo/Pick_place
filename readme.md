### **📌 README: Pick-and-Place with Multi-Camera Capture in Isaac Sim**  

## **📖 Overview**  
This project simulates a **pick-and-place task** using **Isaac Sim**. It captures images from two different cameras in the simulation and saves them as `.npy` files in separate directories. The simulation logs **robot joint positions, gripper state, cube positions, target positions**, and **actions taken**.

---

## **🛠️ Features**
✅ **Pick-and-place task execution**  
✅ **Two camera setup for capturing different views**  
✅ **Saves images separately for each camera**  
✅ **Logs simulation data in `.csv` and `.npy` formats**  
✅ **Runs in real-time using Isaac Sim**

---

## **📂 Folder Structure**
```
📦 project_root/
 ├── 📜 pick_place_with_logging.py    # Main script for pick and place task + camera capture
 ├──    pick_and_place.py  # Main script for pick and place with no logging
 ├── 📂 images/  
 │   ├── 📂 camera1/  # Images from side camera
 │   │   ├── frame_10.npy
 │   │   ├── frame_20.npy
 │   ├── 📂 camera2/  # Images from top camera
 │       ├── frame_10.npy
 │       ├── frame_20.npy
 ├── 📜 simulation_logs.npy   # Logs in NumPy format
 ├── 📜 simulation_logs.csv   # Logs in CSV format
 ├── 📜 README.md   # This documentation
```

---

## **🚀 How to Run**
### **1️⃣ Set Up Isaac Sim**
Ensure you have **Isaac Sim installed** and **Python environment configured**, see [here](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/index.html) for installation .

### **2️⃣ Run the Pick-and-Place Script**
Execute the following command:
```bash
python pick_place_with_logging.py
```
This will:
- Start **Isaac Sim**.
- Initialize the **pick-and-place task**.
- Capture images from **two cameras** (`Camera_side` and `Camera_side_02`) both cameras are opposite each other, like front and back.
- Save images in the `images/` directory.
- Log simulation data in `.csv` and `.npy` files.

---

## **📸 Viewing Captured Images**
Since images are saved as **NumPy arrays (`.npy`)**, use the following Python script to visualize them:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load an image from Camera 1
image = np.load("images/camera1/frame_10.npy")

# Display the image
plt.imshow(image)
plt.axis("off")
plt.title("Camera 1 - Frame 10")
plt.show()
```

---

## **📊 Understanding the Logs**
The **simulation logs** contain:
| Column | Description |
|---------|------------|
| `time` | Simulation step counter |
| `joint_positions` | Robot joint positions at each step |
| `gripper_state` | State of the gripper (open/close) |
| `cube_position` | Position of the cube being picked/placed |
| `target_position` | Target position for the cube |
| `actions` | Robot control actions |
| `camera1_image_paths` | Path to images from **Camera 1** |
| `camera2_image_paths` | Path to images from **Camera 2** |

To analyze logs:
```python
import pandas as pd

df = pd.read_csv("simulation_logs.csv")
print(df.head())  # View first few rows
```

---

### **📌  Configuring Pick and Place Positions in Isaac Sim**

## **🔹 Overview**
This guide explains how to **modify the pick position** (where the robot picks the object from) and **target position** (where the object is placed) in the **pick-and-place task**.

---

## **🛠 Changing the Pick Position**
The **initial pick position** of the object is set inside the `PickPlace` class in:
```
tasks/pick_place.py
```
- Locate the **`PickPlace`** class.
- Find the **`cube_initial_position`** parameter.
- Modify it to set a new **starting location** for the object.

### **Example (tasks/pick_place.py)**
```python
self.cube_initial_position = np.array([0.6, 0.3, 0.85])  # Z should be higher than base either floor or table height
```

---

## **🎯 Changing the Target Position (Where the Object is Placed)**
The **target placement position** is controlled by the **`target_position`** variable in:
```
pick_and_place.py
pick_up_with_log.py
```
- Update `target_position` to set a new **destination** where the robot places the object.

### **Example (pick_and_place.py or pick_up_with_log.py)**
```python
target_position = np.array([0.8, 0.7, 1.0])  # Z should be higher than base either floor or table height
```