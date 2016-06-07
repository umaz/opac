#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")
require("erb")

c = CGI.new
search = c["keyword_easy"]

s = search.split(/\s/)
n = 0
while n < s.size
  if s[n].include?("%")
    s[n]["%"] = "\\%"
  elsif s[n].include?("_")
    s[n]["_"] = "\\_"
  end
  s[n] = "%" + s[n] + "%"
  n = n + 1
end

print(s[0])
db = SQLite3::Database.new("opac.db")
db.transaction{
  nbc = Array.new
  n = 0
  while n < s.size 
    result = Array.new
    x = 0
    db.execute("select distinct nbc from search where nbc like ? or title like ? or sub like ? or author like ? or place  like ? or publ like ? or year like ? or holdr like ? or holdl like ? or ed like ? or name like ?  or isbn like ? or note like ? or titles like ? or authors_n like ? or authors_k like ? escape '\\' ;", s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n], s[n]) {|row|
      result[x] = row[0]
      x = x + 1
    }
    nbc.push(result)
    n = n + 1
  end
  n = 0
  while n < nbc.size
    if n == 0  
     kekka = nbc[n]
    else
     kekka = kekka & nbc[n]
    end
    n = n + 1
  end
 p kekka
}
  db.close
