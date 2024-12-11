#include <cstring>
#include <exception>
#include <fstream>
#include <string>
#include <vector>

#include "mystring.h"
#include "trie.h"
#include "iterator.h"

using Iterator = MyString::Iterator;
using ConstIterator = MyString::ConstIterator;
using ReverseIterator = MyString::ReverseIterator;
using ConstReIterator = MyString::ConstReIterator;

/*
Now we have the opportunity to catch std::exception, for example, out-of-range.
To catch this exception use:
```
try {
    // danger code here
} catch(const std::out_of_range& err) {
    std::cerr << "Exception in _method_name_: " << err.what() << endl;
    // your code here
}
```
To catch other exceptions use:
```
try {
    // danger code here
} catch(const std::exception& err) {
    std::cerr << "Exception in _method_name_: " << err.what() << endl;
    // your code here
}
```
*/

constexpr std::size_t ADD_CAPACITY = 1;
/*
This number will be needed when implementing methods
in which you will need to expand the string (for example, append).
It is usually calculated based on the statistics
of the size of the processed data, sometimes even dynamically.
*/

/* Iterators (extra task) */
Iterator MyString::begin()
{
    return Iterator{ array_ };
}

Iterator MyString::end()
{
    return Iterator{ array_ + size_ };
}

ConstIterator MyString::cbegin()
{
    ConstIterator it;
    it.pointer_ = array_;
    return it;
}

ConstIterator MyString::cend()
{
    ConstIterator it;
    it.pointer_ = array_ + size_;
    return it;
}

ReverseIterator MyString::rbegin()
{
    return ReverseIterator{ array_ + size_ - 1 };
}

ReverseIterator MyString::rend()
{
    return ReverseIterator{ array_ - 1 };
}

ConstReIterator MyString::rcbegin()
{
    ConstReIterator it;
    it.pointer_ = array_;
    return it;
}

ConstReIterator MyString::rcend()
{
    ConstReIterator it;
    it.pointer_ = array_ + size_;
    return it;
}


/* Constructors */
MyString::MyString() :
    array_(new char[ADD_CAPACITY]),
    capacity_(ADD_CAPACITY),
    size_(0)
{
    *array_ = '\0';
}

MyString::MyString(const char* char_array, std::size_t count)
{
    if (char_array == nullptr)
    {
        throw MyException("ERROR: Constructor argument is nullptr!");
    }
    std::size_t i = (mystrlen(char_array) > count) ? count : mystrlen(char_array);
    array_ = new char[i + ADD_CAPACITY];
    for (std::size_t j = 0; j < i; j++)
    {
        *(array_ + j) = *(char_array + j);
    }
    *(array_ + i) = '\0';
    capacity_ = i + ADD_CAPACITY;
    size_ = i;
}

MyString::MyString(std::size_t count, const char sym) :
    array_(new char[count + ADD_CAPACITY]),
    capacity_(count + ADD_CAPACITY),
    size_(count)
{
    for (std::size_t i = 0; i < count; i++)
    {
        *(array_ + i) = sym;
    }
    *(array_ + count) = '\0';
}

MyString::MyString(const char* char_array) : MyString::MyString(char_array, mystrlen(char_array))
{}

MyString::MyString(const std::string& std_string) : MyString::MyString(std_string.data(), std_string.length())
{}

MyString::MyString(const MyString& class_string) : MyString::MyString(class_string.array_, class_string.size_)
{}


/* Extra task constructors */
MyString::MyString(MyString&& moved_string) noexcept
/*
To use move-contructor write:
```
MyString str1{std::move(str2)};
```
std::move() converts the lvalue to rvalue.
*/
{
    array_ = moved_string.array_;
    capacity_ = moved_string.capacity_;
    size_ = moved_string.size_;
    moved_string.array_ = nullptr;
}

MyString::MyString(int number) : MyString::MyString(std::to_string(number))
{}

MyString::MyString(float number) : MyString::MyString(std::to_string(number))
{}


