import functools

test_data = '''Time:      7  15   30
Distance:  9  40  200
'''

test_result = 4*8*9

def ways(time, dist):
    # return how many ways can beat record of dist for given race time
    count = 0
    for tpress in range(time):
        speed = tpress
        duration = time - tpress
        dreached = duration * speed
        if dreached > dist:
            count += 1
    return count

def parse(lines):
    for line in lines:
        l = line.split()
        if l[0] == 'Time:':
            times = list(map(int, l[1:]))
            continue
        if l[0] == 'Distance:':
            dist = list(map(int, l[1:]))
            continue
    assert len(times) == len(dist)
    prod_ways = functools.reduce(lambda x, y: x*y, [
        ways(times[i], dist[i]) for i in range(len(times))
    ])
    return prod_ways

def test():
    lines = test_data.splitlines()
    result = parse(lines)
    assert result == test_result

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

def main2():
    with open('input2', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

if __name__ == '__main__':
    main()
