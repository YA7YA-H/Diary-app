"""Handles contents request"""
from flask_restplus import Resource, Namespace, fields
from Api_v1.app.models.content import Content
from flask import request
from Api_v1.app.models.token import token_required
from Api_v1.app.app import db

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


@entries_namespace.route("/entries")
@entries_namespace.doc(
    responses={201: "Entry successfully created"}, security="apikey")
class UserEntry(Resource):
    """This class handles get requests in user entry endpoint"""

    @token_required
    def get(self, current_user):
        """Handle get request of url /entries"""
        return {"message": db.getall_entries(current_user)}

    @token_required
    @entries_namespace.expect(entries_model)
    def post(self, current_user):
        """Handle post request of url/entries"""
        post = request.get_json()
        date = post["Date"]
        entry = post["Content"]
        user_entry = Content(current_user, date, entry)
        user_entry.create()
        return {"status": "Entry successfully created"}, 201


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
        an_update = [
            result for result in db.getall_entries(current_user)
            if result["ContentID"] == contentID
        ]
        if len(an_update) == 0:
            return {'Status': "No entry found"}, 404
        return an_update

    @token_required
    @entries_namespace.expect(entries_model)
    def put(self, current_user, contentID):
        """Modify a entries."""
        update_entries = [
            entries_data for entries_data in db.getall_entries(current_user)
            if entries_data["ContentID"] == contentID
        ]
        if len(update_entries) == 0:
            return {'message': 'No content found'}, 404
        else:
            post_data = request.get_json()
            update_date = post_data["Date"]
            update_content = post_data["Content"]
            db.update_entries(update_date, update_content, contentID)
            return {'Message': 'successfully updated'}, 201

    @token_required
    def delete(self, current_user, contentID):
        del_item = [
            del_item for del_item in db.getall_entries(current_user)
            if del_item["ContentID"] == contentID
        ]
        if len(del_item) == 0:
            return {"Message": "Sorry, No such id is found to be deleted"}, 404
        db.delete_entry(contentID)
        return {"status": "Entry successfully deleted"}, 201
