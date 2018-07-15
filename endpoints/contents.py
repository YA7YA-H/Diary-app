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
