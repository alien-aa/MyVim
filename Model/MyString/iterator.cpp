#include "iterator.h"

using Iterator        = MyString::Iterator;
using ConstIterator   = MyString::ConstIterator;
using ReverseIterator = MyString::ReverseIterator;
using ConstReIterator = MyString::ConstReIterator;

Iterator::Iterator() :
  pointer_(nullptr)
{}

Iterator::Iterator(char *ptr) :
  pointer_(ptr)
{}

ConstIterator::ConstIterator() :
  pointer_(nullptr)
{}

ConstIterator::ConstIterator(char *ptr) :
  pointer_(ptr)
{}

ReverseIterator::ReverseIterator() :
  pointer_(nullptr)
{}

ReverseIterator::ReverseIterator(char *ptr) :
  pointer_(ptr)
{}

ConstReIterator::ConstReIterator() :
  pointer_(nullptr)
{}

ConstReIterator::ConstReIterator(char *ptr) :
  pointer_(ptr)
{}


char& Iterator::operator*()
{
    return *pointer_;
}

Iterator& Iterator::operator++()
{
  pointer_++;
  return *this;
}

Iterator& Iterator::operator--()
{
  pointer_--;
  return *this;
}

Iterator Iterator::operator++(int)
{
  Iterator ret_it = *this;
  pointer_++;
  return ret_it;
}

Iterator Iterator::operator--(int)
{
  Iterator ret_it = *this;
  pointer_--;
  return ret_it;
}

bool Iterator::operator==(const Iterator &it) const
{
  return (pointer_ == it.pointer_);
}

bool Iterator::operator!=(const Iterator &it) const
{
  return (pointer_ != it.pointer_);
}


char ConstIterator::operator*()
{
    return *pointer_;
}

ConstIterator& ConstIterator::operator++()
{
  pointer_++;
  return *this;
}

ConstIterator& ConstIterator::operator--()
{
  pointer_--;
  return *this;
}

ConstIterator ConstIterator::operator++(int)
{
  ConstIterator ret_it = *this;
  pointer_++;
  return ret_it;
}

ConstIterator ConstIterator::operator--(int)
{
  ConstIterator ret_it = *this;
  pointer_--;
  return ret_it;
}

bool ConstIterator::operator==(const ConstIterator &it) const
{
  return (pointer_ == it.pointer_);
}

bool ConstIterator::operator!=(const ConstIterator &it) const
{
  return (pointer_ != it.pointer_);
}



char& ReverseIterator::operator*()
{
    return *pointer_;
}

ReverseIterator& ReverseIterator::operator++()
{
  pointer_--;
  return *this;
}

ReverseIterator& ReverseIterator::operator--()
{
  pointer_++;
  return *this;
}

ReverseIterator ReverseIterator::operator++(int)
{
  ReverseIterator ret_it = *this;
  pointer_--;
  return ret_it;
}

ReverseIterator ReverseIterator::operator--(int)
{
  ReverseIterator ret_it = *this;
  pointer_++;
  return ret_it;
}

bool ReverseIterator::operator==(const ReverseIterator &it) const
{
  return (pointer_ == it.pointer_);
}

bool ReverseIterator::operator!=(const ReverseIterator &it) const
{
  return (pointer_ != it.pointer_);
}


char ConstReIterator::operator*()
{
    return *pointer_;
}

ConstReIterator& ConstReIterator::operator++()
{
  pointer_--;
  return *this;
}

ConstReIterator& ConstReIterator::operator--()
{
  pointer_++;
  return *this;
}

ConstReIterator ConstReIterator::operator++(int)
{
  ConstReIterator ret_it = *this;
  pointer_--;
  return ret_it;
}

ConstReIterator ConstReIterator::operator--(int)
{
  ConstReIterator ret_it = *this;
  pointer_++;
  return ret_it;
}

bool ConstReIterator::operator==(const ConstReIterator &it) const
{
  return (pointer_ == it.pointer_);
}

bool ConstReIterator::operator!=(const ConstReIterator &it) const
{
  return (pointer_ != it.pointer_);
}

