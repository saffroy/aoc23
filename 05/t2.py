import multiprocessing
import re

test_data = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

test_result = 46

class Mapping:
    def __init__(self):
        self._ranges = []

    def add_range(self, dest, src, length):
        self._ranges.append((dest, src, length))

    def map_to(self, x):
        for (dest, src, length) in self._ranges:
            diff = x - src
            if diff >= 0 and diff < length:
                return dest + diff
        return x

def seed_to_loc(mappings, map_names, seed):
    x = seed
    for name in map_names:
        x = mappings[name].map_to(x)
    return x

def closest_one_range(mappings, map_names, seed_range):
    return min(seed_to_loc(mappings, map_names, seed)
               for seed in seed_range)

def parse(lines):
    seeds = None
    cur_map = None
    mappings = dict()
    map_names = []

    for line in lines:
        if re.match(r'^seeds:', line):
            pairs = list(map(int, line.split(':')[1].split()))
            seeds = []
            while pairs:
                [base, length], pairs = pairs[:2], pairs[2:]
                seeds.append(range(base, base+length))
            print(len(seeds), 'seed ranges')
            continue

        m = re.match(r'([^\s]+) map:', line)
        if m:
            cur_map = m.group(1)
            mappings[cur_map] = Mapping()
            map_names.append(cur_map)
            continue

        m = re.match(r'^(\d+)\s+(\d+)\s+(\d+)', line)
        if m:
            (dest, src, length) = list(map(int, m.groups()))
            mappings[cur_map].add_range(dest, src, length)
            continue

    with multiprocessing.Pool() as pool:
        res = []
        for r in seeds:
            res.append(pool.apply_async(closest_one_range, (mappings, map_names, r)))
        for r in res:
            r.wait()
            print('#')
        closest = min(r.get() for r in res)

    return closest

def test():
    lines = test_data.splitlines()
    result = parse(lines)
    assert result == test_result

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

if __name__ == '__main__':
    main()
