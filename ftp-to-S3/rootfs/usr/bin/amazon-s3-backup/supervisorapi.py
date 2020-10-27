import requests


class SupervisorAPIError(Exception):
    pass


class _BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class SupervisorAPI:
    BASE_URL = "http://supervisor"

    def __init__(self, token: str):
        """Interact with the Home Assistant Supervisor API

        Args:
            token (str): Supervisor bearer token
        """
        self.auth = _BearerAuth(token)

    def _get(self, path: str) -> requests.Response:
        url = f"{SupervisorAPI.BASE_URL}{path}"
        try:
            response = requests.get(url, auth=self.auth)
        except requests.exceptions.ConnectionError as err:
            raise SupervisorAPIError(
                f"Error connecting to Home Assistant Supervisor API: {err}")
        except requests.exceptions.Timeout as err:
            raise SupervisorAPIError(
                "Timeout connecting to Home Assistant Supervisor API")
        else:
            json = None
            if response.ok:
                try:
                    json = response.json()
                except ValueError as err:
                    raise SupervisorAPIError(
                        "Error decoding response from Home Assistant Supervisor API")
            return json

    def _post(self, path: str) -> requests.Response:
        url = f"{SupervisorAPI.BASE_URL}{path}"
        try:
            response = requests.post(url, auth=self.auth)
        except requests.exceptions.ConnectionError as err:
            raise SupervisorAPIError(
                f"Error connecting to Home Assistant Supervisor API: {err}")
        except requests.exceptions.Timeout as err:
            raise SupervisorAPIError(
                "Timeout connecting to Home Assistant Supervisor API")
        else:
            json = None
            if response.ok:
                try:
                    json = response.json()
                except ValueError as err:
                    raise SupervisorAPIError(
                        "Error decoding response from Home Assistant Supervisor API")
            return json

    def get_recordings(self):
        """Get list of all recordings

        Returns:
            List: List of recordings
        """
        response = self._get("/recordings")
        return response.get("data", {}).get("recordings", [])

    def get_recording(self, slug: str):
        """Get details of a single recordings

        Args:
            slug (str): Slug of recordings to retrieve

        Returns:
            dict: Dictionary containing recordings details
        """
        response = self._get(f"/recordings/{slug}/info")
        return response.get("data")

    def remove_recording(self, slug: str) -> bool:
        """Delete a recording

        Args:
            slug (str): Slug of recording to delete

        Returns:
            bool: True if successful
        """
        response = self._post(f"/recordings/{slug}/remove")
        return True if response.get("result") == "ok" else False
