class Base(): # no need to explicitly derive object for it to work
    attr1 = 'I am in class Base'
    attr2 = 'halb halb'

    def virtual(self):
        print("Base's Method")

    def func(self):
        print("%s, %s" % (self.attr1, self.attr2))
        self.virtual()

class Derived(Base):
    attr1 = 'I am in class Derived'
    attr2 = 'blah blah'

    def __init__(self):
  # only way I've found so far is to edit the dict like this
        Base.__dict__['_Base_virtual'] = self.virtual

    def virtual(self):
        print("Derived's Method")

if __name__ == '__main__':
    d = Derived()
    d.func()
