
def work(string, groups, sindex, gindex, mem):
    key = (sindex, gindex)

    if key in mem:
        return mem[key]


    if len(groups) == gindex and len(string) == sindex:
        # end of the string and end of the pattern
        mem[key] = True
        return True
    elif sindex >= len(string):
        # at the end of the string, are the remaining groups globs(*)?
        mem[key] = sum(g['min'] for g in groups[gindex:]) == 0
        return mem[key]
    elif gindex >= len(groups):
        mem[key] = False
        return False
    g = groups[gindex]
    if g['min'] > 0 and g['pattern'] not in ('.', string[sindex]):
        # current pattern is a non glob (single character or + pattern)
        mem[key] = False
        return False

    window = 0
    while window < g['max'] and sindex + window < len(string) and g['pattern'] in ('.', string[sindex+window]):
        # find the maximum sized window
        window += 1

    for buf in range(window, g['min']-1, -1):
        # start with the maximum sized window and attempt to apply the remaining patterns until we have a match
        res = work(string, groups, sindex+buf, gindex+1, mem)
        if res:
            mem[key] = True
            return True
    # after trying all possible window sizes there are no remaining matches available
    mem[key] = False
    return False

def match(pattern, string):
    """
        * `.` - wildcard; any character
        * `*` - 0 or more of the preceding character
        * `+` - 1 or more of the preceding character
        assumptions:    
        * '*' and '+' cannot follow '*' or '+'
        * a string cannot begin with '*' or '+'
        * there are no escape characters ("\*" matching "*")

    """
    # groups are .+, C+, .*, C*
    # groups with + have a minimum length of 1 with calculated maximal length
    # groups with * have a minimum length of 0 with a calculated maximal length
    # groups with neither have a minumum and maximum length of 1    
    groups = []
    i = 0
    sum_min_lens = 0
    def next_pattern(pattern, i):
        if i >= len(pattern): return None, None, None
        if i + 1 == len(pattern): return (pattern[i], None, i+1)
        if pattern[i+1] not in '+*': return (pattern[i], None, i+1)
        return pattern[i], pattern[i+1], i+2
    pindex, sindex = 0, 0
    mem = {}
    q = []
    pmatch = False
    seen = {}
    while sindex < len(string):
        character, operator, next_index = next_pattern(pattern, pindex)
        is_match = character in ('.', string[sindex])
        requires_backtrack = bool(operator)

        if is_match:
            if requires_backtrack and (next_index, sindex, pmatch) not in seen:
                q.append([next_index, sindex, pmatch])
                seen.add((next_index, sindex, pmatch))
            sindex += 1
            pmatch = operator == '+'
        elif (pmatch and requires_backtrack) or operator == '*':
            pmatch = False
            pindex = next_index
        elif q:
            pindex, sindex, pmatch = q.pop(-1)
        else:
            return False
    while pindex:
        (_,op,pindex) = next_pattern(pattern, pindex)
        if pindex and op != '*':
            return False
    return True
