Cab Pool Matcher - Tricky Situations

1. Half-empty cab
If only 1 or 2 students are waiting, the cab just leaves with them. My dispatch loop keeps taking students until the queue is empty or the cab is full, so it doesn't wait around to fill up. It then shows up as something like 2/4 and nobody else can join it. If nobody is waiting for that trip at all, I don't dispatch anything and just show a message.

2. No cabs left
I add every request to the queue no matter what, even if there's no cab for that trip. If all the cabs for a trip have already left, dispatch says "No open cab available for this trip." and stops before it takes anyone out of the queue. So the students just keep waiting and you can still see them in option 2.

3. Same year
Each entry in the queue is (-year, request_counter, request). The counter goes up by 1 with every new request, so when two students are in the same year, the one who asked first has the smaller number and gets picked first. Since the counter is always different, Python never has to compare two RideRequest objects, which is what would crash it.

4. Lots of students (n = students waiting, c = number of cabs)
- Adding one request is O(log n), since heappush only has to move the new item up a few levels.
- Adding all 1,000 is O(n log n), because it's n pushes and each one is O(log n).
- Sending off one cab is O(k log n) where k is at most 4, so it's basically O(log n). It's at most 4 heappops.
- Finding an open cab is O(c), because I just go through the cab list until I find one that's open and matches the trip. There are only a few cabs, so it's quick.
