# -*- coding: utf-8 -*-
"""
Synchronous Scrapinghub AutoExtract API client.
"""

from typing import Optional, Dict, Any, List

import requests

from .batching import record_order, build_query, restore_order
from .constants import API_ENDPOINT, API_TIMEOUT
from .apikey import get_apikey
from .utils import user_agent


def request_raw(query: List[Dict[str, Any]],
                api_key: Optional[str] = None,
                endpoint: str = API_ENDPOINT,
                ) -> List[Dict[str, Any]]:
    """ Send a request to Scrapinghub AutoExtract API.
    Query is a list of dicts, as described in the API docs
    (see https://doc.scrapinghub.com/autoextract.html).
    """
    auth = (get_apikey(api_key), '')
    timeout = API_TIMEOUT + 60
    headers = {'User-Agent': user_agent(requests)}
    resp = requests.post(endpoint, json=query, auth=auth,
                         headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def request_batch(urls: List[str],
                  page_type: str,
                  api_key: Optional[str] = None,
                  endpoint: str = API_ENDPOINT,
                  ) -> List[Dict]:
    query = record_order(build_query(urls, page_type))
    results = request_raw(query, api_key=api_key, endpoint=endpoint)
    return restore_order(results)
