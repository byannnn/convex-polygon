from shape import Shape


def validate_coords(string):
    try:
        x, y = string.split(" ")
        x = int(x)
        y = int(y)
    except:
        return None

    return (
        x,
        y,
    )


def puzzle(shape: Shape):
    print("Your finalized shape is:")
    print(shape.get_coords())

    user_input = None
    while user_input != "#":
        user_input = input(
            "Please key in test coordinates in x y format or enter # to quit the game: "
        )
        if user_input == "#":
            break

        coords = validate_coords(user_input)
        if coords is None:
            print(f"New coordinates({user_input}) is invalid!!!")
            print("Not adding new coordinates to the current shape.")
            continue

        result = shape.point_in_polygon(
            x=coords[0],
            y=coords[1],
        )

        if result:
            print(f"Coordinates ({user_input}) is within your finalized shape")
        else:
            print(
                f"Sorry, coordinates ({user_input}) is outside of your finalized shape"
            )


def choice1():
    shape = Shape()
    while len(shape.coords) < 3:
        user_input = input(
            f"Please enter coordinates {len(shape.coords) + 1} in x y format: "
        )

        coords = validate_coords(user_input)
        if coords is None:
            print(f"New coordinates({user_input}) is invalid!!!")
            print("Not adding new coordinates to the current shape.")
            continue

        result = shape.add_coords(x=coords[0], y=coords[1])

        if not result:
            print(f"New coordinates({coords}) is invalid!!!")
            print("Not adding new coordinates to the current shape.")
            continue
        else:
            print("Your current shape is incomplete")
            print(shape.get_coords())

    print("Your current shape is valid and is complete")
    print(shape.get_coords())

    user_input = None
    while user_input != "#":
        user_input = input(
            f"Please enter # to finalize your shape or enter coordinates {len(shape.coords) + 1} in x y format: "
        )
        if user_input == "#":
            break

        coords = validate_coords(user_input)
        if coords is None:
            print(f"New coordinates({user_input}) is invalid!!!")
            print("Not adding new coordinates to the current shape.")
            continue

        result = shape.add_coords(
            x=coords[0],
            y=coords[1],
        )

        if not result:
            print(f"New coordinates({coords}) is invalid!!!")
            print("Not adding new coordinates to the current shape.")
            continue

        user_input = input(
            f"Please enter # to finalize your shape or enter coordinates {len(shape.coords) + 1} in x y format: "
        )

    puzzle(shape)


def choice2():
    while True:
        shape = Shape()
        shape.generate_convex_shape()

        print("Your random shape is: ")
        print(shape.get_coords())

        if shape.is_convex_polygon():
            break

    puzzle(shape)


def main():
    print("[1] Create a custom shape")
    print("[2] Generate a random shape")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        choice1()
    elif choice == "2":
        choice2()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
