#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")
require("erb")

#検索時間を図るために現在時刻を取得
start_time = Time.now
c = CGI.new
p = c["p"].to_i
search = c["keyword_easy"]
#スペースで分割する

search = search.split(/\s/)

#すべての要素に対し$%_のいずれかが含まれていたらエスケープ文字を挿入し、部分一致のための%を前後につける
s = search.map do |key| 
  escaped = key.gsub(/[$%_]/){|s| '$'+s}
  escaped = "%" + escaped + "%"
end

#検索するフィールドの配列を作成
columns = %w{nbc title sub author place publ year holdr holdl ed name page size isbn note titles authors_n authors_k}
#ｓｑｌ文の作成
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
url = search.join("+")
time = Time.now - start_time
print "Content-Type: text/html; charset=utf-8\n\n"
print ERB.new(File.open('opac-list_easy.erb').read).result(binding)

