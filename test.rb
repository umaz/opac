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

def output(record, db)
  bibrec = record["NBC"][0]
  if record["HOLDINGSRECORD"]
    record["HOLDINGSRECORD"].each{ | stdnum |
      db.execute("insert into isbn values (?, ?)", bibrec, stdnum)
    }
  end
end
open("jbisc.txt", "r"){ | io |
  db = SQLite3::Database.new("test.db")
  begin
    db.transaction{
      while rec = read1record(io)
        output(rec, db)
      end
    }
  ensure
    db.close
    io.lineno
  end
}
