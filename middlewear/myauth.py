from apps.member.models import User

class MemberAuth(object):  
	def autentikasi(self, username=None, password=None):  
		try:
			user = User.objects.get(username=username, password=password)  
			return user
		except User.DoesNotExist:
			return None
		
	#def get_user(self, user_id):
		  
