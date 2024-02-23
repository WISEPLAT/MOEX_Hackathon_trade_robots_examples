class CreateCurrencies < ActiveRecord::Migration[7.1]
  def change
    create_table :currencies do |t|
      t.string :secid, null: false
      t.string :name, null: false
      t.string :short_name, null: false
      t.integer :lot_size, null: false
      t.monetize :face
      t.string :currency, null: false
      t.decimal :minstep, precision: 20, scale: 10, null: false
      t.string :status
      t.string :remarks

      t.timestamps
    end
  end
end
