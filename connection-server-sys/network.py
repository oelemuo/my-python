"""
File: network.py
Author: Obinna Elemuo
Date: 12/13/2023
Section: 26
E-mail: so01811@umbc.edu
Description:
The program creates a phone network using object-oriention. It allows for managing switchboards, connecting phones,
handling calls, and saving/loading the network's state. Demonstrates classes and instance variables,
recursion, and list structures.
"""
HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'

class Phone:
    """
    This class contain the necessary functions to apply a phone.
    Constructor for the Phone class. Initializes a phone with a unique number,
    associates it with a switchboard, and sets default values for call status and connected phone.
    """
    def __init__(self, number, switchboard):
        self.number = number
        self.switchboard = switchboard
        self.call = None
        self.otherPhone = None

    def connect(self, area_code, other_phone_number):
        """
        Connects this phone to another phone using the specified area code
        and phone number.
        """
        # if this phone is already in a call, the current call is disconnected
        if self.call != None:
            print("Disconnecting current call to make new call")
            self.disconnect()
        # empty list to track the switchboards already checked recursively
        previous_codes = []
        # the connect_call method of the switchboard finds a path to the target phone.
        output = self.switchboard.connect_call(area_code, other_phone_number, previous_codes)
        if output == None:
            # connection was not successful
            print(str(self.number)+" and "+str(other_phone_number)+" were not connected.")
        else:
            # output will be the switchboard through which the call is made.
            print(str(self.number)+" and "+str(other_phone_number)+" are now connected.")
            self.call = output
            self.otherPhone = output.findPhone(other_phone_number)
            self.otherPhone.call = self.switchboard
            self.otherPhone.otherPhone = self

            return output

    def searchList(self, list, number):
        """
        Method to find a phone number in the list
        """
        # iterate through list to find phone number
        for i in list:
            if i.number == number:
                print(i.number)

    def display(self, phonenumber):
        """
        Method to display data. Generates a string describing the current status of the phone.
        """
        # Initialize an empty string
        output = ""
        # phone is ideal if it's not called
        if self.call == None:
            output = (" "*9+"Phone with number: " + str(self.number) + " is not in use.")
        else:
            # if phone is in call, display details of connection
            output = (" "*9+"Phone with number: " + str(self.number) + " is connected to " + str(self.call.area_code) + "-" + str(self.otherPhone.otherPhone.number))
        return output

    def disconnect(self):
        """
        Method to disconnect a phone with other phone
        """
        if self.call == None:
            # phone is not currently in a call
            print(str(self.switchboard.area_code) + "-" + str(self.number) + " is not in a call")
        else:
            # phone is in a call, disconnect connection
            print("Hanging up...")
            print("Connection Terminated.")
            print("Disconnected (" + str(self.switchboard.area_code) + "-" + str(self.number) + ") and (" + str(self.call.area_code) + "-" + str(self.otherPhone.number) + ")")
            # Reset the call
            self.otherPhone.call = None
            self.otherPhone.otherPhone = None
            self.call = None
            self.otherPhone = None


class Switchboard:
    """
    This class represents a switchboard in the phone network. Each switchboard contains
    area codes and list of truck lines and phones
    """
    def __init__(self, area_code):
        self.area_code = area_code
        self.trunklines = [] # List to store connections
        self.phones = [] # list to store phones


    def checkPhone(self, phone_number):
        """
        Method to check whether the phone is represented by number
        in the switchboard list
        """
        # initialize output
        output = False
        # iterate through registered phones with switchboard
        for i in self.phones:
            if i.number == phone_number:
                # if a phone with a given number is found, set output to True
                output = True
        return output

    def checkTrunkline(self, switchboard):
        """
        Method to check whether the trunkline is present in the switchboard list
        Returns True if the switchboard is already connected via a trunkline

        """
        #initialize output to false
        output = False
        # iterates through each trunkline connection
        for i in self.trunklines:

            if i == switchboard:
                output = True
        return output

    def add_phone(self, phone_number):
        """
        Method to add a phone to list. Checks if phone is already in network
        """
        # if phone does not exist
        if not self.checkPhone(phone_number):
            self.phones.append(Phone(phone_number, self)) # add phone number
        else:
            # if phone number already exist
            print("Phone number already exists")

    def add_trunk_connection(self, switchboard):
        """
        Method to add switchboard to current trunkline , checks if truckline
        already exist. Otherwise, adds connection
        """
        # if connection does not already exist
        if not self.checkTrunkline(switchboard):
            self.trunklines.append(switchboard) # add connection
        else:
            # connection already exist
            print("Trunk line already exists in current switchboard.")

    def findNumber(self, number):
        """
        Method to check whether the phone number is present in the list
        """
        # intialize output to false
        output = False
        # iterate through each phone registered with this switchboard.
        for i in self.phones:
            # if phone number is found
            if i.number == number:
                output = True
        return output

    def findPhone(self, number):
        """
        Method to return the phone object if it is in the phone list
        """
        # initialize output to None
        output = None
        # iterate through each phone in the switchboard's list of phones
        for i in self.phones:
            # if phone with matching number is found
            if i.number == number:
                output = i
        return output

    def connect_call(self, area_code, number, previous_codes):
        """
        method to check whether two phones have connection and, if yes, connect them
        if not, it recursively searches connected switchboards,
        """
        # add current switchboard's area code to the list of checked area codes
        previous_codes.append(self.area_code)
        # find phone on switchboard if match is found
        if self.area_code == area_code:
            if self.findPhone(number).number == number:
                return self # return switchboard if phone is found
            else:
                return None
        else:
            # iterate through trucklines
            for i in self.trunklines:
                if not i in previous_codes:
                    # recursively calls connect_call on connected switchboards
                    return i.connect_call(area_code, number, previous_codes)
                else:
                    return None


