from pydantic import BaseModel


class TokenOut(BaseModel):
    '''
    - access_token: string
    - token_type: string, default=bearer
    '''
    access_token: str
    token_type: str = "bearer"


class LoginIn(BaseModel):
    '''
    - email: string
    - password: string
    '''
    email: str
    password: str


class RegisterIn(BaseModel):
    '''
    - email: string
    - password: string
    '''
    email: str
    password: str


class DeviceAuthIn(BaseModel):
    '''
    - device_key: string
    '''
    device_key: str
