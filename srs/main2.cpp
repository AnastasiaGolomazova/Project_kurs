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
			Node* temp = new Node(data);
		}
		else {
			Node* current = head;
			while (current->getNext() != nullptr) {
				current = current->getNext();
			}
			Node* temp = current;
			current->setNext(new Node(data));
			temp->setNext(new Node(data));
		}
	}
	void Example_2(int data, int i) {
		Node* current = head;
		Node* temp = new Node(data);
		Node* current2 = head;
		int j = 1;
		if (i == 1)
		{
			temp->setNext(current);
			head = temp;
			temp->setNext(head);
		}
		else {
			while ((current->getNext() != nullptr)) {
				if (i == j)
				{
					current2->setNext(temp);
					temp->setNext(current2);
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
			delete head;
		}
		else {
			while (current->getNext() != nullptr) {
				if (current->getNext()->getData() == data) {
					delete temp;
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
			head->setNext(current);
		}
		int j = 0;	
		while (current->getNext() != nullptr){
			current = current->getNext();
		}
		current->setNext(new Node(data));
		head->setNext(current);		
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
	}
};
int main()
{
	return 0;
}
