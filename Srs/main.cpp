#include <iostream>
#include <string>

using namespace std;

class Node {
	Node* next;
	int data;
public:
	Node(int data, Node* next = nullptr) {
		this->data = data;
		this->next = next;
	}
	int getData() {
		return data;
	}
	void setData(int data) {
		this->data = data;
	};
	Node* getNext() {
		return next;
	}
	void setNext(Node* data) {
		next = data;
	}
};

class SinglyLinkedList {

	Node* head;

public:
	void pushBack(int data) {
		if (head == nullptr) {
			head = new Node(data);
		}
		else {
			Node* current = this->head;
			while (current->getNext() != nullptr) {
				current = current->getNext();
			}
			current->setNext(new Node(data));
		}

	}

	void InsertNode(Node* node, int i) {
		Node* current = head;
		Node* temp;
		int j = 1;
		if (i == 1)
		{
			current->setNext(node);
		}
		else {
			while ((current->getNext() != nullptr)) {
				if (i == j)
				{
					current->setNext(node);
					break;
				}
				else
				{
					current = current->getNext();
					j++;
				}
			}
		}
	}

	void delData(int data) {
		Node* current = head;
		Node* temp;
		if (current == node)
		{
			temp = head;
			head = head->getNext();
			break;
		}
		else {
			while (current->getNext() != nullptr) {
				if (current->getNext()->getData() == data) {
					temp->setNext(current->getNext());
					current = temp;
					break;
				}
				else{
					temp = current;
					current = current->getNext();
				}
			}
		}
	}

	Node* getNode(int num) {
		Node* current = this->head;
		while (current != nullptr)
		{
			if (current->getData() == num)
				return current;
			else
				current = current->getNext();
		}
		return nullptr;
	}

	SinglyLinkedList() {
		this->head = nullptr;
	}
	~SinglyLinkedList() {

		Node* temp;
		while (head != nullptr) {
			temp = head;
			head = head->getNext();
			delete temp;
		}
		cout << "im working" << endl;
	}
};

int main()
{
	SinglyLinkedList* list = new SinglyLinkedList();
	list->pushBack(5);
	list->pushBack(10);
	list->pushBack(0);
	list->pushBack(1);
	list->pushBack(2);
	//cout << list->getNode(2) << endl;
	//cout << list->getNode(10) << endl;
	//list->delData(list->getNode(2));
	//list->delData(list->getNode(10));

	//Node* node = new Node(2);

	//list->InsertNode(node, 2);
	//delete list;
	return 0;
}