/* Destructor */
MyString::~MyString()
{
    delete[] array_;
}


/* Operators */
MyString MyString::operator+(const char* char_array)
{
    MyString result{};
    result += this->c_str();
    result += char_array;
    return result;
}

MyString MyString::operator+(MyString& class_string)
{
    return (*this + class_string.c_str());
}

MyString MyString::operator+(std::string& std_string)
{
    return (*this + std_string.data());
}

MyString& MyString::operator+=(const char* char_array)
{
    return this->append(char_array);
}

MyString& MyString::operator+=(std::string& std_string)
{
    return this->append(std_string);
}

MyString& MyString::operator+=(MyString& class_string)
{
    return this->append(class_string.c_str());
}

bool MyString::operator>(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) < 0);
}

bool MyString::operator<(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) > 0);
}

bool MyString::operator>=(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) <= 0);
}

bool MyString::operator<=(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) >= 0);
}

bool MyString::operator!=(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) != 0);
}

bool MyString::operator==(MyString& class_string) const
{
    return (mystrcmp(this->array_, class_string.c_str()) == 0);
}

MyString& MyString::operator=(const char* char_array)
{
    if (this->capacity_ < mystrlen(char_array) + 1)
    {
        expand(mystrlen(char_array) + 1 - this->capacity_);
    }
    this->clear();
    this->append(char_array);
    return *this;
}

MyString& MyString::operator=(const std::string& std_string)
{
    this->clear();
    this->append(std_string.data());
    return *this;
}

MyString& MyString::operator=(const char sym)
{
    char* array = new char[2];
    array[0] = sym;
    array[1] = '\0';
    this->array_ = const_cast<char*>(array);
    this->capacity_ = 2;
    this->size_ = 1;
    return *this;
}

MyString& MyString::operator=(const MyString& class_string)
{
    if (this->capacity_ < class_string.capacity())
    {
        MyString tmp_obj = MyString{ class_string };
        swap(*this, tmp_obj);
        return *this;
    }
    else
    {
        this->clear();
        this->append(class_string.c_str());
        return *this;
    }
}

char& MyString::operator[](std::size_t index)
{
    if (index >= this->size())
    {
        throw std::out_of_range("ERROR: Out of range in []!");
    }
    return this->array_[index];
}

/* For wrapper*/
MyString& MyString::assign(const char* char_array)
{
    this->clear();
    this->append(char_array);
    return *this;
}

MyString& MyString::assign(const std::string& std_string)
{
    this->clear();
    this->append(std_string.data());
    return *this;
}

MyString& MyString::assign(const char sym)
{
    char* array = new char[2];
    array[0] = sym;
    array[1] = '\0';
    this->array_ = const_cast<char*>(array);
    this->capacity_ = 2;
    this->size_ = 1;
    return *this;
}

MyString& MyString::assign(const MyString& class_string)
{
    if (this->capacity_ < class_string.capacity())
    {
        MyString tmp_obj = MyString{ class_string };
        swap(*this, tmp_obj);
        return *this;
    }
    else
    {
        this->clear();
        this->append(class_string.c_str());
        return *this;
    }
}


/* Output & input operators */
std::ostream& operator<<(std::ostream& stream, const MyString& string)
{
    for (size_t i = 0; i < string.size(); i++) {
        stream << string.c_str()[i];
    }
    return stream;
}

std::istream& operator>>(std::istream& stream, MyString& string)
{
    char c;
    while (stream.get(c))
    {
        string.append(1, c);
    }
    return stream;
}

/* Extra task operators */
MyString& MyString::operator=(MyString&& moved_string) noexcept
{
    if (&moved_string != this)
    {
        delete[] array_;
        array_ = moved_string.array_;
        capacity_ = moved_string.capacity_;
        size_ = moved_string.size_;
        moved_string.array_ = nullptr;
    }
    return *this;
}

