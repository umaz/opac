 #!/usr/bin/ruby
 # -*- coding: utf-8 -*-

require("sqlite3")

def read1field(io)
  line = io.gets
  if !line
    return nil
  end
  line.chomp!
  field = line.split(/:\s*/, 2)
  return field
end

def read1record(io)
  record = Hash.new
  while field = read1field(io)
    if field[0] == "*"
      break
    end
    if record.key?(field[0])
      record[field[0]].push(field[1])
    else
      record[field[0]] = [field[1]]
    end
  end
  if record.empty?
    return nil
  else
    return record
  end
end

def split_tr(record)
  if record.key?("TR")
    record["tr-title"] = Array.new
    record["tr-sub"] = Array.new
    record["tr-author"] = Array.new
    record["TR"].each{ | s |
      v = s.split(/\s+\/\s+/, 2)
      x = v[0].split(/\s+:\s+/, 2)
      record["tr-title"].push(x[0])
      record["tr-sub"].push(x[1])
      record["tr-author"].push(v[1])
    }
  end
end

def split_pub(record)
  if record.key?("PUB")
    record["pub-place"] = Array.new
    record["pub-publ"] = Array.new
    record["pub-year"] = Array.new
    record["pub-date"] = Array.new
    record["PUB"].each{ | s |
      v = s.split(/\s*,\s+/, 2)
      x = v[0].split(/\s+:\s+/, 2)
      y = v[1].split(".", 2)
      record["pub-place"].push(x[0])
      record["pub-publ"].push(x[1])
      record["pub-year"].push(y[0])
      record["pub-date"].push(y[1])
    }
  end
end

def output(record, db)
  bibrec = record["NBC"][0]
  if record["ISBN"]
    record["ISBN"].each{ | stdnum |
      db.execute("insert into isbn values (?, ?)", bibrec, stdnum)
    }
  end
  bibrec = record["NBC"][0]
  if record["tr-title"]
    record["tr-title"].zip(record["tr-sub"], record["tr-author"]).each{ | title, sub, author |
      db.execute("insert into tr values (?, ?, ?, ?)", bibrec, title, sub, author)
    }
  end
  bibrec = record["NBC"][0]
  if record["pub-place"]
    record["pub-place"].zip(record["pub-publ"], record["pub-year"], record["pub-date"]).each{ | place, publ, year, date |
      db.execute("insert into pub values (?, ?, ?, ?, ?)", bibrec, place, publ, year, date)
    }
  end
end

open("jbisc.txt", "r"){ | io |
  db = SQLite3::Database.new("test.db")
  begin
    db.transaction{
      while rec = read1record(io)
        split_tr(rec)
        split_pub(rec)
        output(rec, db)
      end
    }
  ensure
    db.close
    io.lineno
  end
}
