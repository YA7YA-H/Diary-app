"""Handles contents request"""
from flask_restplus import Resource, Namespace, fields
from Api_v1.app.models.content import Content
from flask import request
from Api_v1.app.handlers.token_handler import token_required
from Api_v1.app.app import db
import re

entries_namespace = Namespace("User", description="Content related endpoints")
entries_model = entries_namespace.model(
    "content_model", {
        "Date":
        fields.String(
            required=True,
            description="Date of content entry",
            example="01/01/18"),
        "Content":
        fields.String(
            required=True,
            description="story or detail",
            example="I had fun at the zoo")
    })

content_pattern = re.compile(r"(^[A-Za-z0-9\s\s+]+$)")
date_pattern = re.compile(r"(^[0-9]+/[0-9]+/[0-9]+$)")


@entries_namespace.route("/entries")
@entries_namespace.doc(
    responses={201: "Entry successfully created"}, security="apikey")
class UserEntry(Resource):
    """This class handles get requests in user entry endpoint"""

    @token_required
    def get(self, current_user):
        """Handle get request of url /entries"""
        return {"Entries": db.getall_entries(current_user)}

    @token_required
    @entries_namespace.expect(entries_model)
    def post(self, current_user):
        """Handle post request of url/entries"""
        post = request.get_json()
        date = post["Date"]
        entry = post["Content"]
        if date.isspace() or entry.isspace():
            return {"Message": "please fill it!"}, 400
        try:
            if not re.match(content_pattern, entry):
                return {"Status": "Error", "Message": "Invalid character"}, 400
            if not re.match(date_pattern, date):
                return {"Status": "Error", "Message": "Wrong format"}, 400
        except KeyError:
            return {'Message': "ERROR, try again"}, 400
        else:
            user_entry = Content(current_user, date, entry)
            user_entry.create()
            return {"message": "Entry successfully created"}, 201


@entries_namespace.route('/entries/<int:contentID>')
@entries_namespace.doc(
    responses={
        201: "Entry successfully updated",
        400: "Invalid parameters provided",
        404: "Entry not found"
    },
    security="apikey")
class UpdateEntry(Resource):
    """Handle [UPDATE] request of URL user/entries/id"""

    @token_required
    def get(self, current_user, contentID):
        """Fetch a single entry from db"""
        an_update = [
            result for result in db.getall_entries(current_user)
            if result["ContentID"] == contentID
        ]
        if len(an_update) == 0:
            return {'message': "No entry found"}, 404
        return an_update

    @token_required
    @entries_namespace.expect(entries_model)
    def put(self, current_user, contentID):
        """Modify an entry from db."""
        update_entries = [
            entries_data for entries_data in db.getall_entries(current_user)
            if entries_data["ContentID"] == contentID
        ]
        if len(update_entries) == 0:
            return {'message': 'No content found'}, 404
        else:
            post_data = request.get_json()
            update_date = post_data.get("Date", None)
            update_content = post_data.get("Content", None)
            try:
                if update_content is not None:
                    if not re.match(content_pattern, update_content):
                        return {
                            "Status": "Error",
                            "Message": "Invalid character"
                        }, 400
                if update_date is not None:
                    if not re.match(date_pattern, update_date):
                        return {
                            "Status": "Error",
                            "Message": "Wrong format"
                        }, 400
            except KeyError:
                return {'Message': "ERROR, try again"}, 400
            else:
                if (update_content and update_date) != None:
                    db.update_entries(update_date, update_content, contentID)
                    return {'Message': 'successfully updated entry'}, 201
                else:
                    if update_date is not None:
                        an_update = [
                            result
                            for result in db.getall_entries(current_user)
                            if result["ContentID"] == contentID
                        ]
                        content = an_update[0]['Content']
                        db.update_entries(content, update_date, contentID)
                        return {'Message': 'successfully updated date'}, 201

                    if update_content is not None:
                        an_update = [
                            result
                            for result in db.getall_entries(current_user)
                            if result["ContentID"] == contentID
                        ]
                        date = an_update[0]["Date"]
                        db.update_entries(update_content, date, contentID)
                        return {'Message': 'successfully updated content'}, 201

    @token_required
    def delete(self, current_user, contentID):
        """Delete an entry with an id from db"""
        del_item = [
            del_item for del_item in db.getall_entries(current_user)
            if del_item["ContentID"] == contentID
        ]
        if len(del_item) == 0:
            return {"Message": "Sorry, No such id is found to be deleted"}, 404
        db.delete_entry(contentID)
        return {"status": "Entry successfully deleted"}, 201
