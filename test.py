from server import Group



hello: dict[Group, str] = {}

key_1 = Group(room_number="a")
key_1.participants.append("yt")
key_1.participants.append("yr")
key_2 = Group(room_number="b")
hello[key_1] = "hi"
hello[key_2] = "hello"

finder = Group(room_number="a")

found: Group = None
for group in hello.keys():
    if group.room_number is finder.room_number:
        found = group
        break

print(str(group))