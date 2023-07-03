from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'yo yo'
    birth: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '12a3',
    'birth': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}
user = User(**external_data)
print(user.dict())
