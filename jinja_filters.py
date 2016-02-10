def prettify_preference(pref_value):
    """ Returns nicer, printable format of pref_value of Preference """

    new_string = ""
    for letter in pref_value:
        # read only until first non-letter character
        if letter < "a" or letter > "z":
            break
        # add each character to string
        new_string += letter
    # capitalize first letter
    new_string = new_string[0].upper() + new_string[1:]

    # address single outlier case
    if new_string == "Dk":
        new_string = "DK"
    return new_string