// std::ofstream& operator<<(std::ofstream &stream, const MyString& string)
// {
//   if (stream.is_open())
//   {
//     for (size_t i = 0; i < string.size(); i++) {
//       stream << string.c_str()[i];
//     }
//     stream << " " << string.length() << " " << string.capacity();
//     return stream;
//   }
//   else
//   {
//     throw MyException("ERROR: file is not open!");
//   }
// }

std::ifstream& operator>>(std::ifstream& stream, MyString& string)
{
    if (stream.is_open())
    {
        std::string buffer;
        getline(stream, buffer);
        string = MyString(buffer);
        return stream;
    }
    else
    {
        throw MyException("ERROR: file is not open!");
    }
}


/* Getters methods */
const char* MyString::c_str() const
{
    return array_;
}

const char* MyString::data() const
{
    return this->c_str();
}

std::size_t MyString::size() const
{
    return size_;
}

std::size_t MyString::length() const
{
    return this->size();
}

std::size_t MyString::capacity() const
{
    return capacity_;
}



/* String manipulation methods */
bool MyString::empty() const
{
    return strlen(this->c_str()) == 0;
}

MyString& MyString::shrink_to_fit()
{
    if (this->size_ < this->capacity_)
    {
        char* new_buffer = new char[this->size_ + 1];
        for (std::size_t i = 0; i < this->size_; i++)
        {
            *(new_buffer + i) = *(this->array_ + i);
        }
        *(new_buffer + this->size_) = '\0';
        delete[] this->array_;
        this->array_ = new_buffer;
        this->capacity_ = this->size_ + 1;
    }
    return *this;
}

MyString& MyString::clear()
{
    for (std::size_t i = 0; i < this->size(); i++)
    {
        *(this->array_ + i) = '\0';
    }
    this->size_ = 0;
    return *this;
}


/* Insert methods */
MyString& MyString::insert(std::size_t index, std::size_t count, const char sym)
{
    if (index > size_)
    {
        throw std::out_of_range("ERROR: Out of range in insert!");
    }
    std::size_t diff = (capacity_ > size_ + count + 1) ? 0 : (size_ + count - capacity_ + 1);
    if (diff > 0)
    {
        expand(diff);
    }
    char* buffer = new char[capacity_ - index];
    for (std::size_t i = 0; i <= size_ - index; i++)
    {
        *(buffer + i) = *(array_ + index + i);
    }
    for (std::size_t i = index; i < index + count; i++)
    {
        *(array_ + i) = sym;
    }
    for (std::size_t i = index + count, j = 0; i <= size_ + count; i++, j++)
    {
        *(array_ + i) = *(buffer + j);
    }
    delete[] buffer;
    size_ += count;
    return *this;
}

MyString& MyString::insert(std::size_t index, const char* char_array, std::size_t count)
{
    std::size_t len = mystrlen(char_array);
    if (index > size_ || count > len)
    {
        throw std::out_of_range("ERROR: Out of range in insert!");
    }
    std::size_t diff = (capacity_ > size_ + count + 1) ? 0 : (size_ + count - capacity_ + 1);
    if (diff > 0)
    {
        expand(diff);
    }
    char* buffer = new char[capacity_ - index];
    for (std::size_t i = 0; i <= size_ - index; i++)
    {
        *(buffer + i) = *(array_ + index + i);
    }
    for (std::size_t i = index, j = 0; i < index + count; i++, j++)
    {
        *(array_ + i) = *(char_array + j);
    }
    for (std::size_t i = index + count, j = 0; i <= size_ + count; i++, j++)
    {
        *(array_ + i) = *(buffer + j);
    }
    delete[] buffer;
    size_ += count;
    return *this;
}

MyString& MyString::insert(std::size_t index, const char* char_array)
{
    return this->insert(index, char_array, mystrlen(char_array));
}

MyString& MyString::insert(std::size_t index, const std::string& std_string, std::size_t count)
{
    return this->insert(index, std_string.data(), std_string.length());
}

MyString& MyString::insert(std::size_t index, const std::string& std_string)
{
    return this->insert(index, std_string.data(), std_string.length());
}


