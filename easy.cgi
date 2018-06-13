#!/home/umaz/.anyenv/envs/rbenv/shims/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")


c = CGI.new
search = c["keyword_easy"]
s =search.gsub(/[$%_]/){|s| '$'+s} 
s = "%" + s + "%"
  print("Content-Type: text/html; charset=utf-8\n")
  print("\n")
  db = SQLite3::Database.new("easy.db")
  db.transaction{
  print(" <html>\n")
  print(" <head>\n")
  print(" <link rel=\"stylesheet\" href=\"opac-index.css\" type=\"text/css\">\n")
  print(" <title>検索結果</title>\n")
  print(" </head>\n")
  print(" <body>\n")
  print(" <h2>検索結果</h2>\n")
  print(" <p>\n")
    nbc = Array.new
    n = 0
    db.execute("select * from tr where title like ? escape '$' or sub like ? escape '$' or author like ? escape '$';", s, s, s) {|row|
      nbc[n] = row[0]
      n = n + 1
  }
    n = 0
    while n < nbc.size
      db.execute("select * from tr where nbc like ?;", nbc[n]) {|row|
        x = 0
        while x < row.size
          if row[x] == nil
            row[x]=""
          end
          x = x + 1
        end
      print( printf("%s:%s : %s:%s:",CGI.escapeHTML(row[0]),CGI.escapeHTML(row[1]),CGI.escapeHTML(row[2]),CGI.escapeHTML(row[3])))
  }
      db.execute("select * from pub where nbc like ?;", nbc[n]) {|row|
        x = 0
        while x < row.size
          if row[x] == nil
            row[x]=""
          end
          x = x + 1
        end
      print( printf("%s : %s:%s.%s:",CGI.escapeHTML(row[1]),CGI.escapeHTML(row[2]),CGI.escapeHTML(row[3]),CGI.escapeHTML(row[4])))
  }
        db.execute("select * from isbn where nbc like ?;", nbc[n]) {|row|
        x = 0
        while x < row.size
          if row[x] == nil
            row[x]=""
          end
          x = x + 1
        end
      print( printf("%s",CGI.escapeHTML(row[1])))
  }    
  print(" <br>")
  n = n + 1
  end
  print(" </p>\n")
  print(" </body>\n")
  print(" </html>\n")
}
  db.close
