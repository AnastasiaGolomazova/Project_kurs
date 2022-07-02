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
		if (head == nullptr) {
			head = new Node(data);
		}
		else {
			Node* current = head;
			while (current->getNext() != nullptr) {
				current = current->getNext();
			}
			current->setNext(new Node(data));
		}
	}
	void Example_2(int data, int i) {
		Node* current = head;
		Node* temp = new Node(data);
		Node* current2;
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
					current2->setNext(temp);
					temp->setNext(current);
					break;
				}
				else
				{
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
			delete temp;
		}
		else {
			while (current->getNext() != nullptr) {
				if (current->getNext()->getData() == data) {
					temp->setNext(current->getNext());
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
		}
		int j = 0;	
		while (current->getNext() != nullptr){
			current = current->getNext();
		}
		current->setNext(new Node(data));	
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
