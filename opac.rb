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
def split_phys(record)
  if record.key?("PHYS")
    record["phys-page"] = Array.new
    record["phys-size"] = Array.new
    record["PHYS"].each{ | s |
      v = s.split(/\s+;\s+/, 2)
      record["phys-page"].push(v[0])
      record["phys-size"].push(v[1])
    }
  end
end

def split_series(record)
  if record.key?("SERIES")
    record["series-name"] = Array.new
    record["series-vol"] = Array.new
    record["SERIES"].each{ | s |
      v = s.split(/\s+;\s+/, 2)
      record["series-name"].push(v[0])
      record["series-vol"].push(v[1])
    }
  end
end

def split_titleheading(record)
  if record.key?("TITLEHEADING")
    record["titleh"] = Array.new
    record["titles"] = Array.new
    record["TITLEHEADING"].each{ |s|
      record["titleh"].push(s)
      record["titles"].push(s.gsub(/\s/,""))
    }
  end
end

def split_authorheading(record)
  if record.key?("AUTHORHEADING")
    record["authorh-n"] = Array.new
    record["authorh-k"] = Array.new
    record["authors-n"] = Array.new
    record["authors-k"] = Array.new
    record["AUTHORHEADING"].each{ |s|
      v = s.split(" (")
    if v[1] == nil
      record["authorh-n"].push(v[0])
      record["authors-n"].push(v[0].gsub(",",""))      
      record["authorh-k"].push("")
      record["authors-k"].push("")
    else
      record["authorh-k"].push(v[0])
      record["authors-k"].push(v[0].gsub(", ",""))
      record["authorh-n"].push(v[1].gsub!(")", ""))
      record["authors-n"].push(v[1].gsub(", ",""))
    end
    }
  end
end

def output(record, db)
  bibrec = record["NBC"][0]
  if record["tr-title"]
    record["tr-title"].zip(record["tr-sub"], record["tr-author"], record["pub-place"], record["pub-publ"], record["pub-year"], record["pub-date"], record["HOLDINGSRECORD"], record["HOLDINGLOC"]).each{ |title, sub, author, place, publ, year, date, holdr, holdl |
      db.execute("insert into basic values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", bibrec, title, sub, author, place, publ, year, date, holdr, holdl)
    }
  end

  bibrec = record["NBC"][0]
  if record["series-name"]
    record["series-name"].zip(record["series-vol"]).each{ | name, vol |
      db.execute("insert into series values (?, ?, ?)", bibrec, name, vol)
    }
  end

  bibrec = record["NBC"][0]
  if record["phys-page"]
    record["phys-page"].zip(record["phys-size"]).each{ | page, size |
      db.execute("insert into phys values (?, ?, ?)", bibrec, page, size)
    }
  end

  bibrec = record["NBC"][0]
  if record["ED"]
    record["ED"].each{ | ed |
      db.execute("insert into ed values (?, ?)", bibrec, ed)
    }
  end
  bibrec = record["NBC"][0]
  if record["ISBN"]
    record["ISBN"].each{ | isbn |
      db.execute("insert into isbn values (?, ?)", bibrec, isbn)
    }
  end

  bibrec = record["NBC"][0]
  if record["NOTE"]
    record["NOTE"].each{ | note |
      db.execute("insert into note values (?, ?)", bibrec, note)
    }
  end

  bibrec = record["NBC"][0]
  if record["titleh"]
    record["titleh"].zip(record["titles"]).each{ | titleh, titles |
      db.execute("insert into title values (?, ?, ?)", bibrec, titleh, titles)
    }
  end
  bibrec = record["NBC"][0]
  if record["authorh-n"]
    record["authorh-n"].zip(record["authorh-k"], record["authors-n"], record["authors-k"]).each{ | authorh_n, authorh_k, authors_n, authors_k |
      db.execute("insert into author values (?, ?, ?, ?, ?)", bibrec, authorh_n, authorh_k, authors_n, authors_k)
    }
  end
end

open("jbisc.txt", "r"){ | io |
  db = SQLite3::Database.new("opac.db")
  begin
    db.transaction{
      while rec = read1record(io)
        split_tr(rec)
        split_pub(rec)
        split_phys(rec)
        split_series(rec)
        split_titleheading(rec)
        split_authorheading(rec)
        output(rec, db)
      end
      db.execute(" create view search as select * from basic natural left outer join ed natural left outer join series natural left outer join phys  natural left outer join isbn natural left outer join note natural left outer join title natural left outer join author;")
    }
  ensure
    db.close
    io.lineno
  end
}

