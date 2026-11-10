
from datetime import datetime
import json


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


def loadcabs(filename):

    loadedcabs = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            cabdata = json.load(file)

        if not isinstance(cabdata, list):
            raise ValueError("Cab data must be a JSON list.")

        for data in cabdata:

            if not isinstance(data, dict):
                raise ValueError("Each cab must be a JSON object.")

            drivername = data["drivername"]
            seats = data["seats"]
            destination = data["destination"]
            time = data["time"]

            if not isinstance(drivername, str) or not drivername:
                raise ValueError("Invalid driver name.")

            if type(seats) is not int or seats < 1 or seats > 4:
                raise ValueError("Cab seats must be between 1 and 4.")

            if destination not in ["Delhi", "Jaipur"]:
                raise ValueError("Invalid cab destination.")

            if time not in ["Morning", "Afternoon", "Evening", "Night"]:
                raise ValueError("Invalid cab time slot.")

            cab = Cab(
                drivername,
                seats,
                destination,
                time
            )

            loadedcabs.append(cab)

        print(f"{len(loadedcabs)} cabs loaded successfully.")

        return loadedcabs

    except FileNotFoundError:
        print("Error: cabs.json file not found.")

    except json.JSONDecodeError:
        print("Error: cabs.json contains invalid JSON.")

    except (KeyError, ValueError, TypeError) as error:
        print(f"Error loading cabs: {error}")

    return []


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
        print("No cabs have been loaded.")

    else:
        for index, cab in enumerate(cabs, start=1):       
            print(f"\nCab {index}:")
            cab.display()


def find_matches():

    print("\n MATCH PREVIEW ")
    found_open_cab = False

    for index, cab in enumerate(cabs, start=1):
        if cab.hasleft:
            continue

        found_open_cab = True
        matching_requests = [
            request for request in waiting_requests

            if request.destination == cab.destination
            and request.time == cab.time
        ]

        selected_students = matching_requests[:cab.seats]
        print(f"\nCab {index}: {cab.drivername}")

        if not selected_students:
            print("No students waiting for this trip.")

        else:
            print(
                f"Destination: {cab.destination} | "
                f"Time: {cab.time}"
            )

            print(
                f"Students who would get seats: "
                f"{len(selected_students)}/{cab.seats}"
            )

            for student in selected_students:
                print(
                    f"- {student.name} "
                    f"(Year {student.year})"
                )

    if not found_open_cab:
        print("No open cabs available.")

    print("\nNote: This is only a preview. No seats have been assigned.")


def dispatch_cab():
    print("\n DISPATCH CAB ")

    open_cabs = [
        (index, cab)

        for index, cab in enumerate(cabs)
        if not cab.hasleft
    ]

    if not open_cabs:
        print("No open cabs available.")
        return

    print("\nAvailable cabs:")
    for index, cab in open_cabs:
        print(
            f"{index + 1}. Driver: {cab.drivername} | "
            f"Destination: {cab.destination} | "
            f"Time: {cab.time} | "
            f"Seats: {cab.seats}"
        )

    try:
        choice = int(input("\nEnter cab number to dispatch: "))
    except ValueError:
        print("Error: Please enter a valid cab number.")
        return

    selected_cab = None
    for index, cab in open_cabs:
        if index + 1 == choice:
            selected_cab = cab
            break

    if selected_cab is None:
        print("Invalid cab number.")
        return

    matching_requests = [
        request for request in waiting_requests

        if request.destination == selected_cab.destination
        and request.time == selected_cab.time
    ]

    selected_students = matching_requests[:selected_cab.seats]
    for student in selected_students:

        selected_cab.students.append(student)

        waiting_requests.remove(student)

    selected_cab.hasleft = True

    print("\nCab successfully dispatched!")
    print(f"Driver: {selected_cab.drivername}")
    print("\nStudents assigned:")

    if not selected_students:
        print("No students were assigned.")

    else:
        for student in selected_students:
            print(f"- {student.name}")


def main():

    global cabs    
    cabs = loadcabs("cabs.json")
    
    while True:
        print("\n CAB POOL MATCHER ")
        print("1. Add a new ride request")
        print("2. View waiting students and all cabs")
        print("3. Find matches")
        print("4. Dispatch a cab")
        print("5. Quit")

        choice = input("Enter your choice (Option no): ")

        if choice == "1":
            ride_request()

        elif choice == "2":
            display_data()

        elif choice == "3":
            find_matches()

        elif choice == "4":
            dispatch_cab()

        elif choice == "5":
            print("Exiting Cab Pool Matcher. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
