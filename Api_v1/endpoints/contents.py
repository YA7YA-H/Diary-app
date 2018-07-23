"""Handles contents request"""
from flask_restplus import Resource, Namespace, fields
from Api_v1.models.content import content_data, Content
from flask import request
from Api_v1.models.token import token_required

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
        return content_data

    @token_required
    @entries_namespace.expect(entries_model)
    def post(self, current_user):
        """Handle post request of url/entries"""
        post = request.get_json()
        date = post["Date"]
        entry = post["Content"]
        user_entry = Content(date, entry)
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
            result for result in content_data
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
            entries_data for entries_data in content_data
            if entries_data["ContentID"] == contentID
        ]
        if len(update_entries) == 0:
            return {'message': 'No content found'}, 404
        else:
            post_data = request.get_json()
            update_entries[0]["Date"] = post_data["Date"]
            update_entries[0]["Content"] = post_data["Content"]

            return {"status": " Entry content successfully created"}, 201

    @token_required
    def delete(self, current_user, contentID):
        del_item = [
            del_item for del_item in content_data
            if del_item["ContentID"] == contentID
        ]
        if len(del_item) == 0:
            return {"Message": "Sorry, No such id is found to be deleted"}, 404
        del content_data[contentID]
        return {"status": "Entry successfully deleted"}, 201
