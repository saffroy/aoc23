# AOC'23 day 1 part 1

import re

def main():
    with open('input') as f:
        lines = f.readlines()

    single = re.compile('^[^0-9]*([0-9])[^0-9]*$')
    double = re.compile('^[^0-9]*([0-9]).*([0-9])[^0-9]*$')

    sum = 0
    junk = []
    for line in lines:
        m = single.match(line)
        if m:
            (d,) = m.groups()
            sum += int(d) * 10 + int(d)
            continue
        m = double.match(line)
        if m:
            (d1,d2) = m.groups()
            sum += int(d1) * 10 + int(d2)
            continue
        junk.append(line)

    print('junk lines:', len(junk))
    print('sum:', sum)

    assert len(junk) == 0

if __name__ == '__main__':
    main()
