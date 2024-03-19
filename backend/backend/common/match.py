
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
        if i + 1 == len(pattern): return (pattern[i], None, None)
        if pattern[i+1] not in '+*': return (pattern[i], None, i+1)
        if i + 2 == len(pattern): return (pattern[i], pattern[i+1], None)
        return pattern[i], pattern[i+1], i+2
    pindex, sindex = 0, 0
    mem = {}
    q = []
    pmatch = False
    seen = set()
    
    while sindex < len(string) or q:
        if sindex >= len(string):
            pindex, sindex, pmatch = q.pop(-1)
            continue
        character, operator, next_index = next_pattern(pattern, pindex)
        is_match = character in ('.', string[sindex])
        requires_backtrack = bool(operator)

        if is_match:
            if operator == '*' and (next_index, sindex, pmatch) not in seen and next_index is not None:
                q.append([next_index, sindex, pmatch])
                seen.add((next_index, sindex, pmatch))
            elif operator == '+' and (next_index, sindex+1, pmatch) not in seen and next_index is not None:
                q.append([next_index, sindex+1, pmatch])
                seen.add((next_index, sindex+1, pmatch))
            sindex += 1
            if sindex == len(string):
                if next_index is None:
                    return True
                failed = False
                while pindex is not None and not failed:
                    (_,op,pindex) = next_pattern(pattern, pindex)
                    failed = pindex is not None and op in (None, '+')
                if failed:
                    if q:
                        pindex, sindex, pmatch = q.pop(-1)
                        continue
                    else:
                        return False            
            if not operator:
                pindex = next_index
            pmatch = operator == '+'
        elif (pmatch and requires_backtrack) or operator == '*':
            pmatch = False
            pindex = next_index
        elif q:
            pindex, sindex, pmatch = q.pop(-1)
        else:
            return False
    while pindex is not None:
        (s,op,pindex) = next_pattern(pattern, pindex)
        if op != '*':
            return False
    return True
