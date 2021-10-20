def test_function(a: int, b: int = None):
    return a + (b or 0)
