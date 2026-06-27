import random

# Procedural Science Question Generator
def make_plants_questions():
    questions = []
    # Core plant terms
    parts = ["roots", "leaves", "stem", "flowers", "seeds", "fruit"]
    functions = {
        "roots": "absorb water and minerals from the soil",
        "leaves": "perform photosynthesis to make food",
        "stem": "support the plant and transport nutrients",
        "flowers": "attract pollinators for reproduction",
        "seeds": "grow into new plants under right conditions",
        "fruit": "protect seeds and help with seed dispersal"
    }
    
    # 0 to 33: Easy
    for i in range(35):
        part = parts[i % len(parts)]
        func = functions[part]
        question = f"Which part of the plant is mainy responsible to {func}?"
        options = [part.capitalize()]
        while len(options) < 4:
            w = random.choice(parts).capitalize()
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(part.capitalize())
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    needs = ["Carbon Dioxide", "Water", "Sunlight", "Chlorophyll", "Oxygen", "Glucose"]
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            question = "What gas do plants absorb from the air during photosynthesis?"
            corr = "Carbon Dioxide"
            wrongs = ["Oxygen", "Nitrogen", "Helium"]
        elif q_type == 1:
            question = "What is the green pigment in leaves that captures solar energy?"
            corr = "Chlorophyll"
            wrongs = ["Carotene", "Melanin", "Hemoglobin"]
        else:
            question = "What sugar is produced by plants as food during photosynthesis?"
            corr = "Glucose"
            wrongs = ["Sucrose", "Lactose", "Starch"]
        
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    adaptation_plants = [
        ("Cactus", "desert", "spines to reduce water loss"),
        ("Water Lily", "pond", "floating leaves to capture sunlight"),
        ("Venus Flytrap", "nutrient-poor soil", "traps to capture insects for nitrogen"),
        ("Mangrove", "salty swamp", "special roots to filter salt and breathe air"),
        ("Pine Tree", "cold forest", "needle-like leaves and cones to survive snow")
    ]
    for i in range(30):
        plant, habitat, adapt = adaptation_plants[i % len(adaptation_plants)]
        q_type = i % 2
        if q_type == 0:
            question = f"Where is the '{plant}' plant natively adapted to survive?"
            corr = habitat.capitalize()
            options = [corr]
            while len(options) < 4:
                w = random.choice(adaptation_plants)[1].capitalize()
                if w not in options:
                    options.append(w)
            random.shuffle(options)
            ans_idx = options.index(corr)
        else:
            question = f"Why does a '{plant}' have {adapt}?"
            corr = "Survival adaptation"
            options = [corr, "To attract predators", "Accidental growth", "To absorb less light"]
            random.shuffle(options)
            ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_animals_questions():
    questions = []
    # 0 to 33: Easy
    categories = ["Mammal", "Bird", "Reptile", "Amphibian", "Fish"]
    examples = {
        "Mammal": ["Dog", "Blue Whale", "Bat", "Kangaroo"],
        "Bird": ["Eagle", "Penguin", "Ostrich", "Sparrow"],
        "Reptile": ["Snake", "Turtle", "Crocodile", "Lizard"],
        "Amphibian": ["Frog", "Toad", "Salamander", "Newt"],
        "Fish": ["Shark", "Goldfish", "Salmon", "Tuna"]
    }
    for i in range(35):
        cat = categories[i % len(categories)]
        ex = random.choice(examples[cat])
        question = f"Which biological class does a '{ex}' belong to?"
        options = [cat]
        while len(options) < 4:
            w = random.choice(categories)
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(cat)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    diets = ["Herbivore", "Carnivore", "Omnivore"]
    examples_diet = {
        "Herbivore": ["Deer", "Rabbit", "Koala", "Elephant"],
        "Carnivore": ["Lion", "Tiger", "Shark", "Wolf"],
        "Omnivore": ["Bear", "Human", "Crow", "Pig"]
    }
    for i in range(35):
        diet = diets[i % len(diets)]
        ex = random.choice(examples_diet[diet])
        question = f"An animal like the '{ex}' which eats both plants and animals is a/an:" if diet == "Omnivore" else \
                   f"An animal like the '{ex}' which eats only plants is a/an:" if diet == "Herbivore" else \
                   f"An animal like the '{ex}' which eats only meat is a/an:"
        options = [diet, "Decomposer", "Producer", "Photosynthesizer"]
        options = options[:4]
        random.shuffle(options)
        ans_idx = options.index(diet)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    facts = [
        ("Which of these mammals can fly?", "Bat", ["Eagle", "Flying Squirrel", "Pigeon"]),
        ("Which animal is warm-blooded?", "Eagle", ["Frog", "Snake", "Shark"]),
        ("What do we call animals without a backbone?", "Invertebrates", ["Vertebrates", "Mammals", "Amphibians"]),
        ("What process do insects undergo when changing from larva to adult?", "Metamorphosis", ["Photosynthesis", "Germination", "Respiration"]),
        ("How do reptiles breathe?", "Lungs", ["Gills", "Skin", "Spiracles"])
    ]
    for i in range(30):
        q, corr, wrongs = facts[i % len(facts)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": q, "options": options, "answer": ans_idx})

    return questions

def make_solarsystem_questions():
    questions = []
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    
    # 0 to 33: Easy
    for i in range(35):
        idx = i % len(planets)
        p_name = planets[idx]
        ordinal = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"][idx]
        question = f"Which planet is the {ordinal} planet from the Sun?"
        options = [p_name]
        while len(options) < 4:
            w = random.choice(planets)
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(p_name)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    attributes = [
        ("Mercury", "closest to the Sun", "Smallest"),
        ("Venus", "hottest planet in our solar system", "Brightest"),
        ("Earth", "only planet known to support life", "Blue Planet"),
        ("Mars", "known as the Red Planet", "Mars"),
        ("Jupiter", "largest planet in our solar system", "Giant"),
        ("Saturn", "famous for its prominent rings", "Ringed Planet"),
        ("Uranus", "rotates on its side", "Ice Giant"),
        ("Neptune", "farthest planet from the Sun", "Windy Planet")
    ]
    for i in range(35):
        p, attr, nickname = attributes[i % len(attributes)]
        question = f"Which planet is {attr}?"
        options = [p]
        while len(options) < 4:
            w = random.choice(planets)
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(p)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    facts = [
        ("What lies between Mars and Jupiter?", "Asteroid Belt", ["Kuiper Belt", "Oort Cloud", "Ring system"]),
        ("What is the Sun mainly made of?", "Hydrogen and Helium", ["Oxygen and Carbon", "Liquid Iron", "Rock and Ice"]),
        ("How long does it take for Earth to complete one orbit around the Sun?", "365 days", ["24 hours", "30 days", "12 months"]),
        ("Which of these is a dwarf planet?", "Pluto", ["Neptune", "Mercury", "Titan"]),
        ("What is the name of Earth's natural satellite?", "The Moon", ["Phobos", "Titan", "Ganymede"])
    ]
    for i in range(30):
        q, corr, wrongs = facts[i % len(facts)]
        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": q, "options": options, "answer": ans_idx})

    return questions

def make_humanbody_questions():
    questions = []
    organs = ["heart", "brain", "lungs", "stomach", "kidneys", "liver"]
    functions = {
        "heart": "pumps blood throughout the body",
        "brain": "controls all actions and processes information",
        "lungs": "helps in breathing and gas exchange",
        "stomach": "breaks down food using acids",
        "kidneys": "filter waste from blood to form urine",
        "liver": "detoxifies chemicals and produces bile"
    }

    # 0 to 33: Easy
    for i in range(35):
        org = organs[i % len(organs)]
        func = functions[org]
        question = f"Which organ {func}?"
        options = [org.capitalize()]
        while len(options) < 4:
            w = random.choice(organs).capitalize()
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(org.capitalize())
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            question = "How many bones are in an adult human skeleton?"
            corr = "206"
            wrongs = ["106", "306", "250"]
        elif q_type == 1:
            question = "Which blood cells carry oxygen around the body?"
            corr = "Red blood cells"
            wrongs = ["White blood cells", "Platelets", "Plasma cells"]
        else:
            question = "What is the largest organ of the human body?"
            corr = "Skin"
            wrongs = ["Liver", "Brain", "Heart"]

        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    systems = {
        "Circulatory": "Heart, blood vessels, and blood",
        "Respiratory": "Lungs, trachea, and diaphragm",
        "Digestive": "Stomach, intestines, and esophagus",
        "Nervous": "Brain, spinal cord, and nerves",
        "Skeletal": "Bones, joints, and ligaments"
    }
    sys_list = list(systems.keys())
    for i in range(30):
        sys = sys_list[i % len(sys_list)]
        desc = systems[sys]
        question = f"Which human body system consists of the {desc}?"
        options = [sys]
        while len(options) < 4:
            w = random.choice(sys_list)
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(sys)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

def make_weather_questions():
    questions = []
    # 0 to 33: Easy
    for i in range(35):
        q_type = i % 3
        if q_type == 0:
            question = "Which instrument is used to measure temperature?"
            corr = "Thermometer"
            wrongs = ["Barometer", "Anemometer", "Rain gauge"]
        elif q_type == 1:
            question = "What falls from the sky when water vapor condenses into liquid drops?"
            corr = "Rain"
            wrongs = ["Snow", "Hail", "Dew"]
        else:
            question = "What season is characterized by falling leaves and cooler temperatures?"
            corr = "Autumn"
            wrongs = ["Summer", "Spring", "Winter"]

        options = [corr] + wrongs
        random.shuffle(options)
        ans_idx = options.index(corr)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 35 to 69: Medium
    water_cycle = ["Evaporation", "Condensation", "Precipitation", "Collection"]
    meanings = {
        "Evaporation": "Liquid water turns into gas (water vapor) by heat",
        "Condensation": "Water vapor cools down and turns back into liquid droplets (clouds)",
        "Precipitation": "Water falls from clouds as rain, snow, sleet, or hail",
        "Collection": "Water gathers in oceans, lakes, and rivers"
    }
    for i in range(35):
        step = water_cycle[i % len(water_cycle)]
        desc = meanings[step]
        question = f"In the water cycle, what is the stage where {desc} called?"
        options = [step]
        while len(options) < 4:
            w = random.choice(water_cycle)
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(step)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    # 70 to 99: Hard
    clouds = [
        ("Cumulus", "fluffy, white clouds with flat bases"),
        ("Stratus", "flat, grey blanket-like clouds covering the sky"),
        ("Cirrus", "thin, wispy feather-like clouds high in the sky"),
        ("Cumulonimbus", "tall, dark storm clouds producing thunder and lightning")
    ]
    for i in range(30):
        c_name, desc = clouds[i % len(clouds)]
        question = f"What type of clouds are described as {desc}?"
        options = [c_name]
        while len(options) < 4:
            w = random.choice(clouds)[0]
            if w not in options:
                options.append(w)
        random.shuffle(options)
        ans_idx = options.index(c_name)
        questions.append({"question": question, "options": options, "answer": ans_idx})

    return questions

# Generate on import
JUPITER_QUESTIONS = {
    "Plants": make_plants_questions(),
    "Animals": make_animals_questions(),
    "Solar System": make_solarsystem_questions(),
    "Human Body": make_humanbody_questions(),
    "Weather": make_weather_questions()
}