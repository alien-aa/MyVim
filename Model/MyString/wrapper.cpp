#include <pybind11/pybind11.h>
#include "mystring.h"


namespace py = pybind11;

PYBIND11_MODULE(mystring, m) {
    py::class_<MyString>(m, "MyString")
        // Constructors
        .def(py::init<>())  
        .def(py::init<const char*>()) 
        .def(py::init<const char*, std::size_t>())  
        .def(py::init<std::size_t, const char>())  
        .def(py::init<const std::string&>())  
        .def(py::init<const MyString&>())  
        .def(py::init<int>())  
        .def(py::init<float>()) 

        // Operators (6)
        .def("__add__", py::overload_cast<const char*>(&MyString::operator+))
        .def("__add__", py::overload_cast<MyString&>(&MyString::operator+))
        .def("__add__", py::overload_cast<std::string&>(&MyString::operator+))

        .def("__iadd__", py::overload_cast<const char*>(&MyString::operator+=))
        .def("__iadd__", py::overload_cast<std::string&>(&MyString::operator+=))
        .def("__iadd__", py::overload_cast<MyString&>(&MyString::operator+=))

        .def("__gt__", &MyString::operator>, py::is_operator())
        .def("__lt__", &MyString::operator<, py::is_operator())
        .def("__ge__", &MyString::operator>=, py::is_operator())
        .def("__le__", &MyString::operator<=, py::is_operator())
        .def("__ne__", &MyString::operator!=, py::is_operator())
        .def("__eq__", &MyString::operator==, py::is_operator())

        .def("assign", py::overload_cast<const char*>(&MyString::assign))
        .def("assign", py::overload_cast<const std::string&>(&MyString::assign))
        .def("assign", py::overload_cast<const MyString&>(&MyString::assign))
        .def("assign", py::overload_cast<const char>(&MyString::assign))

        .def("__getitem__", &MyString::operator[], py::is_operator())
        .def("__setitem__", &MyString::operator[], py::is_operator())

        .def("__str__", &MyString::c_str)

        // Getters methods
        .def("c_str", &MyString::c_str) 
        .def("data", &MyString::data)
        .def("size", &MyString::size)  
        .def("length", &MyString::length)
        .def("__len__", &MyString::length)
        .def("capacity", &MyString::capacity) 

        // String manipulation methods 
        .def("empty", &MyString::empty)  
        .def("shrink_to_fit", &MyString::shrink_to_fit) 
        .def("clear", &MyString::clear)  

        // Insert methods 
        .def("insert", py::overload_cast<std::size_t, std::size_t, const char>(&MyString::insert))
        .def("insert", py::overload_cast<std::size_t, const char*, std::size_t>(&MyString::insert))
        .def("insert", py::overload_cast<std::size_t, const char*>(&MyString::insert))
        .def("insert", py::overload_cast<std::size_t, const std::string&, std::size_t>(&MyString::insert))
        .def("insert", py::overload_cast<std::size_t, const std::string&>(&MyString::insert)) 

        // Erase method
        .def("erase", py::overload_cast<std::size_t, std::size_t>(&MyString::erase))

        // Append methods
        .def("append", py::overload_cast<std::size_t, const char>(&MyString::append))
        .def("append", py::overload_cast<const char*>(&MyString::append))
        .def("append", py::overload_cast<const char*, std::size_t, std::size_t>(&MyString::append))
        .def("append", py::overload_cast<std::string&>(&MyString::append))
        .def("append", py::overload_cast<std::string&, std::size_t, std::size_t>(&MyString::append)) 

        // Substr methods
        .def("substr", py::overload_cast<std::size_t, std::size_t>(&MyString::substr))
        .def("substr", py::overload_cast<std::size_t>(&MyString::substr))
        
        // Replace methods
        .def("replace", py::overload_cast<std::size_t, std::size_t, const char*>(&MyString::replace))
        .def("replace", py::overload_cast<std::size_t, std::size_t, std::string&>(&MyString::replace))

        // Find methods
        .def("find", py::overload_cast<const char*, std::size_t>(&MyString::find, py::const_))
        .def("find", py::overload_cast<const char*>(&MyString::find, py::const_))
        .def("find", py::overload_cast<const std::string&>(&MyString::find, py::const_))
        .def("find", py::overload_cast<const std::string&, std::size_t>(&MyString::find, py::const_));
}
