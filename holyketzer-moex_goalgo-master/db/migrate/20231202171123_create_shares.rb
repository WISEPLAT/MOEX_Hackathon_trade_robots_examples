class CreateShares < ActiveRecord::Migration[7.1]
  def change
    create_table :shares do |t|
      t.string :secid, null: false
      t.string :name, null: false
      t.string :short_name, null: false
      t.string :isin, null: false
      t.integer :issue_size, null: false, limit: 8
      t.monetize :nominal_price, null: false
      t.date :issue_date, null: false
      t.integer :list_level, null: false
      t.string :sec_type, null: false

      t.timestamps

      t.index :secid, unique: true
    end
  end
end
