from django.conf import settings

import requests


class StreamClient:
    @property
    def _api_url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/stream"

    @property
    def request_headers(self):
        return {
            "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }

    def get_video_data(self, video_uid):
        res = requests.get(
            f"{self._api_url}/{video_uid}",
            headers=self.request_headers,
        )
        return res.json()["result"]

    def upload_via_link(self, link, meta={}):
        res = requests.post(
            f"{self._api_url}/copy",
            headers=self.request_headers,
            json={"url": link, "meta": meta},
        )
        return res.json()["result"]

    def update_video_data(self, video_uid, data={}):
        res = requests.post(
            f"{self._api_url}/{video_uid}",
            headers=self.request_headers,
            json=data,
        )
        return res.json()["result"]

    def upload_caption_file(self, video_uid, language_code, caption_file):
        res = requests.put(
            f"{self._api_url}/{video_uid}/captions/{language_code}",
            headers={key: value for key, value in self.request_headers.items() if key != "Content-Type"},
            files={"file": caption_file},
        )
        return res.json()

    def delete_video_data(self, video_uid):
        res = requests.delete(
            f"{self._api_url}/{video_uid}",
            headers=self.request_headers,
        )
        return res

    def list_videos(self, params=None):
        # params to paginate ?before=last-video-created
        res = requests.get(
            f"{self._api_url}",
            params=params,
            headers=self.request_headers,
        )
        return res.json()

    def download_video(self, video_uid):
        res = requests.post(
            f"{self._api_url}/{video_uid}/downloads",
            headers=self.request_headers,
        )
        return res.json()
