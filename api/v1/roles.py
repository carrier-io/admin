#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" API """

import flask  # pylint: disable=E0401,W0611
import flask_restful  # pylint: disable=E0401
from flask import g, request

from pylon.core.tools import log  # pylint: disable=E0611,E0401,W0611
from sqlalchemy import schema

from tools import auth, db, api_tools  # pylint: disable=E0401


class AdminAPI(api_tools.APIModeHandler):

    def get(self, target_mode):
        roles = auth.get_roles(target_mode)
        return roles

    def post(self, target_mode):  # pylint: disable=R0201
        """ Process """
        role_name = request.json["name"]
        auth.add_role(role_name, target_mode)
        return {"ok": True}

    def delete(self, target_mode):
        role_name = request.json["name"]
        auth.delete_role(role_name, target_mode)
        return {"ok": True}

    def put(self, target_mode):
        name, new_name = request.json["name"], request.json["new_name"]
        auth.update_role_name(name, new_name, target_mode)
        return {"ok": True}


class ProjectAPI(api_tools.APIModeHandler):

    def get(self, project_id):
        roles = self.module.context.rpc_manager.call.get_roles(project_id)
        return roles

    def post(self, project_id):  # pylint: disable=R0201
        """ Process """
        role_name = request.json["name"]
        result = self.module.context.rpc_manager.call.add_role(project_id, role_name)
        return {"ok": result}

    def delete(self, project_id):
        role_name = request.json["name"]
        result = self.module.context.rpc_manager.call.delete_role(project_id, role_name)
        return {"ok": result}

    def put(self, project_id):
        name, new_name = request.json["name"], request.json["new_name"]
        result = self.module.context.rpc_manager.call.update_role_name(project_id, name,
                                                                       new_name)
        return {"ok": result}


class API(api_tools.APIBase):  # pylint: disable=R0903
    url_params = [
        "<string:target_mode>",
        "<string:mode>/<string:target_mode>",
        "<string:mode>/<int:project_id>",
    ]

    mode_handlers = {
        'project': ProjectAPI,
        'default': ProjectAPI,
        'administration': AdminAPI,
    }
