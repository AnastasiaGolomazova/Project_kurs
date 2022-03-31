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
	void Example_2(Node* node, int i) {
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
	void Example_3(int data) {
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
	Node* Example_4(int num) {
		Node* current = head;
		while (current != nullptr)
		{
			if (current->getData() == num)
				return current;
			else
				current = current->getNext();
		}
		return nullptr;
	}
	void Example_5(int i, int data) {
		Node* current = head;
		Node* temp;
		if (current == head){
			head = current->getNext();
			current = current->getNext();
		}
		j = 0;	
		while (current->getNext() != nullptr){
			if(i==j){
				temp->setNext(current->getNext());
				break;
			}else {
				j++;
				temp = current;
				current = current->getNext();
			}	
		}
		current = NULL;
        head = new Node(data);		
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
