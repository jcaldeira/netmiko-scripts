'''Driver function
print(titleToNumber("CDA"));

This code contributed by Rajput-Ji
https://www.geeksforgeeks.org/find-excel-column-number-column-title/

Python program to return title to result
of excel sheet.'''

import sys

# Returns resul when we pass title.
def titleToNumber(s):
    # This process is similar to binary-to-
    # decimal conversion
    result = 0;
    for B in range(len(s)):
        result *= 26;
        result += ord(s[B]) - ord('A') + 1;

    return result;


def main():
    while True:
        user_input = input('Name of the column: ')
        if user_input != 'exit':
            print(titleToNumber(user_input))
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
