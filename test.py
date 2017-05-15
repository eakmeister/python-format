# pylint: disable=line-too-long
import unittest
import python_format

class PythonFormatTests(unittest.TestCase):
    def test_imports(self):
        s = 'from somemodule.stuff import test_function,other_function,third_function,fourth_function'
        o = python_format.python_format(s)
        self.assertEqual(o, '')

    def test_containers(self):
        s = 'A = [4534,534534,2345,34,5345,34534,534,534,7567856,455423,534545,6456,45645,658,567,4536,34,6456,5678,679,567,456,645]'
        o = python_format.python_format(s)
        self.assertEqual(o,  'A = [4534, 534534, 2345, 34, 5345, 34534, 534, 534, 7567856, 455423, 534545,\n    6456, 45645, 658, 567, 4536, 34, 6456, 5678, 679, 567, 456, 645]')
        s = 'B = [{"foo" : "bar"}, ("tuple" ,432, 67534.432432), ["inner","list", {"nested" : "dictwithareallylongvaluethatisstillgoingbecauseitisdogoddamnlong"}]]'
        o = python_format.python_format(s)
        self.assertEqual(o, '')
        s = 'C = [10000, 200000, 3000000, 40000000, 500000, 60000, 700000, 8000000, [900, 1000, 20000]]'
        o = python_format.python_format(s)
        self.assertEqual(o, '')
        s = 'D = [0000000, [11111111, 222222222, 333333, 444444444, 5555555555, 666666666, 77], [8888888, 9999999999, 000000000, 111111111, 222222222, 333333333, 44444444]]'
        o = python_format.python_format(s)
        self.assertEqual(o, '')

    def test_class_stmt(self):
        s = 'class Test(object):'
        self.assertEqual(python_format.python_format(s), s)

    def test_init_stmt(self):
        s = 'def __init__(self):'
        self.assertEqual(python_format.python_format(s), s)


    def test_long_str(self):
        s = "self.x = 'this:is:a:stringggggggggggggggggggggggggggggggggggggggggggggggg'"
        self.assertEqual(python_format.python_format(s), '')
    
    def test_multi_line(self):
        s = 'self.y =90 + \\\n80 + \\\n3'
        self.assertEqual(python_format.python_format(s), '')

    def test_func(self):
        s = 'def get_x(self):'
        self.assertEqual(python_format.python_format(s), '')

    def test_list_comprehension(self):
        s = 'foo = [fdsafdsfsfsdsfsd for (fdsfdsfdsa, fdsafdsfsfsdsfsd) in jjjjjjjjjjjjjjjj]'
        self.assertEqual(python_format.python_format(s), '')

    def test_for_loop(self):
        s = 'for (aaaaaaaaa, bbbbbbbbbbb, ccccccccc, ddddddddddddddddd) in kkkkkkkkkkkkkkkkkkkkkk:'
        self.assertEqual(python_format.python_format(s), '')

        s = 'for jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj in kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk:'
        self.assertEqual(python_format.python_format(s), '')

        s = 'for llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll in test:'
        self.assertEqual(python_format.python_format(s), '')

    def test_control_flow(self):
        s = 'if self.y == 3:'
        self.assertEqual(python_format.python_format(s), s)

        s = 'return foo'
        self.assertEqual(python_format.python_format(s), s)

        s = 'else:'
        self.assertEqual(python_format.python_format(s), s)

        s = '   self.x += 2'
        self.assertEqual(python_format.python_format(s), s)

        s = '   return self.x'
        self.assertEqual(python_format.python_format(s), s)

if __name__ == '__main__':
    unittest.main()
