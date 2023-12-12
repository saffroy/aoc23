import re

TEST_DATA = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

TEST_RESULT = 21

def perms_rec(prefix, pattern, regex):
    if not pattern:
        return 1 if regex.match(prefix) else 0
    else:
        c, tail = pattern[0], pattern[1:]
        if c != '?':
            return perms_rec(prefix + c, tail, regex)
        else:
            return perms_rec(prefix + '.', tail, regex) \
                + perms_rec(prefix + '#', tail, regex)

def group_sizes_re(group_sizes):
    s = r'^\.*' \
        + r'\.+'.join(['#' * g for g in group_sizes]) \
        + r'\.*$'
    return re.compile(s)

def perms(pattern, group_sizes):
    regex = group_sizes_re(group_sizes)
    return perms_rec('', pattern, regex)

def parse(lines):
    # maybe recursion, on group sizes or/and strings
    # idea:
    # - undamaged left record is a bitstring
    # - can generate "all" possible strings by filling bits,
    #   then check if a string is a match
    # - group sizes ~= regex, like:
    #   2,1,3 ~= '^_*##_+#_+###_*$' (where _ replaces . for readability)
    # - better weed out failing prefixes early, but how?
    #   if count of _complete_ groups in prefix is not a prefix of group size list,
    #   then give up on this prefix
    # - at first, can try "brute force" i.e. without weeding out
    #   => IT WORKS for part 1, completes in 3 secs

    sum_perms = 0
    for line in lines:
        pattern, g_sizes = line.split()
        group_sizes = list(map(int, g_sizes.split(',')))
        sum_perms += perms(pattern, group_sizes)
    return sum_perms

def test():
    lines = TEST_DATA.splitlines()
    result = parse(lines)
    assert result == TEST_RESULT, (result, TEST_RESULT)

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

def bench():
    import timeit
    t = timeit.timeit('main()', number=1, globals=globals())
    print('time: {:3.2f} ms/call'.format(t*1000))

if __name__ == '__main__':
    main()
