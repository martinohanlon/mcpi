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

import time
import math

class Points():
    """
    Points - a collection of minecraft positions or Vec3's. Used when drawing faces ``MinecraftDrawing.drawFace()``.
    """
    def __init__(self):
        self._points = []

    def add(self, x, y, z):
        """
        add a single position to the list of points.

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.
        """
        self._points.append(minecraft.Vec3(x, y, z))

    def getVec3s(self):
        """
        returns a list of Vec3 positions
        """
        return self._points
    
class MinecraftDrawing:
    """
    MinecraftDrawing - a class of useful drawing functions

    :param mcpi.minecraft.Minecraft mc:
        A Minecraft object which is connected to a world. 
    """
    def __init__(self, mc):
        self.mc = mc

    def drawPoint3d(self, x, y, z, blockType, blockData=0):
        """
        draws a single point in Minecraft, i.e. 1 block

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        
        self.mc.setBlock(x,y,z,blockType,blockData)
        #print "x = " + str(x) + ", y = " + str(y) + ", z = " + str(z)

    def drawFace(self, vertices, filled, blockType, blockData=0):
        """
        draws a face, when passed a collection of vertices which make up a polyhedron

        :param list vertices:
            The a list of points, passed as either a ``minecraftstuff.Points`` object 
            or as a list of ``mcpi.minecraft.Vec3`` objects.

        :param boolean filled:
            If ``True`` fills the face with blocks.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        
        # was a Points class passed?  If so get the list of Vec3s.
        if isinstance(vertices, Points):
            vertices = vertices.getVec3s()  

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

        :param list vertices:
            A list of ``mcpi.minecraft.Vec3`` objects.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """

        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType, blockData)

    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType, blockData=0):
        """
        draws a line between 2 points

        :param int x1:
            The x position of the first point.

        :param int y1:
            The y position of the first point.

        :param int z1:
            The z position of the first point.

        :param int x2:
            The x position of the second point.

        :param int y2:
            The y position of the second point.

        :param int z2:
            The z position of the second point.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType, blockData)

    
    def drawSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        """
        draws a sphere around a point to a radius

        :param int x1:
            The x position of the centre of the sphere.

        :param int y1:
            The y position of the centre of the sphere.

        :param int z1:
            The z position of the centre of the sphere.

        :param int radius:
            The radius of the sphere.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        for x in range(radius * -1, radius):
            for y in range(radius * -1, radius):
                for z in range(radius * -1, radius):
                    if x**2 + y**2 + z**2 < radius**2:
                        self.drawPoint3d(x1 + x, y1 + y, z1 + z, blockType, blockData)

    def drawHollowSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        """
        draws a hollow sphere around a point to a radius, sphere has to big enough to be hollow!

        :param int x1:
            The x position of the centre of the sphere.

        :param int y1:
            The y position of the centre of the sphere.

        :param int z1:
            The z position of the centre of the sphere.

        :param int radius:
            The radius of the sphere.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        for x in range(radius * -1, radius):
            for y in range(radius * -1, radius):
                for z in range(radius * -1, radius):
                    if (x**2 + y**2 + z**2 < radius**2) and (x**2 + y**2 + z**2 > (radius**2 - (radius * 2))):
                        self.drawPoint3d(x1 + x, y1 + y, z1 +z, blockType, blockData)

    def drawCircle(self, x0, y0, z, radius, blockType, blockData=0):
        """
        draws a circle in the Y plane (i.e. vertically)

        :param int x0:
            The x position of the centre of the circle.

        :param int y0:
            The y position of the centre of the circle.

        :param int z:
            The z position of the centre of the circle.

        :param int radius:
            The radius of the sphere.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
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

        :param int x0:
            The x position of the centre of the circle.

        :param int y:
            The y position of the centre of the circle.

        :param int z0:
            The z position of the centre of the circle.

        :param int radius:
            The radius of the circle.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
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

        :param int x1:
            The x position of the first point.

        :param int y1:
            The y position of the first point.

        :param int z1:
            The z position of the first point.

        :param int x2:
            The x position of the second point.

        :param int y2:
            The y position of the second point.

        :param int z2:
            The z position of the second point.
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
    MinecraftShape - the implementation of a 'shape' in Minecraft.

    Each shape consists of one or many blocks with a position relative to each other.
    
    Shapes can be transformed by movement and rotation.
    
    When a shape is changed and redrawn in Minecraft only the blocks which have changed are updated.

    :param mcpi.minecraft.Minecraft mc:
        A Minecraft object which is connected to a world.

    :param mcpi.minecraft.Vec3 position:
        The position where the shape should be created

    :param list shapeBlocks:
        A list of ShapeBlocks which make up the shape. This defaults to ``None``.

    :param bool visible:
        Where the shape should be visible. This defaults to ``True``.
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
        draws the shape in Minecraft, taking into account where it was last drawn, 
        only updating the blocks which have changed
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
        self.drawnShapeBlocks = self._copyBlocks(self.shapeBlocks)
        self.visible = True

    def redraw(self):
        """
        redraws the shape in Minecraft, by clearing all the blocks and redrawing them 
        """
        if self.drawnShapeBlocks != None:
            for blockToClear in self.drawnShapeBlocks:
                self.mc.setBlock(blockToClear.actualPos.x, blockToClear.actualPos.y, blockToClear.actualPos.z, block.AIR.id)

        for blockToDraw in self.shapeBlocks:
            self.mc.setBlock(blockToDraw.actualPos.x, blockToDraw.actualPos.y, blockToDraw.actualPos.z, blockToDraw.blockType, blockToDraw.blockData)

        #update the blocks which have been drawn
        self.drawnShapeBlocks = self._copyBlocks(self.shapeBlocks)
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
        
        :param int x:
            The number of blocks to move in x.

        :param int y:
            The number of blocks to move in y.

        :param int z:
            The number of blocks to move in z.

        """
        return self._move(self.position.x + x, self.position.y + y, self.position.z + z)

    def move(self, x, y, z):
        """
        moves the position of the shape to x,y,z

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.
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
    
    def _copyBlocks(self, shapeBlocks):
        """
        Internal. copy a list of shapeBlocks to new objects, item level, as
        opposed to the expensive copy.deepcopy() or copy.copy()
        """
        newShapeBlocks = []
        for shapeBlock in shapeBlocks:
            newShapeBlock = ShapeBlock(shapeBlock.actualPos.x, shapeBlock.actualPos.y, shapeBlock.actualPos.z, shapeBlock.blockType, shapeBlock.blockData, shapeBlock.tag)
            newShapeBlock.originalPos = minecraft.Vec3(shapeBlock.originalPos.x, shapeBlock.originalPos.y, shapeBlock.originalPos.z)
            newShapeBlock.relativePos = minecraft.Vec3(shapeBlock.relativePos.x, shapeBlock.relativePos.y, shapeBlock.relativePos.z)
            newShapeBlocks.append(newShapeBlock)
        return newShapeBlocks

    def _recalcBlocks(self):
        """
        Internal. recalculate the position of all of the blocks in a shape
        """
        for shapeBlock in self.shapeBlocks:
            self._recalcBlock(shapeBlock)
            
    def _recalcBlock(self, shapeBlock):
        """
        Internal. recalulate the shapeBlock's position based on its relative position,
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

        :param float yaw:
            The yaw rotation in degrees.

        :param float pitch:
            The pitch rotation in degrees.

        :param float roll:
            The roll rotation in degrees.        
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

        :param float yaw:
            The yaw rotation in degrees.

        :param float pitch:
            The pitch rotation in degrees.

        :param float roll:
            The roll rotation in degrees.
        """
        return self.rotate(self.yaw + yaw, self.pitch + pitch, self.roll + roll)
        
    def _moveShapeBlock(self, shapeBlock, x, y, z):
        """
        Internal. offset the position of the block by the position
        """
        shapeBlock.actualPos.x = shapeBlock.relativePos.x + x
        shapeBlock.actualPos.y = shapeBlock.relativePos.y + y
        shapeBlock.actualPos.z = shapeBlock.relativePos.z + z

    def _rotateShapeBlock(self, shapeBlock, yaw, pitch, roll):
        """
        Internal. rotate the block
        """
        self._rotateShapeBlockY(shapeBlock, yaw)
        self._rotateShapeBlockZ(shapeBlock, roll)
        self._rotateShapeBlockX(shapeBlock, pitch)
        

    def _rotateShapeBlockY(self, shapeBlock, theta):
        """
        Internal. rotate y = yaw (direction)
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
        Internal. rotate z = roll
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
        Internal. rotate x = pitch
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

        draws a single point in Minecraft, i.e. 1 block

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.

        :param string tag:
            A tag for the block, this is useful for grouping blocks together and keeping 
            track of them as the position of blocks can change, defaults to ``""``. 
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

        :param int x1:
            The x position of the first point.

        :param int y1:
            The y position of the first point.

        :param int z1:
            The z position of the first point.

        :param int x2:
            The x position of the second point.

        :param int y2:
            The y position of the second point.

        :param int z2:
            The z position of the second point.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.

        :param string tag:
            A tag for the block, this is useful for grouping blocks together and keeping 
            track of them as the position of blocks can change, defaults to ``""``. 
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
        returns the ShapeBlock for an 'actual position'  

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.
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
    ShapeBlock - a class to hold one block within a shape

    :param int x:
        The x position.

    :param int y:
        The y position.

    :param int z:
        The z position.

    :param int blockType:
        The block id.

    :param int blockData:
        The block data value, defaults to ``0``.

    :param string tag:
        A tag for the block, this is useful for grouping blocks together and keeping 
        track of them as the position of blocks can change, defaults to ``""``. 
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

