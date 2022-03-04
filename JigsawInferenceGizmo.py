# JIG code from Stand-up Maths video "Why don't Jigsaw Puzzles have the correct number of pieces?"
from dataclasses import dataclass

# percentage we'll check in either direction
THRESHOLD = 0.1

# the extra badness per piece
PENALTY = 1.005


@dataclass
class ResultDetails:
    num_pieces: int = 0
    sides: tuple = (0, 0)
    ratio: float = 0
    piece_ratio: float = 0
    badness_score: float = 100


def low_factors(n):
    # all the factors which are the lower half of each factor pair
    return [i for i in range(1, int(n ** 0.5) + 1) if n % i == 0]


def switched_ratio(width, height):
    return max(width, height) / min(width, height)  # switched to be greater than 1


def jig_v1(width, height, num_pieces, debug=False):
    ratio = switched_ratio(width, height)

    print(f"\n{width} by {height} is picture ratio {round(ratio, 4)}\n")

    max_cap = int((1 + THRESHOLD) * num_pieces)
    min_cap = int((1 - THRESHOLD) * num_pieces)

    up_range = [i for i in range(num_pieces, max_cap + 1)]
    down_range = [i for i in range(min_cap, num_pieces)]  # do not want n included again
    down_range.reverse()

    # start at 100 which is silly high and then move down.
    up_best, down_best = ResultDetails(), ResultDetails()

    # I am using the run marker so I know if looking above or below n
    for run, this_range in enumerate((up_range, down_range)):
        best = ResultDetails()

        if run == 0:
            print(f"Looking for >= {num_pieces} solutions:\n")
        else:
            print("\nJust out of interest, here are smaller options:\n")

        for pieces in this_range:
            best_ratio = 0
            best_sides = (0, 0)
            for side1 in low_factors(pieces):
                side2 = int(pieces / side1)  # must be a whole number anyway
                this_ratio = side2 / side1

                if best_ratio == 0:
                    best_ratio = this_ratio
                    best_sides = (side1, side2)
                else:
                    if abs(this_ratio / ratio - 1) < abs(best_ratio / ratio - 1):
                        best_ratio = this_ratio
                        best_sides = (side1, side2)

            is_better = False
            if best.num_pieces == 0:
                is_better = True
            else:
                if abs(best_ratio / ratio - 1) < abs(best.ratio / ratio - 1):
                    is_better = True

            if is_better:
                piece_ratio = (max(ratio, best_ratio) / min(ratio, best_ratio))
                badness_score = (PENALTY ** (abs(pieces - num_pieces))) * piece_ratio

                best = ResultDetails(pieces, best_sides, best_ratio, piece_ratio, badness_score)

                if run == 0:
                    if best.badness_score < up_best.badness_score:
                        up_best = best
                else:
                    if best.badness_score < down_best.badness_score:
                        down_best = best

                print(f"{best.num_pieces} pieces in {best.sides} (grid ratio {round(best.ratio, 4)}) "
                      f"needs piece ratio {round(best.piece_ratio, 4)}")
                if debug:
                    print(f"[badness = {round(best.badness_score, 5)}]")

        print(f"for {num_pieces} the best is {best.num_pieces} pieces with size {best.sides}")

    print(f"\nIf I had to guess: I think it's {up_best.num_pieces} pieces.")

    if down_best.badness_score < up_best.badness_score:
        print(f"\nBUT, fun fact, {down_best.num_pieces} would be even better.")

    print()
    return 'DONE'


# I duplicated jig_v0 to make is easier to show in the video
def jig_v0(width, height, num_pieces, debug=False):
    ratio = switched_ratio(width, height)

    print(f"\n{width} by {height} is picture ratio {round(ratio, 4)}\n")

    max_cap = int((1 + THRESHOLD) * num_pieces)
    min_cap = int((1 - THRESHOLD) * num_pieces)

    up_range = [i for i in range(num_pieces, max_cap + 1)]
    down_range = [i for i in range(min_cap, num_pieces)]  # do not want n included again
    down_range.reverse()

    # start at 100 which is silly high and then move down.
    up_best, down_best = ResultDetails(), ResultDetails()

    # I am using the run marker so I know if looking above or below n
    run = 0

    for this_range in (up_range, down_range):
        best = ResultDetails()

        if run == 0:
            print(f"Looking for >= {num_pieces} solutions:\n")
        else:
            print("\nJust out of interest, here are smaller options:\n")

        for pieces in this_range:
            best_ratio = 0
            best_sides = (0, 0)
            for side1 in low_factors(pieces):
                side2 = int(pieces / side1)  # must be a whole number anyway
                this_ratio = side2 / side1
                if best_ratio == 0:
                    best_ratio = this_ratio
                    best_sides = (side1, side2)
                else:
                    if abs(this_ratio / ratio - 1) < abs(best_ratio / ratio - 1):
                        best_ratio = this_ratio
                        best_sides = (side1, side2)

            is_better = False
            if best.num_pieces == 0:
                is_better = True
            else:
                if abs(best_ratio / ratio - 1) < abs(best.ratio / ratio - 1):
                    is_better = True
            if is_better:
                piece_ratio = (max(ratio, best_ratio) / min(ratio, best_ratio))
                badness_score = (PENALTY ** (abs(pieces - num_pieces))) * piece_ratio

                best = ResultDetails(pieces, best_sides, best_ratio, piece_ratio, badness_score)

                if run == 0:
                    if best.badness_score < up_best.badness_score:
                        up_best = best
                else:
                    if best.badness_score < down_best.badness_score:
                        down_best = best
                print(f"{best.num_pieces} pieces in {best.sides} (grid ratio {round(best.ratio, 4)}) "
                      f"needs piece ratio {round(best.piece_ratio, 4)}")
                if debug:
                    print(f"[badness = {round(best.badness_score, 5)}]")

        run += 1

    print()
    return 'DONE'


def jig(width, height, num_pieces, debug=False, version=1):
    if version == 0:
        return jig_v0(width, height, num_pieces, debug)
    elif version == 1:
        return jig_v1(width, height, num_pieces, debug)
    else:
        return 0


if __name__ == '__main__':
    print(f'Example: {jig(33, 22.8, 1000, debug=True, version=1) = }')
