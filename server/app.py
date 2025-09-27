#!/usr/bin/env python3

from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # Get query params with defaults
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # Run paginated query
        paginated = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        # Serialize items
        items = [BookSchema().dump(book) for book in paginated.items]

        # Build response with metadata
        response = {
            "page": page,
            "per_page": per_page,
            "total": paginated.total,
            "total_pages": paginated.pages,
            "items": items
        }

        return response, 200


api.add_resource(Books, '/books', endpoint='books')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
