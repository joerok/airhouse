
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
    seen = set()
    log = [(pattern, string)]
    while sindex < len(string):
        character, operator, next_index = next_pattern(pattern, pindex)
        is_match = character in ('.', string[sindex])
        requires_backtrack = bool(operator)
        log.append({
            'character': character, 
            'operator': operator, 
            'next_index': next_index,
            'sindex': sindex,
            'pindex': pindex,
            'is_match': is_match,
            'requires_backtrack': requires_backtrack,
            'pmatch': pmatch,
            'queue': q})
        if is_match:
            if requires_backtrack and (next_index, sindex, pmatch) not in seen:
                q.append([next_index, sindex, pmatch])
                seen.add((next_index, sindex, pmatch))
            sindex += 1
            if not operator:
                pindex = next_index
            pmatch = operator == '+'
            if sindex == len(string):
                failed = False
                while pindex and not failed:
                    (_,op,pindex) = next_pattern(pattern, pindex)
                    failed = pindex and op != '*'
                if failed:
                    log.append('failed on tail')
                    if q:
                        pindex, sindex, pmatch = q.pop(-1)
                        continue
                    return False
                return True
        elif (pmatch and requires_backtrack) or operator == '*':
            pmatch = False
            pindex = next_index
        elif q:
            pindex, sindex, pmatch = q.pop(-1)
        else:
            log.append('failed in loop')
            raise Exception(log)
            return False
    raise Exception(log)
    return True
