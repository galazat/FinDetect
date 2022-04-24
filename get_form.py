# br = Browser()
    # # Create cookie jar and attach it to Browser
    # #cj = cookielib.LWPCookieJar()
    # #br.set_cookiejar(cj)
    #
    # br.addheaders = [('User-agent',
    #                   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    # # Open url in Browser instance
    # br.open(service.url)
    #
    # response = urlopen(service.url)
    # forms = ParseResponse(response, backwards_compat=False)
    # form = forms[0]
    # print(form)

    br = mechanize.Browser()
    br.open(service.url)

    response1 = br.follow_link(nr=0)
    print(br.title())
    print(response1.geturl())
    print(response1.info())  # headers
    print(response1.read())  # body

    br.select_form(name="order")
    # Browser passes through unknown attributes (including methods)
    # to the selected HTMLForm.
    br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
    # Submit current form.  Browser calls .close() on the current response on
    # navigation, so this closes response1
    response2 = br.submit()

    # print currently selected form (don't call .submit() on this, use br.submit())
    print(br.form)

    response3 = br.back()  # back to cheese shop (same data as response1)
    # the history mechanism returns cached response objects
    # we can still use the response, even though it was .close()d
    response3.get_data()  # like .seek(0) followed by .read()
    response4 = br.reload()  # fetches from server