/* Erase method */
MyString& MyString::erase(std::size_t index, std::size_t count)
{
    if (index + count > size_)
    {
        throw std::out_of_range("ERROR: Out of range in erase!");
    }
    char* i = this->array_ + index;
    std::size_t j = 0;
    for (; j < this->size_ - count; j++)
    {
        *(i + j) = *(i + j + count);
    }
    for (; j < this->size_; j++)
    {
        *(i + j) = '\0';
    }
    size_ -= count;
    return *this;
}


/* Append methods */
MyString& MyString::append(std::size_t count, const char sym)
{
    return this->insert(this->size_, count, sym);
}

MyString& MyString::append(const char* char_array)
{
    return this->insert(this->size_, char_array);
}

MyString& MyString::append(const char* char_array, std::size_t index, std::size_t count)
{
    // this->erase(index, this->size_ - index);
    // return this->insert(index, char_array, count);
    char* ptr = const_cast<char*>(char_array) + index;
    return this->insert(size_, ptr, count);
}

MyString& MyString::append(std::string& std_sting)
{
    return this->insert(this->size_, std_sting);
}

MyString& MyString::append(std::string& std_sting, std::size_t index, std::size_t count)
{
    // this->erase(index, this->size_ - index);
    // return this->insert(index, std_sting, count);
    char* ptr = const_cast<char*>(std_sting.data()) + index;
    return this->insert(size_, ptr, count);
}


/* Substr methods*/
MyString MyString::substr(std::size_t index, std::size_t count)
{
    if (index + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in substr!");
    }
    char* buffer = new char[count + 1];
    for (std::size_t i = 0; i < count; i++)
    {
        *(buffer + i) = *(this->array_ + index + i);
    }
    *(buffer + count) = '\0';
    return MyString{ static_cast<const char*>(buffer) };
}

MyString MyString::substr(std::size_t index)
{
    if (index > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in substr!");
    }
    return this->substr(index, this->size_ - index);
}


/* Replace methods */
MyString& MyString::replace(std::size_t index, std::size_t count, const char* char_array)
{
    if (index + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in replace!");
    }
    this->erase(index, count);
    this->insert(index, char_array);
    return *this;
}

MyString& MyString::replace(std::size_t index, std::size_t count, std::string& std_string)
{
    if (index + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in replace!");
    }
    this->erase(index, count);
    return this->insert(index, std_string.data());
}

/* Find methods */
int MyString::find(const char* char_array, std::size_t index) const
{
    if (index >= this->size_) {
        return -1;
    }
    if (!(*char_array)) {
        return index;
    }
    for (std::size_t i = index; i <= this->size_ - mystrlen(char_array); i++) {
        
        for (std::size_t j = 0; j < mystrlen(char_array); j++)
        {
            if (*(this->array_ + i + j) == *(char_array + j) && !*(char_array+j+1)) return i;
            else if (*(this->array_ + i + j) == *(char_array + j)) continue;
            else break;
        }
    }
    return -1;
}

int MyString::find(const char* char_array) const
{
    return this->find(char_array, 0);
}

int MyString::find(const std::string& std_string) const
{
    return this->find(std_string.data(), 0);
}

int MyString::find(const std::string& std_string, std::size_t index) const
{
    return this->find(std_string.data(), index);
}


/* Extra task find method */
std::vector<int> MyString::find_aho(const std::vector<std::string>& substring)
{
    Trie* trie = new Trie(substring);
    std::vector<int> result = trie->findAllPos(std::string(MyString::c_str()));
    delete trie;
    return result;
}


/* Extra task string to number methods and at */
char MyString::at(std::size_t index) const
{
    if (index >= size_)
    {
        throw std::out_of_range("ERROR: Out of range in at!");
    }
    else
    {
        return *(array_ + index);
    }
}

int MyString::to_int(const char* char_array) const
{
    if (char_array == nullptr)
    {
        throw MyException("ERROR: to_int argument is nullptr!");
    }
    long result = std::strtol(char_array, nullptr, 10);
    if (result < INT_MIN || result > INT_MAX)
    {
        throw std::out_of_range("ERROR: Out of range in to_int!");
    }
    return static_cast<int>(result);
}

