import json

import google.auth.transport.requests
import requests
from flask import redirect, request
from flask.wrappers import Response
from flask_cors import cross_origin
from flask_restful import Resource
from google.oauth2 import id_token
from pip._vendor import cachecontrol

from config.config import FRONTEND_URL, GOOGLE_CLIENT_ID, flow
from init_app import db
from src.const import *
from src.models.states_md import States
from src.models.users_md import Users
from src.services.ratings_sv import *
from src.services.users_sv import *
from src.utils import *


class Login(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        authorization_url, state = flow.authorization_url()
        # response = redirect(authorization_url)

        db.session.add(States(state))
        db.session.commit()
        print("STATE FROM LOGIN(): ", state)  # gud

        response = Response(
            response=json.dumps(
                {'auth_url': authorization_url, 'state': state}),
            status=200,
            mimetype='application/json'
        )
        # response.set_cookie(STATE, state)

        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response


class Callback(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        # print("STATE AT BEGINNING OF CALLBACK(): ", request.cookies.get(STATE)) # wrong

        flow.fetch_token(authorization_response=request.url)

        # response = redirect(f"{FRONTEND_URL}/account")

        db_state = States.query.filter_by(
            state=request.args[STATE]).first()
        if not db_state:
            # remove_current_state()
            print("DB_STATE: ", db_state.state)
            return {"message": "States don't match. You may delete your cookies and retry."}, 500

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(
            session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=3
        )

        current_email = id_info.get(EMAIL)

        user = Users.query.filter_by(email=current_email).first()
        if user is None:
            user = Users(email=current_email, profile_pic=id_info.get(PICTURE))
            db.session.add(user)

        user.login_state = db_state.state
        db.session.commit()

        if user.user_role == 0:
            response = redirect(f"{FRONTEND_URL}/account")
        else:
            response = redirect(f"{FRONTEND_URL}/dashboard")

        return response


# class Logout(Resource):
#     def get(self):
#         # remove_current_state()
#         # response = redirect("/")
#         # response.delete_cookie(STATE)
#         # return response

#         return Response(
#             response=json.dumps({"message": "Logged out"}),
#             status=202,
#             mimetype='application/json'
#         )
