
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
    while i < len(pattern):
        # compress patterns into like consecutive groups:
        #    a*a+a* -> a+
        # keep a minimum length for each pattern group:
        #    a* -> 0, a+ -> 1, a -> 1, aaaa -> 4, a+a+a+a* -> 3
        current_character = pattern[i]
        next_character = None
        if i+1 < len(pattern):
            next_character = pattern[i+1]

        if groups and current_character == groups[-1]['pattern']:
            new_group = groups[-1]
        else:
            new_group = {
                'pattern': current_character,
                'min': 0,
                'max': len(string)
            }
            groups.append(new_group)

        i += 1
        if not next_character or next_character not in '*+':
            new_group['min'] = new_group['max'] = 1
        elif next_character:
            if next_character in '*+':
                # include glob or plus into the current group
                i += 1
            if next_character != '*':
                # only globs can be 0 length
                new_group['min'] += 1
                sum_min_lens += 1
    sindex = 0
    gindex = 0
        
    for group in reversed(groups):
        # weak maximums for each group
        if group['max'] != 1:
            group['max'] = len(string) - sum_min_lens + group['min']

    gindex, sindex = 0, 0
    mem = {}
    q = []
    gmatch = False
    raise Exception(groups)
    while sindex < len(string):
        g = groups[gindex]
        if g['min'] == g['max'] == 1 and g['pattern'] in ('.', string[sindex]):
            gindex += 1
            sindex += 1
            gmatch = False
        elif g['pattern'] in ('.', string[sindex]):
            if gmatch or g['min'] == 0:
                q.append([gindex+1,sindex])
            sindex += 1
            gmatch = True
        elif g['min'] == 0:
            gindex += 1
            gmatch = False
        elif gmatch:
            gindex+=1
            gmatch = False
        elif q:
            gindex, sindex = q.pop(-1)
        else:
            return False
    
    return all(g['min'] == 0 for g in groups[gindex:])
