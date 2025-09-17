from __future__ import annotations

import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from django.conf import settings


class DarkerDBClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.DARKERDB_API_KEY
        self.base_url = (base_url or settings.DARKERDB_API_BASE).rstrip("/")

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = dict(params or {})
        if self.api_key:
            params.setdefault("key", self.api_key)
        url = f"{self.base_url}{path}"
        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        return res.json()

    def health(self) -> Dict[str, Any]:
        return self._get("/v1/health-check")

    def items(self, **params: Any) -> Dict[str, Any]:
        return self._get("/v1/items", params=params)

    def item(self, item_id: str, **params: Any) -> Dict[str, Any]:
        return self._get(f"/v1/items/{item_id}", params=params)

    def market(self, **params: Any) -> Dict[str, Any]:
        return self._get("/v1/market", params=params)

    def leaderboards(self) -> Dict[str, Any]:
        return self._get("/v1/leaderboards")

    def leaderboard(self, leaderboard_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/leaderboards/{leaderboard_id}")

    def population(self) -> Dict[str, Any]:
        return self._get("/v1/population")

    def population_history(self, **params: Any) -> Dict[str, Any]:
        return self._get("/v1/population/history", params=params)


