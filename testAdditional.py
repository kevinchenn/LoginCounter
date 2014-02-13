"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests. nrFailed="+str(respData['nrFailed'])
        # When we test the actual project, we require at least 10 unit tests
        minimumTests = 10
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])


        
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd1(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    def testAddUserWithSameUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData1 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData1, None, testLib.RestTestCase.ERR_USER_EXISTS)

    
class TestLoginUser(testLib.RestTestCase):
    """Test Login Users"""
    def assertAddResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def assertLoginResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode, 'count' : 2 }
        self.assertDictEqual(expected, respData)

    def testLogin(self):
        # add user
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertAddResponse(respData, count = 1)

        # login user
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertLoginResponse(respData)

class TestResetFixtureUser(testLib.RestTestCase):
    """Test Reset Fixture Users"""
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        expected = {'errCode':errCode}
        self.assertDictEqual(expected, respData)

    def assertAddResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def assertLoginResponse(self, respData, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode}
        self.assertDictEqual(expected, respData)


    def testRestFixture(self):
        # create user
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertAddResponse(respData, count = 1)

        # resetFixture
        respData = self.makeRequest("/TESTAPI/resetFixture", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData)

        # test that user is no longer there
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertLoginResponse(respData)


