#!/home/umaz/.anyenv/envs/rbenv/shims/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")
require("erb")

c = CGI.new
keyword = c.params["keyword"]
field = c.params["field"]
condition = c.params["condition"]
terms = c.params["terms"]
year = c.params["year"]

search = keyword.zip(field, condition)
print "Content-Type: text/html; charset=utf-8\n\n"
print ERB.new(File.open('opac.erb').read).result(binding)
