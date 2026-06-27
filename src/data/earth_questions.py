import random

def generate_numbers_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            num = random.randint(10, 99)
            even_odd = "even" if num % 2 == 0 else "odd"
            question = f"Is the number {num} even or odd?"
            options = ["Even", "Odd", "Neither", "Both"]
            ans_idx = 0 if even_odd == "even" else 1
        elif q_type == 1:
            num = random.randint(10, 100)
            next_num = num + 1
            question = f"What number comes immediately after {num}?"
            options = [str(next_num), str(num - 1), str(num + 2), str(num + 10)]
            random.shuffle(options)
            ans_idx = options.index(str(next_num))
        else:
            n1 = random.randint(10, 50)
            n2 = random.randint(51, 99)
            question = f"Which number is greater?"
            options = [str(n1), str(n2), "They are equal", "None"]
            random.shuffle(options)
            ans_idx = options.index(str(n2))
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            # Roman Numerals
            roman_map = {5: "V", 9: "IX", 10: "X", 15: "XV", 20: "XX", 40: "XL", 50: "L"}
            val = random.choice(list(roman_map.keys()))
            roman = roman_map[val]
            question = f"What is the value of the Roman numeral '{roman}'?"
            options = [str(val), str(val+5), str(val-2), str(val*2)]
            random.shuffle(options)
            ans_idx = options.index(str(val))
        elif q_type == 1:
            # Place value
            num = random.randint(100, 999)
            digits = list(str(num))
            digit = digits[1]
            question = f"In the number {num}, what is the place value of the digit {digit}?"
            val = int(digit) * 10
            options = ["Units", "Tens", "Hundreds", "Thousands"]
            ans_idx = 1 # Tens
        else:
            # Simple primes
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
            non_primes = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18]
            prime = random.choice(primes)
            other_options = random.sample(non_primes, 3)
            options = [str(prime)] + [str(x) for x in other_options]
            random.shuffle(options)
            question = "Which of the following is a prime number?"
            ans_idx = options.index(str(prime))
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    for i in range(30):
        q_type = i % 3
        if q_type == 0:
            # Sequences
            start = random.randint(2, 10)
            step = random.randint(3, 7)
            seq = [start + j * step for j in range(4)]
            next_val = start + 4 * step
            question = f"What is the next number in the sequence: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ...?"
            options = [str(next_val), str(next_val + 2), str(next_val - step), str(next_val * 2)]
            random.shuffle(options)
            ans_idx = options.index(str(next_val))
        elif q_type == 1:
            # Larger place value
            num = random.randint(1000, 9999)
            digit = str(num)[0]
            question = f"In the number {num}, what is the place value of the digit {digit}?"
            options = ["Ones", "Tens", "Hundreds", "Thousands"]
            ans_idx = 3 # Thousands
        else:
            # Larger Primes
            primes = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
            non_primes = [33, 35, 39, 45, 49, 51, 55, 57, 63, 65, 69, 77, 81, 85, 91, 95]
            prime = random.choice(primes)
            other_options = random.sample(non_primes, 3)
            options = [str(prime)] + [str(x) for x in other_options]
            random.shuffle(options)
            question = "Which of the following is a prime number?"
            ans_idx = options.index(str(prime))
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def generate_math_op_questions(op):
    questions = []
    # Generate 100 questions of operation
    for i in range(100):
        if i < 33:
            # Easy
            n1 = random.randint(1, 20)
            n2 = random.randint(1, 20)
        elif i < 66:
            # Medium
            n1 = random.randint(15, 120)
            n2 = random.randint(10, 80)
        else:
            # Hard
            n1 = random.randint(100, 999)
            n2 = random.randint(50, 500)

        if op == "+":
            ans = n1 + n2
            question = f"What is {n1} + {n2}?"
        elif op == "-":
            # Ensure positive answer
            if n1 < n2:
                n1, n2 = n2, n1
            ans = n1 - n2
            question = f"What is {n1} - {n2}?"
        elif op == "*":
            # For multiplication, reduce sizes slightly to keep it fair
            if i >= 66:
                n1 = random.randint(12, 35)
                n2 = random.randint(11, 25)
            elif i >= 33:
                n1 = random.randint(7, 15)
                n2 = random.randint(6, 12)
            else:
                n1 = random.randint(2, 9)
                n2 = random.randint(2, 9)
            ans = n1 * n2
            question = f"What is {n1} × {n2}?"
        else: # Division
            # Ensure perfect division
            if i >= 66:
                n2 = random.randint(11, 25)
                ans = random.randint(5, 20)
            elif i >= 33:
                n2 = random.randint(5, 12)
                ans = random.randint(5, 12)
            else:
                n2 = random.randint(2, 9)
                ans = random.randint(2, 9)
            n1 = n2 * ans
            question = f"What is {n1} ÷ {n2}?"

        options = [str(ans)]
        while len(options) < 4:
            offset = random.choice([-3, -2, -1, 1, 2, 3, 5, 10, -10])
            wrong_ans = ans + offset
            if wrong_ans >= 0 and str(wrong_ans) not in options:
                options.append(str(wrong_ans))
        
        random.shuffle(options)
        ans_idx = options.index(str(ans))
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def generate_fractions_questions():
    questions = []
    for i in range(100):
        if i < 33:
            # Easy
            denom = random.choice([2, 3, 4, 6, 8])
            num = random.randint(1, denom - 1)
            # Question about fractional value or basic addition of like denominators
            q_type = random.randint(0, 1)
            if q_type == 0:
                tot = denom * random.randint(2, 8)
                ans = int(tot * (num / denom))
                question = f"What is {num}/{denom} of {tot}?"
                options = [str(ans)]
            else:
                n1 = random.randint(1, denom - 2) if denom > 2 else 1
                n2 = 1
                ans = f"{n1+n2}/{denom}"
                question = f"What is {n1}/{denom} + {n2}/{denom}?"
                options = [ans]
        elif i < 66:
            # Medium
            # Unlike denominators
            d1, d2 = random.choice([(2,4), (3,6), (4,8), (2,3), (2,5)])
            # d1 * d2 is common denom
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            num_ans = n1 * d2 + n2 * d1
            denom_ans = d1 * d2
            # Simplify
            from math import gcd
            g = gcd(num_ans, denom_ans)
            ans = f"{num_ans//g}/{denom_ans//g}"
            if num_ans//g == denom_ans//g:
                ans = "1"
            question = f"What is {n1}/{d1} + {n2}/{d2}?"
            options = [ans]
        else:
            # Hard
            # Multiplication of fractions
            d1 = random.randint(2, 5)
            d2 = random.randint(2, 5)
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            num_ans = n1 * n2
            denom_ans = d1 * d2
            from math import gcd
            g = gcd(num_ans, denom_ans)
            ans = f"{num_ans//g}/{denom_ans//g}"
            question = f"What is {n1}/{d1} × {n2}/{d2}?"
            options = [ans]

        # Generate wrong answers
        while len(options) < 4:
            w_num = random.randint(1, 12)
            w_den = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
            from math import gcd
            wg = gcd(w_num, w_den)
            w_ans = f"{w_num//wg}/{w_den//wg}"
            if w_num//wg == w_den//wg:
                w_ans = "1"
            if w_ans not in options:
                options.append(w_ans)

        random.shuffle(options)
        ans_idx = options.index(options[0]) # Temp, let's search correct answer
        # Wait, let's find the correct answer string in the shuffled list
        # The correct answer is options[0] before shuffling if we did options = [ans] + others
    
    # Let's fix this list creation
    # We will build choices: correct answer first, then append wrong answers, shuffle, and get index.
    # Let's write it cleaner:
    # correct = ans
    # choices = [correct]
    # ... add 3 wrong ...
    # shuffle
    # ans_idx = choices.index(correct)
    return questions # Wait, let's write the loop below to properly generate fractions and decimals with clean code.

