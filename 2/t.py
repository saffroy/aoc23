# AOC'23 day 2 part 1+2

from dataclasses import dataclass, field

@dataclass
class Count:
    red: int = 0
    green: int = 0
    blue: int = 0

@dataclass
class Game:
    gid: int
    draws: list[Count] = field(default_factory=list)

    def draw(self, d: Count):
        self.draws.append(d)

test_input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''

test_filter = Count(red=12, green=13, blue=14)

test_result = 8

test_sumpow = 2286

def parse(lines):
    games = []
    for line in lines:
        head, tail = line.split(':')
        _, gid = head.split(' ')
        draws = tail.split(';')

        game = Game(int(gid))
        games.append(game)

        for draw in draws:
            counts = draw.split(',')
            d = dict()

            for count in counts:
                n, col = count.strip().split(' ')
                d[col] = int(n)

            game.draw(Count(**d))
    return games

def is_possible(count, game):
    max_balls = max((d.red + d.green + d.blue) for d in game.draws)
    max_r = max(d.red for d in game.draws)
    max_g = max(d.green for d in game.draws)
    max_b = max(d.blue for d in game.draws)
    return (count.red >= max_r
            and count.green >= max_g
            and count.blue >= max_b
            and count.red + count.green + count.blue >= max_balls)

def sum_possible(count, games):
    return sum(g.gid for g in games if is_possible(count, g))

def min_power(game):
    max_r = max(d.red for d in game.draws)
    max_g = max(d.green for d in game.draws)
    max_b = max(d.blue for d in game.draws)
    return max_r * max_g * max_b

def sum_pow(games):
    return sum(min_power(game) for game in games)

def test():
    games = parse(test_input.splitlines())
    assert test_result == sum_possible(test_filter, games)
    assert test_sumpow == sum_pow(games)

def main():
    with open('input', encoding='ascii') as f:
        lines = f.readlines()
    games = parse(lines)

    # part 1
    print(sum_possible(test_filter, games))
    # part 2
    print(sum_pow(games))

if __name__ == '__main__':
    main()
