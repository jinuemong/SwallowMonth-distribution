import json

from rest_framework.renderers import JSONRenderer


class UserJsonRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self,data,media_type=None,renderer_context=None):
        
        #view에서 error를 던지면 내부 data에 errors가 담김
        
        errors = data.get('errors',None) # 에러 받기 
        
        # 토큰은 byte 형태라 직렬화가 불가능 
        # rendering 전에 decode 필수 : 해독과정
        # token만 따로 저장 
        
        token = data.get('token',None)
        
        # 에러 발견 시 data를 user key에 넣지 않고 그대로 반환
        if errors is not None:
            return super(UserJsonRenderer,self).render(data)
        
        
        # 토큰이 바이트인 경우 처리
        
        if token is not None and isinstance(token,bytes):
            data['token'] = token.decode('utf-8') #charset으로 처리 
        
        
        # 데이터를 user 키에 넣고 반환
        
        return json.dumps({
            'user':data
        })
        
        # 바이트에서 utf-8로 변환 후 다시 토큰에 추가 
        # 뷰에 적용 