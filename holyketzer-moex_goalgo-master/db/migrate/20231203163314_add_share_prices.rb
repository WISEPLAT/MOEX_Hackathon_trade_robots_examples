class AddSharePrices < ActiveRecord::Migration[7.1]
  def change
    create_table :share_prices do |t|
      t.references :share, null: false
      t.string :secid, null: false
      t.date :date, null: false
      t.decimal :open, precision: 10, scale: 2
      t.decimal :close, precision: 10, scale: 2
      t.decimal :low, precision: 10, scale: 2
      t.decimal :high, precision: 10, scale: 2
      t.decimal :volume, precision: 10, scale: 2
      t.decimal :waprice, precision: 10, scale: 2

      t.index [:share_id, :date], unique: true
      t.index [:secid]
    end
  end
end
