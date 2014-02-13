import unittest
from loginCounter.models import User
from django.test import TestCase

# Create your tests here.
class UserTestCase(unittest.TestCase):

	def setUp(self):
		User.objects.all().delete()

	def testAddUser(self):
		"""
		Tests adding user
		"""
		user = User()
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

	def testAddUserThatCountIsOne(self):
		"""
		Tests that adding user initailizes count 1
		"""

		# create user
		user = User()
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# get just created user
		thisUser = User.objects.get(user="user1", password="password")
		self.assertEquals(thisUser.count, 1)

	def testAddUserIfUserAlreadyExists(self):
		"""
		Tests adding user when same user already exists
		"""
		user = User()

		# create user
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# create duplicate user
		errCode1 = user.add("user1", "password")
		self.assertEquals(User.ERR_USER_EXISTS, errCode1)

	def testAddTwoUsers(self):
		"""
		Tests adding 2 users
		"""
		user = User()

		# add user 1
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# add user 2
		errCode1 = user.add("user2", "password1")
		self.assertEquals(User.SUCCESS, errCode1)

	def testAddTwoUserThenDuplicateUserOfFirstUser(self):
		"""
		Tests adding 2 users then adding the first user again
		"""
		user = User()

		# add user 1
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# add user 2
		errCode1 = user.add("user2", "password1")
		self.assertEquals(User.SUCCESS, errCode1)

		# add duplicate user 1
		errCode2 = user.add("user1", "password")
		self.assertEquals(User.ERR_USER_EXISTS, errCode2)

	def testAddTwoUserThenDuplicateUserOfSecondUser(self):
		"""
		Tests adding 2 users then adding the second user again
		"""
		user = User()

		# add user 1
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# add user 2
		errCode1 = user.add("user2", "password1")
		self.assertEquals(User.SUCCESS, errCode1)

		# add duplicate user 1
		errCode2 = user.add("user2", "password1")
		self.assertEquals(User.ERR_USER_EXISTS, errCode2)

	def testAddEmptyUsername(self):
		"""
		Tests adding when username is empty
		"""
		user = User()

		# add user with empty username
		errCode = user.add("", "password")
		self.assertEquals(User.ERR_BAD_USERNAME, errCode)

	def testAddEmptyPassword(self):
		"""
		Tests adding when password is empty
		"""
		user = User()

		# add user with empty password
		errCode = user.add("user1", "")
		self.assertEquals(User.SUCCESS, errCode)

	def testAddUserWithMoreThanMaxLengthUsername(self):
		"""
		Tests adding when username is greater than 128 length
		"""
		user = User()

		# check username test length
		username = "thisstringwillbeover128characteresinlengthhopefullyafterIwritethissentencethisstringwillbeover128characteresinlengthhopefullyafterIwritethissentence"
		self.assertTrue(len(username) >= 128)

		# add user with string length of 128 for username
		errCode = user.add(username, "password")
		self.assertEquals(User.ERR_BAD_USERNAME, errCode)

	def testAddUserWIthExactlyMaxLength(self):
		"""
		Tests adding when username is exactly 128 length
		"""
		user = User()

		# check username test length
		username = "thisstringwillbeover128characteresinlengthhopefullyafterIwritethissentencethisstringwillbeover128characteresinlengthhopefullyaft"
		self.assertTrue(len(username) == 128)

		# add user with string length of 128 for username
		errCode = user.add(username, "password")
		self.assertEquals(User.SUCCESS, errCode)

	def testLogin(self):
		"""
		Tests login
		"""
		user = User()

		# create a user
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# login with that user
		errCode1 = user.login("user1", "password")
		self.assertEquals(User.SUCCESS, errCode1)

	def testLoginWithCountIncrease(self):
		"""
		Tests that login increases count
		"""
		user = User()

		# create a user
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# get just created user should have count with 1
		thisUser = User.objects.get(user="user1", password="password")
		self.assertEquals(thisUser.count, 1)

		# login with that user
		errCode1 = user.login("user1", "password")
		self.assertEquals(User.SUCCESS, errCode1)

		# get that user again and count should be 2
		thisUserAgain = User.objects.get(user="user1", password="password")
		self.assertEquals(thisUserAgain.count, 2)

	def testLoginTwiceToIncreaseCountTwice(self):
		"""
		Tests that 2 logins increases count by 2
		"""
		user = User()

		# create a user
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# get just created user should have count with 1
		thisUser = User.objects.get(user="user1", password="password")
		self.assertEquals(thisUser.count, 1)

		# login with that user
		errCode1 = user.login("user1", "password")
		self.assertEquals(User.SUCCESS, errCode1)

		# login with that user again
		errCode1 = user.login("user1", "password")
		self.assertEquals(User.SUCCESS, errCode1)

		# get that user again and count should be 3
		thisUserAgain = User.objects.get(user="user1", password="password")
		self.assertEquals(thisUserAgain.count, 3)

	def testLoginWithWrongPassword(self):
		"""
		Tests login with badCredentials - wrong password
		"""
		user = User()

		# create a user
		errCode = user.add("user1", "password")
		self.assertEquals(User.SUCCESS, errCode)

		# login with that user
		errCode1 = user.login("user1", "password123")
		self.assertEquals(User.ERR_BAD_CREDENTIALS, errCode1)

	def testLoginWithBlankUserName(self):
		"""
		Tests login with badCredentials - empty username
		"""
		user = User()

		# login with blank username
		errCode1 = user.login("", "password123")
		self.assertEquals(User.ERR_BAD_CREDENTIALS, errCode1)

	def testLoginWithBlankPassword(self):
		"""
		Tests adding when password is empty
		"""
		user = User()

		# add user with empty password
		errCode = user.add("user1", "")
		self.assertEquals(User.SUCCESS, errCode)

		# login with that user
		errCode1 = user.login("user1", "")
		self.assertEquals(User.SUCCESS, errCode1)



