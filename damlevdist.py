# Damerau-Levenshtein edit distance implementation
# Based on pseudocode from Wikipedia: https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance

def damerau_levenshtein_distance(a, b):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    len_a = len(a)
    len_b = len(b)
    INF = len_a + len_b

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in range(len_b + 2)]]
    matrix += [[INF] + list(range(len_b + 1))]
    matrix += [[INF, m] + [0] * len_b for m in range(1, len_a + 1)]

    # Holds last row each element was encountered: `DA` in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in range(1, len_a + 1):
        # Current character in `a`
        ch_a = a[row-1]

        # Column of last match on this row: `DB` in pseudocode
        last_match_col = 0

        for col in range(1, len_b + 1):
            # Current character in `b`
            ch_b = b[col-1]

            # Last row with matching character; `i1` in pseudocode
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion

                # Transposition
                matrix[last_matching_row][last_match_col]
                    + (row - last_matching_row - 1) + 1
                    + (col - last_match_col - 1))

            # If there was a match, update last_match_col
            # Doing this here lets me be rid of the `j1` variable from the original pseudocode
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return edit distance and percent
    max_dist = min(len_a, len_b) + abs(len_a - len_b)
    return matrix[-1][-1], (max_dist - matrix[-1][-1]) / max_dist

if __name__ == "__main__":
    print(damerau_levenshtein_distance('kossuth lajos', 'Kosuth Lajos'.lower()))
    print(damerau_levenshtein_distance('kossuth lajos', 'Kosuth Lajos'))
    print(damerau_levenshtein_distance('ÁrvíztűrőtükörfúrógÉp', 'árvíztűrőtükörfúrógép'))
    print(damerau_levenshtein_distance('ÁrvíztűrőtükörfúrógÉp'.lower(), 'árvíztűrőtükörfúrógép'))
