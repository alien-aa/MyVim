#define _CRT_SECURE_NO_WARNINGS

#include "mystring.h"
#include "iterator.h"

#include <iostream>
#include <fstream>
#include <ctime>
#include <cstring>
#include <string>

using namespace std;


void mylogger(char type, std::string msg) {
    time_t current_time = time(0);
    char* current_time_str = ctime(&current_time);
    current_time_str[strlen(current_time_str) - 1] = '\0';

    if (type == 0) {
        cout << "\033[34m" << "[" << current_time_str << "]" << " INFO: " << msg << "\033[0m\n";
    }
    else if (type == 1) {
        cout << "\033[32m" << "[" << current_time_str << "]" << " Success: " << msg << "\033[0m\n";
    }
    else if (type == 2) {
        cout << "\033[31m" << "[" << current_time_str << "]" << " Error: " << msg << "\033[0m\n";
    }
}

void mylog_assertion(bool condition, std::string test_name)
{
    condition
        ? mylogger(1, test_name)
        : mylogger(2, test_name);
}

void extra_tests() {
    mylogger(0, "EXTRA TASK TESTING");
    string test_name;
    //--------------------------------|
    // TEST 1: OUT-OF-RANGE           |
    //--------------------------------|
    test_name = "TEST 1 - OUT-OF-RANGE";
    MyString str1("Hi");
    try {
        str1.insert(6, "Herbert");
    }
    catch (const std::out_of_range& err) {
        //std::cerr << "Exception in insert: " << err.what() << endl;
    }
    mylogger(1, test_name); // If this line is executed, test has been successfully passed. Otherwise, the program should crash
    //-----------------------------------|
    // TEST 2: MY EXCEPTION              |
    //-----------------------------------|
    test_name = "TEST 2 - MY EXCEPTION";
    try {
        const char* evil = nullptr;
        MyString str2(evil);
    }
    catch (const MyException& err) {
        //std::cerr << "Exception in constructor: " << err.what() << endl;
    }
    mylogger(1, test_name); // If this line is executed, test has been successfully passed. Otherwise, the program should crash
    //------------------------------------|
    // TEST 3: MOVE CONSTRUCTOR           |
    //------------------------------------|
    test_name = "TEST 3 - MOVE CONSTRUCTOR";
    MyString str3("aaaaaaaaaa");
    MyString str4(std::move(str3));
    str4.length() == 10 && str4.capacity() >= 11 && \
        !strcmp(str4.c_str(), "aaaaaaaaaa") ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------------|
    // TEST 4  NUM TO STR CONSTRUCTORS |
    //---------------------------------|
    test_name = "TEST 4 - NUM TO STR CONSTRUCTORS";
    int number = 25654;
    float fnumber = 256.849;
    MyString str5(number);
    MyString str6(fnumber);
    str5.length() == 5 && str5.capacity() >= 6 && \
        !strcmp(str5.c_str(), "25654") && \
        str6.length() == std::to_string(fnumber).size() && str6.capacity() >= std::to_string(fnumber).size() + 1 && \
        !strcmp(str6.c_str(), std::to_string(fnumber).data()) ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------|
    // TEST 5: MOVE OPERATOR       |
    //-----------------------------|
    test_name = "TEST 5 - MOVE OPERATOR";
    MyString str7("Hello World");
    MyString str8 = std::move(str7);
    //str8 = std::move(str7);
    str8.length() == 11 && str8.capacity() >= 12 && \
        !strcmp(str8.c_str(), "Hello World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------|
    // TEST 6: >> TO FILE          |
    //-----------------------------|
    // test_name = "TEST 6 - >> TO FILE";
    // MyString strf("Why are you here? :)");
    // std::ofstream ofs;
    // ofs.open("testfile.txt");
    // ofs << str6; 
    // ofs.close();
    // // check
    //----------------------------|
    // TEST 7: FIND AHO           |
    //----------------------------|
    test_name = "TEST 7 - FIND AHO";
    MyString str_aho("cdabslkjnvsd");
    std::vector<std::string> patterns = { "abs", "bslk", "nv", "hahaha" };
    std::vector<int> index = str_aho.find_aho(patterns);
    std::vector<int> correct = { 2, 3, 8, -1 };
    (index == correct) ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------|
    // TEST 8: AT (OK)           |
    //---------------------------|
    test_name = "TEST 8 - AT (OK)";
    MyString str9("Hello World");
    std::size_t at = 3;
    try {
        char sym = str9.at(at);
        (sym == 'l') ? mylogger(1, test_name) : mylogger(2, test_name);
    }
    catch (const std::out_of_range& err) {}
    //---------------------------|
    // TEST 9: AT (EXC)          |
    //---------------------------|
    test_name = "TEST 8 - AT (EXC)";
    MyString str10("Hello World");
    at = 500;
    try {
        char sym = str10.at(at);
    }
    catch (const std::out_of_range& err) {}
    mylogger(1, test_name); // If this line is executed, test has been successfully passed. Otherwise, the program should crash
    //-----------------------------|
    // TEST 10: STR TO INT         |
    //-----------------------------|
    test_name = "TEST 10 - STR TO INT";
    MyString str11("15234");
    int res_num = str11.to_int();
    (res_num == 15234) ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------|
    // TEST 11: STR TO FLOAT       |
    //-----------------------------|
    test_name = "TEST 11 - STR TO FLOAT";
    MyString str12("15.25");
    float res_num_2 = str12.to_float();
    (res_num_2 == 15.25) ? mylogger(1, test_name) : mylogger(2, test_name);
    mylogger(0, "ITERATOR TESTS");
    //--------------------------------|
    // TEST 1: INSERT IN EMPTY STRING |
    //--------------------------------|
    test_name = "TEST 1 - INSERT IN EMPTY STRING";
    MyString _str1("");
    MyString::Iterator it1 = _str1.begin();
    _str1.insert(it1, "Hello", 5);
    !strcmp(_str1.c_str(), "Hello") ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------------|
    // TEST 2: INSERT IN BEGIN OF STRING |
    //-----------------------------------|
    test_name = "TEST 2 - INSERT IN BEGIN OF STRING";
    MyString _str2(" World");
    MyString::Iterator it2 = _str2.begin();
    _str2.insert(it2, "Hello", 5);
    !strcmp(_str2.c_str(), "Hello World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //------------------------------------|
    // TEST 3: INSERT IN MIDDLE OF STRING |
    //------------------------------------|
    test_name = "TEST 3 - INSERT IN MIDDLE OF STRING";
    MyString _str3("Hello World");
    MyString::Iterator it3 = _str3.begin();
    for (std::size_t i = 0; i < 6; i++, it3++);
    _str3.insert(it3, "Beautiful ", 10);
    !strcmp(_str3.c_str(), "Hello Beautiful World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------------|
    // TEST 4  INSERT IN END OF STRING |
    //---------------------------------|
    test_name = "TEST 4 - INSERT IN END OF STRING";
    MyString _str4("Hello");
    MyString::Iterator it4 = _str4.begin();
    for (std::size_t i = 0; i < 5; i++, it4++);
    _str4.insert(it4, " World", 6);
    !strcmp(_str4.c_str(), "Hello World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------|
    // TEST 5: INSERT EMPTY STRING |
    //-----------------------------|
    test_name = "TEST 5 - INSERT EMPTY STRING";
    MyString _str5("Hello World");
    MyString::Iterator it5 = _str5.begin();
    for (std::size_t i = 0; i < 6; i++, it5++);
    _str5.insert(it5, "", 0);
    !strcmp(_str5.c_str(), "Hello World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------------------------|
    // TEST 6: INSERT EMPTY STRING IN EMPTY STRING |
    //---------------------------------------------|
    test_name = "TEST 6 - INSERT EMPTY STRING IN EMPTY STRING";
    MyString _str6;
    MyString::Iterator it6 = _str6.begin();
    _str6.insert(it6, "", 0);
    !strcmp(_str6.c_str(), "") && _str6.length() == 0 && \
        _str6.capacity() >= 1 ? mylogger(1, test_name) : mylogger(2, test_name);
    //----------------------------|
    // TEST 7: INSERT LONG STRING |
    //----------------------------|
    test_name = "TEST 7 - INSERT LONG TAIL REWRITE ON COPY";
    MyString _str7("0123456789");
    MyString::Iterator it7 = _str7.begin();
    for (std::size_t i = 0; i < 3; i++, it7++);
    _str7.insert(it7, "**");
    !strcmp(_str7.c_str(), "012**3456789") ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------|
    // TEST 8: INSERT ONE SYMBOL |
    //---------------------------|
    test_name = "TEST 8 - INSERT ONE SYMBOL";
    MyString _str8("Hello World");
    MyString::Iterator it8 = _str8.begin();
    for (std::size_t i = 0; i < 5; i++, it8++);
    _str8.insert(it8, "X", 1);
    !strcmp(_str8.c_str(), "HelloX World") ? mylogger(1, test_name) : mylogger(2, test_name);
    //-----------------------------|
    // TEST 9: INSERT A LOT OF 'A' |
    //-----------------------------|
    test_name = "TEST 9 - INSERT A LOT OF \'A\'";
    MyString _str9;
    MyString::Iterator it9 = _str9.begin();
    _str9.insert(it9, 5000, 'a');
    _str9.length() == 5000 && _str9.capacity() >= 5001 ? mylogger(1, test_name) : mylogger(2, test_name);
    //------------------------------------|
    // TEST 10: INSERT STRING INTO ITSELF |
    //------------------------------------|
    test_name = "TEST 10 - INSERT STRING INTO ITSELF";
    MyString _str10("Hello");
    MyString::Iterator it10 = _str10.begin();
    for (std::size_t i = 0; i < 5; i++, it10++);
    _str10.insert(it10, _str10.c_str());
    !strcmp(_str10.c_str(), "HelloHello") ? mylogger(1, test_name) : mylogger(2, test_name);
    //---------------------------------------|
    // TEST 10: INSERT BY OUT OF RANGE INDEX |
    //---------------------------------------|
    test_name = "TEST 11 - INSERT BY OUT OF RANGE INDEX";
    MyString _str11("Hello");
    try {
        MyString::Iterator it11 = _str11.begin();
        for (std::size_t i = 0; i < 1; i++, it11++);
        _str11.insert(it11, " World", 6);
    }
    catch (...) {}
    mylogger(1, test_name);
    // TEST 1
    test_name = "TEST 1 - ERASE FROM START";
    MyString s_1("LongString");
    MyString::Iterator it_1 = s_1.begin();
    s_1.erase(it_1, 4);
    mylog_assertion(s_1.length() == 6 && strcmp(s_1.c_str(), "String") == 0, test_name);
    // TEST 2
    test_name = "TEST 2 - ERASE FROM END";
    MyString s_2("LongString");
    MyString::Iterator it_2 = s_2.begin();
    for (std::size_t i = 0; i < 4; i++, it_2++);
    s_2.erase(it_2, 6);
    mylog_assertion(s_2.length() == 4 && strcmp(s_2.c_str(), "Long") == 0, test_name);
    // TEST 3
    test_name = "TEST 3 - ERASE BY OUT OF BOUND INDEX";
    MyString s_3("LongString");
    try {
        MyString::Iterator it_3 = s_3.begin();
        for (std::size_t i = 0; i < 12; i++, it_3++);
        s_3.erase(it_3, 6);
    }
    catch (...) {}
    mylogger(1, test_name);
    // TEST 1
    test_name = "TEST 1 - REPLACE FROM START";
    MyString _s_1("LongString");
    MyString::Iterator _it_1 = _s_1.begin();
    _s_1.replace(_it_1, 4, "Short");
    mylog_assertion(_s_1.length() == 11 && strcmp(_s_1.c_str(), "ShortString") == 0, test_name);
    // TEST 2
    test_name = "TEST 2 - REPLACE FROM END";
    MyString _s_2("LongString");
    MyString::Iterator _it_2 = _s_2.begin();
    for (std::size_t i = 0; i < 4; i++, _it_2++);
    _s_2.replace(_it_2, 6, "Int");
    mylog_assertion(_s_2.length() == 7
        && _s_2.capacity() >= 11
        && strcmp(_s_2.c_str(), "LongInt") == 0, test_name);
    // TEST 1
    test_name = "TEST 1 - SUBSTRING FULL SIZE";
    MyString s1_1("Str1 Str2 Str3");
    MyString::Iterator it21 = s1_1.begin();
    for (std::size_t i = 0; i < 5; i++, it21++);
    auto s1_sub = s1_1.substr(it21);
    mylog_assertion(s1_sub.length() == 9 && strcmp(s1_sub.c_str(), "Str2 Str3") == 0, test_name);
    // TEST 2
    test_name = "TEST 2 - SUBSTRING OF LENGTH";
    MyString s2_2("Str1 Str2 Str3");
    MyString::Iterator it22 = s2_2.begin();
    for (std::size_t i = 0; i < 5; i++, it22++);
    auto s2_sub = s2_2.substr(it22, 4);
    mylog_assertion(s2_sub.length() == 4 && strcmp(s2_sub.c_str(), "Str2") == 0, test_name);
}
