//   "Title": "The Year of the Monkey",
//   "Author": "Berry, Carole",
//   "BookFormat": "Mass Market Paperback",
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
        console.log(this.authors);
    },

    processItem: function(item)
    {
        if (item.Author)
        {
            var authors = this.parseAuthors(item.Author);
            this.processItemByAuthors(item, authors);
//          console.log(item.Title, authors);
        }
    },

    processItemByAuthors: function(item, authors)
    {
        for (var i = 0; i < authors.length; i++)
        {
            var author = authors[i];
            var works = this.authors[author] || [];
            works.push(item.Title);
            this.authors[author] = works;
        }
    },

    parseAuthors: function(authorsEntry)
    {
        var authors = authorsEntry.split(/\&|\Wand\W/);
        for (var i = 0; i < authors.length; i++)
            authors[i] = this.parseAuthor(authors[i]);
        return authors;
    },

    parseAuthor: function(authorEntry)
    {
        var lastName, firstName;
        var names = authorEntry.split(/, /);
        if (names.length > 1)
        {
            lastName = names[0]; firstName = names[1];
        }
        else
        {
            names = authorEntry.split(/ /);
            firstName = names[0];
            lastName = names[1];
        }

        return [lastName, firstName];
    }
};

var rware = massageData.massage(Readerware.Data.Books);
