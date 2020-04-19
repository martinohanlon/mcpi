class Entity:
    '''Minecraft PI entity description. Can be sent to Minecraft.spawnEntity'''

    def __init__(self, id, name = None):
        self.id = id
        self.name = name

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __eq__(self, rhs):
        return self.id == rhs.id

    def __hash__(self):
        return self.id

    def __iter__(self):
        '''Allows an Entity to be sent whenever id is needed'''
        return iter((self.id,))

    def __repr__(self):
        return 'Entity(%d)'%(self.id)

EXPERIENCE_ORB = Entity(2, "EXPERIENCE_ORB")
AREA_EFFECT_CLOUD = Entity(3, "AREA_EFFECT_CLOUD")
ELDER_GUARDIAN = Entity(4, "ELDER_GUARDIAN")
WITHER_SKELETON = Entity(5, "WITHER_SKELETON")
STRAY = Entity(6, "STRAY")
EGG = Entity(7, "EGG")
LEASH_HITCH = Entity(8, "LEASH_HITCH")
PAINTING = Entity(9, "PAINTING")
ARROW = Entity(10, "ARROW")
SNOWBALL = Entity(11, "SNOWBALL")
FIREBALL = Entity(12, "FIREBALL")
SMALL_FIREBALL = Entity(13, "SMALL_FIREBALL")
ENDER_PEARL = Entity(14, "ENDER_PEARL")
ENDER_SIGNAL = Entity(15, "ENDER_SIGNAL")
THROWN_EXP_BOTTLE = Entity(17, "THROWN_EXP_BOTTLE")
ITEM_FRAME = Entity(18, "ITEM_FRAME")
WITHER_SKULL = Entity(19, "WITHER_SKULL")
PRIMED_TNT = Entity(20, "PRIMED_TNT")
HUSK = Entity(23, "HUSK")
SPECTRAL_ARROW = Entity(24, "SPECTRAL_ARROW")
SHULKER_BULLET = Entity(25, "SHULKER_BULLET")
DRAGON_FIREBALL = Entity(26, "DRAGON_FIREBALL")
ZOMBIE_VILLAGER = Entity(27, "ZOMBIE_VILLAGER")
SKELETON_HORSE = Entity(28, "SKELETON_HORSE")
ZOMBIE_HORSE = Entity(29, "ZOMBIE_HORSE")
ARMOR_STAND = Entity(30, "ARMOR_STAND")
DONKEY = Entity(31, "DONKEY")
MULE = Entity(32, "MULE")
EVOKER_FANGS = Entity(33, "EVOKER_FANGS")
EVOKER = Entity(34, "EVOKER")
VEX = Entity(35, "VEX")
VINDICATOR = Entity(36, "VINDICATOR")
ILLUSIONER = Entity(37, "ILLUSIONER")
MINECART_COMMAND = Entity(40, "MINECART_COMMAND")
BOAT = Entity(41, "BOAT")
MINECART = Entity(42, "MINECART")
MINECART_CHEST = Entity(43, "MINECART_CHEST")
MINECART_FURNACE = Entity(44, "MINECART_FURNACE")
MINECART_TNT = Entity(45, "MINECART_TNT")
MINECART_HOPPER = Entity(46, "MINECART_HOPPER")
MINECART_MOB_SPAWNER = Entity(47, "MINECART_MOB_SPAWNER")
CREEPER = Entity(50, "CREEPER")
SKELETON = Entity(51, "SKELETON")
SPIDER = Entity(52, "SPIDER")
GIANT = Entity(53, "GIANT")
ZOMBIE = Entity(54, "ZOMBIE")
SLIME = Entity(55, "SLIME")
GHAST = Entity(56, "GHAST")
PIG_ZOMBIE = Entity(57, "PIG_ZOMBIE")
ENDERMAN = Entity(58, "ENDERMAN")
CAVE_SPIDER = Entity(59, "CAVE_SPIDER")
SILVERFISH = Entity(60, "SILVERFISH")
BLAZE = Entity(61, "BLAZE")
MAGMA_CUBE = Entity(62, "MAGMA_CUBE")
ENDER_DRAGON = Entity(63, "ENDER_DRAGON")
WITHER = Entity(64, "WITHER")
BAT = Entity(65, "BAT")
WITCH = Entity(66, "WITCH")
ENDERMITE = Entity(67, "ENDERMITE")
GUARDIAN = Entity(68, "GUARDIAN")
SHULKER = Entity(69, "SHULKER")
PIG = Entity(90, "PIG")
SHEEP = Entity(91, "SHEEP")
COW = Entity(92, "COW")
CHICKEN = Entity(93, "CHICKEN")
SQUID = Entity(94, "SQUID")
WOLF = Entity(95, "WOLF")
MUSHROOM_COW = Entity(96, "MUSHROOM_COW")
SNOWMAN = Entity(97, "SNOWMAN")
OCELOT = Entity(98, "OCELOT")
IRON_GOLEM = Entity(99, "IRON_GOLEM")
HORSE = Entity(100, "HORSE")
RABBIT = Entity(101, "RABBIT")
POLAR_BEAR = Entity(102, "POLAR_BEAR")
LLAMA = Entity(103, "LLAMA")
LLAMA_SPIT = Entity(104, "LLAMA_SPIT")
PARROT = Entity(105, "PARROT")
VILLAGER = Entity(120, "VILLAGER")
ENDER_CRYSTAL = Entity(200, "ENDER_CRYSTAL")