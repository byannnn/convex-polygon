from shape import Shape


def test_validate_coordinates():
    shape1 = Shape(coords=[(1, 1), (5, 1), (5, 5)])
    assert shape1.validate_coordinates() == True

    shape2 = Shape(coords=[(1, 1), (5, 1), (5, 5), (4, 0)])
    assert shape2.validate_coordinates() == False

    shape3 = Shape(coords=[(4, 8), (6, 7), (8, 5), (9, 0), (6, 2)])
    assert shape3.validate_coordinates() == True

    shape4 = Shape(coords=[(0, 1), (5, 6), (8, 8), (9, 5)])
    assert shape4.validate_coordinates() == True


def test_add_coords():
    shape1 = Shape()
    shape1.add_coords(1, 1)
    shape1.add_coords(2, 4)
    shape1.add_coords(3, 6)
    shape1.add_coords(4, 8)
    shape1.add_coords(1, 1)
    assert len(shape1.coords) == 3

    shape2 = Shape()
    shape2.add_coords(1, 1)
    shape2.add_coords(5, 1)
    shape2.add_coords(5, 1)
    shape2.add_coords(5, 5)
    shape2.add_coords(4, 0)
    assert len(shape2.coords) == 3


def test_is_convex_polygon():
    shape1 = Shape(coords=[(4, 8), (6, 7), (8, 5), (9, 0), (6, 2)])
    assert shape1.is_convex_polygon() == True

    shape2 = Shape(coords=[(4, 8), (6, 2), (6, 7), (8, 5), (9, 0)])
    assert shape2.is_convex_polygon() == False

    shape3 = Shape(coords=[(6, 2), (6, 7), (8, 5), (9, 0), (4, 8)])
    assert shape3.is_convex_polygon() == False

    shape4 = Shape(
        coords=[(3, 15), (10, 24), (16, 14), (22, 4)]
    )  # Byan: fails because triangle is formed
    assert shape4.is_convex_polygon() == False

    shape5 = Shape(coords=[(3, 15), (10, 24), (16, 16), (22, 4)])
    assert shape5.is_convex_polygon() == True


def test_generate_convex_shape():
    count = 0
    while count < 100:
        shape = Shape()
        shape.generate_convex_shape()
        print(shape.get_coords())
        assert shape.is_convex_polygon() == True
        count += 1


def test_point_in_polygon():
    shape = Shape(coords=[(4, 8), (6, 7), (8, 5), (9, 0), (6, 2)])
    assert shape.point_in_polygon(8, 5) == True
    assert shape.point_in_polygon(6, 3) == True
    assert shape.point_in_polygon(5, 5) == True
    assert shape.point_in_polygon(7, 6) == True
    assert shape.point_in_polygon(9, 1) == False
    assert shape.point_in_polygon(7, 1) == False
