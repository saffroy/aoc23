import functools

TEST_DATA = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

TEST_RESULT = 525152

@functools.lru_cache(maxsize=1000)
def perms_rec(in_group, cur_group_size, pattern, group_sizes):
    if not pattern:
        if in_group:
            # completing last group
            matched = group_sizes == (cur_group_size,)
        else:
            matched = group_sizes == ()
        return 1 if matched else 0
    elif not group_sizes:
        assert not in_group, (in_group, cur_group_size, pattern, group_sizes)
        return 0 if '#' in pattern else 1
    else:
        c = pattern[0]
        match c:
            case '.':
                if in_group:
                    # end of current group
                    if cur_group_size != group_sizes[0]:
                        return 0
                    else:
                        return perms_rec(False, 0, pattern[1:], group_sizes[1:])
                else:
                    return perms_rec(False, 0, pattern[1:], group_sizes)
            case '#':
                if in_group:
                    # adding one to current group
                    if cur_group_size+1 > group_sizes[0]:
                        return 0
                    else:
                        return perms_rec(True, cur_group_size+1, pattern[1:], group_sizes)
                else:
                    # beginning of new group
                    return perms_rec(True, 1, pattern[1:], group_sizes)
            case '?':
                tail = pattern[1:]
                return perms_rec(in_group, cur_group_size, '.'+tail, group_sizes) \
                    + perms_rec(in_group, cur_group_size, '#'+tail, group_sizes)
            case _: assert False, c

def perms(pattern, group_sizes):
    # group_sizes made into a tuple so it can be hashed by lru_cache
    return perms_rec(False, 0, pattern, tuple(group_sizes))

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
    #   => TOO SLOW for part 2
    # - so then, above optimizations + memoization \o/

    sum_perms = 0
    for line in lines:
        pattern, g_sizes = line.split()
        group_sizes = list(map(int, g_sizes.split(',')))

        # "unfold" => N-bit problem becomes (N*5+4)-bit problem :cry:
        pattern = '?'.join([pattern] * 5)
        group_sizes = group_sizes * 5

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
