#!/usr/bin/ruby
# -*- coding: utf-8 -*-
print "Content-Type: text/html; charset=utf-8\n\n"

start_time = Time.now
require("sqlite3")
require("cgi")
require("erb")

c = CGI.new
p = c["p"].to_i
type = c["type"]
name = c["name"]

com = Hash["author", "authorh_n like ? escape '$'", "pub", "publ like ? escape '$'", "series", "name like ? escape '$'"]
sql = "select distinct nbc, title, sub, ed, name, vol, author, place, publ, year, date from search where" + ' ' + com["#{type}"]
result = Array.new{Array.new}

db = SQLite3::Database.new("opac.db")
db.transaction{
  x = 0
  db.execute(sql, name) {|row|
    result[x] = row
    if result[x][2] == nil
    else
     result[x][2] = ' ' + ":" + ' ' + result[x][2]
    end
    if result[x][5] == nil
    else
      result[x][5] = ' ' + ";" + ' ' + result[x][5]
    end
    x = x + 1
  }
}
  db.close

url = "type=" + type + "&name=" + name
time = Time.now - start_time
print ERB.new(File.open('opac-list_field.erb').read).result(binding)

