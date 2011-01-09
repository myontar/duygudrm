# Copyright (c) Microsoft Corporation. All rights reserved
import urlparse
import pprint
import urllib
import urllib2
import string

class OAuthWrapHandler:
    #Contains the logic for issuing WRAP requests to LIVE services.

    #Instance variables that control the settings that are sent as part of
    #requests to the LIVE services.
    app_id  = None
    app_secret = None
    callback = None
    scope = None
    verification_code = None
    access_token  = None
    refresh_code = None
    wrap_urls = None

    #Tuples that contain the parameter responses returned from the LIVE service
    #requests.
    consent_response = None
    access_response = None
    refresh_response = None

    def build_consent_url(self):
        #Generates a URL with parameters to access the LIVE consent UX.

        consentUrl = self.__build_consent_url(self.app_id, self.callback, self.scope)
        return consentUrl

    def __build_consent_url(self, app_id, callback, scope):
        #Constructs a url to pass along in the redirect to the Live consent page.
		
        consentUrlParts = {
            'wrap_client_id': app_id,
            'wrap_callback': callback,
            'wrap_scope': scope
        }

        consentUrl = self.wrap_urls['consent'] + '?' + urllib.urlencode(consentUrlParts)
        return consentUrl

    def get_authorization_token(self):
        #Gets the authorization token after the user granted an application
        #access to resources via the consent UX.
        self.access_response = self.__get_authorization_response(
            self.wrap_urls['access'],
            self.app_id,
            self.app_secret,
            self.callback,
            self.verification_code)
            
        if 'wrap_refresh_token' in self.access_response:
            self.refresh_code = self.access_response['wrap_refresh_token']

        self.access_token = self.access_response['wrap_access_token']

        return self.access_token

    def refresh_authorization_token(self):
        #Gets a refreshed authorization token after the existing authorization
        #token has expired.
        self.refresh_response = self.__get_refresh_response(
                                            self.wrap_urls['refresh'],
                                            self.app_id,
                                            self.app_secret,
                                            self.refresh_code)
                                            
        if 'wrap_refresh_token' in self.refresh_response:
            self.access_token = self.refresh_response['wrap_access_token']

        return self.access_token

    def __get_authorization_response(self, url, app_id, app_secret, callback, verification_code):
        #Private method that issues a call to the LIVE service that will
        #return an authorization token.
        access_params = {
            'wrap_client_id': app_id,
            'wrap_client_secret': app_secret,
            'wrap_callback': callback,
            'wrap_verification_code': verification_code
        }

        response = self.__post_data(url, access_params)
        return response

    def __get_refresh_response(self, url, app_id, app_secret, refresh_code):
        #Private method that issues the call to LIVE service that will
        #refresh an expired authorization token.
        refresh_params = {
                          'wrap_refresh_token': refresh_code,
                          'wrap_client_id': app_id,
                          'wrap_client_secret': app_secret
                          }
        response = self.__post_data(url, refresh_params)
        return response
    def userdata(self):


        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "WRAP access_token=" + self.access_response['wrap_access_token'],
            
            }
        import httplib
        import json
        webservice = httplib.HTTPSConnection("apis.live.net")
        webservice.putrequest("GET", "/v4.1/")
        if headers != None:
            for head in headers:

                webservice.putheader(head, headers[head])
        webservice.endheaders()

        webservice.send('')
        rt = webservice.getresponse()
        
        uri = json.loads(rt.read())['SignedInUser']['Cid']



        webservice = httplib.HTTPSConnection("profiles.apis.live.net")
        webservice.putrequest("GET", "/v4.1/cid-"+uri+"/Profiles")
        if headers != None:
            for head in headers:

                webservice.putheader(head, headers[head])
        webservice.endheaders()

        webservice.send('')
        rt = webservice.getresponse()
        data = json.loads(rt.read())
        email = data['Entries'][0]['Emails'][0]['Address']
        name = data['Entries'][0]['FirstName']
        surname = data['Entries'][0]['LastName']
        propic = data['Entries'][0]['ThumbnailImageLink']




        webservice = httplib.HTTPSConnection("bay.apis.live.net")
        webservice.putrequest("GET", "/V4.1/cid-"+uri.upper()+"/Contacts/AllContacts")
        print "/V4.1/cid-"+uri.upper()+"/AllContacts"
        if headers != None:
            for head in headers:

                webservice.putheader(head, headers[head])
        webservice.endheaders()

        webservice.send('')
        rt = webservice.getresponse()
        data = rt.read()
        print rt.status
        data =  json.loads(data)
        mail_contacts = []
        service_contacts = []
        
        for i in data['Entries']:
            if i['Title'].find("@") > -1:
                mail_contacts.append(i['Title'])
            else:
                try:
                    service_contacts.append(i['Cid'])
                except:
                    pass
        #http://contacts.apis.live.net/V4.1/cid-5C99C117A11FC952/Contacts/AllContacts
        return {"uid":uri,'name':name,'surname':surname,'mail':email,'avatar':propic,"mail_contacts":mail_contacts,"service_contacts":service_contacts}
        return webservice.headers
        return headers

    def __post_data(self, url, data):
        #Private method that posts encoded data to a LIVE service and returns
        #the response.

        encodedParams = urllib.urlencode(data)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Content-length": str(len(encodedParams))
            }
        
        try:
            request = urllib2.Request(url, encodedParams, headers)

            #The data returned after a request is parsed into key/value
            #pairs so that it can be passed on.
            response = urlparse.parse_qs(urllib2.urlopen(request).read())
            for key, value in response.items():
                # Remove invalid characters from the response
                temp = string.replace(str(value), '[\'','')
                response[key] = string.replace(str(temp), '\']', '')

        except urllib2.HTTPError, e:
            response = {
                        "Http Error Code" : str(e.code),
                        "Error Msg": e.msg,
                        "Returned Headers" : urllib.unquote_plus(pprint.pformat(e.headers)),
                        "Inner Html": urllib.unquote_plus(e.fp.read())
                        }

        return response
