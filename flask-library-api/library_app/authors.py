from flask import jsonify, request
from webargs.flaskparser import use_args
from library_app import app, db
from library_app.models import Author, AuthorSchema, author_schema
from library_app.utils import validate_json_content_type


@app.route('/api/v1/authors', methods = ['GET'])
def get_authors():
    query = Author.query
    schema_args = Author.get_schema_args(request.args.get('fields'))
    query = Author.apply_order(query, request.args.get('sort'))
    query = Author.apply_filter(query, request.args)
    authors = query.all()
    author_schema = AuthorSchema(**schema_args)
    
    return jsonify({
        'success': True,
        'data': author_schema.dump(authors),
        'number_of_records': len(authors)
    })


@app.route('/api/v1/authors/<int:author_id>', methods = ['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')

    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@app.route('/api/v1/authors', methods = ['POST'])
@validate_json_content_type
@use_args(author_schema, error_status_code = 400)
def create_author(args: dict):
    author = Author(**args)
    db.session.add(author)
    db.session.commit()

    # data = request.get_json()
    # first_name = data.get('first_name')
    # last_name = data.get('last_name')
    # birth_date = data.get('birth_date')
    # author = Author(first_name=first_name, last_name=last_name, birth_date=birth_date)
    # print(author)

    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    }), 201


@app.route('/api/v1/authors/<int:author_id>', methods = ['PUT'])
@validate_json_content_type
@use_args(author_schema, error_status_code = 400)
def update_author(args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')
    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@app.route('/api/v1/authors/<int:author_id>', methods = ['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')

    db.session.delete(author)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Author with id {author_id} has been deleted'
    })
