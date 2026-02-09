__app_name__ = "rptodo"
__version__ = "0.1.0"

# This code creates a set of named integer constants for different status
# or error codes that your application might encounter.
# Tuple Unpacking: Assigning each number (0-6)from that sequence to the
# corresponding variable in the tuple. i.e SUCCESS = 0
# Using names like DB_WRITE_ERROR instead of raw numbers like 3 makes the
# code more readable and easier to maintain
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

# It maps the integer error codes you saw earlier
# (like DIR_ERROR, FILE_ERROR, etc.)
# to corresponding human-readable error messages as strings.
# For example, since DIR_ERROR is 1, ERRORS[1]
# will give you the string "config directory error".
ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_WRITE_ERROR: "database write error",
    DB_READ_ERROR: "database read error",
    JSON_ERROR: "json operation error",
    ID_ERROR: "to-do id error",
}
