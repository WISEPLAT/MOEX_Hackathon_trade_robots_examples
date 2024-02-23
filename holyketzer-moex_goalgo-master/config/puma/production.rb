environment "production"
threads 8, 8
workers 1

cwd = "/var/www/your_stock_index/current"

on_worker_boot do
  require "active_record"
  ActiveRecord::Base.connection.disconnect! rescue ActiveRecord::ConnectionNotEstablished
  ActiveRecord::Base.establish_connection(ENV["DATABASE_URL"] || YAML.load_file("#{cwd}/config/database.yml")["production"])
end

bind "unix://#{cwd}/tmp/sockets/puma_web.sock"
pidfile "#{cwd}/tmp/pids/server.pid"
