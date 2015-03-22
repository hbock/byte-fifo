import fifo
import unittest

class BytesFIFO(unittest.TestCase):
    def setUp(self):
        self.f = fifo.BytesFIFO(10)

    def test_fifo_empty(self):
        self.assertTrue(self.f.empty())
        self.assertEqual(b"", self.f.read(5))
        self.assertEqual(b"", self.f.read(5))

    def test_fifo_not_empty(self):
        self.f.write(b"ham")
        self.assertFalse(self.f.empty())

    def test_len_zero(self):
        self.assertEqual(0, len(self.f))

    def test_len_positive(self):
        self.f.write(b"ham")
        self.assertEqual(3, len(self.f))

    def test_free(self):
        self.assertEqual(10, self.f.free())

    def test_fifo_write_then_read(self):
        self.assertEqual(8, self.f.write(b"hamsalad"))
        self.assertEqual(b"hamsa", self.f.read(5))
        self.assertEqual(b"lad", self.f.read(5))
        self.assertEqual(b"", self.f.read(5))

    def test_write_to_end(self):
        self.assertEqual(10, self.f.write(b"hamsaladsandwich"))
        self.assertEqual(10, len(self.f))
        self.assertEqual(b"hamsaladsa", self.f.read(50))
        self.assertEqual(b"", self.f.read(50))

    def test_write_wrap(self):
        self.assertEqual(5, self.f.write(b"hamsa"))
        self.assertEqual(b"hamsa", self.f.read(5))
        self.assertEqual(8, self.f.write(b"sandwich"))
        self.assertEqual(b"sandwich", self.f.read(50))

    def test_write_read_wrap(self):
        self.assertEqual(8, self.f.write(b"hamsalad"))
        self.assertEqual(b"hamsal", self.f.read(6))
        self.assertEqual(8, self.f.write(b"sandwich"))
        self.assertEqual(b"adsandwich", self.f.read(50))

    def test_read_empty(self):
        self.assertEqual(b"", self.f.read(20))
        self.assertEqual(b"", self.f.read(5))
        self.assertTrue(self.f.empty())

    def test_read_0(self):
        self.assertEqual(5, self.f.write(b"salad"))
        self.assertEqual(b"", self.f.read(0))
        self.assertEqual(b"salad", self.f.read(5))

    def test_full(self):
        self.assertFalse(self.f.full())
        self.f.write(b"johnsnoww")
        self.assertFalse(self.f.full())
        self.f.write(b"h")
        self.assertTrue(self.f.full())
    
    def test_nonzero(self):
        self.assertFalse(bool(self.f))
        self.f.write(b"1")
        self.assertTrue(bool(self.f))
        self.f.read(1)
        self.assertFalse(bool(self.f))

    def test_capacity(self):
        self.assertEqual(10, self.f.capacity())
        self.assertEqual(5, fifo.BytesFIFO(5).capacity())
    
    def test_resize_raise_less_than_1(self):
        self.assertRaises(ValueError, self.f.resize, 0)
        self.assertRaises(ValueError, self.f.resize, -1)
        self.assertRaises(ValueError, self.f.resize, -100)

    def test_resize_raise_too_small(self):
        self.f.write(b"cheese")
        self.assertRaises(ValueError, self.f.resize, 5)
        self.assertRaises(ValueError, self.f.resize, 4)
        self.assertRaises(ValueError, self.f.resize, 1)
        self.assertRaises(ValueError, self.f.resize, 0)
    
    def test_resize_empty_smaller(self):
        self.f.resize(1)
        self.assertTrue(self.f.empty())
        self.assertEqual(b"", self.f.read(1))
        self.assertEqual(1, self.f.capacity())

    def test_resize_empty_larger(self):
        self.f.resize(50)
        self.assertTrue(self.f.empty())
        self.assertEqual(b"", self.f.read(1))
        self.assertEqual(50, self.f.capacity())

    def test_resize_larger_write(self):
        self.f.resize(20)
        self.f.write(b"Simpsons did it")
        self.assertEqual(15, len(self.f))
        self.assertEqual(b"Simpsons did it", self.f.read(len(self.f)))
    
    def test_resize_larger_fill(self):
        self.f.resize(20)
        self.f.write(b"A"*25)
        self.assertEqual(20, len(self.f))
        self.assertEqual(b"A"*20, self.f.read(25))
        
    def test_resize_larger_retain_contiguous(self):
        self.f.write(b"Underwood")
        self.f.resize(20)
        self.assertEqual(9, len(self.f))
        self.assertEqual(b"Underwood", self.f.read(20))
        self.assertEqual(b"", self.f.read(20))

    def test_resize_smaller_retain_contiguous(self):
        self.f.write(b"Under")
        self.f.resize(6)
        self.assertEqual(5, len(self.f))
        self.assertEqual(b"Under", self.f.read(20))
        self.assertEqual(b"", self.f.read(20))

    def test_resize_smaller_retain_noncontiguous(self):
        self.f.write(b"Underwood")
        self.assertEqual(b"Underwood", self.f.read(9))
        # 1 byte at end, 6 bytes wrap
        self.assertEqual(7, self.f.write(b"Francis"))
        self.assertEqual(7, len(self.f))
        self.f.resize(7)
        self.assertEqual(7, len(self.f))
        self.assertEqual(b"Francis", self.f.read(7))
        self.assertTrue(self.f.empty())

    def test_resize_larger_retain_noncontiguous(self):
        self.f.write(b"Underwood")
        self.assertEqual(b"Underwood", self.f.read(9))
        # 1 byte at end, 6 bytes wrap
        self.assertEqual(7, self.f.write(b"Francis"))
        self.assertEqual(7, len(self.f))
        self.f.resize(20)
        self.assertEqual(7, len(self.f))
        self.assertEqual(b"Francis", self.f.read(7))
        self.assertTrue(self.f.empty())

    def test_resize_full_larger_retain_noncontiguous(self):
        self.f.write(b"Underwood")
        self.assertEqual(b"Underwood", self.f.read(9))
        # 1 byte at end, 6 bytes wrap
        self.assertEqual(10, self.f.write(b"1234567890"))
        self.assertEqual(10, len(self.f))
        self.assertTrue(self.f.full())
        self.f.resize(20)
        self.assertEqual(10, len(self.f))
        self.assertEqual(b"1234567890", self.f.read(20))
        self.assertTrue(self.f.empty())

    def test_read_negative(self):
        self.f.write(b"Underwood")
        self.assertEqual(b"Underwood", self.f.read(-1))

    def test_read_default(self):
        self.f.write(b"Underwood")
        self.assertEqual(b"Underwood", self.f.read())
