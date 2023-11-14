import errno

# This isn't quite how I'd like it (the SpriteModel object is thrown around a bit) but it'll do for now

class jtrukSpriteModel():
    def __init__(self, iSlot, filepath):
        self.iSlot = iSlot
        self.filepath = filepath
        self.isSpriteLoaded = False

    # returns w, h, data
    #def getData(self, gfx):
    #    return gfx.load_sprite("./goal.png", source=(0,0,16,16))
    
    def load(self, gfx):
        try:
            for _ in range(2):  # Once for each 2040?
                if not gfx.load_sprite(self.filepath, self.iSlot):
                    raise Exception("Failed to load sprite")
                gfx.update()
            self.isSpriteLoaded = True

        except OSError as ioe:
            if ioe.errno == errno.ENOENT:
                print("Sprite file not found")
            else:
                print("Unexpected error loading sprite:", ioe)
        
        return self.isSpriteLoaded

    def isLoaded(self):
        return self.isSpriteLoaded

    def getSlot(self):
        return self.iSlot

class jtrukSprites():
    def __init__(self, maxSprites):
        self.maxSprites = maxSprites
        self.sprites = [None] * self.maxSprites

    # returns the index - or None if none free
    def add(self, gfx, spr, x, y, blend=1, scale=1):
        for i in range(self.maxSprites):
            if self.sprites[i] is None:
                self.set(gfx, i, spr, x, y, blend, scale)
                return i
        return None

    def set(self, gfx, iSprite, spr, x, y, blend=1, scale=1):
        self.sprites[iSprite] = True
        self._spriteUpdate(gfx, iSprite, spr.getSlot(), x, y, blend, scale)
    
    def _spriteUpdate(self, gfx, iSprite, iSlot, x, y, blend, scale):
        gfx.display_sprite(iSprite, iSlot, x, y, blend, scale)

    def remove(self, gfx, iSprite):
        gfx.clear_sprite(iSprite)
        self.sprites[iSprite] = None

    def removeAll(self, gfx):
        for i in range(self.maxSprites):
            if self.sprites[i] is not None:
                self.remove(gfx, i)     
