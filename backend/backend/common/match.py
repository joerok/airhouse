class Pattern:
    def __init__(self, pattern):
        self.char, self.op = pattern[0:1], pattern[1:2]
        if self.op not in '+*': 
            self.op = None

def match(pattern, string):
    pindex, sindex = 0, 0
    bt = []  # a q that contains at most one entry per pindex
    can_match_zero = True
    while pindex < len(pattern) or sindex < len(string):
        clause = Pattern(pattern[pindex:pindex+2])
        matched = sindex < len(string) and clause.char in ('.', string[sindex])

        if pindex != len(pattern) and sindex == len(string):
            # end of the string, but more patterns, are they all *?
            while Pattern(pattern[pindex:pindex+2]).op == '*':
                pindex += 2
            if pindex == len(pattern):
                return True
        elif clause.op is None and matched:
            # single char match
            pindex, sindex = pindex + 1, sindex + 1
        elif clause.op == '*' and can_match_zero:
            # non-greedy, try to not match * at first, save matched state for later
            bt.append((pindex, sindex))
            pindex += 2
            matched = True
        elif matched:
            # op = +/*: match 1, and move on to the next clause and char
            bt.append((pindex, sindex + 1))
            pindex, sindex = pindex + 2, sindex + 1

        if not matched:
            if not len(bt):
                return False
            pindex, sindex = bt.pop(-1)

        # coming from the q, the pattern has already attempted to match 0
        can_match_zero = matched 
    return True