class Network:
    """
    This class represents the Network system. It manages the collection of switchboards,
    """
    def __init__(self):
        self.switchboards = []
        self.temp = []

    def searchSwitchboards(self, area_code):
        """
        Method to find a switchboard object by its area code
        """
        # initialize output to None
        output = None
        # iterates through switchboard list
        for i in self.switchboards:
            # if switchboard with matching area code is found:
            if i.area_code == area_code:
                output = i
        return output

    def presentSwitchboards(self, area_code):
        """
        Method to check whether a switchboard exists
        """
        # initialize boolean flag
        flag = False
        # iterate through switchboard list in network
        for i in self.switchboards:
            # if switchboard with matching area code exists, set flag to True,
            # indicating switchboard is present
            if i.area_code == area_code:
                flag = True
        return flag

    def load_network(self, filename):
        """
        Method to load the existing network, reading the input line by line
        from a specific file, processes each command and updates networks state.

        """
        file = open(filename, 'r')
        for command in file.readlines():
            # process each line in file
            split_command = command.split()
            # store command parts into temp list
            self.temp.append(split_command)
            # execute SWITCH_CONNECT command
            if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
                # parse area codes and connect corresponding switchboards
                area_1 = int(split_command[1])
                area_2 = int(split_command[2])
                the_network.connect_switchboards(area_1, area_2)

            # execute SWITCH_ADD
            elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
                # parse area codes and add new switchboard with corresponding area codes
                the_network.add_switchboard(int(split_command[1]))
            # executes PHONE_ADD command
            elif len(split_command) == 3 and split_command[0].lower() == PHONE_ADD:
                # parse area code and phone number from the command
                area_code = int(split_command[1])
                phone_number = int(split_command[2])
                # find switchboard with specific area code and add phone to switchboard
                switchBoard = the_network.searchSwitchboards(area_code)
                if switchBoard != None:
                    if not switchBoard.checkPhone(phone_number):
                        switchBoard.add_phone(phone_number)

    def save_network(self, filename, list):
        """
        Method to save a network
        """
        file = open(filename, 'a+')
        for i in list:
            file.write(i + "\n")
        file.close()

    def add_switchboard(self, area_code):
        """
        Method to add a switchboard to network list if it does not exist
        """
        # if switchboard already exist in system.
        if not self.presentSwitchboards(area_code):
            self.switchboards.append(Switchboard(area_code))
        else:
            print("Area code already exists.")

    def connect_switchboards(self, area_1, area_2):
        """
        Method to connects 2 switchboards together with area codes by adding each
        as a truckline to the other
        """
        # if either of switchboards does not exist.
        if self.presentSwitchboards(area_1) == False or self.presentSwitchboards(area_2) == False:
            print("One or more of the switchboards do not exist")
        else:
            # connect switchboards to each other
            self.searchSwitchboards(area_1).add_trunk_connection(self.searchSwitchboards(area_2))
            self.searchSwitchboards(area_2).add_trunk_connection(self.searchSwitchboards(area_1))

    def display(self):
        """
        Method to display current state of entire network
        """
        for i in self.switchboards:
            # print the area code of the switchboard
            print("Switchboard with area code: " + str(i.area_code))
            # print each trunk line connected to the switchboard
            print(" "*5+"Trunk lines are: ")
            for j in i.trunklines:
                print(" "*9+"Trunkline connection to: " + str(j.area_code))
            print(" "*5+"Local phone numbers are:")
            # Print each phone number registered with the switchboard
            for j in i.phones:
                print(j.display(j.number))



if __name__ == '__main__':
    # all commands applied by user are written in COMMANDS
    COMMANDS = []
    the_network = Network()
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            the_network.connect_switchboards(area_1, area_2)
            # append the command to the COMMANDS list
            COMMANDS.append(str(SWITCH_CONNECT + " " + str(area_1) + " " +  str(area_2)))

        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            the_network.add_switchboard(int(split_command[1]))

            COMMANDS.append(str(SWITCH_ADD + " " + str(split_command[1])))

        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))
            # append the command to the COMMANDS list
            COMMANDS.append(str(PHONE_ADD + " " + str(area_code) + " " + str(phone_number)))

            switchBoard = the_network.searchSwitchboards(area_code)
            # add the phone to the specified switchboard
            if switchBoard == None:
                print("Invalid area_code, create a new switchboard or enter a valid area code.")
            else:
                # phone number exists
                if switchBoard.checkPhone(phone_number):
                    print("Phone number already exists in area code")
                else:
                    switchBoard.add_phone(phone_number)
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            the_network.save_network(split_command[1], COMMANDS)
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            the_network = Network()
            the_network.load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))

            # start a call from source phone
            switch = the_network.searchSwitchboards(src_area_code)
            if switch == None:
                print("Area code does not exist")
            else:
                phone = switch.findPhone(src_number)
                if phone == None:
                    print("Source phone number does not exist")
                else:
                    phone.connect(dest_area_code,dest_number)

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))

            # End the call on the specified phone
            switch = the_network.searchSwitchboards(area_code)
            if switch == None:
                print("Area code not found")
            else:
                phone = switch.findPhone(number)
                if phone == None:
                    print("Phone not found")
                else:
                    phone.disconnect()

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            # dispaly network
            the_network.display()
        # prompt for command
        s = input('Enter command: ')

