#include "trie.h"
#include <iostream>

Trie::Trie(const std::vector< std::string > &substrings):
  root(new Node()),
  current(root),
  substrings(substrings)
{
    std::vector<int> result(substrings.size(), -1);
    result_ = result;
    for (int i = 0; i < substrings.size(); i++) {
    add_string(substrings[i], i);
  }
}

std::vector< int > Trie::findAllPos(const std::string &s)
{
  Node *u = root;
  for (int i = 0; i < s.length(); i++) {
    u = getAutoMove(u, s[i]);
    check(u, i + 1);
  }
  return this->result_;
}

void Trie::add_string(const std::string &str, int str_index)
{
  for (int i = 0; i < str.length(); i++) {
    char ch = str[i];
    bool is_char_in_trie = false;
    for (size_t i = 0; i < current->kids.size(); i++) {
      if (current->kids[i].second == ch) {
        current = current->kids[i].first;
        is_char_in_trie = true;
        break;
      }
    }
    if (!is_char_in_trie) {
      Node *newNode = new Node();
      newNode->parent = current;
      newNode->sym = ch;
      current->kids.emplace_back(newNode, ch);
      current = newNode;
    }
  }
  current->is_complete = true;
  current->pattern_num = str_index;
  current = root;
}

Trie::~Trie()
{
  deleteNode(root);
};

Trie::Node::Node():
  sym('\0'),
  is_complete(false),
  pattern_num(-1),
  suffix(nullptr),
  parent(nullptr),
  good_suffix(nullptr)
{};

Trie::Node *Trie::getSuffixLink(Node *node)
{
  if (node->suffix == nullptr) {
    if (node == root || node->parent == root) {
      node->suffix = root;
    } else {
      node->suffix = getAutoMove(getSuffixLink(node->parent), node->sym);
    }
  }
  return node->suffix;
}

Trie::Node *Trie::getAutoMove(Node *node, char sym)
{
  bool ifPathExistsInAutoMove = false;
  Node *result;
  for (int i = 0; i < node->autoMove.size(); i++) {
    if (node->autoMove[i].second == sym) {
      ifPathExistsInAutoMove = true;
      result = node->autoMove[i].first;
      break;
    }
  }

  if (!ifPathExistsInAutoMove) {
    bool ifPathExistsInKids = false;
    Node *kid = nullptr;
    for (int i = 0; i < node->kids.size(); i++) {
      if (node->kids[i].second == sym) {
        ifPathExistsInKids = true;
        kid = node->kids[i].first;
        break;
      }
    }

    if (ifPathExistsInKids) {
      result = kid;
      node->autoMove.emplace_back(kid, sym);
    } else {
      if (node == root) {
        result = root;
        node->autoMove.emplace_back(root, sym);
      } else {
        result = getAutoMove(getSuffixLink(node), sym);
        node->autoMove.emplace_back(result, sym);
      }
    }
  }
  return result;
}

Trie::Node *Trie::getGoodSuffix(Node *node)
{
  if (node->good_suffix == nullptr) {
    Node *u = getSuffixLink(node);
    if (u == root)
      node->good_suffix = root;
    else
      node->good_suffix = (u->is_complete) ? u : getGoodSuffix(u);
  }
  return node->good_suffix;
}

void Trie::check(Node *v, int i)
{
  for (Node *u = v; u != root; u = getGoodSuffix(u)) {
    if (u->is_complete) {
        result_[u->pattern_num] = i - substrings[u->pattern_num].length();
        // std::cout << i - substrings[u->pattern_num].length() + 1 << " "
        //         << substrings[u->pattern_num] << "\n";
    }
  }
}

void Trie::deleteNode(Node *node)
{
  for (int i = 0; i < node->kids.size(); i++) {
    deleteNode(node->kids[i].first);
  }
  delete node;
}