def build_all_fractions():
    questions = []
    for i in range(100):
        if i < 33:
            # Easy: like denominators or visual fractions
            d = random.choice([3, 4, 5, 6, 8])
            n1 = random.randint(1, d-2)
            n2 = 1
            corr = f"{n1+n2}/{d}"
            question = f"What is {n1}/{d} + {n2}/{d}?"
            wrongs = [f"{n1}/{d}", f"{n1+n2+1}/{d}", f"{n1+n2}/{d+1}"]
        elif i < 66:
            # Medium: unlike denominators
            pairs = [(1,2, 1,4, "3/4"), (1,2, 1,3, "5/6"), (1,3, 1,4, "7/12"), (2,3, 1,6, "5/6"), (1,4, 3,8, "5/8")]
            n1, d1, n2, d2, corr = random.choice(pairs)
            question = f"What is {n1}/{d1} + {n2}/{d2}?"
            wrongs = ["1/2", "2/3", "4/5", "1/4", "3/8", "7/8"]
        else:
            # Hard: multiplication/division
            pairs = [(1,2, 1,2, "1/4"), (2,3, 3,4, "1/2"), (1,3, 3,5, "1/5"), (3,4, 1,3, "1/4"), (4,5, 1,2, "2/5")]
            n1, d1, n2, d2, corr = random.choice(pairs)
            question = f"What is {n1}/{d1} × {n2}/{d2}?"
            wrongs = ["2/3", "3/5", "5/8", "1/3", "4/7", "3/10"]

        options = [corr]
        for w in wrongs:
            if w != corr and w not in options:
                options.append(w)
        while len(options) < 4:
            options.append(f"{random.randint(1,9)}/{random.randint(2,10)}")
        options = options[:4]
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})
    return questions

