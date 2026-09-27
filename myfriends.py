"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

# ------------ BEGIN YOUR CODE ------------

        for line in infile:
            stripped_line = line.strip()
            if not stripped_line:
                continue    # skip empty lines
            names = stripped_line.split()
            list_of_pairs.append((names[0], names[1]))

# ------------ END YOUR CODE ------------

    return list_of_pairs 

def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of 
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way: 
      if given a pair (x,y), then assume that y is a friend of x, and x is 
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    # ------------ BEGIN YOUR CODE ------------

    for x, y in pairs:
        if x == y:
            continue    # ignore own-relationships

        directory.setdefault(x, set()).add(y)
        directory.setdefault(y, set()).add(x)

    # ------------ END YOUR CODE ------------

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list 
    of 2-tuples, where each tuples has the person's name as the first element,
    the the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------

    friends_list = [(person, len(friends)) for person, friends in my_dir.items()]

    # sort by name first (ASCII order), then stably sort by count descending
    # so that ties keep their ASCII-ordered relative positions
    friends_list.sort(key=lambda item: item[0])
    friends_list.sort(key=lambda item: item[1], reverse=True)

    # ------------ END YOUR CODE ------------

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the 
        team leader's name, i.e. A.  Subsequent unique substrings are 
        friends of A or friends of friends of A, in ASCII order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus 
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------

    team = set()
    direct_friends = my_dir.get(person, set())
    team.update(direct_friends)

    # add friends-of-friends (second circle)
    for friend in direct_friends:
        team.update(my_dir.get(friend, set()))

    team.discard(person)   # leader shouldn't appear twice

    if team:
        label = '_'.join([person] + sorted(team))

    # ------------ END YOUR CODE ------------

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ASCII order
    """
    smallest_teams = []

    # ------------ BEGIN YOUR CODE

    best_size = None
    for person in my_dir:
        roster = make_team_roster(person, my_dir)
        size = len(roster.split('_'))

        if best_size is None or size < best_size:
            best_size = size
            smallest_teams = [roster]
        elif size == best_size:
            smallest_teams.append(roster)

    smallest_teams.sort()   # break ties in ASCII order

    # ------------ END YOUR CODE

    return smallest_teams[0] if smallest_teams else ""



def generate_friends(friends_dir):
    """Karma (optional): generator version of the Friends iterator class.

    Yields the same unique (x, y) pairs, in the same ASCII order, as
    Friends(friends_dir) would -- without needing a separate class.

    Usage:
        for pair in generate_friends(my_dir):
            print(pair)

        # or collect them all into a list:
        all_pairs = list(generate_friends(my_dir))
    """
    for person in sorted(friends_dir.keys()):
        for friend in sorted(friends_dir[person]):
            if friend > person:    # only emit each unique pair once
                yield (person, friend)


if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('myfriends.txt')
    print(my_pairs)

    print('\n2. run make_friends_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir) 

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))

    print('\n4. run make_team_roster')
    my_person = 'DARTHVADER'   # test with this person as team leader
    team_roster = make_team_roster(my_person, my_dir)
    print(team_roster) 

    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        if num == 10:
            break
    # since index 0 we read 11 elements
    print(len(list(friends_iterator)) + num + 1)
