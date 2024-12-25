#ifndef _TRIE_H_
#define _TRIE_H_

#include <vector>
#include <string>

class Trie
{
public:
  Trie(const std::vector< std::string > &substrings);

  std::vector< int > findAllPos(const std::string &s);

  ~Trie();

private:
  struct Node
  {
    char sym;
    std::vector< std::pair< Node *, char > > kids;
    std::vector< std::pair< Node *, char > > autoMove;
    bool is_complete;
    int pattern_num;
    Node *suffix;
    Node *parent;
    Node *good_suffix;

    Node();
  };

  Node *root;
  Node *current;
  std::vector< std::string > substrings;
  std::vector< int > result_;

  Node *getSuffixLink(Node *node);

  Node *getAutoMove(Node *node, char sym);

  Node *getGoodSuffix(Node *node);

  void check(Node *v, int i);

  void deleteNode(Node *node);

  void add_string(const std::string &str, int str_index);
};

#endif // _TRIE_H_
