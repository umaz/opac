#!/usr/bin/ruby
# -*- coding: utf-8 -*-
#
# ex-cgi1.cgi - RubyによるCGIテストプログラム
# 環境変数を確認する(GETメソッド専用)
#
print("Content-Type: text/plain; charset=UTF-8\r\n")	# ヘッダ情報出力
print("\r\n")						# 空行出力
print("----- 環境変数一覧 -----\n")
ENV.each{ | name, value |
  printf("%s=%s\n", name, value)
}
print("----- QUERY_STRING の値 -----\n")
name = Hash.new
ENV["QUERY_STRING"].split("&").each do |x|
  y = x.split("=")
  key = y[0].gsub("+", " ")
  key = key.gsub(/%[0-9A-F][0-9A-F]/i) do |p|
    p.gsub!(/%/,"")
    p.to_i(16).chr
  end
  if y.size == 2
    val = y[1].gsub("+", " ")
    val = val.gsub(/%[0-9A-F][0-9A-F]/i) do |p|
      p.gsub!(/%/,"")
      p.to_i(16).chr
    end
  else
    val = ""
  end
#  name[y[0]] = y[1]
   name[key] = val
end

name.each do |key, val|
=begin
  key = key.gsub("+", " ")
  key = key.gsub(/%[0-9A-F][0-9A-F]/i) do |p|
    p.gsub!(/%/,"")
    p.to_i(16).chr
  end
  val = val.gsub("+", " ")
  val = val.gsub(/%[0-9A-F][0-9A-F]/i) do |p|
    p.gsub!(/%/,"")
    p.to_i(16).chr
  end
=end
  printf("%s=%s\n%s=%s\n", "field", key, "value", val)
end
print("----- おわり -----\n")
