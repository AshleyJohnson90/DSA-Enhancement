from Graph import Graph


# Game class to create the game play
class Game:
    def __init__(self):
        self.graph = Graph()
        # list of all the names of the locations, to load into the graph
        self.location_names = ['Hallway', 'Bathroom', 'Kitchen', 'Walk-In', 'Hostess Counter', 'Stove', 'Sink Station',
                               'Dining Room']
        # dictionary mapping the location to the item that's in it, Hallway and Dining Room do not contain items
        self.items = {
            'Bathroom': 'Apron',
            'Kitchen': 'Serving Tray',
            'Walk-In': 'Salad',
            'Hostess Counter': 'Order Pad',
            'Stove': 'Steak',
            'Sink Station': 'Plate'
        }
        # list that contains the player's running inventory
        self.inventory = []
        self.current_location = 'Hallway'
        self.create_graph()

    def create_graph(self):
        for location in self.location_names:
            self.graph.add_location(location)

        connections = [
            ('Hallway', 'south', 'Kitchen', 'north'),
            ('Kitchen', 'east', 'Bathroom', 'west'),
            ('Bathroom', 'east', 'Walk-In', 'west'),
            ('Walk-In', 'south', 'Hostess Counter', 'north'),
            ('Hostess Counter', 'east', 'Dining Room', 'west'),
            ('Hostess Counter', 'west', 'Stove', 'east'),
            ('Stove', 'north', 'Sink Station', 'south'),
            ('Sink Station', 'west', 'Dining Room', '')
        ]
        for location1, direction, location2, opposite_direction in connections:
            self.graph.add_connection(location1, direction, location2, opposite_direction)

    def show_instructions(self):
        print('---------------------------------------------------------------------------------------\n'
              'A restaurant adventure game\n'
              "You walk into the No. 9 Grill to see every table full and you're the only wait staff on duty\n"
              "You must move from location to location and collect the items you'll need to successfully complete your day\n"
              'All 6 items must be added to your inventory before making it to the Dining Room to serve the hangry customers or else...FIRED!\n'
              'How to move from one location to the next: enter "go North", "go South", "go East", or "go West"\n'
              'How to add an item to your inventory: enter "take item"\n'
              '---------------------------------------------------------------------------------------')

    # moving between the locations using the direction stored as the connection
    def move_locations(self, direction):
        connections = self.graph.get_connections(self.current_location)
        if direction in connections:
            self.current_location = connections[direction]
        else:
            print("You can't go that way.\n"
                  '-----------------------------------------------------------------------------------------')

    # take the item and remove it from the location's inventory and put it in the player's inventory
    def grab_item(self):
        if self.current_location in self.items:
            self.inventory.append(self.items.pop(self.current_location))
            print(f'You grabbed the {self.inventory[-1]}.\n'
                  '-----------------------------------------------------------------------------------------')

    def play(self):
        NUMBER_OF_ITEMS_TO_WIN = 6

        self.show_instructions()

        while True:
            if self.current_location == 'Dining Room':
                if len(self.inventory) == NUMBER_OF_ITEMS_TO_WIN:
                    print(
                        'Well done! You made it to the Dining Room with all 6 items!\n'
                        'That 30% tip is going directly in your pocket, no mis-steaks were made. Now to wash these dishes...')
                    break
                else:
                    print(
                        'Oh noooo! You are standing in the Dining Room without all the items.\n'
                        'The customer asked to speak to your manager...time to apply for unemployment! Try again.')
                    break

            print(f'Your location: {self.current_location}')
            print(f'Your inventory: {self.inventory}')
            if self.current_location in self.items:
                print(f'You see the {self.items[self.current_location]}.')
            if self.current_location not in self.items and self.current_location != 'Hallway':
                print('You have the item from this location.')

            action = input('What are you going to do next?\n').lower().split()
            print('-----------------------------------------------------------------------------------------')

            # player must enter 'go' and then a direction to make a valid move
            if action[0] == 'go' and len(action) == 2:
                direction = action[1]
                self.move_locations(direction)
            # player must enter 'take item' to put item in inventory
            elif action[0] == 'take' and action[1] == 'item':
                self.grab_item()
            # player can enter 'cheat' to use the dfs to find the path to win, must use cheat as the very first entry
            elif action[0] == 'cheat':
                result = self.graph.shortest_path('Hallway', 'Dining Room')
                if result:
                    path_directions = result
                    path = " -> ".join(path_directions)
                    print(f'Path to visit all locations and end in the Dining Room: {path}\n'
                          '-----------------------------------------------------------------------------------------')
                else:
                    print('No valid path found ending in the Dining Room.')
            else:
                print('Invalid command. Use "go <direction>" or "take item".\n'
                      '-----------------------------------------------------------------------------------------')
