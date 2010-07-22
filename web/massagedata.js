//   "Title": "The Year of the Monkey",
//   "Author": "Berry, Carole",
//   "ISBN": "0-440-20672-3",
//   "CopyDate": "1988"

var massageData = {
    index: {},
    authors: {},

    massage: function(jsonData)
    {
        for (var i = 0; i < jsonData.length; i++)
        {
            this.processItem(jsonData[i]);
        }
        this.authorIndex = this.sortAuthors();
        this.insertAuthors($('#authors'));
    },

    sortAuthors: function()
    {
        var authorIndex = [];
        for (var author in this.authors)
        {
            authorIndex.push(author);
        }
        authorIndex.sort();
        return authorIndex;
    },

    insertAuthors: function(elem)
    {
        var me = this;
        $.each(me.authorIndex, function(i, author) {
            console.log(i+1, author);
            $.each(me.authors[author], function(j, work) {
                console.log("\t", j+1, work.Title);
            });
        });
    },

    processItem: function(item)
    {
        if (item.Author)
        {
            this.processItemByAuthors(item, this.parseAuthors(item.Author));
        }
    },

    processItemByAuthors: function(item, authors)
    {
        for (var i = 0; i < authors.length; i++)
        {
            var author = authors[i];
            var works = this.authors[author] || [];
            works.push(item);
            this.authors[author] = works;
        }
    },

    parseAuthors: function(authorsEntry)
    {
        var authors = authorsEntry.split(/\&|\Wand\W/);
        for (var i = 0; i < authors.length; i++)
        {
            authors[i] = this.parseAuthor(authors[i]);
        }
        return authors;
    },

    parseAuthor: function(authorEntry)
    {
        authorEntry = this.stripEditor(authorEntry);
        var names = authorEntry.split(/,/), lastName, firstName;
        if (names.length > 1)
        {
            lastName = names[0]; firstName = names[1];
        }
        else
        {
            names = authorEntry.split(/ /);
            firstName = names[0]; lastName = names[1];
        }

        return [jQuery.trim(lastName), jQuery.trim(firstName)];
    },

    stripEditor: function(authorEntry)
    {
        return jQuery.trim(authorEntry.replace(/\W\(?Editor\)?/, ""));
    },

    normalizeName: function(lastName, firstName)
    {
        // TODO: handle initials, case, etc
    }
};

var rware = massageData.massage(Readerware.Data.Books);
