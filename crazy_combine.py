"""
Program to compute arithmetic operations and reach a desired target_num number
given a list of input numbers. To run, execute the program using python3
and follow the prompts.
"""

import os
import sys
import re


def helper(num_list, accum, target_num, curr_str, print_out, mult, div, exp):
    count = 0
    list_len = len(num_list)

    if list_len == 1:
        if accum + num_list[0] == target_num:
            count += 1
            if print_out:
                print(curr_str + ' + {} = {}'.format(num_list[0], target_num))

        if accum - num_list[0] == target_num:
            count += 1
            if print_out:
                print(curr_str + ' - {} = {}'.format(num_list[0], target_num))

        last_int = int(curr_str.rsplit(' ', 1)[-1])
        new_accum = accum - last_int
        combined_last_int = int('{}{}'.format(last_int, num_list[0]))
        curr_str = curr_str.rsplit(' ', 1)[0]

        if (new_accum > accum and accum - combined_last_int == target_num) or \
                (new_accum < accum and accum + combined_last_int == target_num):
            count += 1
            if print_out:
                print(curr_str + ' {} = {}'.format(combined_last_int, target_num))

        elif new_accum == 0 and combined_last_int == target_num:
            count += 1
            if print_out:
                print('{} = {}'.format(combined_last_int, target_num))

    else:
        count += helper(num_list[1:], accum + num_list[0], target_num,
                        curr_str + ' + {}'.format(num_list[0]), print_out, mult, div, exp)
        count += helper(num_list[1:], accum - num_list[0], target_num,
                        curr_str + ' - {}'.format(num_list[0]), print_out, mult, div, exp)
        count += helper(num_list[1:], int('{}{}'.format(accum, num_list[0])), target_num,
                        curr_str + '{}'.format(num_list[0]), print_out, mult, div, exp)

    return count


def crazy_combine(num_list, target_num, mode, mult=False, div=False, exp=False):
    count = 0
    print_out = bool(mode == 'normal')
    list_len = len(num_list)

    if list_len == 1:
        if num_list[0] == target_num:
            count += 1
            if print_out:
                print('{} = {}'.format(num_list[0], target_num))

    elif list_len > 1:
        count = helper(num_list[1:], num_list[0], target_num, '{}'.format(num_list[0]), print_out, mult, div, exp)

    print('The number of solutions is {}'.format(count))


class ArithmeticFinder(object):

    def __init__(self):
        self.num_list = None
        self.target_num = None
        self.mode = None

    @staticmethod
    def verify_input_list(num_list):
        prompt = 'To be sure I am understanding correctly, confirm the ' \
                 'following numbers match your input: \n'
        num_prompt = ' '.join(str(x) for x in num_list)
        prompt += num_prompt
        print(prompt)
        not_finished = True
        while not_finished:
            prompt = 'Is this correct? [y/n]: '
            response = input(prompt)
            if response == 'y':
                return True
            elif response == 'n':
                return False
            else:
                print('Invalid input. Please try again.')

    @staticmethod
    def _get_valid_int(prompt, default=None):
        while True:
            try:
                if default:
                    num = int(input(prompt) or default)
                else:
                    num = int(input(prompt))
            except ValueError:
                print('Invalid integer. Please try again.')
            else:
                return num

    @staticmethod
    def get_choice(prompt, allowed_responses):
        not_finished = True
        while not_finished:
            choice = input(prompt).lower()
            if choice in allowed_responses:
                return choice
            else:
                print('Invalid input. Please try again.')

    @staticmethod
    def display_help_menu():
        print('Please execute {} with no additional arugments.'.format(os.path.basename(__file__)))
        return

    def get_num_list(self):
        """ Get a list of numbers from the user. """
        not_finished = True
        while not_finished:
            prompt = 'Enter a list of integers, separated by a space: '
            raw_list = input(prompt)
            if re.search(r'[^\d -]+', raw_list):
                print('Invalid input list. Please try again.')
                continue
            raw_list = raw_list.split(' ')
            # Remove any entries that do not contain a number
            num_list = []
            for num in raw_list:
                if re.search(r'\d', num):
                    num_list.append(int(num))
            if self.verify_input_list(num_list):
                self.num_list = num_list
                return

    def get_num_range(self):
        not_finished = True
        while not_finished:
            start_num = self._get_valid_int('Enter start of range (inclusive): ')
            stop_num = self._get_valid_int('Enter stop of range (inclusive): ')
            if start_num > stop_num:
                stop_num -= 1
            else:
                stop_num += 1
            interval = self._get_valid_int('Enter step size of range, if other than 1: ', default=1)
            num_list = list(range(start_num, stop_num, interval))
            if self.verify_input_list(num_list):
                self.num_list = num_list
                return

    def read_inputs(self):
        not_finished = True
        choice = None
        while not_finished:
            menu = 'Would you like to enter:\n' \
                   '1) A list of numbers\n' \
                   '2) A range of numbers\n' \
                   '3) Exit\n' \
                   ': '
            choice = input(menu)
            if choice in {'1', '2', '3'}:
                not_finished = False
            else:
                print('Invalid input, please try again.')
        if choice == '3':
            sys.exit()
        elif choice == '1':
            self.get_num_list()
        elif choice == '2':
            self.get_num_range()
        self.target_num = self._get_valid_int('Enter a desired target integer: ')
        prompt = 'Would you like to enable quiet mode (only show number of solutions)? [y/n]: '
        allowed_responses = {'y', 'n'}
        choice = self.get_choice(prompt, allowed_responses)
        if choice == 'y':
            self.mode = 'quiet'
        else:
            self.mode = 'normal'

        # KKM: TAKE IT FROM HERE
        crazy_combine(self.num_list, self.target_num, self.mode)


if __name__ == '__main__':
    af = ArithmeticFinder()
    if len(sys.argv) == 1:
        af.read_inputs()
    else:
        af.display_help_menu()
