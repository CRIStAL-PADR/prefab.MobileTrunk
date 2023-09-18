import Sofa
import sys
from stlib3.scene import Scene
from summitxl_controller import *
from summitxl_roscontroller import *
from echelon3.RosCableController import *
from stlib3.physics.rigid import Floor
#from floor import Floor
from mobile_trunk import mobileTrunk
from addCamera import addCamera



def createScene(rootNode):

    #########################################
    # Plugins, data and Solvers
    ######################################### 

    rootNode.addObject('RequiredPlugin', name='SofaPython3')
    rootNode.addObject('RequiredPlugin', name='BeamAdapter')
    rootNode.addObject('RequiredPlugin', name='SoftRobots')
    rootNode.addObject('RequiredPlugin', name='SofaMeshCollision')
    rootNode.addObject('RequiredPlugin', name='SofaPlugins', pluginName='SofaGeneralRigid SofaGeneralEngine SofaConstraint SofaImplicitOdeSolver SofaSparseSolver SofaDeformable SofaEngine SofaBoundaryCondition SofaRigid SofaTopologyMapping SofaOpenglVisual SofaMiscCollision')


    scene = Scene(rootNode, iterative=False)
    scene.addMainHeader()
    scene.addContact(alarmDistance=0.1*1000, contactDistance=0.05*1000, frictionCoef=8)
    scene.VisualStyle.displayFlags = 'hideBehaviorModels showForceFields showCollisionModels showInteractionForceFields'
    scene.addObject('DefaultVisualManagerLoop')
    scene.dt = 0.01
    scene.gravity = [0., -9810., 0.]
    scene.Settings.removeObject(scene.Settings.OglSceneFrame)

    scene.Simulation.addObject('GenericConstraintCorrection', solverName='LinearSolver', ODESolverName='GenericConstraintSolver')

    #scene.Simulation.addObject('GenericConstraintCorrection', linearSolver='@LinearSolver', ODESolver='@GenericConstraintSolver')
    scene.Simulation.TimeIntegrationSchema.vdamping.value = 0.1
    scene.Simulation.TimeIntegrationSchema.rayleighStiffness = 0.01

    #########################################
    # add robot
    #########################################
    scale = 500
    self, trunk, cables = mobileTrunk(scene.Modelling)
    scene.Simulation.addChild(trunk)
    scene.Simulation.addChild(self)

    floor = Floor(rootNode,
                  name="Floor",
                  translation=[-2*scale, -0.1*scale, 2*scale],
                  uniformScale=0.5*scale,
                  isAStaticObject=True)

    #def myAnimation(target, body, factor):
    #    body.position += [[0.0,0.0,0.001,0.0,0,0,1]]
    #    target.position = [[factor* 3.14 * 2]]*len(target.position.value)

    #animate(myAnimation, {
    #        "body" : scene.Modelling.SummitXL.Chassis.position,
    #        "target": scene.Modelling.SummitXL.Chassis.WheelsMotors.angles}, duration=2, mode="loop")

    if sys.argv[1] == "KeyboardController":
        scene.Modelling.SummitXL.addObject(SummitxlController(name="KeyboardController", robot=scene.Modelling.SummitXL, test=False))

    elif sys.argv[1] == "SimToRobot":
            import sofaros
            from sofaros import RosReceiver  
            rosNode = sofaros.init("SofaNode")
            robot=scene.Modelling.SummitXL
            scene.Modelling.SummitXL.addObject(SummitxlROSController(name="KeyboardController", robot=robot, robotToSim=False, test=False))

            # scene.Modelling.SummitXL.addObject(sofaros.RosSender(rosNode, "/summit_xl/robotnik_base_control/odom",
            #                                                                         [robot.findData('timestamp'), 
            #                                                                         robot.findData('sim_position'), 
            #                                                                         robot.findData('sim_orientation'),
            #                                                                         robot.findData('robot_linear_vel'), 
            #                                                                         robot.findData('robot_angular_vel')], 
            #                                                                         Odometry, odom_send))

            # scene.Modelling.SummitXL.addObject(sofaros.RosSender(rosNode, "/summit_xl/robotnik_base_control/cmd_vel",
            #                                [robot.findData('robot_linear_vel'),robot.findData('robot_angular_vel')],
            #                                Twist, vel_send))
            scene.Modelling.SummitXL.addObject(RosReceiver(rosNode, "/summit_xl/robotnik_base_control/cmd_vel", [robot.findData('robot_linear_vel'),
                                                                    robot.findData('robot_angular_vel')],
                                                                    Twist, vel_recv))

    elif sys.argv[1] == "RobotToSim":
        import sofaros
        from sofaros import RosReceiver, RosSender  
        rosNode = sofaros.init("SofaNode")
        robot=scene.Modelling.SummitXL
        scene.Modelling.SummitXL.addObject(SummitxlROSController(name="KeyboardController", robot=robot, robotToSim=True, test=False))
        scene.Modelling.SummitXL.addObject(RosReceiver(rosNode, "/summit_xl/robotnik_base_control/odom",
                                                                             [robot.findData('timestamp'),
                                                                              robot.findData('reel_position'),
                                                                              robot.findData('reel_orientation'),
                                                                              robot.findData('robot_linear_vel'),
                                                                              robot.findData('robot_angular_vel')],
                                                                                Odometry, odom_recv))
                                                                                                                                                       
        scene.Modelling.SummitXL.addObject(RosSender(rosNode, "/digital_twin/odom", [robot.findData('sim_position'),
                                                              robot.findData('sim_orientation')],Odometry, 
                                                              position_and_orientation_send))
        
        scene.Modelling.SummitXL.addObject(RosSender(rosNode, "/digital_twin/joint_states", robot.findData('digital_twin_joints_states_vel'),
                                                            sensor_msgs.msg.JointState, digital_twin_jointstate_pub))
        
        scene.Modelling.SummitXL.addObject(RosReceiver(rosNode, "/summit_xl/joint_states", robot.findData('summit_xl_joints_states_vel'),
                                                            sensor_msgs.msg.JointState, summit_xl_jointstate_recv))


        scene.Modelling.SummitXL.addObject(CableROSController(name="CableROSController", rosNode = rosNode, cables=cables, robot=robot, robotToSim=True, test=False))

        for i in range(1,10):
            
            topic = str("/Sim/Cable"+str(i)+"/state/displacement")
            scene.Modelling.SummitXL.addObject(RosReceiver(rosNode, topic, robot.findData("effector_cable_data"),Float64, cable_displacement_recv))
            print(topic)  

        scene.Modelling.SummitXL.addObject(RosSender(rosNode, "/Robot/end_effector/pos", robot.findData("end_effector_pos"),Float64MultiArray, end_effector_pos_send))

    return rootNode
