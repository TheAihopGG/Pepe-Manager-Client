import requests
import json
from services.typed_dicts import TypedPackage
from data.settings import API_URL

__doc__ == """"""

def get_package_from_api(*,
    name: str | None = None,
    version: str | None = None,
    id: int | None = None
) -> (TypedPackage | None):
    if name and version:
        response = requests.get(f'{API_URL}api/package/?name={name}&version={version}')
        if response.ok: 
            return json.loads(response.content.decode())['package']
        
        else:
            return None
        
    elif id:
        response = requests.get(f'{API_URL}api/package/?id={id}')
        if response.ok: 
            return json.loads(response.content.decode())['package']
        
        else:
            return None
        
    else:
        return None
