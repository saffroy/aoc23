TEST_DATA = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

TEST_RESULT = 2

def extrapolate(nums):
    diffs = [t1 - t0 for (t0, t1) in zip(nums, nums[1:])]
    if all(n == 0 for n in diffs):
        extra = nums[-1]
    else:
        extra = nums[-1] + extrapolate(diffs)
    return extra

def parse(lines):
    sum_ext = 0
    for line in lines:
        nums = list(map(int, line.split()))
        nums = list(reversed(nums)) # part 2
        extra = extrapolate(nums)
        sum_ext += extra
    return sum_ext

def test():
    lines = TEST_DATA.splitlines()
    result = parse(lines)
    assert result == TEST_RESULT

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

if __name__ == '__main__':
    main()
