import ujson
import os

class Config():
    def __init__(self, filename="config.json"):
        self.filename = filename
        try:
            os.stat(filename)
        except OSError:
            f = open(filename, "w")
            f.write("{}")
            f.flush()
            f.close()

    def __del__(self):
        pass

    def read(self,name):
        c = ""
        with open(self.filename, "r") as f:
            c = ujson.load(f)
            f.close()
        return c[name]
    
    def write(self,name,value):
        c = ""

        with open(self.filename, "r") as f:
            c = ujson.load(f)
            f.close()

        with open(self.filename, "w") as f:
            c[name] = value
            ujson.dump(c, f)
            f.flush()
            f.close()

#Example usage:
def main():
    filename = input("Enter filename: ")
    conf = Config(filename)
    conf.write("A", 123)
    conf.write("B", 0.123)
    conf.write("C", 'Hello')
    conf.write("D", True)
    conf.write("E", [1,2,3,4,5])
    conf.write("F", {'a':1, 'b':2, 'c':3})
    conf.write("G", (1,2,3,4,5))
    conf.write("H", None)
    a = conf.read("A")
    print('A={0}'.format(a))
    with open(filename, "r") as f:
        c = ujson.load(f)
        f.close()
        os.remove(filename)
    print(c)
    
if __name__ == "__main__":
    main()