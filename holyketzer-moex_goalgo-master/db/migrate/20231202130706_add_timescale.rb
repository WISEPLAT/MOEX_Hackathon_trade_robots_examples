class AddTimescale < ActiveRecord::Migration[7.1]
  def change
    execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
  end
end
