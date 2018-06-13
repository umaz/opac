#!/home/umaz/.anyenv/envs/rbenv/shims/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")
require("erb")
require("benchmark")

time = Benchmark.realtime do
c = CGI.new
p = c["p"].to_i
search = c["keyword_easy"]
search = search.split(/\s/)

s = search.map do |key| 
  escaped = key.gsub(/[$%_]/){|s| '$'+s}
  escaped = "%" + escaped + "%"
end

columns = %w{nbc title sub author place publ year holdr holdl ed name page size isbn note titles authors_n authors_k}
columns = columns.map{|col| "#{col} like ? escape '$'"}.join(' or ')
sql = "nbc in (select nbc from search where" + ' ' + columns + ")"
sql2 = "and" + ' ' + sql

n = s.size
  sql = "select distinct nbc, title, sub, ed, name, vol, author, place, publ, year, date from search where " + ' ' + sql
  sql = sql + ' ' + sql2 * (n - 1)
  keyword = s.map do |word|
    [word] * 18
  end

result = Array.new{Array.new}

db = SQLite3::Database.new("opac.db")
db.transaction{
  x = 0
  db.execute(sql, keyword.flatten) {|row|
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
p time 
print "Content-Type: text/html; charset=utf-8\n\n"
print ERB.new(File.open('opac-easy.erb').read).result(binding)

