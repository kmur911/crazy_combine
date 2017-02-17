
def helper(start, end, accum, target, curr_str, print_out, mult, div, exp):
    count = 0
    if start == end:
        if accum + end == target:
            count += 1
            if print_out:
                print curr_str + ' + {} = {}'.format(end, target)

        if accum - end == target:
            count += 1
            if print_out:
                print curr_str + ' - {} = {}'.format(end, target)

        last_int = int(curr_str.rsplit(' ', 1)[-1])
        new_accum = accum - last_int
        combined_last_int = int('{}{}'.format(last_int, end))
        curr_str = curr_str.rsplit(' ', 1)[0]

        if (new_accum > accum and accum - combined_last_int == target) or (new_accum < accum and accum + combined_last_int == target):
            count += 1
            if print_out:
                print curr_str + ' {} = {}'.format(combined_last_int, target)

        elif new_accum == 0 and combined_last_int == target:
            count += 1
            if print_out:
                print '{} = {}'.format(combined_last_int, target)

    if start < end:
        count += helper(start + 1, end, accum + start, target, curr_str + ' + {}'.format(start), print_out, mult, div, exp)
        count += helper(start + 1, end, accum - start, target, curr_str + ' - {}'.format(start), print_out, mult, div, exp)
        count += helper(start + 1, end, int('{}{}'.format(accum, start)), target, curr_str + '{}'.format(start), print_out, mult, div, exp)

    return count


def crazy_combine(start, end, target, print_out, mult=False, div=False, exp=False):
    count = 0

    if start == end:
        if start == target:
            count += 1
            if print_out:
                print '{} = {}'.format(start, target)

    elif start < end:
        count = helper(start + 1, end, start, target, '{}'.format(start), print_out, mult, div, exp)

    print 'The number of solutions is {}'.format(count)

if __name__ == '__main__':
    crazy_combine(1, 1, 1, False)
