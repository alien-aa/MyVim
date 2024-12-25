#ifndef _MYSTRING_H_
#define _MYSTRING_H_
/*
The goal of header guards is to prevent a code file
from receiving more than one copy of a guarded header.
*/

#include <iostream>
#include <vector>

class MyString
{
public:
    // Iterators (extra task)
    class Iterator;
    Iterator begin();
    Iterator end();
    class ConstIterator;
    ConstIterator cbegin();
    ConstIterator cend();
    class ReverseIterator;
    ReverseIterator rbegin();
    ReverseIterator rend();
    class ConstReIterator;
    ConstReIterator rcbegin();
    ConstReIterator rcend();

    // Constructors
    MyString();
    MyString(const char* char_array, std::size_t count);
    MyString(std::size_t count, const char sym);
    MyString(const char* char_array);
    MyString(const std::string& std_string);
    MyString(const MyString& class_string);


    // Extra task constructors
    MyString(MyString&& moved_string) noexcept;
    MyString(int number);
    MyString(float number);

    // Destructor
    ~MyString();

    // Operators
    MyString operator+(const char* char_array);
    MyString operator+(MyString& class_string);
    MyString operator+(std::string& std_string);

    MyString& operator+=(const char* char_array);
    MyString& operator+=(std::string& std_string);
    MyString& operator+=(MyString& class_string);

    bool operator>(MyString& class_string) const;
    bool operator<(MyString& class_string) const;
    bool operator>=(MyString& class_string) const;
    bool operator<=(MyString& class_string) const;
    bool operator!=(MyString& class_string) const;
    bool operator==(MyString& class_string) const;

    MyString& operator=(const char* char_array);
    MyString& operator=(const std::string& std_string);
    MyString& operator=(const char sym);
    MyString& operator=(const MyString& class_string);
    char& operator[](std::size_t index);
    
    // For wrapper
    MyString& assign(const char* char_array);
    MyString& assign(const std::string& std_string);
    MyString& assign(const char sym);
    MyString& assign(const MyString& class_string);

    // Output & input operators
    friend std::ostream& operator<<(std::ostream& stream, const MyString& class_string);
    friend std::istream& operator>>(std::istream& stream, MyString& class_string);

    // Extra task operators
    MyString& operator=(MyString&& moved_string) noexcept;
    //friend std::ofstream& operator<<(std::ofstream &stream, const MyString &class_string);
    friend std::ifstream& operator>>(std::ifstream& stream, MyString& class_string);

    // Getters methods
    const char* c_str() const;
    const char* data() const;
    std::size_t size() const;
    std::size_t length() const;
    std::size_t capacity() const;

    // String manipulation methods
    bool empty() const;
    MyString& shrink_to_fit();
    MyString& clear();

    // Insert methods
    MyString& insert(std::size_t index, std::size_t count, const char sym);
    MyString& insert(std::size_t index, const char* char_array, std::size_t count);
    MyString& insert(std::size_t index, const char* char_array);
    MyString& insert(std::size_t index, const std::string& std_string, std::size_t count);
    MyString& insert(std::size_t index, const std::string& std_string);

    // Erase method
    MyString& erase(std::size_t index, std::size_t count);

    // Append methods
    MyString& append(std::size_t count, const char sym);
    MyString& append(const char* char_array);
    MyString& append(const char* char_array, std::size_t index, std::size_t count);
    MyString& append(std::string& std_sting);
    MyString& append(std::string& std_sting, std::size_t index, std::size_t count);

    // Substr methods
    MyString substr(std::size_t index, std::size_t count);
    MyString substr(std::size_t index);

    // Replace methods
    MyString& replace(std::size_t index, std::size_t count, const char* char_array);
    MyString& replace(std::size_t index, std::size_t count, std::string& std_string);

    // Find methods
    int find(const char* char_array, std::size_t index) const;
    int find(const char* char_array) const;
    int find(const std::string& std_string) const;
    int find(const std::string& std_string, std::size_t index) const;

    // Extra task find method
    std::vector<int> find_aho(const std::vector<std::string>& substring);

    // Extra task string to number methods and at
    char at(std::size_t index) const;
    int to_int(const char* char_array) const;
    int to_int(std::string& std_string) const;
    int to_int() const;
    float to_float(const char* char_array) const;
    float to_float(std::string& std_string) const;
    float to_float() const;

    // Extra task methods with iterators
    MyString& insert(Iterator& it, std::size_t count, const char sym);
    MyString& insert(Iterator& it, const char* char_array, std::size_t count);
    MyString& insert(Iterator& it, const char* char_array);
    MyString& insert(Iterator& it, const std::string& std_string, std::size_t count);
    MyString& insert(Iterator& it, const std::string& std_string);
    MyString& erase(Iterator& it, std::size_t count);
    MyString& append(const char* char_array, Iterator& it, std::size_t count);
    MyString& append(std::string& std_sting, Iterator& it, std::size_t count);
    MyString substr(Iterator& it, std::size_t count);
    MyString substr(Iterator& it);
    MyString& replace(Iterator& it, std::size_t count, const char* char_array);
    MyString& replace(Iterator& it, std::size_t count, std::string& std_string);
    int find(const char* char_array, Iterator& it);
    int find(std::string& std_string, Iterator& it);
    char at(Iterator& it) const;


private:
    // Class attributes
    char* array_;
    std::size_t capacity_;
    std::size_t size_;

    // Service methods
    MyString& expand(std::size_t diff);
    std::size_t mystrlen(const char* char_array) const;
    void swap(MyString& class_string1, MyString& class_string2);
    int mystrcmp(const char* arg_array1, const char* arg_array2) const;
    int index_it(Iterator& it);
};

class MyException : public std::exception
    /*
    Inheritance from the std::exception class.
    It will be used in cases of invalid conversion.
    For example, if constructor's argument is nullptr or argument of mystrlen is nullptr
    To catch this exception use:
    ```
    try {
      obj = danger_method(maybe_nullptr);
    } catch(const MyException& err) {
      std::cerr << "Exception in _method_name_: " << err.what() << endl;
      // your code here
    }
    ```
    */
{
public:
    MyException(const char* msg) : message_(msg)
    {
    }
    const char* what() const noexcept override
    {
        return message_;
    }

private:
    const char* message_;
};

#endif // _MYSTRING_H_