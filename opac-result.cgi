#!/usr/bin/ruby
# -*- coding: utf-8 -*-
print "Content-Type: text/html; charset=utf-8\n\n"

require("sqlite3")
require("cgi")
require("erb")

c = CGI.new
nbc = c["nbc"]
main = Array.new
isbn = Array.new{Array.new}
note = Array.new{Array.new}
title = Array.new{Array.new}
author = Array.new{Array.new}
db = SQLite3::Database.new("opac.db")
db.transaction{
  db.execute("select author, title, sub, name, vol, ed, place, publ, year, date, page, size, nbc, holdr, holdl from main where nbc like ?;", nbc) {|row|
    main = row
    if main[2] == nil
    else
      main[2] =  ' ' + ":" + ' ' + main[2]
    end
    if main[5] == nil
    else
      main[5] = ' ' + ";" + ' ' + main[5]
    end
  }
  x = 0
  db.execute("select titleh from title where nbc like ?;", nbc) {|row|
    title[x] = row[0]
    x = x + 1
  }
  x = 0
  db.execute("select authorh_n, authorh_k from author where nbc like ?;", nbc) {|row|
    author[x] = row
    x = x + 1
  }
  x = 0
  db.execute("select isbn from isbn where nbc like ?;", nbc) {|row|
    isbn[x] = row[0]
    x = x + 1
  }
  x = 0
  db.execute("select note from note where nbc like ?;", nbc) {|row|
    note[x] = row[0]
    x = x + 1
  }
  main.insert(3, title)
  main.insert(7, author)
  main.insert(14, isbn)
  main.insert(16, note)
}
  db.close
  header = %w{著者 書名 書名ヨミ シリーズ名 版表示 著者名 出版地 出版者 出版年 ページ数 大きさ ISBN 全国書誌番号 注記 所在識別番号 所在情報}
print ERB.new(File.open('opac-result.erb').read).result(binding)

