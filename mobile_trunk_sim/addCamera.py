def addCamera(rootNode):

    camera = rootNode.addChild('Camera')
    camera.addObject('MechanicalObject' , template='Rigid3d', rotation=[180, 0, 0],position=[0, 0, 0, -0.5, -0.5, 0.5, 0.5],
                          showObject=False, showObjectScale=100)

    camera.addObject('RigidRigidMapping', name="mapping", input = rootNode.Trunk.framesNode.frames.getLinkPath() ,index=100)

    rootNode.getRoot().addObject('OglViewport', screenSize=[320, 200], name='Camera', zNear=5,
                                      zFar=-10, fovy=55,
                                      cameraRigid=camera.MechanicalObject.position.getLinkPath(), useFBO=False)
