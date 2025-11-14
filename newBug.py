"""
Linked List Implementation with a Bug

This module contains a simple linked list implementation with basic operations.
There is an intentional bug in the delete method.
"""

class Node:
    """Represents a node in the linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """A simple singly linked list implementation."""

    def __init__(self):
        self.head = None

    def append(self, data):
        """Add a new node with the given data to the end of the list."""
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """Add a new node with the given data to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """
        Delete the first node with the given data.

        BUG INTRODUCED: This method fails to update the head pointer when
        deleting the first node in the list. It only updates current.next
        but doesn't reassign self.head, causing the deleted node to remain
        as the head of the list.
        """
        if not self.head:
            return

        current = self.head

        # BUG: When deleting the head node, we don't update self.head
        if current.data == data:
            self.head = current.next  # Correctly update self.head
            return
        # Rest of the deletion logic works correctly
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def display(self):
        """Display all elements in the linked list."""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) if elements else "Empty list"

    def find(self, data):
        """Find a node with the given data."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False


if __name__ == "__main__":
    # Test the linked list
    ll = LinkedList()

    # Add some elements
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)

    print("Initial list:", ll.display())

    # Try to delete the head node (this will fail due to the bug)
    ll.delete(0)
    print("After deleting 0:", ll.display())  # Expected: "1 -> 2 -> 3", Actual: "0 -> 1 -> 2 -> 3"

    # Delete a middle node (this works correctly)
    ll.delete(2)
    print("After deleting 2:", ll.display())