int MyString::to_int(std::string& std_string) const
{
    return to_int(std_string.data());
}

int MyString::to_int() const
{
    const char* data = (*this).c_str();
    return to_int(data);
}

float MyString::to_float(const char* char_array) const
{
    if (char_array == nullptr)
    {
        throw MyException("ERROR: to_float argument is nullptr!");
    }
    char* end;
    float result = std::strtof(char_array, &end);
    if (end == char_array)
    {
        throw MyException("ERROR: invalid argument");
    }
    return result;
}

float MyString::to_float(std::string& std_string) const
{
    return to_float(std_string.data());
}

float MyString::to_float() const
{
    const char* data = (*this).c_str();
    return to_float(data);
}


/* Extra task methods with iterarots */
MyString& MyString::insert(Iterator& it, std::size_t count, const char sym)
{
    if (index_it(it) == -1)
    {
        throw std::out_of_range("ERROR: Out of range in insert!");
    }
    std::size_t index_save = index_it(it);
    std::size_t diff = (capacity_ > size_ + count + 1) ? 0 : (size_ + count - capacity_ + 1);
    if (diff > 0)
    {
        expand(diff);
        it.pointer_ = array_ + index_save;
    }
    char* buffer = new char[capacity_];
    *buffer = '\0';
    auto tmp_it = it;
    std::size_t j = 0;
    for (; tmp_it != this->end(); j++, tmp_it++)
    {
        *(buffer + j) = *tmp_it;
    }
    *(buffer + j) = '\0';
    tmp_it = it;
    for (std::size_t i = 0; i < count; i++, tmp_it++)
    {
        *tmp_it = sym;
    }
    for (std::size_t i = 0; *(buffer + i) != '\0'; i++, tmp_it++)
    {
        *tmp_it = *(buffer + i);
    }
    *tmp_it = '\0';
    delete[] buffer;
    size_ += count;
    return *this;
}

MyString& MyString::insert(Iterator& it, const char* char_array, std::size_t count)
{
    std::size_t len = mystrlen(char_array);
    if (index_it(it) == -1 || count > len)
    {
        throw std::out_of_range("ERROR: Out of range in insert!");
    }
    std::size_t index_save = index_it(it);
    std::size_t diff = (capacity_ > size_ + count + 1) ? 0 : (size_ + count - capacity_ + 1);
    if (diff > 0)
    {
        expand(diff);
        it = this->begin();
        for (std::size_t i = 0; i < index_save; i++, it++);
    }
    char* buffer = new char[capacity_];
    *buffer = '\0';
    auto tmp_it = it;
    std::size_t j = 0;
    for (; tmp_it != this->end(); j++, tmp_it++)
    {
        *(buffer + j) = *tmp_it;
    }
    *(buffer + j) = '\0';
    tmp_it = it;
    for (std::size_t k = 0; k < count; tmp_it++, k++)
    {
        *tmp_it = *(char_array + k);
    }
    for (std::size_t i = 0; *(buffer + i) != '\0'; i++, tmp_it++)
    {
        *tmp_it = *(buffer + i);
    }
    *tmp_it = '\0';
    delete[] buffer;
    size_ += count;
    return *this;
}

MyString& MyString::insert(Iterator& it, const char* char_array)
{
    return this->insert(it, char_array, mystrlen(char_array));
}

MyString& MyString::insert(Iterator& it, const std::string& std_string, std::size_t count)
{
    return this->insert(it, std_string.data(), std_string.length());
}

MyString& MyString::insert(Iterator& it, const std::string& std_string)
{
    return this->insert(it, std_string.data(), std_string.length());
}

