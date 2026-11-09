
from datetime import datetime

class RideRequest:

    def __init__(self, name, destination, time, year):

        self.name = name
        self.destination = destination
        self.time = time
        self.year = year
        self.submitted_at = datetime.now()

    def display(self):

        print(
            f"Name: {self.name} | "
            f"Destination: {self.destination} | "
            f"Time: {self.time} | "
            f"Year: {self.year}"
        )


class Cab:

    def __init__(self, drivername, seats, destination, time):

        self.drivername = drivername
        self.seats = seats
        self.destination = destination
        self.time = time

        self.hasleft = False
        self.students = []

    def display(self):

        status = "Departed" if self.hasleft else "Open"

        print(
            f"Driver: {self.drivername} , "
            f"Destination: {self.destination} , "
            f"Time: {self.time} , "
            f"Seats: {len(self.students)}/{self.seats} , "
            f"Status: {status}"
        )


waiting_requests = []
cabs = []


def ride_request():

    name = input("Enter student name: ")

    if not name:
        print("Error: Name cannot be empty.")
        return

    destination = input(
        "Enter destination (Delhi/Jaipur): "
    ).title()

    if destination not in ["Delhi", "Jaipur"]:
        print("Error: Invalid destination.")
        return

    time = input(
        "Enter time (Morning/Afternoon/Evening/Night): "
    ).title()

    valid_times = ["Morning", "Afternoon", "Evening", "Night"]

    if time not in valid_times:
        print("Error: Invalid time slot.")
        return

    try:
        year = int(input("Enter your year (1-5): "))

        if year < 1 or year > 5:
            print("Error: Year must be between 1 and 5.")
            return

    except ValueError:
        print("Error: Please enter a valid number for year.")
        return

    request = RideRequest(name, destination, time, year)

    waiting_requests.append(request)

    print("Ride request successfully added!")


def display_data():

    print("\n WAITING STUDENTS ")

    if not waiting_requests:
        print("No students are currently waiting.")

    else:
        for request in waiting_requests:
            request.display()

    print("\n ALL CABS ")

    if not cabs:
        print("No cabs have been added yet.")

    else:
        for cab in cabs:
            cab.display()


def main():

    while True:

        print("\n CAB POOL MATCHER ")
        print("1. Add a new ride request")
        print("2. View waiting students and all cabs")
        print("3. Quit")

        choice = input("Enter your choice (Option no): ")

        if choice == "1":
            ride_request()

        elif choice == "2":
            display_data()

        elif choice == "3":
            print("Exiting Cab Pool Matcher. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
