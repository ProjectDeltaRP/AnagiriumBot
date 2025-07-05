import requests


class RobloxGroupManager:
    def __init__(self, api_key, group_ids):
        self.api_key = api_key
        self.group_ids = group_ids
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def get_roles(self, group_id):
        roles = {}
        page = None
        while True:
            params = {"maxPageSize": 20}
            if page:
                params["pageToken"] = page
            r = requests.get(f"https://apis.roblox.com/cloud/v2/groups/{group_id}/roles", headers=self.headers, params=params)
            r.raise_for_status()
            data = r.json()
            for role in data["groupRoles"]:
                roles[role["id"]] = role["displayName"]
            page = data.get("nextPageToken")
            if not page:
                break
        return roles

    def get_memberships(self, group_id):
        members = []
        page = None
        while True:
            params = {"maxPageSize": 50}
            if page:
                params["pageToken"] = page
            r = requests.get(f"https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships", headers=self.headers, params=params)
            r.raise_for_status()
            data = r.json()
            members.extend(data["groupMemberships"])
            page = data.get("nextPageToken")
            if not page:
                break
        return members

    def fetch_username(self, user_id):
        r = requests.get(f"https://apis.roblox.com/cloud/v2/users/{user_id}", headers=self.headers)
        r.raise_for_status()
        return r.json().get("displayName")

    def get_members_list(self):
        all_members = {}
        for group_id in self.group_ids:
            roles = self.get_roles(group_id)
            members = self.get_memberships(group_id)
            group_members = []
            for m in members:
                uid = m["user"].split("/")[-1]
                rid = m["role"].split("/")[-1]
                name = self.fetch_username(uid)
                role_name = roles.get(rid, None)
                group_members.append({'user_id': uid, 'username': name, 'role_id': rid, 'role_name': role_name})
            all_members[group_id] = group_members
        return all_members

    def change_member_role(self, group_id, user_id, role_name):
        roles = self.get_roles(group_id)
        target = next((rid for rid, name in roles.items() if name.lower() == role_name.lower()), None)
        if not target:
            raise ValueError(f"Role '{role_name}' not found")

        members = self.get_memberships(group_id)
        membership = next((m for m in members if m["user"].endswith(f"/{user_id}")), None)
        if not membership:
            raise ValueError(f"User {user_id} not found in group")
        membership_id = membership["path"].split("/")[-1]

        resp = requests.patch(
            f"https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships/{membership_id}",
            headers=self.headers,
            json={"role": f"groups/{group_id}/roles/{target}"}
        )
        resp.raise_for_status()
        return True
