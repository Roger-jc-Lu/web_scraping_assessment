from collections import deque


def mask_repetitive_char(s, k):
    res = ""
    window = deque()
    seen = set()
    for char in s:
        if char in seen:
            res += '-'
        else:
            res += char
            seen.add(char)
        
        window.append(char)
        
        if len(window) > k:
            least_recent = window.popleft()
            if least_recent not in window:
                seen.remove(least_recent)

    return res

if __name__ == "__main__":
    assert mask_repetitive_char('abcdefaxc', 10) == "abcdef-x-"
    assert mask_repetitive_char('abcdefaxcqwertba', 10) == "abcdef-x-qw-rtb-"


