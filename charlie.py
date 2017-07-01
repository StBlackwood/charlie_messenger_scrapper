import gi
import urllib2
import urllib
import gzip
import os
import json
import time
import StringIO

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyApp(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("groupMessage.glade")
        self.builder.connect_signals(self)

    def run(self):
        self.builder.get_object("window").show_all()
        Gtk.main()

    def on_window_destroy(self, *args):
        Gtk.main_quit()

    def on_button1_clicked(self, *args):
        talk=self.builder.get_object("conversation_id").get_text()
        cookieValue=self.builder.get_object("cookie").get_text()
        userValue=self.builder.get_object("__user").get_text()
        aValue=self.builder.get_object("__a").get_text()
        dynValue=self.builder.get_object("__dyn").get_text()
        reqValue=self.builder.get_object("__req").get_text()
        fb_dtsgValue=self.builder.get_object("fb_dtsg").get_text()
        timeStampVlaue=self.builder.get_object("time_stamp").get_text()
        revValue=self.builder.get_object("__rev").get_text()
        doc_idValue=self.builder.get_object("doc_id").get_text()
        afValue=self.builder.get_object("__af").get_text()
        jazoestValue=self.builder.get_object("jazoest").get_text()
        pcValue=self.builder.get_object("__pc").get_text()
        beValue=self.builder.get_object("__be").get_text()

        error_timeout = 30
        general_timeout = 7
        messages_data = "lolno"
        end_mark = "\"payload\":{\"end_of_history\""
        limit = 30
        offset = limit
        timestamp = int(timeStampVlaue)
        headers = {"origin": "https://www.messenger.com",
                   "accept-encoding": "gzip,deflate",
                   "accept-language": "en-US,en;q=0.8",
                   "cookie": cookieValue,
                   "pragma": "no-cache",
                   "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36",
                   "content-type": "application/x-www-form-urlencoded",
                   "accept": "*/*",
                   "cache-control": "no-cache",
                   "referer": "https://www.facebook.com/messages/zuck"}
        base_directory = "Messages/"
        directory = base_directory + str(talk) + "/"
        attachment_directory = directory+"attachments/"
        try:
            os.makedirs(directory)
        except OSError:
            pass  # already exists
        try:
            os.makedirs(attachment_directory)
        except OSError:
            pass  # already exists

        while end_mark not in messages_data:
            try:
                pass
            except:
                time.sleep(error_timeout)

            data_text = {"__user":str(userValue),
                         "__a":str(aValue),
                         "__dyn":str(dynValue),
                         "__af":str(afValue),
                         "__req":str(reqValue),
                         "__be":str(beValue),
                         "__pc":str(pcValue),
                         "__rev":str(revValue),
                         "fb_dtsg":str(fb_dtsgValue),
                         "jazoest":str(jazoestValue),
                         "queries":{
                             "o0":{
                                 "doc_id":str(doc_idValue),
                                 "query_params":{
                                     "id":str(talk),
                                     "message_limit":str(offset),
                                     "load_messages":"1",
                                     "load_read_receipts":"true",
                                     "before":str(timestamp)
                                 }
                             }
                         }}
            data = urllib.urlencode(data_text)
            url = "https://www.messenger.com/api/graphqlbatch/"

            print "Retrieving messages " + str(offset-limit) + "-" + str(offset) + " for conversation ID " + str(talk)
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            print response
            compressed = StringIO.StringIO(response.read())
            decompressedFile = gzip.GzipFile(fileobj=compressed)

            outfile = open(directory + str(offset) + "-" + str(limit + offset) + ".json", 'w')
            messages_data = decompressedFile.read()
            rightIndex=messages_data.rfind('{')
            rightIndex= len(messages_data)-rightIndex
            messages_data = messages_data[:-rightIndex]
            # print messages_data
            json_data = json.loads(messages_data)
            if json_data is not None and json_data['o0'] is not None:
                try:
                    timestamp = int(json_data['o0']['data']['message_thread']['messages']['nodes'][0]['timestamp_precise']) - 1
                    print timestamp
                    for message in json_data['o0']['data']['message_thread']['messages']['nodes']:
                        # print message['message']['text']
                        for attachment in message['blob_attachments']:
                            # print attachment['large_preview']['uri']
                            os.system("curl \""+str(attachment['large_preview']['uri'])+"\" -o "+attachment_directory+str(attachment['filename']))

                except KeyError:
                    pass
            else:
                print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
                print "Data Dump:"
                print json_data
                time.sleep(error_timeout)
                continue
            outfile.write(messages_data)
            outfile.close()
            offset = offset + limit
            time.sleep(general_timeout)

MyApp().run()
