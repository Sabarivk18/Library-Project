from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Data storage (can be replaced with a database in a production environment)
books = []
members = []
transactions = []


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Book management routes
@app.route('/books', methods=['GET', 'POST'])
def book_management():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        quantity = int(request.form['quantity'])
        book = {'title': title, 'author': author, 'quantity': quantity}
        books.append(book)
        return redirect('/books')
    else:
        return render_template('books.html', books=books)


@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    del books[book_id]
    return redirect('/books')


# Member management routes
@app.route('/members', methods=['GET', 'POST'])
def member_management():
    if request.method == 'POST':
        name = request.form['name']
        initial_debt = int(request.form['initial_debt'])
        member = {'name': name, 'debt': 0}
        members.append(member)
        return redirect('/members')
    else:
        return render_template('members.html', members=members)

@app.route('/members/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    del members[member_id]
    return redirect('/members')


# Book issuing and returning routes
@app.route('/transactions', methods=['GET', 'POST'])
def transaction_management():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        member_id = int(request.form['member_id'])
        book = books[book_id]
        member = members[member_id]
        
        if book['quantity'] > 0:
            transaction = {'book_id': book_id, 'member_id': member_id, 'returned': False, 'fee': 0}
            transactions.append(transaction)
            
            # Decrease book quantity by 1
            book['quantity'] -= 1
            
            return redirect('/transactions')
        else:
            return "Book is not available."
    else:
        return render_template('transactions.html', transactions=transactions, books=books, members=members)


@app.route('/transactions/return/<int:transaction_id>', methods=['POST'])
def return_book(transaction_id):
    transaction = transactions[transaction_id]
    book_id = transaction['book_id']
    member_id = transaction['member_id']
    
    book = books[book_id]
    member = members[member_id]
    
    # Increase book quantity by 1
    book['quantity'] += 1
    
    # Calculate rent fee based on rental duration
    rental_duration = 7  # Assuming a rental duration of 7 days
    rent_fee = rental_duration * 10  # Adjust the fee calculation as per your requirement
    
    # Update the rent fee in the transaction
    transaction['fee'] = rent_fee
    
    # Update the returned status
    transaction['returned'] = True
    
    # Update the member's debt
    member['debt'] += rent_fee
    
    return redirect('/transactions')

# Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query'].lower()
        search_results = []
        for book in books:
            if query in book['title'].lower() or query in book['author'].lower():
                search_results.append(book)
        return render_template('search.html', search_results=search_results, query=query)
    else:
        return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