def build_all_decimals():
    questions = []
    for i in range(100):
        if i < 33:
            # Easy
            n1 = round(random.uniform(0.1, 0.9), 1)
            n2 = round(random.uniform(0.1, 0.9), 1)
            corr = round(n1 + n2, 1)
            question = f"What is {n1} + {n2}?"
            wrongs = [round(corr + 0.1, 1), round(corr - 0.1, 1), round(corr + 1.0, 1)]
        elif i < 66:
            # Medium
            n1 = round(random.uniform(1.1, 9.9), 1)
            n2 = round(random.uniform(0.1, 0.9), 1)
            corr = round(n1 - n2, 1)
            question = f"What is {n1} - {n2}?"
            wrongs = [round(corr + 0.2, 1), round(corr - 0.2, 1), round(corr + 0.5, 1)]
        else:
            # Hard: fractional conversion or division
            val = random.choice([0.25, 0.5, 0.75, 0.2, 0.4, 0.6, 0.8, 0.125])
            frac_map = {0.25: "1/4", 0.5: "1/2", 0.75: "3/4", 0.2: "1/5", 0.4: "2/5", 0.6: "3/5", 0.8: "4/5", 0.125: "1/8"}
            corr = frac_map[val]
            question = f"What fraction is equivalent to the decimal {val}?"
            wrongs = ["1/3", "2/3", "3/8", "5/8", "1/10", "3/10"]

        options = [str(corr)]
        for w in wrongs:
            if str(w) != str(corr) and str(w) not in options:
                options.append(str(w))
        while len(options) < 4:
            options.append(str(round(random.uniform(0.1, 9.9), 2)))
        options = options[:4]
        random.shuffle(options)
        ans_idx = options.index(str(corr))
        questions.append({"question": question, "options": options, "answer": ans_idx})
    return questions


# Generate on import
EARTH_QUESTIONS = {
    "Numbers": generate_numbers_questions(),
    "Addition": generate_math_op_questions("+"),
    "Subtraction": generate_math_op_questions("-"),
    "Multiplication": generate_math_op_questions("*"),
    "Division": generate_math_op_questions("/"),
    "Fractions": build_all_fractions(),
    "Decimals": build_all_decimals()
}