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
	}
	
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
	void Example_1(int data) {
		Node* temp;
		if (head == nullptr) {
			head = new Node(data);
		}
		else {
			Node* current = head;
			while (current->getNext() != nullptr) {
				temp = current;
				current = current->getNext();
				temp->setNext(current->getNext());
			}
			current->setNext(new Node(data));
			head = current;
		}
	}
	void Example_2(int data, int i) {
		Node* current = head;
		Node* temp = new Node(data);
		Node* current2 = new Node(data);
		int j = 1;
		if (i == 1)
		{
			temp->setNext(current);
			head = temp;
		}
		else {
			while ((current->getNext() != nullptr)) {
				if (i == j)
				{
					current2->setNext(current);
					temp->setNext(current);
					delete temp;
					break;
				}
				else
				{
					current2 = current->getNext();
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
			head = head->getNext();
			delete current;
		}
		else {
			while (current->getNext() != nullptr) {
				if (current->getNext()->getData() == data) {
					temp->setNext(current);
					head = current;
					delete current;
				}
				else{
					temp = current;
					current = current->getNext();
				}
			}
		}
	}
	void Example_4(int data) {
		Node* current = head;
		Node* temp;
		if (head->getData() == data){
			temp = head;
			head = head->getNext();
		}
		int j = 0;	
		while (current->getNext() != nullptr){
			current = current->getNext();
		}
		current->setNext(new Node(data));
		temp = head;
		temp = current;	
		current->setNext(head);
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
