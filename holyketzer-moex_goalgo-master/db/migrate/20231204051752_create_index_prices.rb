class CreateIndexPrices < ActiveRecord::Migration[7.1]
  def change
    create_table :index_prices do |t|
      t.references :shares_index, null: false
      t.string :secid, null: false
      t.date "date", null: false
      t.decimal :open, precision: 10, scale: 2
      t.decimal :close, precision: 10, scale: 2
      t.decimal :low, precision: 10, scale: 2
      t.decimal :high, precision: 10, scale: 2
      t.bigint :volume

      t.index [:shares_index_id, :date], unique: true
      t.index [:secid]

      t.timestamps
    end
  end
end
