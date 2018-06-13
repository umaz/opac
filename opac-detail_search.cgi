#!/home/umaz/.anyenv/envs/rbenv/shims/ruby
# -*- coding: utf-8 -*-
print "Content-Type: text/html; charset=utf-8\n\n"

require("sqlite3")
require("cgi")
require("erb")

start_time = Time.now
c = CGI.new
p = c["p"].to_i
#検索語
keyword = c.params["keyword"]
#検索するフィールド
field = c.params["field"]
#検索方法
condition = c.params["condition"]
#andor
terms = c.params["terms"]
#年
year = c.params["year"]

terms.unshift(nil)

search = keyword.zip(field, condition, terms)
ur = keyword.zip(field, condition, terms)
ur = ur.each do |x|
  x[0] = x[0].split(/\s/)
end
if keyword.all? {|x| x==""}
    sql = "select distinct nbc, title, sub, ed, name, vol, author, place, publ, year, date from search where nbc is not null"
result = Array.new{Array.new}
db = SQLite3::Database.new("opac.db")
db.transaction{
  x = 0
  db.execute(sql) {|row|
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
else
search = search.each do |x|
  if x[2] == "all"
    x[0] = x[0].split(/\s/)
    x[0] = x[0].map do |key| 
      x[0] = key.gsub(/[$%_]/){|s| '$'+s}
      x[0] = "%" + x[0] + "%"
    end
  elsif x[2] == "once"
    x[0] = x[0].split(/\s/)
    x[0] = x[0].map do |key| 
      x[0] = key.gsub(/[$%_]/){|s| '$'+s}
      x[0] = "%" + x[0] + "%"
    end
  elsif x[2] == "not"
    x[0] = x[0].split(/\s/)
    x[0] = x[0].map do |key| 
      x[0] = key.gsub(/[$%_]/){|s| '$'+s}
      x[0] = "%" + x[0] + "%"
    end
  elsif x[2] == "start"
    x[0] = x[0].gsub(/[$%_]/){|s| '$'+s}
    x[0] = x[0] + "%"
    a = [x[0]]
    x[0] = a
  elsif x[2] == "equal"
    x[0] = x[0].gsub(/[$%_]/){|s| '$'+s}
    x[0] = x[0]
    a = [x[0]]
    x[0] = a
  end
end
any = %w{nbc title sub author place publ year holdr holdl ed name page size isbn note titles authors_n authors_k}
any = any.map{|col| "#{col} like ? escape '$'"}.join(' or ')
title = %w{title sub name titles}
title = title.map{|col| "#{col} like ? escape '$'"}.join(' or ')
author = %w{author authors_n authors_k}
author = author.map{|col| "#{col} like ? escape '$'"}.join(' or ')
pub = %w{place publ}
pub = pub.map{|col| "#{col} like ? escape '$'"}.join(' or ')


com = Hash["any", "#{any}", "title", "#{title}", "author", "#{author}", "pub", "#{pub}", "ed", "ed like ? escape '$'", "series", "name like ? escape '$'", "page", "page like ? escape '$'", "size", "size like ? escape '$'", "isbn", "isbn like ? escape '$'", "nbc", "nbc like ? escape '$'", "note", "note like ? escape '$'", "holdingsrecord", "holdr like ? escape '$'", "holdingloc", "holdl like ? escape '$'", "year", "year like ? escape '$'"]

join = Hash["all", "and", "once", "or", "start", "and", "equal", "and", "not", "and"]

times = Hash["any", 18, "title", 4, "author", 3, "pub", 2, "ed", 1, "series", 1, "page", 1, "size", 1, "isbn", 1, "nbc", 1, "note", 1, "holdr", 1, "holdl", 1, "year", 1]

sql = "select distinct nbc, title, sub, ed, name, vol, author, place, publ, year, date from search where"

word = Array.new
research = Array.new
connect = Array.new
s = 0
for x in search do 
  n = x[0].size
  if n == 0
  else
    if x[2] == "not"
      sql3_3 = com["#{x[1]}"].gsub("like", "not like")
      sql3_1 = "nbc in (select nbc from search where" + ' ' + sql3_3 + ")"
    else
      sql3_1 = "nbc in (select nbc from search where" + ' ' + com["#{x[1]}"] + ")"
    end
    sql3_2 = join["#{x[2]}"] + ' ' + sql3_1
    sql3 = sql3_1 + ' ' + sql3_2 * (n - 1)
    research[s] = sql3
  word[s] = x[0].map do |word|
    [word] * times["#{x[1]}"]
  end
  sql2_1 = "nbc in (select nbc from search where" + ' ' + research[s] + ")"
  if x[3] == nil
    sql2 = sql2_1
  else
    sql2 = x[3] + ' ' + sql2_1
  end
  connect[s] = sql2
  s = s + 1
  end
end
sql = sql + ' ' + connect.join(" ")
result = Array.new{Array.new}
db = SQLite3::Database.new("opac.db")
db.transaction{
  x = 0
  db.execute(sql, word.flatten) {|row|
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
end
un =["field=", "keyword=", "condition=", "terms="]
url = "field=" + ur[0][1] + "&keyword=" + ur[0][0].join("+") + "&condition=" + ur[0][2]

n = 1
while n < ur.size
  url = url + "&" + un[0] + ur[n][1]
  url = url + "&" + un[1] + ur[1][0].join("+")
  url = url + "&" + un[2] + ur[n][2]
  url = url + "&" + un[3] + ur[n][3]
  n = n + 1
end
time = Time.now - start_time
print ERB.new(File.open('opac-list_detail.erb').read).result(binding)

