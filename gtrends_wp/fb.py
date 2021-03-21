
import facebook


def read_file(file_n):
    f = open(file_n,"r+")
    d = f.read()
    f.close()
    return d


def fb():
    graph = facebook.GraphAPI(access_token='EAADrqhBh6REBAKrwrdpGp6poipVJfUEbKk4QlRtmt5efIm4rNVfRE3FAYCOMZBApomCD8deSV4KjJFgJK3vhDufgWzJHywcOmZA5f13ZBvN0KFQcqZBQ7suVmsvx0pj3gSqZA3MtTM9gHn8w8IdvOK14CBUsY8Hli5n62gmyRipxqGCIPq7uFRsfrCJsvH4xXcuR3SuQPRTMnNPoSOCKP3SYBGdIRBE0dlxUmWxDFygZDZD', version='3.1')
    #if version 2.8 show error use 2.6
    attachment =  {
        'name': 'Link name',
        'link': 'https://www.example.com/',
        'caption': 'Check out this example',
        'description': 'This is a longer description of the attachment',
        'picture': 'https://cdn.searchenginejournal.com/wp-content/uploads/2019/04/shutterstock_456779230-1520x800.png',
    }

    e = graph.put_wall_post(message='Check this out...', attachment=attachment, profile_id='ad.net.7545')
    print (e)

fb()
exit()
