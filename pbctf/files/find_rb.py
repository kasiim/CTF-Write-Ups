from pwn import *


# r = remote('find-rbtree.chal.perfect.blue', 1)
r = remote('localhost', 1234)

# Parse person information
def get_person_info(r):
    r.recvuntil("]")
    _ = r.recvline()
    head_wear = str(r.recvline()).split(": ")[1][:-3]
    eye_color = str(r.recvline()).split(": ")[1][:-3]
    hair = str(r.recvline()).split(": ")[1][:-3]
    outerwear = str(r.recvline()).split(": ")[1][:-3]
    t_shirt_color = str(r.recvline()).split(": ")[1][:-3]
    trousers = str(r.recvline()).split(": ")[1][:-3]
    socks = str(r.recvline()).split(": ")[1][:-3]
    shoes = str(r.recvline()).split(": ")[1][:-3]

    person = {
        'props' : (head_wear, eye_color, hair, outerwear, t_shirt_color, trousers, socks, shoes),
        'candidate' : True,
        'chance_of_rb' : 0
    }

    return person

# show and give choices of right person
def show_people_left(people_left):
    valid_indexes = []
    for id, person in enumerate(people_left):
        if person['candidate'] == True:
            print(id, person)
            valid_indexes.append(id)
    return valid_indexes

properties = {
    "Eyewear": ["Glasses", "Monocle", "None"],
    "Eye color": ["Brown", "Blue", "Hazel"],
    "Hair": ["Straight", "Curly", "Bald"],
    "Outerwear": ["Coat", "Hoodie", "Poncho"],
    "T-shirt color": ["Red", "Orange", "Green"],
    "Trousers": ["Jeans", "Leggings", "Sweatpants"],
    "Socks color": ["Black", "Gray", "White"],
    "Shoes": ["Boots", "Slippers", "Sneakers"],
}
# Guess numbers and people count
cases = [(5, 3), (7, 3), (10, 4), (15, 4), (20, 5), (25, 5), (50, 6), (75, 7), (100, 8), (250, 9)]
cases += [(400, 10)] * 5 + [(750, 11)] * 5 + [(1000, 12)] * 5 + [(1600, 12)] * 5

prop_names = tuple(properties.keys())
# Get stage
for stage in range(30):
    r.recvuntil("STAGE ")
    stage = str(r.recvline()).split(' / ')[0][2:]
    people_count, question_count = cases[int(stage) - 1]
    print(stage, people_count, question_count)

    # Gather people information first time
    people = []
    for person in range(people_count):
        people.append(get_person_info(r))




    # Ask questions about people
    for i in range(question_count):
        people_left = []
        for person in people:
            if person['candidate']:
                people_left.append(person)

        prop_distribution = {}


        # Get property distribution
        for prop_category in properties.keys():
            prop_distribution[prop_category] = {}
            for prop in properties[prop_category]:
                for person in people_left:
                    for person_prop in person['props']:
                        if prop == person_prop:
                            try:
                                prop_distribution[prop_category][prop] += 1
                            except:
                                prop_distribution[prop_category][prop] = 1

        # Best choice so far

        best_choice = {
            'category' : "Unknown",
            'prop' : "Unknown",
            'value' : 0.5,
            'amount_of_choices' : 3
        }

        # Loop over categories 8 of them
        for category in prop_distribution.keys():
            print(category, prop_distribution[category], end=' ')
            ## Loop over items to get their distribution
            for distribution in prop_distribution[category].keys():
                
                distribution_value = prop_distribution[category][distribution] / len(people_left)
                ## Amount of choices
                amount_of_choices = len(prop_distribution[category])
                ## Error from 0.5
                difference = abs(0.5 - distribution_value)
                
                # Assign best choice # Distrtibution value 1 means no choice there
                if best_choice['value'] >= difference and distribution_value != 1:
                    # Priortize 2 choices over 1
                    if len(prop_distribution[category]) <= best_choice['amount_of_choices']:
                        best_choice['value'] = difference
                        best_choice['category'] = category
                        best_choice['prop'] = distribution
                        best_choice['amount_of_choices'] = len(prop_distribution[category])

                print(distribution_value, end=' ')
            print()

        # Handle first loop case
        if i == 0:
            r.recvuntil("Now ask me!\n")

        # print(best_choice)

        # IF best choice = unknown person is detected already, present solution
        if best_choice['category'] != 'Unknown':

            selected_category = best_choice['category']
            r.sendline(selected_category)
            selected_prop = best_choice['prop']
            r.sendline(selected_prop)
            print(selected_category, selected_prop)
            response = str(r.recvline()).split("> ")[2][0]

        # Send solution straight away
        else:
            r.sendline("Solution")
            break

        
        for person in people_left:
            if response == "Y":
                if person['props'][prop_names.index(selected_category)] != selected_prop:
                    person['candidate'] = False
            else:
                if person['props'][prop_names.index(selected_category)] == selected_prop:
                    person['candidate'] = False
                    
    # Get possible choices usually one
    which_is_rb = show_people_left(people_left)
    # If not one, pray to RNG jesus and hope for the best
    rb_index = random.choice(which_is_rb)
    # rb_index = int(input())

    # Send answer
    r.sendline(" ".join(people_left[rb_index]['props']))

    # Eat some text
    print(r.recvline())

# Switch to interactive just in case, to see the flag
r.interactive()