MyString& MyString::erase(Iterator& it, std::size_t count)
{
    Iterator tmp_it1 = it;
    Iterator tmp_it2{ it.pointer_ + count };
    if (index_it(it) == -1)
    {
        throw std::out_of_range("ERROR: Out of range in erase!");
    }
    std::size_t j = 0;
    for (; j < this->size_ - count; j++, tmp_it1++, tmp_it2++)
    {
        *tmp_it1 = *tmp_it2;
    }
    for (; j < this->size_; j++, tmp_it1++)
    {
        *tmp_it1 = '\0';
    }
    size_ -= count;
    return *this;
}

MyString& MyString::append(const char* char_array, Iterator& it, std::size_t count)
{
    this->erase(it, this->size_ - index_it(it));
    return this->insert(it, char_array, count);
}

MyString& MyString::append(std::string& std_sting, Iterator& it, std::size_t count)
{
    this->erase(it, this->size_ - index_it(it));
    return this->insert(it, std_sting, count);
}

MyString MyString::substr(Iterator& it, std::size_t count)
{
    if (index_it(it) + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in substr!");
    }
    char* buffer = new char[count + 1];
    Iterator tmp_it = it;
    for (std::size_t i = 0; i < count; i++, tmp_it++)
    {
        *(buffer + i) = *tmp_it;
    }
    *(buffer + count) = '\0';
    return MyString{ static_cast<const char*>(buffer) };
}

MyString MyString::substr(Iterator& it)
{
    if (index_it(it) > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in substr!");
    }
    return this->substr(it, this->size_ - index_it(it));
}

MyString& MyString::replace(Iterator& it, std::size_t count, const char* char_array)
{
    if (index_it(it) + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in replace!");
    }
    this->erase(it, count);
    this->insert(it, char_array);
    return *this;
}

MyString& MyString::replace(Iterator& it, std::size_t count, std::string& std_string)
{
    if (index_it(it) + count > this->size_)
    {
        throw std::out_of_range("ERROR: Out of range in replace!");
    }
    this->erase(it, count);
    return this->insert(it, std_string.data());
}

int MyString::find(const char* char_array, Iterator& it)
{
    if (!*it) {
        return -1;
    }
    if (!(*char_array)) {
        return index_it(it);
    }
    for (std::size_t i = index_it(it); i <= this->size_ - mystrlen(char_array); i++) 
    {
        for (std::size_t j = 0; j < mystrlen(char_array); j++)
        {
            if (*(this->array_ + i + j) == *(char_array + j) && !*(char_array+j+1)) return i;
            else if (*(this->array_ + i + j) == *(char_array + j)) continue;
            else break;
        }
    }
    return -1;
}

int MyString::find(std::string& std_string, Iterator& it)
{
    return this->find(std_string.data(), it);
}

char MyString::at(Iterator& it) const
{
    return *it;
}


/* Service methods */
MyString& MyString::expand(std::size_t diff)
{
    char* new_array = new char[capacity_ + diff];
    for (std::size_t i = 0; i <= size_; i++)
    {
        *(new_array + i) = *(array_ + i);
    }
    array_ = new_array;
    capacity_ += diff;
    return *this;
}

std::size_t MyString::mystrlen(const char* arg_array) const
{
    if (arg_array == nullptr)
    {
        throw MyException("ERROR: strlen argument is nullptr!");
    }
    std::size_t len = 0;
    for (; *(arg_array + len); len++);
    return len;
}

void MyString::swap(MyString& string1, MyString& string2)
{
    std::swap(string1.array_, string2.array_);
    std::swap(string1.size_, string2.size_);
    std::swap(string1.capacity_, string2.capacity_);
}

int MyString::mystrcmp(const char* arg_array1, const char* arg_array2) const
{
    const char* str1 = arg_array1, * str2 = arg_array2;
    while ('\0' != *str1 && *str1 == *str2) {
        str1++;
        str2++;
    }
    return *str2 - *str1;
}

int MyString::index_it(Iterator& it)
{
    std::size_t i = 0;
    auto tmp_it = this->begin();
    while (1)
    {
        if (tmp_it == it) return i;
        else if (tmp_it == this->end()) return -1;
        tmp_it++;
        i++;
    }
}
