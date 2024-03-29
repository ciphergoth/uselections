#   Copyright 2020 Google LLC

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       https://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import dataclasses

import requests_cache
import toml

@dataclasses.dataclass
class Context:
    config: dict
    session: requests_cache.CachedSession

def get():
    with open("config.toml") as f:
        config = toml.load(f)
    session = requests_cache.CachedSession(expire_after=86400)
    return Context(session = session, config = config)
