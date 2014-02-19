from django.db import models

# Create your models here.
class User(models.Model):
	
	## The success return code
    SUCCESS               =   1

    ## Cannot find the user/password pair in the database (for login only)
    ERR_BAD_CREDENTIALS   =  -1

    ## trying to add a user that already exists (for add only)
    ERR_USER_EXISTS       =  -2

    ## invalid user name (empty or longer than MAX_USERNAME_LENGTH) (for add, or login)
    ERR_BAD_USERNAME      =  -3

    ## invalid password name (longer than MAX_PASSWORD_LENGTH) (for add)
    ERR_BAD_PASSWORD      =  -4


    ## The maximum length of user name
    MAX_USERNAME_LENGTH = 128

    ## The maximum length of the passwords
    MAX_PASSWORD_LENGTH = 128

    user = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    count = models.IntegerField()

    
    def login(self, user, password):
    	try:
    		user = User.objects.get(user=user, password=password)
    		user.count = user.count + 1
    		user.save()
    		return User.SUCCESS
    	except User.DoesNotExist:
    		return User.ERR_BAD_CREDENTIALS

    def add(self, user, password):

    	if User.objects.filter(user=user).exists():
    		return User.ERR_USER_EXISTS

    	def valid_username(username):
            return username != "" and len(username) <= User.MAX_USERNAME_LENGTH

        def valid_password(password):
            return len(password) <= User.MAX_PASSWORD_LENGTH

        if not valid_username(user):
            return User.ERR_BAD_USERNAME
        if not valid_password(password):
            return User.ERR_BAD_PASSWORD

        user = User(user = user, password = password, count = 1)
        user.save()
        return User.SUCCESS

    def resetFixture(self):
    	User.objects.all().delete()
    	return User.SUCCESS

    def errorMessage(self, errCode):
        if errCode == User.ERR_BAD_USERNAME:
            return 'Bad Username!'
        elif errCode == User.ERR_BAD_PASSWORD:
            return 'Bad Password!'
        elif errCode == User.ERR_USER_EXISTS:
            return 'Username Already Exists!'
        elif errCode == User.ERR_BAD_CREDENTIALS:
            return 'Bad credentials! Incorrect username/password'
        elif errCode == User.MAX_PASSWORD_LENGTH:
            return 'Password exceeds 128 characters'
        elif errCode == User.MAX_USERNAME_LENGTH:
            return 'Username must not be empty and must also be under 128 characters'