class MinecraftTurtle:
    """
    MinecraftTurle - a graphics turtle, which can be used to create 'things' in Minecraft by 
    controlling its position, angles and direction

    :param mcpi.minecraft.Minecraft mc:
        A Minecraft object which is connected to a world.

    :param mcpi.minecraft.Vec3 position:
        The position where the shape should be created, defaults to ``0,0,0``.
    """

    SPEEDTIMES = {0: 0, 10: 0.1, 9: 0.2, 8: 0.3, 7: 0.4, 6: 0.5, 5: 0.6, 4: 0.7, 3: 0.8, 2: 0.9, 1: 1}

    def __init__(self, mc, position=minecraft.Vec3(0, 0, 0)):
        # set defaults
        self.mc = mc
        # start position
        self.startposition = position
        # set turtle position
        self.position = position
        # set turtle angles
        self.heading = 0
        self.verticalheading = 0
        # set pen down
        self._pendown = True
        # set pen block to black wool
        self._penblock = block.Block(block.WOOL.id, 15)
        # flying to true
        self.flying = True
        # set speed
        self.turtlespeed = 6
        # create turtle
        self.showturtle = True
        # create drawing object
        self.mcDrawing = MinecraftDrawing(self.mc)
        # set turtle block
        self.turtleblock = block.Block(block.DIAMOND_BLOCK.id)
        # draw turtle
        self._drawTurtle(int(self.position.x), int(self.position.y), int(self.position.y))

    def forward(self, distance):
        """
        move the turtle forward

        :param int distance:
            the number of blocks to move.
        """
        # get end of line
        # x,y,z = self._findTargetBlock(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading, distance)
        x, y, z = self._findPointOnSphere(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading, distance)
        # move turtle forward
        self._moveTurtle(x, y, z)

    def backward(self, distance):
        """
        move the turtle backward

        :param int distance:
            the number of blocks to move.
        """
        # move turtle backward
        # get end of line
        # x,y,z = self._findTargetBlock(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading - 180, distance)
        x, y, z = self._findPointOnSphere(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading - 180, distance)
        # move turtle forward
        self._moveTurtle(x, y, z)

    def _moveTurtle(self, x, y, z):
        # get blocks between current position and next
        targetX, targetY, targetZ = int(x), int(y), int(z)
        # if walking, set target Y to be height of world
        if not self.flying:
            targetY = self.mc.getHeight(targetX, targetZ)
        currentX, currentY, currentZ = int(self.position.x), int(self.position.y), int(self.position.z)

        # clear the turtle
        if self.showturtle:
            self._clearTurtle(currentX, currentY, currentZ)

        # if speed is 0 and flying, just draw the line, else animate it
        if self.turtlespeed == 0 and self.flying:
            # draw the line
            if self._pendown:
                self.mcDrawing.drawLine(currentX, currentY - 1, currentZ, targetX, targetY - 1, targetZ, self._penblock.id, self._penblock.data)
        else:
            blocksBetween = self.mcDrawing.getLine(currentX, currentY, currentZ, targetX, targetY, targetZ)
            for blockBetween in blocksBetween:
                # print blockBetween
                # if walking update the y, to be the height of the world
                if not self.flying:
                    blockBetween.y = self.mc.getHeight(blockBetween.x, blockBetween.z)
                # draw the turtle
                if self.showturtle:
                    self._drawTurtle(blockBetween.x, blockBetween.y, blockBetween.z)
                # draw the pen
                if self._pendown:
                    self.mcDrawing.drawPoint3d(blockBetween.x, blockBetween.y - 1, blockBetween.z, self._penblock.id, self._penblock.data)
                # wait
                time.sleep(self.SPEEDTIMES[self.turtlespeed])
                # clear the turtle
                if self.showturtle:
                    self._clearTurtle(blockBetween.x, blockBetween.y, blockBetween.z)

        # update turtle's position to be the target
        self.position.x, self.position.y, self.position.z = x, y, z
        # draw turtle
        if self.showturtle:
            self._drawTurtle(targetX, targetY, targetZ)

    def right(self, angle):
        """
        rotate the turtle right

        :param float angle:
            the angle in degrees to rotate.
        """
        # rotate turtle angle to the right
        self.heading = self.heading + angle
        if self.heading > 360:
            self.heading = self.heading - 360

    def left(self, angle):
        """
        rotate the turtle left

        :param float angle:
            the angle in degrees to rotate.
        """
        # rotate turtle angle to the left
        self.heading = self.heading - angle
        if self.heading < 0:
            self.heading = self.heading + 360

    def up(self, angle):
        """
        rotate the turtle up

        :param float angle:
            the angle in degrees to rotate.
        """        
        # rotate turtle angle up
        self.verticalheading = self.verticalheading + angle
        if self.verticalheading > 360:
            self.verticalheading = self.verticalheading - 360
        # turn flying on
        if not self.flying:
            self.flying = True

    def down(self, angle):
        """
        rotate the turtle down

        :param float angle:
            the angle in degrees to rotate.
        """
        # rotate turtle angle down
        self.verticalheading = self.verticalheading - angle
        if self.verticalheading < 0:
            self.verticalheading = self.verticalheading + 360
        # turn flying on
        if not self.flying:
            self.flying = True

    def setx(self, x):
        """
        set the turtle's x position

        :param int x:
            the x position.
        """
        self.setposition(x, self.position.y, self.position.z)

    def sety(self, y):
        """
        set the turtle's y position

        :param int y:
            the y position.
        """
        self.setposition(self.position.x, y, self.position.z)

    def setz(self, z):
        """
        set the turtle's z position

        :param int z:
            the z position.
        """
        self.setposition(self.position.x, self.position.y, z)

    def setposition(self, x, y, z):
        """
        set the turtle's position

        :param int x:
            the x position.

        :param int y:
            the y position.

        :param int z:
            the z position.
        """
        # clear the turtle
        if self.showturtle:
            self._clearTurtle(self.position.x, self.position.y, self.position.z)
        # update the position
        self.position.x = x
        self.position.y = y
        self.position.z = z
        # draw the turtle
        if self.showturtle:
            self._drawTurtle(self.position.x, self.position.y, self.position.z)

    def setheading(self, angle):
        """
        set the turtle's horizontal heading

        :param float angle:
            the angle in degrees.
        """
        self.heading = angle

    def setverticalheading(self, angle):
        """
        set the turtle's verticle heading

        :param float angle:
            the angle in degrees.
        """
        self.verticalheading = angle
        # turn flying on
        if not self.flying:
            self.flying = True

    def home(self):
        """
        reset the turtle's position
        """
        self.position.x = self.startposition.x
        self.position.y = self.startposition.y
        self.position.z = self.startposition.z

    def pendown(self):
        """
        put the turtles pen down, show it will draw
        """
        self._pendown = True

    def penup(self):
        """
        put the turtles pen up, show it wont draw
        """
        self._pendown = False

    def isdown(self):
        """
        returns ``True`` if the pen is down
        """
        return self.pendown

    def fly(self):
        """
        sets the turtle to 'fly', i.e. not have to move along the ground.
        """
        self.flying = True

    def walk(self):
        """
        sets the turtle to 'walk', i.e. it has to move along the ground.
        """
        self.flying = False
        self.verticalheading = 0

    def penblock(self, blockId, blockData=0):
        """
        set the block the turtle uses as its pen.

        :param int blockType:
            The block id.

        :param int blockData:
            The block data value, defaults to ``0``.
        """
        self._penblock = block.Block(blockId, blockData)

    def speed(self, turtlespeed):
        """
        set the turtle's speed.

        :param int turtlespeed:
            ``1`` - ``10``, 1 being the slowest, 10 being the fastest, defaults to ``6``. 
            When set to ``0`` the turtle draws instantaneously.
        """
        self.turtlespeed = turtlespeed

    def _drawTurtle(self, x, y, z):
        # draw turtle
        self.mcDrawing.drawPoint3d(x, y, z, self.turtleblock.id, self.turtleblock.data)
        lastDrawnTurtle = minecraft.Vec3(x, y, z)

    def _clearTurtle(self, x, y, z):
        # clear turtle
        self.mcDrawing.drawPoint3d(x, y, z, block.AIR.id)

    def _findTargetBlock(self, turtleX, turtleY, turtleZ, heading, verticalheading, distance):
        x, y, z = self._findPointOnSphere(turtleX, turtleY, turtleZ, heading, verticalheading, distance)
        x = int(round(x, 0))
        y = int(round(y, 0))
        z = int(round(z, 0))
        return x, y, z

    def _findPointOnSphere(self, cx, cy, cz, horizontalAngle, verticalAngle, radius):
        x = cx + (radius * (math.cos(math.radians(verticalAngle)) * math.cos(math.radians(horizontalAngle))))
        y = cy + (radius * (math.sin(math.radians(verticalAngle))))
        z = cz + (radius * (math.cos(math.radians(verticalAngle)) * math.sin(math.radians(horizontalAngle))))
        return x, y, z

    def _roundXYZ(x, y, z):
        return int(round(x, 0)), int(round(y, 0)), int(round(z, 0))

    def _roundVec3(position):
        return minecraft.vec3(int(position.x), int(position.y), int(position.z))

