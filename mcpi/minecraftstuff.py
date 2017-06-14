#www.stuffaboutcode.com
#github.com/martinohanlon/minecraft-stuff
#Raspberry Pi, Minecraft - Minecraft 'stuff' extensions

try:
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    import mcpi.util as util
except ImportError:
    import minecraft
    import block
    import util
    
from copy import deepcopy
import time
import math

class MinecraftDrawing:
    """
    MinecraftDrawing - a class of 'useful' drawing functions
    """
    def __init__(self, mc):
        self.mc = mc

    def drawPoint3d(self, x, y, z, blockType, blockData=0):
        """
        draws a single point in Minecraft, i.e. 1 block
        """
        
        self.mc.setBlock(x,y,z,blockType,blockData)
        #print "x = " + str(x) + ", y = " + str(y) + ", z = " + str(z)

    def drawFace(self, vertices, filled, blockType, blockData=0):
        """
        draws a face, when passed a collection of vertices which make up a polyhedron
        """
        
        # get the edges of the face
        edgesVertices = []
        # persist the first vertex
        firstVertex = vertices[0]
        # get the last vertex
        lastVertex = vertices[0]
        
        # loop through vertices and get edges
        for vertex in vertices[1:]:
            # get the points for the edge
            edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z)
            # persist the last vertex found    
            lastVertex = vertex
        
        # get edge between the last and first vertices, so the polyhedron 'joins up'
        edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, firstVertex.x, firstVertex.y, firstVertex.z)

        if (filled):
            #draw solid face
            # this algorithm isnt very efficient, but it does always fill the gap
            
            # sort the edges vertices
            def keyX( point ): return point.x
            def keyY( point ): return point.y
            def keyZ( point ): return point.z
            edgesVertices.sort( key=keyZ )
            edgesVertices.sort( key=keyY )
            edgesVertices.sort( key=keyX )

            #draw lines between the points on the edges
            lastVertex = edgesVertices[0]
            for vertex in edgesVertices[1:]:
                # got 2 vertices, draw lines between them
                self.drawLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z, blockType, blockData)
                #print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
                # persist the last vertex found
                lastVertex = vertex

        else:
            #draw wireframe
            self.drawVertices(edgesVertices, blockType, blockData)
        
    def drawVertices(self, vertices, blockType, blockData=0):
        """
        draws all the points in a collection of vertices with a block
        """
        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType, blockData)

    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType, blockData=0):
        """
        draws a line between 2 points
        """
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType, blockData)

    
    def drawSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        """
        draws a sphere around a point to a radius
        """
        for x in range(radius * -1, radius):
            for y in range(radius * -1, radius):
                for z in range(radius * -1, radius):
                    if x**2 + y**2 + z**2 < radius**2:
                        self.drawPoint3d(x1 + x, y1 + y, z1 + z, blockType, blockData)

    def drawHollowSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        """
        draws a hollow sphere around a point to a radius, sphere has to bigger enough to be hollow!
        """
        for x in range(radius * -1, radius):
            for y in range(radius * -1, radius):
                for z in range(radius * -1, radius):
                    if (x**2 + y**2 + z**2 < radius**2) and (x**2 + y**2 + z**2 > (radius**2 - (radius * 2))):
                        self.drawPoint3d(x1 + x, y1 + y, z1 +z, blockType, blockData)

    def drawCircle(self, x0, y0, z, radius, blockType, blockData=0):
        """
        draws a circle in the Y plane (i.e. vertically)
        """
        
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.drawPoint3d(x0, y0 + radius, z, blockType, blockData)
        self.drawPoint3d(x0, y0 - radius, z, blockType, blockData)
        self.drawPoint3d(x0 + radius, y0, z, blockType, blockData)
        self.drawPoint3d(x0 - radius, y0, z, blockType, blockData)
     
        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x   
            self.drawPoint3d(x0 + x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 + x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 - x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 - x, z, blockType, blockData)

    
    def drawHorizontalCircle(self, x0, y, z0, radius, blockType, blockData=0):
        """
        draws a circle in the X plane (i.e. horizontally)
        """

        f = 1 - radius
        ddf_x = 1
        ddf_z = -2 * radius
        x = 0
        z = radius
        self.drawPoint3d(x0, y, z0 + radius, blockType, blockData)
        self.drawPoint3d(x0, y, z0 - radius, blockType, blockData)
        self.drawPoint3d(x0 + radius, y, z0, blockType, blockData)
        self.drawPoint3d(x0 - radius, y, z0, blockType, blockData)
     
        while x < z:
            if f >= 0:
                z -= 1
                ddf_z += 2
                f += ddf_z
            x += 1
            ddf_x += 2
            f += ddf_x   
            self.drawPoint3d(x0 + x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 + x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 - x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 - x, blockType, blockData)
    
    def getLine(self, x1, y1, z1, x2, y2, z2):
        """
        Returns all the points which would make up a line between 2 points as a list

        3d implementation of bresenham line algorithm
        """
        # return the maximum of 2 values
        def MAX(a,b):
            if a > b: return a
            else: return b

        # return step
        def ZSGN(a):
            if a < 0: return -1
            elif a > 0: return 1
            elif a == 0: return 0

        # list for vertices
        vertices = []

        # if the 2 points are the same, return single vertice
        if (x1 == x2 and y1 == y2 and z1 == z2):
            vertices.append(minecraft.Vec3(x1, y1, z1))
                            
        # else get all points in edge
        else:
        
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            ax = abs(dx) << 1
            ay = abs(dy) << 1
            az = abs(dz) << 1

            sx = ZSGN(dx)
            sy = ZSGN(dy)
            sz = ZSGN(dz)

            x = x1
            y = y1
            z = z1

            # x dominant
            if (ax >= MAX(ay, az)):
                yd = ay - (ax >> 1)
                zd = az - (ax >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (x == x2):
                        loop = False
                    if (yd >= 0):
                        y += sy
                        yd -= ax
                    if (zd >= 0):
                        z += sz
                        zd -= ax
                    x += sx
                    yd += ay
                    zd += az
            # y dominant
            elif (ay >= MAX(ax, az)):
                xd = ax - (ay >> 1)
                zd = az - (ay >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (y == y2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= ay
                    if (zd >= 0):
                        z += sz
                        zd -= ay
                    y += sy
                    xd += ax
                    zd += az
            # z dominant
            elif(az >= MAX(ax, ay)):
                xd = ax - (az >> 1)
                yd = ay - (az >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (z == z2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= az
                    if (yd >= 0):
                        y += sy
                        yd -= az
                    z += sz
                    xd += ax
                    yd += ay
                    
        return vertices

# MinecraftShape - a class for managing shapes
class MinecraftShape:
    """
    MinecraftShape

    The implementation of a 'shape' in Minecraft.
    Each shape consists of one or many blocks with a position relative to each other.
    Shapes can be transformed by movement and rotation.
    When a shape is changed and redrawn in Minecraft only the blocks which have changed are updated.
    """
     
    def __init__(self, mc, position, shapeBlocks = None, visible = True):
        #persist the data
        self.mc = mc
        self.position = position
        self.originalPos = self.position.clone()
        
        if shapeBlocks == None:
            self.shapeBlocks = []
        else:
            self.shapeBlocks = shapeBlocks

        self.visible = visible

        #setup properties

        #drawnShapeBlocks is the last positions the shape was drawn too
        self.drawnShapeBlocks = None

        #set yaw, pitch, roll
        self.yaw, self.pitch, self.roll = 0, 0, 0

        #move the shape to its starting position
        self._move(position.x, position.y, position.z)

    def draw(self):
        """
        draws the shape in Minecraft
        taking into account where it was last drawn and only updates the blocks which have changed
        """

        #create 2 sets only of the blocks which are drawn and one of the shapeBlocks
        if self.drawnShapeBlocks == None:
            drawnSet = set()
        else:
            drawnSet = set(self.drawnShapeBlocks)
        currentSet = set(self.shapeBlocks)
        
        #work out the blocks which need to be cleared
        for blockToClear in drawnSet - currentSet:
            self.mc.setBlock(blockToClear.actualPos.x, blockToClear.actualPos.y, blockToClear.actualPos.z, block.AIR.id)

        #work out the blocks which have changed and need to be re-drawn
        for blockToDraw in currentSet - drawnSet:
            self.mc.setBlock(blockToDraw.actualPos.x, blockToDraw.actualPos.y, blockToDraw.actualPos.z, blockToDraw.blockType, blockToDraw.blockData)

        #update the blocks which have been drawn
        self.drawnShapeBlocks = deepcopy(self.shapeBlocks)
        self.visible = True

    def redraw(self):
        """
        draws the shape in Minecraft, by clearing all the blocks and redrawing them 
        """
        if self.drawnShapeBlocks != None:
            for blockToClear in self.drawnShapeBlocks:
                self.mc.setBlock(blockToClear.actualPos.x, blockToClear.actualPos.y, blockToClear.actualPos.z, block.AIR.id)

        for blockToDraw in self.shapeBlocks:
            self.mc.setBlock(blockToDraw.actualPos.x, blockToDraw.actualPos.y, blockToDraw.actualPos.z, blockToDraw.blockType, blockToDraw.blockData)

        #update the blocks which have been drawn
        self.drawnShapeBlocks = deepcopy(self.shapeBlocks)
        self.visible = True

    def clear(self):
        """
        clears the shape in Minecraft
        """
        #clear the shape
        if self.drawnShapeBlocks != None:
            for blockToClear in self.drawnShapeBlocks:
                self.mc.setBlock(blockToClear.actualPos.x,
                                 blockToClear.actualPos.y,
                                 blockToClear.actualPos.z,
                                 block.AIR.id)
            self.drawnShapeBlocks = None
        
        self.visible = False

    def reset(self):
        """
        resets the shape back to its original position
        """
        self.rotate(0,0,0)
        self.move(self.originalPos.x, self.originalPos.y, self.originalPos.z)

    def moveBy(self, x, y, z):
        """
        moves the position of the shape by x,y,z
        """
        return self._move(self.position.x + x, self.position.y + y, self.position.z + z)

    def move(self, x, y, z):
        """
        moves the position of the shape to x,y,z
        """
        #is the position different
        if self.position.x != x or self.position.y != y or self.position.z != z:
            self.position.x = x
            self.position.y = y
            self.position.z = z

            self._recalcBlocks()
            
            if self.visible:
                self.draw()

            return True
        
        else:
            
            return False

    def _move(self, x, y, z):
        """
        Internal. moves the position of the shape to x,y,z
        """
        self.position.x = x
        self.position.y = y
        self.position.z = z

        self._recalcBlocks()
        
        if self.visible:
            self.draw()

    def _recalcBlocks(self):
        """
        recalculate the position of all of the blocks in a shape
        """
        for shapeBlock in self.shapeBlocks:
            self._recalcBlock(shapeBlock)
            
    def _recalcBlock(self, shapeBlock):
        """
        recalulate the shapeBlock's position based on its relative position,
         its actual position in the world and its rotation
        """
        #reset the block's position before recalcing it
        shapeBlock.resetRelativePos()
        
        #rotate the block
        self._rotateShapeBlock(shapeBlock, self.yaw, self.pitch, self.roll)
        
        #move the block
        self._moveShapeBlock(shapeBlock, self.position.x, self.position.y, self.position.z)
        
    def rotate(self, yaw, pitch, roll):
        """
        sets the rotation of a shape by yaw, pitch and roll
        """
        #is the rotation different?
        if yaw != self.yaw or pitch != self.pitch or roll != self.roll:
            
            #update values
            self.yaw, self.pitch, self.roll = yaw, pitch, roll
            
            #recalc all the block positions
            self._recalcBlocks()

            #if its visible redraw it
            if self.visible:
                self.draw()

            return True
        
        else:
            
            return False

    def rotateBy(self, yaw, pitch, roll):
        """
        increments the rotation of a shape by yaw, pitch and roll
        """
        return self.rotate(self.yaw + yaw, self.pitch + pitch, self.roll + roll)
        
    def _moveShapeBlock(self, shapeBlock, x, y, z):
        """
        offset the position of the block by the position
        """
        shapeBlock.actualPos.x = shapeBlock.relativePos.x + x
        shapeBlock.actualPos.y = shapeBlock.relativePos.y + y
        shapeBlock.actualPos.z = shapeBlock.relativePos.z + z

    def _rotateShapeBlock(self, shapeBlock, yaw, pitch, roll):
        """
        rotate the block
        """
        self._rotateShapeBlockY(shapeBlock, yaw)
        self._rotateShapeBlockZ(shapeBlock, roll)
        self._rotateShapeBlockX(shapeBlock, pitch)
        

    def _rotateShapeBlockY(self, shapeBlock, theta):
        """
        rotate y = yaw (direction)
        """
        if theta != 0:
            sin_t = math.sin(math.radians(theta))
            cos_t = math.cos(math.radians(theta))
            x = shapeBlock.relativePos.x * cos_t - shapeBlock.relativePos.z * sin_t
            z = shapeBlock.relativePos.z * cos_t + shapeBlock.relativePos.x * sin_t
            shapeBlock.relativePos.x = int(round(x,0))
            shapeBlock.relativePos.z = int(round(z,0))
        
    def _rotateShapeBlockZ(self, shapeBlock, theta):
        """
        rotate z = roll
        """
        if theta != 0:
            sin_t = math.sin(math.radians(theta))
            cos_t = math.cos(math.radians(theta))
            x = shapeBlock.relativePos.x * cos_t - shapeBlock.relativePos.y * sin_t
            y = shapeBlock.relativePos.y * cos_t + shapeBlock.relativePos.x * sin_t
            shapeBlock.relativePos.x = int(round(x,0))
            shapeBlock.relativePos.y = int(round(y,0))
        
    def _rotateShapeBlockX(self, shapeBlock, theta):
        """
        rotate x = pitch
        """
        if theta != 0:
            sin_t = math.sin(math.radians(theta))
            cos_t = math.cos(math.radians(theta))
            y = shapeBlock.relativePos.y * cos_t - shapeBlock.relativePos.z * sin_t
            z = shapeBlock.relativePos.z * cos_t + shapeBlock.relativePos.y * sin_t
            shapeBlock.relativePos.y = int(round(y,0))
            shapeBlock.relativePos.z = int(round(z,0))

    def setBlock(self, x, y, z, blockType, blockData = 0, tag = ""):
        """
        sets one block in the shape and redraws it 
        """
        self._setBlock(x, y, z, blockType, blockData, tag)

        #if the shape is visible (re)draw it
        if self.visible:
            self.draw()

    def _setBlock(self, x, y, z, blockType, blockData, tag):
        """
        sets one block in the shape 
        """
        #does the block already exist?
        for shapeBlock in self.shapeBlocks:
            if shapeBlock.originalPos.x == x and shapeBlock.originalPos.y == y and shapeBlock.originalPos.z == z:
                #it does exist, update it
                shapeBlock.blockType = blockType
                shapeBlock.blockData = blockData
                shapeBlock.tag= tag
                break
        else:
            #it doesn't append it
            newShapeBlock = ShapeBlock(x, y, z, blockType, blockData, tag)
            self._recalcBlock(newShapeBlock)
            self.shapeBlocks.append(newShapeBlock)

    def setBlocks(self, x1, y1, z1, x2, y2, z2, blockType, blockData = 0, tag = ""):
        """
        creates a cuboid of blocks in the shape and redraws it
        """
        #order x, y, z's
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        if z1 > z2: z1, z2 = z2, z1

        #create the cuboid
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    self._setBlock(x, y, z, blockType, blockData, tag)

        #if the shape is visible (re)draw it
        if self.visible:
            self.draw()

    def getShapeBlock(self, x, y, z):
        """
        returns the shape block for an 'actual position'        
        """
        #does the block exist?
        for shapeBlock in self.shapeBlocks:
            if shapeBlock.actualPos.x == x and shapeBlock.actualPos.y == y and shapeBlock.actualPos.z == z:
                return shapeBlock
        else:
            #it doesn't return None
            return None
        
# a class created to manage a block within a shape
class ShapeBlock():
    """
    ShapeBlock
    a class to hold one block within a shape
    """
    def __init__(self, x, y, z, blockType, blockData = 0, tag = ""):
        #persist data
        self.blockType = blockType
        self.blockData = blockData

        #store the positions
        # original pos
        self.originalPos = minecraft.Vec3(x, y, z)
        # relative pos - block position relatively to other shape blocks
        self.relativePos = minecraft.Vec3(x, y, z)
        # actual pos - actual block position in the world
        self.actualPos = minecraft.Vec3(x, y, z)

        #the tag system is used to give a particular block inside a shape meaning
        # e.g. for an animal shape you could tag the block which is its head
        self.tag = tag

        # the mc block object
        self.mcBlock = block.Block(blockType, blockData)

    def resetRelativePos(self):
        """
        resets the relative position of the block back to its original position
        """
        self.relativePos = self.originalPos.clone()

    def __hash__(self):
        return hash((self.actualPos.x, self.actualPos.y, self.actualPos.z, self.blockType, self.blockData))

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return (self.actualPos.x, self.actualPos.y, self.actualPos.z, self.blockType, self.blockData) == (other.actualPos.x, other.actualPos.y, other.actualPos.z, other.blockType, other.blockData)

# rotation test
if __name__ == "__main__2":

    #connect to minecraft
    mc = minecraft.Minecraft.create()

    #test shape
    pos = mc.player.getTilePos()
    pos.y += 40

    myShape = MinecraftShape(mc, pos)
    try:
        #myShape.setBlocks(-3, 0, 0, 3, 0, 0, block.WOOL.id, 2)
        #myShape.setBlocks(0, -3, 0, 0, 3, 0, block.WOOL.id, 3)
        #myShape.setBlocks(0, 0, -3, 0, 0, 3, block.WOOL.id, 4)
        print("draw shape")
        myShape.setBlocks(-5, 0, -5, 3, 0, 3, block.WOOL.id, 5)
        print("draw shape done")
        
        time.sleep(5)
        roll = 0
        pitch = 0
        yaw = 0

        #angles = [15,30,45,60,75,90]
        angles = [45, 90]

        print("roll shape")
        for roll in angles:
            myShape.rotate(yaw, pitch, roll)
            print("roll shape {} done".format(roll))
            time.sleep(1)
        
        for pitch in angles:
            myShape.rotate(yaw, pitch, roll)
            time.sleep(1)

        for yaw in angles:
            myShape.rotate(yaw, pitch, roll)
            time.sleep(1)

        for count in range(0,5):
            myShape.moveBy(1,0,0)
            time.sleep(0.5)

        time.sleep(5)
    finally:
        myShape.clear()
    
# minecraft stuff testing
if __name__ == "__main__":

    #connect to minecraft
    mc = minecraft.Minecraft.create()

    #test MinecraftDrawing

    #clear area
    mc.setBlocks(-25, 0, -25, 25, 25, 25, block.AIR.id)

    #create drawing object
    mcDrawing = MinecraftDrawing(mc)

    #line
    mcDrawing.drawLine(0,0,-10,-10,10,-5,block.STONE.id)

    #circle
    mcDrawing.drawCircle(-15,15,-15,10,block.WOOD.id)

    #sphere
    mcDrawing.drawSphere(-15,15,-15,5,block.OBSIDIAN.id)
    
    #face - solid triangle
    faceVertices = []
    faceVertices.append(minecraft.Vec3(0,0,0))
    faceVertices.append(minecraft.Vec3(5,10,0))
    faceVertices.append(minecraft.Vec3(10,0,0))
    mcDrawing.drawFace(faceVertices, True, block.SNOW_BLOCK.id)

    #face - wireframe square
    faceVertices = []
    faceVertices.append(minecraft.Vec3(0,0,5))
    faceVertices.append(minecraft.Vec3(10,0,5))
    faceVertices.append(minecraft.Vec3(10,10,5))
    faceVertices.append(minecraft.Vec3(0,10,5))
    mcDrawing.drawFace(faceVertices, False, block.DIAMOND_BLOCK.id)

    #face - 5 sided shape
    faceVertices = []
    faceVertices.append(minecraft.Vec3(0,15,0))
    faceVertices.append(minecraft.Vec3(5,15,5))
    faceVertices.append(minecraft.Vec3(3,15,10))
    faceVertices.append(minecraft.Vec3(-3,15,10))
    faceVertices.append(minecraft.Vec3(-5,15,5))
    mcDrawing.drawFace(faceVertices, True, block.GOLD_BLOCK.id)

    #test MinecraftShape
    playerPos = mc.player.getTilePos()

    #create the shape object
    shapeBlocks = [ShapeBlock(0,0,0,block.DIAMOND_BLOCK.id),
                  ShapeBlock(1,0,0,block.DIAMOND_BLOCK.id),
                  ShapeBlock(1,0,1,block.DIAMOND_BLOCK.id),
                  ShapeBlock(0,0,1,block.DIAMOND_BLOCK.id),
                  ShapeBlock(0,1,0,block.DIAMOND_BLOCK.id),
                  ShapeBlock(1,1,0,block.DIAMOND_BLOCK.id),
                  ShapeBlock(1,1,1,block.DIAMOND_BLOCK.id),
                  ShapeBlock(0,1,1,block.DIAMOND_BLOCK.id)]
    
    #move the shape about
    myShape = MinecraftShape(mc, playerPos, shapeBlocks)
    print("drawn shape")
    time.sleep(10)
    myShape.moveBy(-1,1,-1)
    time.sleep(1)
    myShape.moveBy(1,0,1)
    time.sleep(1)
    myShape.moveBy(1,1,0)
    time.sleep(1)

    #rotate the shape
    myShape.rotate(90,0,0)
    
    #clear the shape
    myShape.clear()
