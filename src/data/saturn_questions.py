import random

def make_variables_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            var_name = random.choice(["count", "score", "total", "health", "speed"])
            val = random.randint(1, 10)
            question = f"In Python, what is the value of variable '{var_name}' after running:\n{var_name} = {val}?"
            corr = str(val)
            wrongs = [str(val + 1), str(val - 1), "None"]
        elif q_type == 1:
            val1 = random.randint(1, 5)
            val2 = random.randint(1, 5)
            question = f"What is the output of:\nx = {val1}\ny = {val2}\nprint(x + y)?"
            corr = str(val1 + val2)
            wrongs = [str(val1 * val2), str(val1 - val2), f"{val1}{val2}"]
        else:
            val_str = random.choice(["'hello'", '"world"', "'42'", '"Python"'])
            question = f"What is the data type of the variable x in:\nx = {val_str}?"
            corr = "str"
            wrongs = ["int", "float", "bool"]

        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            val = random.randint(5, 15)
            inc = random.randint(2, 6)
            question = f"What is the final value of x after executing:\nx = {val}\nx = x + {inc}?"
            corr = str(val + inc)
            wrongs = [str(val), str(inc), str(val * inc)]
        elif q_type == 1:
            val = random.randint(1, 100)
            question = f"Which variable name is invalid in Python?"
            corr = "1st_place"
            wrongs = ["first_place", "place_1", "_place"]
        else:
            val = random.choice(["True", "False"])
            question = f"What is the data type of x = {val}?"
            corr = "bool"
            wrongs = ["str", "int", "float"]

        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        q_type = i % 3
        if q_type == 0:
            a = random.randint(2, 6)
            b = random.randint(2, 6)
            question = f"What is the value of x after executing:\nx = {a}\ny = {b}\nx, y = y, x?"
            corr = str(b)
            wrongs = [str(a), str(a+b), "None"]
        elif q_type == 1:
            question = f"What is the result of float('3.5') in Python?"
            corr = "3.5"
            wrongs = ["3", "4", "Error"]
        else:
            val = round(random.uniform(1.5, 9.5), 1)
            question = f"What is the data type of x = {val}?"
            corr = "float"
            wrongs = ["int", "str", "list"]

        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_loops_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        num = random.randint(2, 10)
        question = f"How many times will this loop run?\nfor i in range({num}):\n    print(i)"
        corr = str(num)
        wrongs = [str(num - 1), str(num + 1), "0"]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        start = random.randint(1, 4)
        end = start + random.randint(3, 6)
        question = f"How many times will this loop run?\nfor i in range({start}, {end}):\n    print(i)"
        corr = str(end - start)
        wrongs = [str(end), str(start), str(end - start + 1)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        tot = 0
        limit = random.randint(3, 5)
        step = random.randint(2, 3)
        # Simulate:
        # x = 0
        # while x < limit:
        #     x += step
        x = 0
        iterations = 0
        while x < limit:
            x += step
            iterations += 1
        
        question = f"How many times will this loop execute?\nx = 0\nwhile x < {limit}:\n    x += {step}"
        corr = str(iterations)
        wrongs = [str(limit), str(step), "Infinite Loop"]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_conditions_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        if a == b:
            b += 1
        
        q_type = i % 2
        if q_type == 0:
            question = f"What is the output of:\nx = {a}\ny = {b}\nif x > y:\n    print('A')\nelse:\n    print('B')"
            corr = "A" if a > b else "B"
        else:
            question = f"What is the output of:\nx = {a}\ny = {b}\nif x == y:\n    print('Yes')\nelse:\n    print('No')"
            corr = "No"

        options = [corr, "A" if corr != "A" else "B", "None", "Error"]
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        score = random.choice([55, 65, 75, 85, 95])
        question = f"What is the output of:\nscore = {score}\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')"
        if score >= 90: corr = "A"
        elif score >= 80: corr = "B"
        elif score >= 70: corr = "C"
        else: corr = "F"

        options = ["A", "B", "C", "F"]
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        # boolean operators
        a = random.choice([True, False])
        b = random.choice([True, False])
        question = f"What does this condition evaluate to?\na = {a}\nb = {b}\nresult = a and b\nprint(result)"
        corr = str(a and b)
        wrongs = [str(not (a and b)), "None", "Error"]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_functions_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        q_type = i % 2
        if q_type == 0:
            question = "Which keyword is used to declare a function in Python?"
            corr = "def"
            wrongs = ["func", "function", "define"]
        else:
            question = "Which keyword exits a function and returns a value?"
            corr = "return"
            wrongs = ["exit", "break", "give"]
        
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        val = random.randint(2, 6)
        question = f"What is the output of this code?\ndef double(n):\n    return n * 2\n\nprint(double({val}))"
        corr = str(val * 2)
        wrongs = [str(val), str(val + 2), str(val ** 2)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        v1 = random.randint(2, 5)
        v2 = random.randint(2, 5)
        question = f"What is the output of this code?\ndef math_op(x, y):\n    return x * y - y\n\nprint(math_op({v1}, {v2}))"
        corr = str(v1 * v2 - v2)
        wrongs = [str(v1 * v2), str(v1 + v2), str(v1 - v2)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_lists_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        items = ["apple", "banana", "cherry", "date", "elderberry"]
        idx = random.randint(0, 3)
        question = f"What is items[{idx}] in this list?\nitems = {items}"
        corr = f"'{items[idx]}'"
        wrongs = [f"'{items[idx+1]}'", f"'{items[idx-1]}'", str(idx)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        items = [random.randint(10, 50) for _ in range(random.randint(3, 5))]
        question = f"What is the value of len(nums) for the following list?\nnums = {items}"
        corr = str(len(items))
        wrongs = [str(len(items) - 1), str(len(items) + 1), "0"]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        # append/pop operations
        val = random.randint(5, 9)
        question = f"What is the output of the following code?\nmy_list = [1, 2, 3]\nmy_list.append({val})\nprint(my_list)"
        corr = str([1, 2, 3, val])
        wrongs = [str([val, 1, 2, 3]), str([1, 2, 3]), "Error"]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

# Generate on import
SATURN_QUESTIONS = {
    "Variables": make_variables_questions(),
    "Loops": make_loops_questions(),
    "Conditions": make_conditions_questions(),
    "Functions": make_functions_questions(),
    "Lists": make_lists_questions()
}