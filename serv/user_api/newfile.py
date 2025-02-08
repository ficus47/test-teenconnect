import pickle

class User:
    def __init__(self, pseudo=None, acces=None, age=None, desc=None, img=None, birth=None, premium_ex_date=None):
        self.pseudo = pseudo
        self.acces = acces
        self.age = age
        self.desc = desc
        self.img = img if img is not None else 'delfault'
        self.birth = birth
        self.admin_lvl = 0
        self.log = []
        self.warning_lvl = 0
        self.ban = False
        self.sparks = 0
        self.premium_ex_date = premium_ex_date

    def save(self, dir="/"):
        pickle.dump(open(dir+self.pseudo), self)
        return 0
    def load(self, dir="/", pseudo=""):
        self = pickle.load(open(dir+pseudo))
        return self
        
    def modify_desc(self, desc):
        self.desc = desc
        
    def modify_img(self, img):
        self.img = img
    
    def modify_acces(self, acces):
        self.acces = acces
    
    def modify_birth(self, birth):
        self.birth = birth
        
    def set_admin_lvl(self, new_lvl):
        self.admin_lvl = new_lvl
        
    def log(self, **kwarg):
         self.log.append(kwarg)
      
    def warn(self, lvl=1):
        self.warning_lvl +=  lvl
        self.warn_update()
    
    def ban(self):
        self.warn(lvl=6)
    
    def warn_update(self):
        if self.warn_lvl >= 5:
            self.ban = True