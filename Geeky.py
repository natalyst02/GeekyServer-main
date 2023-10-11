import os
from flask import render_template
from flask_restful import Api

from init_app import app
from src.controller.admin_ctrl import *
from src.controller.authors_ctrl import *
from src.controller.bookmark_ctrl import *
from src.controller.books_ctrl import *
from src.controller.collection_ctrl import *
from src.controller.login_ctrl import *
from src.controller.rating_ctrl import *
from src.controller.user_ctrl import *
from src.controller.subscribe_ctrl import *

# this is to set our environment to https because OAuth 2.0 only supports https environments
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api = Api(app)


api.add_resource(MainPage, '/')
api.add_resource(BooksSearch, '/books/search')
api.add_resource(BooksSearchImage, '/books/search_image')
api.add_resource(BooksFilter, '/books/filter')
api.add_resource(BookDetail, '/books/')

api.add_resource(Login, '/login')
api.add_resource(Callback, '/callback')
# api.add_resource(Logout, '/logout')


api.add_resource(MyAccount, '/my_account')
api.add_resource(MyBookmarks, '/my_bookmark')
api.add_resource(MyNoti, '/my_notification')
api.add_resource(MyRatings, '/my_ratings')
api.add_resource(MyCollections, '/my_collections/<string:coll_name>')
api.add_resource(Subscribe, '/subscribe')

api.add_resource(UserList, '/user_list')
api.add_resource(ChangeRole, '/change_role')
api.add_resource(BanUser, '/ban_user')


# api.add_resource(Authors, '/authors/all')
api.add_resource(AuthorsSearch, '/authors/search')
api.add_resource(AuthorInfo, '/authors/')


@app.route("/home")
@app.route("/search")
@app.route("/login")
@app.route("/reading/<int:book_id>")
@app.route("/Dashboard")
@app.route("/team")
@app.route("/form")
@app.route("/account")
@app.route("/author/<int:auth_id>")
@app.route("/book/<int:book_id>")
def show_item(book_id=None):
    return render_template("index.html")


if __name__ == '__main__':
    from src.utils import *

    app.run(debug=True, host='10.244.2.232', port=3000)
