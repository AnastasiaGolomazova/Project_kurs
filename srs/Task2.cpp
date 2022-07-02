#include <iostream>
#include <string>

using namespace std;

class Node {
	Node* next;
	Node* prev;
	int data;
public:
	Node(int data, Node* next = nullptr, Node* prev = nullptr) {
		this->data = data;
		this->next = next;
		this->prev = prev;
	}
	int getData() {
		return data;
	}
	void setData(int data) {
		this->data = data;
	}

	Node* getNext() {
		return next;
	}
	void setNext(Node* data) {
		next = data;
	}

	Node* getPrev() {
		return next;
	}
	void setPrev(Node* data) {
		next = data;
	}
};

class SinglyLinkedList {

	Node* head;

public:
	void Example_1(int data) {
		if (head == nullptr) {
			head = new Node(data);
		}
		else {
			Node* current = head;
			Node* temp;
			while (current->getNext() != nullptr) {
				current = current->getNext();
			}
			current->setNext(new Node(data));
			temp = current;
			current = current->getNext();
			current->setPrev(temp);
			head = head->getNext();
		}
	}
	void Example_2(int data, int i) {
		Node* current = head;
		Node* temp = new Node(data);
		Node* current2;
		int j = 1;
		if (i == 1)
		{
			temp->setNext(head);
		}
		else {
			while ((current->getNext() != nullptr)) {
				if (i == j)
				{
					current2->setPrev(temp);
					temp->setPrev(current);
					break;
				}
				else
				{
					head = head->getNext();
					current2 = current;
					current = current->getNext();
					j++;
				}
			}
		}
	}
	void Example_3(int data) {
		Node* current = head;
		Node* temp;
		if (current->getData() == data)
		{
			temp = head;
			head = head->getNext();
		}
		else {
			while (current->getNext() != nullptr) {
				if (current->getNext()->getData() == data) {
					temp->setNext(current->getPrev());
					delete current;
				}
				else {
					head = head->getNext();
					temp = current;
					current = current->getNext();
				}
			}
		}
	}
	void Example_4(int data) {
		Node* current = head;
		Node* temp;
		Node* prev;
		if (head->getData() == data) {
			temp = head;
			head = head->getNext();
		}
		int j = 0;
		while (current->getNext() != nullptr) {
			current = current->getNext();
		}
		prev = current->getPrev();
		delete current;
		prev->setNext(new Node(data));
		head = head->getNext();
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
	return 0;
}

