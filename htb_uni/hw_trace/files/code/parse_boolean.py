def parse_boolean_to_python(expression, output_variable_name):
    # Parses boolean expression into python executable code
    expression = expression.replace(" ", "")
    new_python_expression = ""

    last_char = None
    or_was_used = False
    and_needed = False
    for char_index, char in enumerate(expression):
        if last_char == None:
            last_char = char
        else:
            # Deal with inversion
            if char == "'":
                new_python_expression += "not " + last_char
                
                # Ignore index error, since it is last character anyway
                try:
                    if expression[char_index + 1] != "+":
                        and_needed = True 
                except IndexError:
                    pass

            
            elif last_char.isalpha() and not or_was_used:
                new_python_expression += last_char
                if char != "+":
                    and_needed = True

            elif last_char.isalpha() and or_was_used:
                new_python_expression += last_char
                or_was_used = False
                if char != "+":
                    and_needed = True

            elif last_char == "+":
                new_python_expression += ") or ("
                or_was_used = True


            if and_needed:
                new_python_expression += " and "
                and_needed = False
            last_char = char

    
    new_python_expression = "(" + new_python_expression + ")"
    return output_variable_name + " = " + new_python_expression

A_1 = "a'bcd' + ab'c'd + ab'cd' + abc'd'"
A_2 = "a'bcd + ab'cd + ac'd'"
A_3 = "a'bcd' + abc'd + ab'd'"
A_4 = "ab'cd' + a'bcd + ac'd"
A_5 = "ab'c'd' + a'bcd + ab'cd + abc'd"
A_6 = "a'bcd + abc'd + ab'd'"
A_7 = "a'bcd + ab'd' + ac'd'"
A_8 = "a'bcd' + ab'cd + ac'd'"
A_9 = "abc'd' + a'bcd + ab'd"


B_1 = "a'b'cd + ab'cd' + bc'd'"
B_2 = "bc'd' + b'cd"
B_3 = "a'bc'd' + a'b'cd + ab'cd' + abc'd"
B_4 = "a'b'cd + ab'cd' + bc'd"
B_5 = "a'b'cd' + ab'cd + bc'd"
B_6 = "a'bc'd + abc'd' + b'cd'"
B_7 = "b'cd' + bc'd"
B_8 = "a'bc'd + abc'd' + b'cd"


C_1 = "ab'c'd + a'c'd' + bc'd'"
C_2 = "c'd'"
C_3 = "abc'd + a'c'd' + b'c'd'"
C_4 = "a'b'c'd' + bc'd + ac'd"
C_5 = "b'c'd' + bc'd"
C_6 = "a'bc'd + b'c'd' + ac'd'"
C_7 = "abc'd' + ab'c'd + a'bc'd + a'b'c'd'"

A_FF = [A_1, A_2, A_3, A_4, A_5, A_6, A_7, A_8, A_9]
A_FF_names = ["A_1", "A_2", "A_3", "A_4", "A_5", "A_6", "A_7", "A_8", "A_9"]
B_FF = [B_1, B_2, B_3, B_4, B_5, B_6, B_7, B_8]
B_FF_names = ["B_1", "B_2", "B_3", "B_4", "B_5", "B_6", "B_7", "B_8"]
C_FF = [C_1, C_2, C_3, C_4, C_5, C_6, C_7]
C_FF_names = ["C_1", "C_2", "C_3", "C_4", "C_5", "C_6", "C_7"]

OR_GATES = [A_FF, B_FF, C_FF]
OR_GATES_names = [A_FF_names, B_FF_names, C_FF_names]


for gates, names in zip(OR_GATES, OR_GATES_names):
    print()
    for expression, name in zip(gates, names):
        print(parse_boolean_to_python(expression, name))