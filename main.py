from collections import deque
from math import log
from PIL import Image, ImageDraw

from colour import Color
red = Color("red")
yellow = Color("yellow")
blue = Color("blue")
green = Color("green")


# 6,2 => true => 8,2 also true
# 7,2 => false => 9,2 also false

# i,j => xTruth => i+j,j => xTruth ; i+j,i => xTruth

class DivisiblesTable(object):
    '''
    Computes a prime and divisible table without division
    True values are integer pairs where the first divides into the second
    But for some reason anything like 2/2 is bad
    '''

    def __init__(self, initial_truth=[(1, 2)], size=100):
        self.size = size
        self.divisibles = {} # (2, 1) => true #is divisible
        self._que = deque()
        self.initial_truth = initial_truth
        for i, j in initial_truth:
            self.que(i, j, 1)

    def que(self, i, j, truthValue):
        '''Que up a truth update'''
        #if i == j:
        #    return
        #assert i != j, "Non-identical constraint voilated."
        if i > self.size or j > self.size:
            return
        if (i, j) in self.divisibles:
            return
        self._que.append((i, j, truthValue))

    def run(self):
        while self._que:
            i, j, truthValue = self._que.popleft()
            self.divisibles[(i, j)] = truthValue
            #mirror to other side
            self.divisibles[(j, i)] = truthValue
            self._next(i, j, truthValue + 1)

    def _next(self, i, j, truthValue):
        #self.que(i, i, True)
        #self.que(j, j, True)
        #self.que(i, j+i, truthValue)
        #self.que(j, j+i, truthValue)
        self.que(i+j, j, truthValue)
        self.que(i+j, i, truthValue)

    def draw_values(self):
        # some color constants for PIL
        width = self.size
        height = self.size

        rgb = lambda x: tuple(int(c*255) for c in x.get_rgb())

        # create empty PIL image and draw objects to draw on
        # PIL draws in memory only, but the image can be saved
        image = Image.new("RGB", (width+1, height+1), rgb(Color("white")))
        draw = ImageDraw.Draw(image)

        number_of_colors = self.size/2 #int(log(self.size, 2))
        colors = map(rgb, red.range_to(blue, number_of_colors))
        #print("colors:", colors)

        truthCount = 0

        # draw truth table
        abs_color = rgb(Color("brown")) #(0, 0, 0)
        for (x, y), truthValue in self.divisibles.items():
            # PIL (to memory for saving to file)
            if truthValue:
                truthCount += 1
                if 1 in (x, y) or x + 1 == y or y + 1 == x:
                    color = abs_color
                else:
                    color = colors[truthValue-2]
                draw.point((x, y), color)

        index_str = "_".join([str(i)+"-"+str(j) for i, j in self.initial_truth])

        filename = index_str + "_" + str(self.size) + ".png"
        image.save(filename)
        print("pixel count:", truthCount)
        return image

if __name__ == '__main__':
    table = DivisiblesTable([(1, 1)], size=1000)
    table.run()
    table.draw_values()
