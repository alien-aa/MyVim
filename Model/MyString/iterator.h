#ifndef _ITERATOR_H_
#define _ITERATOR_H_

#include "mystring.h"

class MyString::Iterator
{
public:
  friend class MyString;

  Iterator();
  explicit Iterator(char *ptr);

  char& operator*();
  Iterator& operator++();
  Iterator& operator--();
  Iterator operator++(int); 
  Iterator operator--(int); 
  bool operator==(const Iterator &it) const;
  bool operator!=(const Iterator &it) const;

protected:
  char *pointer_;
};


class MyString::ConstIterator 
{
public:
  friend class MyString;

  ConstIterator();
  explicit ConstIterator(char *ptr);

  char operator*();
  ConstIterator& operator++();
  ConstIterator& operator--();
  ConstIterator operator++(int); 
  ConstIterator operator--(int); 
  bool operator==(const ConstIterator &it) const;
  bool operator!=(const ConstIterator &it) const;

protected:
  char *pointer_;
};


class MyString::ReverseIterator 
{
public:
  friend class MyString;

  ReverseIterator();
  explicit ReverseIterator(char *ptr);

  char& operator*();
  ReverseIterator& operator++();
  ReverseIterator& operator--();
  ReverseIterator operator++(int); 
  ReverseIterator operator--(int); 
  bool operator==(const ReverseIterator &it) const;
  bool operator!=(const ReverseIterator &it) const;

protected:
  char *pointer_;
};


class MyString::ConstReIterator 
{
public:
  friend class MyString;

  ConstReIterator();
  explicit ConstReIterator(char *ptr);

  char operator*();
  ConstReIterator& operator++();
  ConstReIterator& operator--();
  ConstReIterator operator++(int); 
  ConstReIterator operator--(int); 
  bool operator==(const ConstReIterator &it) const;
  bool operator!=(const ConstReIterator &it) const;

protected:
  char *pointer_;
};


#endif // _ITERATOR_H_