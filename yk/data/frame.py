class Frame:
    # Frame class provides a structure for abstract datasets storage and representation

    def __init__(self, names, items):
        self.names = names
        self.items = items

    def print_to_console(self):
        # prints the data to console

        for name in self.names:
            print(str(name) + "\t", end="")

        print()

        for item in self.items:
            for name in self.names:
                value = item[name]
                if value == "":
                    value = "-"

                print(str(value) + "\t", end="")

            print()

