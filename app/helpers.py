import re


def validate_isbn(isbn):
    if not isinstance(isbn, str):
        return False

    if len(isbn) == 13:
        regex = re.compile(r"^(978|979)\d{1,5}\d{1,7}\d{1,6}(\d)$")
        if re.fullmatch(regex, isbn):
            match = re.search(regex, isbn)
            check_digit = int(match.group(2))

            result = 0
            for i in range(12):
                if i % 2 == 0:
                    result += int(isbn[i])
                else:
                    result += int(isbn[i]) * 3

            result %= 10

            if result != 0:
                result = 10 - result

            if result == check_digit:
                return True

            return False
    elif len(isbn) == 10:
        regex = re.compile(r"^\d{1,5}\d{1,7}\d{1,6}(\d)$")
        if re.fullmatch(regex, isbn):
            match = re.search(regex, isbn)
            check_digit = int(match.group(1))

            result = 0
            for i in range(9):
                result += int(isbn[i]) * (10 - i)

            result %= 11

            if result != 0:
                result = 11 - result

            if result == check_digit:
                return True

            return False

    return False
