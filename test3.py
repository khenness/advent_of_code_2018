from enum import Enum
from types import SimpleNamespace


class Intersection(Enum):
    LEFT = 1
    STRAIGHT = 2
    RIGHT = 3

    @classmethod
    def next(cls, val):
        try:
            return cls(val.value + 1)
        except ValueError:
            return cls.LEFT


class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'

    @classmethod
    def turn(cls, direction, next_turn):
        if direction is cls.UP and next_turn is Intersection.LEFT:
            return cls.LEFT
        if direction is cls.UP and next_turn is Intersection.STRAIGHT:
            return cls.UP
        if direction is cls.UP and next_turn is Intersection.RIGHT:
            return cls.RIGHT

        if direction is cls.DOWN and next_turn is Intersection.LEFT:
            return cls.RIGHT
        if direction is cls.DOWN and next_turn is Intersection.STRAIGHT:
            return cls.DOWN
        if direction is cls.DOWN and next_turn is Intersection.RIGHT:
            return cls.LEFT

        if direction is cls.LEFT and next_turn is Intersection.LEFT:
            return cls.DOWN
        if direction is cls.LEFT and next_turn is Intersection.STRAIGHT:
            return cls.LEFT
        if direction is cls.LEFT and next_turn is Intersection.RIGHT:
            return cls.UP

        if direction is cls.RIGHT and next_turn is Intersection.LEFT:
            return cls.UP
        if direction is cls.RIGHT and next_turn is Intersection.STRAIGHT:
            return cls.RIGHT
        if direction is cls.RIGHT and next_turn is Intersection.RIGHT:
            return cls.DOWN


Cart = SimpleNamespace


class Solver13:
    def __init__(self, lines):
        #lines = inp.split('\n')
        self.max_x = max((len(x) for x in lines))
        self.max_y = len(lines)
        self.matrix = [[' ' for _ in range(self.max_y)] for _ in range(self.max_x)]
        for y, line in enumerate(lines):
            for x, sym in enumerate(line):
                self.matrix[x][y] = sym

        self.parse_carts()

    def find_cart(self, x, y):
        carts = [cart for cart in self.carts if cart.x == x and cart.y == y]
        if carts:
            return carts[0]
        return None

    def print_map(self):
        def get_sym(x, y):
            cart = self.find_cart(x, y)
            if cart:
                return cart.direction.value
            return self.matrix[x][y]

        for y in range(self.max_y):
            print(''.join((get_sym(x, y) for x in range(self.max_x))))

    def parse_carts(self):
        self.carts = []

        def is_cart(x, y):
            return self.matrix[x][y] in ('^', 'v', '<', '>')

        def is_hor_road(x, y):
            return self.matrix[x][y] in ('-', '\\', '/', '+')

        def is_vert_road(x, y):
            return self.matrix[x][y] in ('|', '\\', '/', '+')

        def parse_cart(x, y):
            sym = self.matrix[x][y]
            if sym == '^':
                direction = Direction.UP
            elif sym == 'v':
                direction = Direction.DOWN
            elif sym == '<':
                direction = Direction.LEFT
            elif sym == '>':
                direction = Direction.RIGHT

            adj = []  # left, right, up, down
            adj.append(1 if x > 0 and is_hor_road(x - 1, y) else 0)
            adj.append(1 if x < self.max_x - 1 and is_hor_road(x + 1, y) else 0)
            adj.append(1 if y > 0 and is_vert_road(x, y - 1) else 0)
            adj.append(1 if y < self.max_y - 1 and is_vert_road(x, y + 1) else 0)

            setup = {
                (1, 1, 0, 0): '-',
                (0, 0, 1, 1): '|',
                (1, 0, 0, 1): '\\',
                (1, 0, 1, 0): '/',
                (0, 1, 0, 1): '/',
                (0, 1, 1, 0): '\\',
                (1, 1, 1, 1): '+',
            }
            replacement = setup.get(tuple(adj), ' ')

            return direction, replacement

        for x in range(self.max_x):
            for y in range(self.max_y):
                if not is_cart(x, y):
                    continue
                direction, replacement = parse_cart(x, y)
                self.matrix[x][y] = replacement
                cart = Cart(x=x, y=y, direction=direction, next_turn=Intersection.LEFT)
                self.carts.append(cart)

    def tick(self, remove_crashing=False):
        def move_cart(cart):
            x = cart.x
            y = cart.y
            direction = cart.direction
            next_turn = cart.next_turn

            if cart.direction == Direction.UP:
                y -= 1
                if self.matrix[x][y] == '\\':
                    direction = Direction.LEFT
                if self.matrix[x][y] == '/':
                    direction = Direction.RIGHT

            elif cart.direction == Direction.DOWN:
                y += 1
                if self.matrix[x][y] == '\\':
                    direction = Direction.RIGHT
                if self.matrix[x][y] == '/':
                    direction = Direction.LEFT

            elif cart.direction == Direction.LEFT:
                x -= 1
                if self.matrix[x][y] == '\\':
                    direction = Direction.UP
                if self.matrix[x][y] == '/':
                    direction = Direction.DOWN

            elif cart.direction == Direction.RIGHT:
                x += 1
                if self.matrix[x][y] == '\\':
                    direction = Direction.DOWN
                if self.matrix[x][y] == '/':
                    direction = Direction.UP

            if self.matrix[x][y] == '+':
                direction = Direction.turn(direction, next_turn)
                next_turn = Intersection.next(next_turn)

            return x, y, direction, next_turn

        def is_free(x, y):
            return not self.find_cart(x, y)

        removed = []
        to_process = list(sorted(self.carts, key=lambda x: (x.x, x.y)))
        for cart in to_process:
            if cart in removed:
                continue
            x, y, direction, next_turn = move_cart(cart)
            if not is_free(x, y):
                if not remove_crashing:
                    return True, (x, y)
                else:
                    removed += [cart, self.find_cart(x, y)]
                    self.carts.remove(cart)
                    self.carts.remove(self.find_cart(x, y))
                    continue

            cart.x = x
            cart.y = y
            cart.direction = direction
            cart.next_turn = next_turn

        return False, ()

    def solve(self, do_print=True):
        while True:
            if do_print:
                self.print_map()
                print('')
            crashed, coords = self.tick()
            if crashed:
                return ','.join(map(str, coords))

    def solve2(self, do_print=True):
        while True:
            if do_print:
                self.print_map()
                print('')

            self.tick(remove_crashing=True)

            if len(self.carts) == 1:
                cart = self.carts[0]
                return f'{cart.x},{cart.y}'


def read_file_into_list_v2(filepath):
    # Read file into list of lines
    # For bigger files look into using yield and doing chunking, even just for practice
    # If the file is line-based, the file object is already a lazy generator of lines:
    # https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    with open(filepath) as fp:
        line_list = []
        line = fp.readline()
        while line:
            #print_debug(line.strip())
            line_list.append(line.replace("\n", ""))
            line = fp.readline()

    return line_list

lines = read_file_into_list_v2("./problem_13_input.txt")
mySolver = Solver13(lines)
print(mySolver.solve())