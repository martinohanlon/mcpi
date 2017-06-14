from .connection import Connection
from .vec3 import Vec3
from .event import BlockEvent, ChatEvent
from .block import Block
import math
from .util import flatten

""" Minecraft PI low level api v0.1_1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB"""

""" Updated to include functionality provided by RaspberryJuice:
- getBlocks()
- getDirection()
- getPitch()
- getRotation()
- getPlayerEntityId()
- pollChatPosts() """

def intFloor(*args):
    return [int(math.floor(x)) for x in flatten(args)]

class CmdPositioner:
    """Methods for setting and getting positions"""
    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getPos", id)
        return Vec3(*list(map(float, s.split(","))))

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setPos", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getTile", id)
        return Vec3(*list(map(int, s.split(","))))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send(self.pkg + b".setTile", id, intFloor(*args))

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def getRotation(self, id):
        """get entity rotation (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getRotation", id))

    def getPitch(self, id):
        """get entity pitch (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getPitch", id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + b".setting", setting, 1 if bool(status) else 0)


class CmdEntity(CmdPositioner):
    """Methods for entities"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"entity")


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"player")
        self.conn = connection

    def getPos(self):
        return CmdPositioner.getPos(self, [])
    def setPos(self, *args):
        return CmdPositioner.setPos(self, [], args)
    def getTilePos(self):
        return CmdPositioner.getTilePos(self, [])
    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, [], args)
    def getDirection(self):
        return CmdPositioner.getDirection(self, [])
    def getRotation(self):
        return CmdPositioner.getRotation(self, [])
    def getPitch(self):
        return CmdPositioner.getPitch(self, [])

class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send(b"camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send(b"camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send(b"camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send(b"camera.setPos", args)


class CmdEvents:
    """Events"""
    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send(b"events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""
    def __init__(self, connection):
        self.conn = connection

        self.camera = CmdCamera(connection)
        self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection)
        self.events = CmdEvents(connection)

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.sendReceive(b"world.getBlock", intFloor(args)))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        ans = self.conn.sendReceive(b"world.getBlockWithData", intFloor(args))
        return Block(*list(map(int, ans.split(","))))

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        s = self.conn.sendReceive(b"world.getBlocks", intFloor(args))
        return map(int, s.split(","))

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.conn.send(b"world.setBlock", intFloor(args))

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        self.conn.send(b"world.setBlocks", intFloor(args))

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.sendReceive(b"world.getHeight", intFloor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive(b"world.getPlayerIds")
        return list(map(int, ids.split("|")))

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return int(self.conn.sendReceive(b"world.getPlayerId", name))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send(b"world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send(b"world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send(b"chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send(b"world.setting", setting, 1 if bool(status) else 0)

    @staticmethod
    def create(address = "localhost", port = 4711):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")
