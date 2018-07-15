"""Handles contents request"""
from flask_restplus import Resource, Namespace, fields
from models.content import content_data, Content
from flask import request

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
@entries_namespace.doc(responses={201: "Entry successfully created"})
class UserEntry(Resource):
    """This class handles get requests in user entry endpoint"""

    def get(self):
        """Handle get request of url /entries"""
        return content_data

    @entries_namespace.expect(entries_model)
    def post(self):
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
    })
class UpdateEntry(Resource):
    """Handle [UPDATE] request of URL user/entries/id"""

    def get(self, contentID):
        an_update = [
            result for result in content_data
            if result["contentID"] == contentID
        ]
        if len(an_update) == 0:
            return {'Status': "No entry found"}
        return an_update
