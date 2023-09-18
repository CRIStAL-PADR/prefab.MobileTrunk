# prefab.MobileTrunk
[![SoftRobots](https://img.shields.io/badge/info-on_website-purple.svg)](https://project.inria.fr/softrobot/) 
[![SOFA](https://img.shields.io/badge/SOFA-on_github-blue.svg)](https://github.com/sofa-framework)
[![Ronotnik Automation](https://img.shields.io/badge/RonotnikAutomation-on_github-green.svg)](https://github.com/RobotnikAutomation)
[![Ros](https://img.shields.io/badge/Ros-on_readthedocs-chocolate.svg)](https://docs.ros.org/en/foxy/index.html)

The *MobileTrunk's* robot prefab for SoftRobots. 

Index
-----

  * [Requirement](#requirement)
  * [Compile sofa](#compile-sofa)
  * [Install Required dependencies](#install-required-dependencies)
  * [Download and set up working space](#download-and-set-up-working-space)
  * [Install *ROS* and set up working space](#install-ros-and-set-up-working-space)
  * [Launch test](#launch-test)
  * [Connecting the digital twin to the physical robot](#connecting-the-digital-twin-to-the-physical-robot)
  * [License](#license)

Requirement
-----------
This prefab was developed as part of the SOMOROB project. The goal is to integrate a
deformable robotic trunk (softrobot) on a 4-wheeled mobile robot base equipped with 
a LIDAR and to develop its digital twin equivalent. The deformable trunk is a project
[Echelon 3](https://www.inria.fr/en/interface-inria-centre-university-lille-demonstration-space)
developed by the Defrost team at INRIA. The mobile base is developed by the company
[Robotnik automation](https://robotnik.eu/)

Software version
---------------
The softwares are use with the following version :
- Python 3

The following Sofa plugins are required. version V21.12 is needed.

- SofaPython3
- BeamAdapter
- SoftRobots

The following python module are required :

- time
- threading
- math
- numpy
- dataclasses
- sys

Compile *SOFA*
--------------

Install Required dependencies
------------------------------------
For that follow these [instructions](https://www.sofa-framework.org/download/) (We will install the linux one)
<!--(The best way to add plugin to SOFA is explained [here](https://www.sofa-framework.org/community/doc/getting-started/video-tutorials/how-to-compile-a-plugin/)) 

- STLIB

    ```console
    foo@bar:~$  git clone https://github.com/SofaDefrost/STLIB.git
    ```

- SoftRobots

    ```console
    foo@bar:~$  git clone https://github.com/SofaDefrost/SoftRobots.git
    ```

- SofaPython3

    ```console
    foo@bar:~$  git clone https://github.com/sofa-framework/SofaPython3
    ```
    
- BeamAdapter

    ```console
    foo@bar:~$  git clone https://github.com/SofaDefrost/BeamAdapter
    ``` 
-->

Download and set up working space
---------------------------------

### Download the mobile trunk's prefab

Now that you have install SOFA binairy we can clone
prefab.MobileTrunk repository.

- Create a directory where you will put it
- Move into it and clone the last working version

    ```console
    foo@bar:~$  git clone https://github.com/CRIStAL-PADR/prefab.MobileTrunk
    ```

### Set up working space
Open your bashrc and add the following lines in order to setup your working space
- Add to the PATH the path to the folder where the binary files are located

    ```console
        export PATH="/path to binary folder/bin:$PATH"
    ```

- Tell to  *SOFA_ROOT* the path where to find the path to the buid folder of SOFA

    ```console
        export SOFA_ROOT=/path to binary folder
    ```

- Make an alias in order to be able to launch Sofa easily by doing a runSofa

    ```console
        runSofa="/path to binary folder/bin/runSofa"
    ```

- Add to the PYTHONPATH the path to *SofaPython3*, *STLIB* , *SofaROS* , *Python3*
    ```console
        export PYTHONPATH=$PYTHONPATH:"/path to binary folder/plugin/SofaPython3/lib/python3/site-packages":"/path to binary folder/plugin/STLIB/lib/python3/site-packages":"/usr/local/lib/python3.8/dist-packages":"/path to binary folder/plugin/SoftRobots/share/sofa/examples/SoftRobots/sofaros"
    ```

- Now you can source your .bashrc file with the command
    ```console
        source ~/.bashrc
    ```

- And run the command:
    ```console
        runSofa
    ```
If everything went well, you should see the Sofa GUI appear.

Now, click on the *Edit* button and go to *Plugin Manager*. Then click on *Add*. A window will appear. You need to navigate to the directory where the binary files are located. Go to the *plugins* directory, then to *ArticulatedSystemPlugin*, and then to *lib*. There, you will find a file named *libArticulatedSystemPlugin.so*. Click on *Open*.

Repeat the same procedure to add the *.so* files for the *SofaPython3* plugin.

Install *ROS* and set up working space
--------------------------------------

The digital twin has a *ros2* interface while the mobile platform (summit_xl) has a *ros1* interface.
It is possible to be able to link the digital twin to the real robot using rosbridge.

### Install ros2 and ros1

Install the [noetic](http://wiki.ros.org/noetic/Installation/Ubuntu) version for ros1 in order to be able to use rosbridge

Install the [foxy](https://docs.ros.org/en/foxy/Installation.html) version for ros2.

If you are new to ros you can follow the [tutorials](https://docs.ros.org/en/foxy/Tutorials.html) before continuing

Install rosbridge
    
```console
    foo@bar:~$  sudo apt-get install -y ros-foxy-ros1-bridge
```

### Set up working space

Open your bashrc and add the following lines in order to setup your working space for ros

- Create an alias for noetic(ros1) and foxy(ros2) in order to be able to source your terminal more easily

    ```console
        alias foxy="source /opt/ros/foxy/setup.bash"
        alias noetic="source /opt/ros/noetic/setup.bash"
    ```

- Open sofaros.py file located in plugings/SoftRobots/share/sofa/examples/SoftRobots folder.
Then replace in the callback method of RosReceiver class the line
    ```console
        self.data = data.data by self.data = data
    ``` 
Launch test
-----------
To confirm all the previous steps and verify that the prefab is working properly you can :

#### Test using sofa controller

-  Launch the scene.py SOFA scene situated in prefab.MobileTrunk/mobile_trunk_sim by doing:
 ```console
    foo@bar:~$  runSofa scene.py --argv KeyboardController
```
- If everything went well you should see the GUI Sofa with the digital twin of

    ![somorob](/docs/somorob.png)


- Then with your keyboard send velocity and orientation command to the Sofa scene in order to see the robot
move.
 

#### Test using ros api

- source your terminal using : 
    ```console
    foo@bar:~$  foxy
    ```

- Go to the directory where the prefab.MobleTrunk/mobile_trunk_sim folder is located and run 
 the following command:

    ```console
    foo@bar:~$  runSofa scene.py --argv  RobotToSim
    ```
- Open a new terminal then source it as before then execute the commands to the following command:

    ```console
        foo@bar:~$  colcon build && . install/setup.bash && foxy
    ```

-  You can now launch the keyboard controller to interact with the robot in the simulation

    ```console
        foo@bar:~$  ros2 run summitxl summitxl_teleop_key

    ```

- If everything went well you should see this appear in the terminal
    
    ![ros_teleop_key](/docs/ros_teleopkey.png/)


## Echelon

### Controller

#### Forward kinematics

- ctl + i : To select the cable i (from 1 to 9) you want to actuate
- ctl + plus : if you want to pull the cable
- ctl + minus : if you want to release the cable

### Links

You can found the Echelon3 folder with the reference simulation there : https://gitlab.inria.fr/defrost/Robots/Echelon3.git with the branch Centrale_Dynamixel. The reference simulation is in the folder **simulation**.

There is also the ros2 package : https://gitlab.inria.fr/defrost/Robots/sim_echelon3_ros.git with the branch ros2.

You can find all the details and the explanation in this two repository.

Connecting the digital twin to the physical robot
-------------------------------------------------



### Electrical Components Required:

Following components will be required to run the Dynamixel motors. Please find attached links as well for better understanding-

* U2D2 : 1 piece [Link to Product](http://www.robotis.fr/index.php?id_product=283&controller=product)

* U2D2 PHB Set: 1 piece [Link to Product](http://www.robotis.fr/index.php?id_product=370&controller=product)

* Dynamixel Motors Model XM430-W350-T : 9 pieces [Link to Product](http://www.robotis.fr/index.php?id_product=328&controller=product)

* SMPS Adapter O/P 12V 5A: 1 piece [Link to Product](https://www.amazon.fr/Transformateur-Alimentation-Adaptateur-pour-Noir/dp/B06XT7NZQJ/ref=asc_df_B06XT7NZQJ/?tag=googshopfr-21&linkCode=df0&hvadid=454911510608&hvpos=&hvnetw=g&hvrand=12519235580864950353&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9055767&hvtargid=pla-684858899945&psc=1)

* USB To B-Type Cable : 1 piece [Link to Product](https://www.amazon.fr/DragonTrading-C%C3%A2ble-chargement-pour-Playstation/dp/B00XNG1OFI/ref=asc_df_B00XNG1OFI/?tag=googshopfr-21&linkCode=df0&hvadid=411501339018&hvpos=&hvnetw=g&hvrand=18051668094716050382&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9055767&hvtargid=pla-626821137567&psc=1&tag=&ref=&adgrpid=84799750530&hvpone=&hvptwo=&hvadid=411501339018&hvpos=&hvnetw=g&hvrand=18051668094716050382&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9055767&hvtargid=pla-626821137567)

* 3 pin TTL Connector wires : 10 pieces
    This comes with the Dynamixel motors. 


### Softwares/Platforms Required

* Dynamixel Wizard 2.0 for setting IDs of each Dynamixel motor

* ROS2 to give commands via keyboard

* SOFA to see simulation of the trunk


### Connections of Motors with U2D2 Module

* Attach the U2D2 on the U2D2 PHB Set.

* Connect the U2D2 with U2D2 PHB Set using TTL connection wires.

* Connect the Dynamixel motor with the U2D2 PHB Set using TTL connector wire. 

* Connect the other Dynamixel motors with each other in a series using TTL connector wires. (this step should be done after 
setting up IDs for each motor which is explained later)

* Connect the U2D2 to the USB hub of the computer via USB-B type Convertor Cable. 

* Connect the adapter to the U2D2 PHB Set to give power to it.


Please find the following links for better understanding to make connections-

* [Robotis Website Documentation](http://www.robotis.fr/index.php?id_product=370&controller=product)

* [Youtube Video 1](https://www.youtube.com/watch?v=FIj_NULYOKQ)

* [Youtube Video 2](https://www.youtube.com/watch?v=E8XPqDjof4U)



### Setting IDs of motors using Dynamixel Wizard software


* Go to the following page link and download the software for your OS. You can follow the same link for understanding of setting up 
 of IDs of each Dynamixel motors-
[Robotis eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)


* After successful installation, open the software Dynamixel Wizard 2.0.

* Now we will provide individual IDs to each motor so we connect each Dynamixel separately to the U2D2 PHB Set.
In order to avoid ID collision, it is important to connect Dynamixel motors one by one to the U2D2 PHB Set.
If you connect multiple motors together, it is possible that all IDs are not visible on software if they have same IDs.

* Connect any one Dynamixel motor to U2D2 PHB Set.
 Once this is done, click on the 'Options' on the software page.

    * For protocol, choose 'Protocol 2.0'  
    * For port, choose 'Select All'
    * For baudrate, choose '57600 bps'
    * For ID range to scan, choose Start '0' and End as '252'


* Click 'OK'

* Now click on 'Scan' option on the display page of the software.
* Wait for sometime as it will scan the connected Dynamixel motor.
* You will see the motor ID being shown on the display page and then it will open the parameters page of that motor.
* In order to change the ID of the motor, you can look for 'ID' option in the 'Item' List and accordingly set ID. Click 'Save'.
* You can verify the motion of your motor by choosing 'Position' option in the right panel and then enabling 'Torque' option. 
* You can then select a point on the black disc to make the motor move to that position value.
* You should be able to see your actual physical motor move to that position.

* Repeat the process with other motors individually to set their IDs.
* Once each motor is provided a unique ID ranging from 1 to 9, you can connect all Dynamixel motors with each other in series using 
 TTL connector wires with one of the motors connected to the U2D2 PHB Set.

* Again use the 'Scan' option on the display page of the software and this time, you should be able to see all the 9 Dynamixel motors
  being displayed on the screen with different Motor IDs.

* Close the software as we have successfully set up separate IDs for each motor.


# Steps to run Physical Motors through ROS2 on Linux Terminal:


### Run the program to open USB port to connect to Dynamixel motors

    * Open Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel
    * Source the workspace- source install/setup.bash
    * Open a file- ros2 run dynamixel_sdk_examples read_write_node

You should see a message somewhat like this-

    [INFO] [1693911266.107186716] [read_write_node]: Succeeded to open the port.
    [INFO] [1693911266.107633590] [read_write_node]: Succeeded to set the baudrate.
    [INFO] [1693911266.107658897] [read_write_node]: Succeeded to set Position Control Mode.
    [INFO] [1693911266.107671859] [read_write_node]: Succeeded to enable torque.
    [INFO] [1693911266.124372397] [read_write_node]: Run read write node
    [INFO] [1693911334.166192254] [read_write_node]: Set [ID: 1] [Goal Position: 0]
    [INFO] [1693911334.202227369] [read_write_node]: [TxRxResult] There is no status packet!

In case you see an error like this-

    [PortHandlerLinux::SetupPort] Error opening serial port!
    [ERROR] [1693925235.287672274] [read_write_node]: Failed to open the port!

then check your USB Connection with the U2D2 module or try to change the USB port and then retry.


### Run the program to create a link between publisher and subscriber

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open a file- ros2 run dynamixel_sdk_examples dynamixel_pub_sub


### Run the program to give commands through keyboard to set ID and position of motors

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open a file- ros2 run keyboard_trunk_controller keyboard_controller 
    
You should be able to see a message like this-


    Enter a cable ID (1-9), or press ESC to quit:


It asks for selection of Motor ID so you can type any number in the range of 1 to 9.
After you select the motor ID, that particular motor id will move in clockwise direction when you press '+' button and it will move in anti-clockwise direction when you press '-' button. So now you will get the following message incase you selected motor ID 1 before-


    Selected Cable 1
    Current Cable: 1
    Press + to increase position, - to decrease, or press any digit to change cable

You will get the following message in case you pressed '+' sign-

    Position increased by 100. New position: 100


You can keep pressing '+' or '-' sign for as long as you want to give position values. The minimum and maximum position values of the motors are 0 and 4100 respectively.
You can change the motor id by pressing any other number and then select '+' or '-' to give position values.

You can also see the received messages on previous terminal of dynamixel_pub_sub showing ID and position.
You will see a message somewhat like this-


    [INFO] [1693911338.379470090] [subscriber_node]: Received: ID = 1, Position = 200




# Steps to run Simulation on SOFA:


### Run the program to convert SetPosition message to Float64 message for SOFA to read

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open a file- ros2 run keyboard_trunk_controller set_position_to_float64_converter
 

### Run the program to launch SOFA

    * Open another Linux terminal using Ctrl+Alt+T.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Get into the following workspace- cd Somorob_Dynamixel/prefab.MobileTrunk/mobile_trunk_sim
    * Open a file- runSofa scene.py --argv RobotToSim
    

This will open SOFA Framework with the mobile robot and trunk visible on the screen.
Press on the 'Animate' option to allow the robot show changes to our commands.


### Run the physical motors and see simulation on SOFA simultaneously:

Open the SOFA Framework, terminal of 'dynamixel_pub_sub' and terminal of 'keyboard_controller' on your display so that you can see all these screens together.
Give the required commands of ID and position on the terminal of 'keyboard_controller'.

You will see following-

* The physical motors move as per the commands you have published.

* SOFA Framework shows animation of the mobile trunk and the corresponding cable moves in the simulation.

* The terminal of 'dynamixel_pub_sub' shows the Received messages of ID and position set of the corresponding motor.


### See the publisher and subscriber node graph using rqt_graph

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open rqt_graph- rqt_graph

You will see various nodes and topics visible on the rqt_graph showing publishers and subscribers alongwith topics.

### List of Nodes

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open list of nodes- ros2 node list

You will see following list of nodes-

    /Keyboard_Controller
    /conversion_node
    /read_write_node
    /subscriber_node
    /SofaNode


### List of Topics

    * Open another Linux terminal.
    * Type command- source /opt/ros/foxy/setup.bash
    * Open your workspace- cd Somorob_Dynamixel (You can avoid this step if you are already inside this workspace)
    * Source the workspace- source install/setup.bash
    * Open list of topics- ros2 topic list

You will see following list of topics-

    /Robot/Cable1/state/displacement
    /Robot/Cable2/state/displacement
    /Robot/Cable3/state/displacement
    /Robot/Cable4/state/displacement
    /Robot/Cable5/state/displacement
    /Robot/Cable6/state/displacement
    /Robot/Cable7/state/displacement
    /Robot/Cable8/state/displacement
    /Robot/Cable9/state/displacement
    /Sim/Cable1/state/displacement
    /Sim/Cable2/state/displacement
    /Sim/Cable3/state/displacement
    /Sim/Cable4/state/displacement
    /Sim/Cable5/state/displacement
    /Sim/Cable6/state/displacement
    /Sim/Cable7/state/displacement
    /Sim/Cable8/state/displacement
    /Sim/Cable9/state/displacement
    /parameter_events
    /rosout
    /set_position


### License
-----------

Creative Commons Zero v1.0 Universal see LICENSE