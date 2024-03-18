
def work(string, pattern, los, his, lop, hip, minstr, nextchar, mem):
    key = f'{los}|{his}|{lop}|{hip}|{minstr}'
    if key in mem:
        return mem[key]

    if ((lop==hip and pattern[lop] == '*') or (hip-lop == his-los and pattern[lop:hip+1] == string[los:his+1] )):
        mem[key] = True
        return True

    if his-los+1 < minstr or hip-lop+1 == 0:
        mem[key] = False
        return False

    while los <= his and lop <= hip and string[los] == pattern[lop]:
        los += 1
        lop += 1
        minstr -= 1

    while los <= his and lop <= hip and string[his] == pattern[hip]:
        his -= 1
        hip -= 1
        minstr -= 1

    if lop == hip and p[lop] == '*':
        mem[key] = True
        return True
    
    if lop > hip:
        mem[key] = minstr == 0 and los > his
        return mem[key]

    if his-los+1 < minstr or hip-lop+1 == 0:
        mem[key] = False
        return False
 
    if p[lop:lop+1] == "*":
        for i in range(his-los):
            nc = nextchar[lop]
            if nc == -1 or string[his-i] == pattern[nc]:
                if work(string, pattern, his-i, his, lop+1, hip, minstr, nextchar,mem):
                    mem[key] = True
                    return True
                
        mem[key] = work(string, pattern, los, his, lop+1, hip, minstr, nextchar,mem)
        return mem[key]

    elif p[lop:lop+1] == "+":
        for i in range(1, his-los):
            nc = nextchar[lop]
            if nc != -1 or s[his-i] == p[nc]:
                if work(string, pattern, his-i, his, lop+1, hip, minstr, nextchar, mem):
                    mem[key] = True
                    return True
        mem[key] = work(string, pattern, los, his, lop+1, hip, minstr, nextchar,mem)
        return mem[key]

    mem[key] = string == pattern
    return mem[key]


def match(pattern, string):
    minstr = 0
    np = ""
    nextchar = [0] * len(pattern)
    j = 0
    for i, c in enumerate(pattern):
        if c != '*':
            minstr += 1
        if i > 0 and pattern[i] == pattern[i-1] and pattern[i] == '*':
            continue
        np += pattern[i]
    
    pattern = np
    for i, _ in enumerate(p):
        if j < i and j != -1:
            j = i
        while j != -1 and j < len(pattern) and pattern[j] == '*':
            j += 1
        if j == len(pattern):
            j = -1
        nextchar[i] = j
    return work(string, np, 0, len(string)-1, 0, len(pattern)-1, minstr, nextchar, {})


def match(pattern, string):
    return False
