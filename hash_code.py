from tqdm import tqdm


files = [
    'a_example',
    'b_should_be_easy',
    'c_no_hurry',
    'd_metropolis',
    'e_high_bonus',
]

# ride: x0 y0 x1 y1 es lf score id
# vehicle: [x0 y0] [x1 y2] [r1 r2 ...] any_r

def r_score(r):
        return abs(r[0] - r[2]) + abs(r[1] - r[3])


def best_ride(v, rides, B, t):
        best = None
        best_score = -1
        for r in rides:
            if in_time(v, r, t):
                w = weight(v, r, t, B)
                if w > best_score:
                    best = r
                    best_score = w

        if not best:
            v[3] = False

        return best


def in_time(v, r, t):
    return (t + abs(v[0][0] - r[0]) + abs(v[0][1] - r[1]) + r[6] < r[5])


def assign_rides(vehicles, rides, B, t):
    for v in vehicles:
        if rides:
            if v[1] is None and v[3]:
                best = best_ride(v, rides, B, t)
                if best:
                    v[1] = [best[2], best[3]]
                    v[2].append(best[-1])
                    rides.remove(best)


for file in files:
    def old_weight(v, r, t, B):
    s = r[6]
    d = abs(v[0][0] - r[0]) + abs(v[0][1] - r[1])
    c = d if d > r[4] - t else r[4] - t

    w = s/c if c != 0 else s
    if t + d < r[4]:
        w += (s + B)/c

    return w


    def weight(v, r, t, B):
        p1 = 500 if file == 'e_high_bonus' else 1
        s = r[6]
        d = abs(v[0][0] - r[0]) + abs(v[0][1] - r[1])
        c = d if d > r[4] - t else r[4] - t

        w = s/c if c != 0 else s
        if t + d < r[4]:
            w += (s + p1*B)/c

        return w


    rides = []
    vehicles = []
    with open("in/{}.in".format(file), 'r') as f:
        R, C, F, N, B, T = map(int, f.readline().split())
        for ride_id, r in enumerate(f.readlines()):
            tmp = list(map(int, r.split()))
            rides.append(tmp + [r_score(tmp), ride_id])

    for v in range(F):
        vehicles.append([[0, 0], None, [], True])

    # assign 0
    assign_rides(vehicles, rides, B, 0)
    for t in tqdm(range(T)):
        # Update vehicles position and remove destination if reached
        if rides:
            # Update positions
            for v in vehicles:
                if v[1] is not None:
                    if v[0][0] < v[1][0]: v[0][0] += 1
                    elif v[0][0] > v[1][0]: v[0][0] -= 1
                    elif v[0][1] < v[1][1]: v[0][1] += 1
                    elif v[0][1] > v[1][1]: v[0][1] -= 1

                    # Remove destination
                    if v[0] == v[1]:
                        v[1] = None

            assign_rides(vehicles, rides, B, t)

    with open("out/{}.out".format(file), 'w') as f:
        for v in vehicles:
            f.write("{} {}\n".format(len(v[2]), " ".join(map(str, v[2]))))
